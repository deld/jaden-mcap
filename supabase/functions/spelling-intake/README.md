# spelling-intake

Weekly spelling list, from the teacher's email into the app, without anyone
retyping it.

    teacher emails ClassroomParent
      -> Gmail filter forwards to CloudMailin
      -> CloudMailin POSTs JSON to this function
      -> read the linked Google Doc, find Jaden's group on the roster,
         take that group's words
      -> publish as typed-spelling questions + record the run

The app shows a banner for the newest unseen run, including a failure — a
refusal matters more than a success, because it means this week's words did
**not** arrive.

## Setup (one time)

**1. Set the shared secret.** Supabase dashboard → Edge Functions → Secrets:

    INTAKE_SECRET = 7Ot9QmBeVpwGZ7x8JCYEXvp0uOfpqkrg9EdPfkw6DG8

Until this is set the endpoint rejects everything (fail-closed), which is the
safe state.

**2. Create a CloudMailin address** (free plan, 10k/month, no card). Point its
target at:

    https://zvffmucghcrqackghhlf.supabase.co/functions/v1/spelling-intake?secret=7Ot9QmBeVpwGZ7x8JCYEXvp0uOfpqkrg9EdPfkw6DG8

Format: JSON.

**3. Add a Gmail filter** on lt.dzirasa@gmail.com:
from `mailer@email-support.classroomparent.com` **or** subject contains
`SPELLING LIST` → forward to the CloudMailin address. Gmail will ask to verify
the forwarding address once.

**4. The doc must be shared "anyone with the link"** — the function fetches its
HTML export with no credentials.

## Try a real doc before trusting it

`?dry=1` parses and reports without writing anything:

    curl -s -X POST "https://zvffmucghcrqackghhlf.supabase.co/functions/v1/spelling-intake?dry=1" \
      -H 'Content-Type: application/json' \
      -H 'x-intake-secret: 7Ot9QmBeVpwGZ7x8JCYEXvp0uOfpqkrg9EdPfkw6DG8' \
      -d '{"headers":{"subject":"SPELLING LIST"},"plain":"https://docs.google.com/document/d/YOUR_DOC_ID/edit"}'

It returns the group it found and the exact words it would publish.

## Why it refuses

The doc's shape is the teacher's to change. Every parse step is strict and
throws rather than guessing: unknown student, no matching column, fewer than 8
words, more than 40, no tables at all. A refusal is recorded and shown in the
app; nothing is published. A wrong list reaching Jaden is worse than an import
that visibly failed.

Re-forwarding the same email does not double-publish — a list already present
for that week is detected and skipped.
