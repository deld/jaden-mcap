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

> **Never commit the secret.** It belongs only in the Supabase dashboard and
> the CloudMailin target URL. This repository is public; an earlier revision
> of this file leaked one, which is why the value below is a placeholder.

**1. Set the shared secret.** Generate one with
`python3 -c "import secrets;print(secrets.token_urlsafe(32))"`, then put it in
the Supabase dashboard → Edge Functions → Secrets:

    INTAKE_SECRET = <YOUR_INTAKE_SECRET>

Until this is set the endpoint rejects everything (fail-closed), which is the
safe state.

**2. Create a CloudMailin address** (free plan, 10k/month, no card). Point its
target at:

    https://zvffmucghcrqackghhlf.supabase.co/functions/v1/spelling-intake?secret=<YOUR_INTAKE_SECRET>

Format: JSON.

**3. Add a Gmail filter** on lt.dzirasa@gmail.com:
from `mailer@email-support.classroomparent.com` **or** subject contains
`SPELLING LIST` → forward to the CloudMailin address. Gmail will ask to verify
the forwarding address once.

**4. The doc must be shared "anyone with the link"** — the function fetches its
HTML export with no credentials. Verified against the real Week 4 doc.

## What the real email actually looks like

Checked against a real forwarded Week 4 email, and it differs from what the
issue assumed in one important way:

**There is no `docs.google.com` link in the email.** Every link is a
ClassroomParent click-tracker:

    http://url7847.email-support.classroomparent.com/ls/click?upn=u001....

The doc link is the anchor text "Week 4 SPELLING LIST". So the function ranks
anchors by their visible text and follows the best candidate until one lands on
a Google Doc.

One of those trackers is the **unsubscribe** link. Following it would silently
cut the school's emails off, so anything whose anchor text or URL suggests
unsubscribe / opt-out / preferences is excluded and never requested. There is a
test for exactly that.

## What the real doc actually looks like

One table, words on top and the roster underneath in the same columns:

    (blank)   | SUN   | GREEN 1 | GREEN 2 | SKY and SEA
    (blank)   | care  | use     | jacket  | microwave
    ...                                   ...
    Groups    | Sun   | Green 1 | Green 2 | Sky        | Sea
    Students  | ...   | ...     | ...     | Jaden      | ...

Two consequences the parser handles:
- Jaden's group reads as **"Sky"** from the roster, but his words live under the
  combined header **"SKY and SEA"** — matched by splitting on "and"/"/"/"&".
- Without a roster boundary the children's *names* get collected as spelling
  words. Verified: the boundary stops at the `Groups`/`Students` row, and the
  Week 4 parse returns exactly the 23 real words with no names.

## Try a real doc before trusting it

`?dry=1` parses and reports without writing anything:

    curl -s -X POST "https://zvffmucghcrqackghhlf.supabase.co/functions/v1/spelling-intake?dry=1" \
      -H 'Content-Type: application/json' \
      -H 'x-intake-secret: <YOUR_INTAKE_SECRET>' \
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


## Why the CloudMailin address is also a credential

CloudMailin attaches our secret to every message it relays, so anyone who
emails the inbound address gets their content POSTed here **with a valid
secret**. The shared secret protects the endpoint; it does not protect the
mailbox.

So the function also checks provenance: the mail must come from a known
forwarder (`INTAKE_ALLOWED_FROM`) or carry the school's domain in its body
(`INTAKE_ALLOWED_ORIGIN`). Both are env vars with sensible defaults. Mail that
passes neither is recorded as ignored and nothing is published.

That is what makes it safe for the inbound address to be known.
