# worksheet-intake

Turn a worksheet into practice by emailing it in. Take photos of the pages (or
attach the PDF) and send them to the worksheet address. A few minutes later the
app asks you to review new questions and publish them to Classwork.

    parent emails photos / PDF of a worksheet
      -> CloudMailin POSTs JSON (attachments included) to this function
      -> Claude reads the pages and writes NEW questions on the same skills
         (different numbers, original passages - like the packet scripts)
      -> a second Claude pass solves every question blind; any question
         where the two disagree is dropped
      -> the questions that are left are inserted INACTIVE
      -> the app shows "N questions ready to review": Show questions /
         Publish to Classwork / Discard

This differs from spelling on purpose: spelling words are copied from the
teacher's doc as written, so spelling publishes itself. Worksheet questions are
written by a model, so a person sees them before Jaden does.

## Sending a worksheet

- Attach JPEG/PNG photos or a PDF. Send each worksheet as its own email. One
  email becomes one sheet in Classwork.
- Optionally say what it is in the subject or body ("Math - fractions, pages
  46-53"). That text is passed along as a hint.
- iPhone HEIC photos can't be read. If one is attached, the run is refused and
  the banner says how to send JPEG instead. Mail from an iPhone usually
  converts photos to JPEG on its own.
- Send from an address on `INTAKE_ALLOWED_FROM`. Mail from anyone else is
  recorded as ignored.
- Sending the same pages twice does not create a second set.

## Setup (one time)

**1. Run `migrations/006_worksheet_intake.sql`** in the Supabase SQL editor. It
adds the worksheet columns and statuses to `intake_runs`.

**2. Add the Anthropic API key** in Supabase dashboard -> Edge Functions ->
Secrets:

    ANTHROPIC_API_KEY = <your key>

`INTAKE_SECRET` and `INTAKE_ALLOWED_FROM` are the ones spelling-intake already
uses. Nothing new is needed for them.

**3. Deploy:**

    supabase functions deploy worksheet-intake

`supabase/config.toml` pins `verify_jwt = false` for it, as it does for spelling.

**4. Create a second CloudMailin address** and point its target at:

    https://zvffmucghcrqackghhlf.supabase.co/functions/v1/worksheet-intake?secret=<YOUR_INTAKE_SECRET>

Format: **JSON**. Attachments must be **embedded** (the default when no
attachment store is configured). If you do configure an attachment store, the
function downloads from the URL CloudMailin gives instead.

> **Never commit the secret.** Same rule as spelling-intake: it lives only in
> the Supabase dashboard and the CloudMailin target URL.

## Try a real worksheet before trusting it

`?dry=1` reads the worksheet and returns the questions it would add, plus every
question it dropped and why, without writing anything:

    B64=$(base64 -w0 page1.jpg)
    curl -s -X POST "https://zvffmucghcrqackghhlf.supabase.co/functions/v1/worksheet-intake?dry=1" \
      -H 'Content-Type: application/json' \
      -H 'x-intake-secret: <YOUR_INTAKE_SECRET>' \
      -d "{\"headers\":{\"from\":\"lt.dzirasa@gmail.com\",\"subject\":\"fractions\"},
           \"attachments\":[{\"file_name\":\"page1.jpg\",\"content_type\":\"image/jpeg\",\"content\":\"$B64\"}]}"

## What gets checked

Every question has to pass all of these, and a worksheet with fewer than 5
survivors is refused rather than published thin. The checks live in
`worksheet.js`, and `worksheet.test.mjs` covers each one:

- the marked answer is exactly one of the options, and no two options are the same
- options have no `A.`/`B)` prefixes (the app draws its own letters, see #29)
- numeric answers are plain numbers, since the app's answer box is
  `type="number"` and a fraction answer would always be marked wrong
- no question refers to a picture or diagram Jaden can't see
- an independent solve, which never sees the key, reaches the same answer

The second pass is the same generate-then-solve idea as the `verify` checks in
the packet scripts, without writing an expression by hand for each question.
When the two passes disagree there's no telling which one is wrong, so the
question is dropped either way.

## How a run moves

    processing -> review -> published   (Publish: questions set active)
                         -> discarded   (Discard: questions stay inactive)
    processing -> failed                (nothing inserted; reason shown)

Reading the pages takes longer than CloudMailin waits for a reply, so the
function answers right away and finishes in the background
(`EdgeRuntime.waitUntil`). If it's cut off partway through, the run stays in
`processing`. After 15 minutes the app shows it as "did not import" instead of
waiting forever.
