# weekly-report

Every Monday morning, each parent linked to a student gets an email about that
student's practice for the week that just ended (Monday to Sunday, Eastern
time):

- sessions, minutes, questions and accuracy, with minutes per day
- accuracy by subject, compared with the week before
- topics that need more work (at least 3 tries, under 70%) and topics going
  well (at least 5 tries, 90% or more)
- a few questions he missed, with the typed answer where there is one
- what was added to the app that week (spelling lists, emailed worksheets)
- a plain "no practice recorded" when there wasn't any

The numbers use the same rules as the app's Progress screen, so the email and
the app agree. `report.js` builds the report and `report.test.mjs` covers it.

    pg_cron, Monday 12:00 UTC (8am EDT / 7am EST)
      -> POST weekly-report with REPORT_SECRET
      -> for each student with parents in `parents`
      -> one email per parent, sent through Gmail
      -> report_runs records it, so a second firing doesn't resend

## Parents

`parents` links any number of parents to a student, one row per email
address:

    insert into parents (student, name, email) values
      ('Jaden', 'Delali', 'delali.dzirasa@gmail.com'),
      ('Jaden', '<name>', 'lt.dzirasa@gmail.com');

- Set `receives_report = false` to pause a parent without deleting the row.
- A new student just needs parent rows with that student's name.
- The table holds email addresses, so the app's public anon key has no access
  to it. Edit it in the SQL editor or the Table Editor.

## Why Gmail

Without a domain, the dependable option is to send *from* a Gmail account
through Gmail's own servers. The mail is genuinely from Gmail, so it isn't
marked as spoofed. Services like Resend or Postmark need a verified domain
before they'll send to anyone except the account owner.

Use a Gmail account you control. A separate one for the app (e.g.
`jaden.practice@gmail.com`) keeps the reports out of your own Sent folder.
Gmail allows about 500 messages a day, far more than this needs.

## Setup (one time)

**1. Run `migrations/007_parents_and_weekly_report.sql`**, then insert the
parent rows above.

**2. Make a Gmail app password** for the sending account. The account needs
2-Step Verification on. Then go to <https://myaccount.google.com/apppasswords>
and create one named "jaden-mcap". It's 16 characters.

**3. Add the secrets** under Supabase dashboard -> Edge Functions -> Secrets:

    GMAIL_USER          = <sending gmail address>
    GMAIL_APP_PASSWORD  = <the 16-character app password>
    REPORT_SECRET       = <python3 -c "import secrets;print(secrets.token_urlsafe(32))">
    APP_URL             = <the app's address, for the "Open the app" link>   (optional)

**4. Deploy:**

    supabase functions deploy weekly-report

**5. Preview without sending:**

    curl -s -X POST "https://zvffmucghcrqackghhlf.supabase.co/functions/v1/weekly-report?dry=1" \
      -H "x-report-secret: <REPORT_SECRET>"

This returns the summary and each rendered email. Add `&now=2026-10-19` to
preview a particular week.

**6. Send one real email to yourself first:**

    curl -s -X POST "https://zvffmucghcrqackghhlf.supabase.co/functions/v1/weekly-report?to=<your linked address>" \
      -H "x-report-secret: <REPORT_SECRET>"

`to=` only accepts a linked parent's address, and doesn't mark the week as
sent.

**7. Schedule it.** In the SQL editor, enable the `pg_cron` and `pg_net`
extensions (Database -> Extensions), then:

    select vault.create_secret('<REPORT_SECRET>', 'report_secret');

    select cron.schedule('weekly-report', '0 12 * * 1', $$
      select net.http_post(
        url := 'https://zvffmucghcrqackghhlf.supabase.co/functions/v1/weekly-report',
        headers := jsonb_build_object(
          'Content-Type', 'application/json',
          'x-report-secret', (select decrypted_secret from vault.decrypted_secrets where name = 'report_secret')),
        body := '{}'::jsonb,
        timeout_milliseconds := 60000)
    $$);

pg_cron runs in UTC, so 12:00 UTC is 8am in summer and 7am in winter.

> **Never commit the secrets.** They live only in the Supabase dashboard and
> Vault.

## Checking it ran

    select * from report_runs order by created_at desc limit 10;

A `failed` row has the reason in `detail`. To resend a week, call the function
with `&force=1`.
