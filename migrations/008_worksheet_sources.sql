-- Keep every worksheet's original file.
--
-- Until now a worksheet's pages went to the model and were thrown away; only
-- a hash survived (for spotting a resend). A parent reviewing questions could
-- not see the page they came from, and a worksheet could not be re-run.
--
-- Originals live in a PRIVATE storage bucket. They are photos of a child's
-- homework, so nothing here is public and the anon key gets no access:
--   email/<run>/NN-name    saved by worksheet-intake (service role)
--   uploads/<stamp>/NN-name saved by the browser, full size, by a signed-in
--                          parent - the copy sent for reading is shrunk
-- A signed-in parent can read any of them (the app asks for a short-lived
-- signed URL to show one).

INSERT INTO storage.buckets (id, name, public, file_size_limit)
VALUES ('worksheets', 'worksheets', false, 52428800)   -- 50 MB per file
ON CONFLICT (id) DO NOTHING;

-- Is the signed-in user one of the parents? `parents` is service-role only
-- (it holds email addresses), so this runs as its owner to look - and
-- answers only yes or no.
CREATE OR REPLACE FUNCTION public.is_parent() RETURNS boolean
LANGUAGE sql STABLE SECURITY DEFINER SET search_path = public AS $$
  SELECT EXISTS (
    SELECT 1 FROM parents
    WHERE lower(email) = lower(coalesce(auth.jwt() ->> 'email', ''))
  );
$$;
REVOKE ALL ON FUNCTION public.is_parent() FROM public, anon;
GRANT EXECUTE ON FUNCTION public.is_parent() TO authenticated;

DROP POLICY IF EXISTS worksheets_parent_upload ON storage.objects;
CREATE POLICY worksheets_parent_upload ON storage.objects FOR INSERT TO authenticated
  WITH CHECK (bucket_id = 'worksheets'
              AND (storage.foldername(name))[1] = 'uploads'
              AND public.is_parent());

DROP POLICY IF EXISTS worksheets_parent_read ON storage.objects;
CREATE POLICY worksheets_parent_read ON storage.objects FOR SELECT TO authenticated
  USING (bucket_id = 'worksheets' AND public.is_parent());

-- Which files a run came from: [{ path, name, type, bytes }]. Paths only -
-- they are useless without a parent's sign-in, since the bucket is private.
ALTER TABLE intake_runs ADD COLUMN IF NOT EXISTS source_files jsonb;
