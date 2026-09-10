1. **Every write is drafted first, without exception.** Show the exact comment text,
   worklog or field change — the real body, not a summary of it — and wait for a yes.
   This holds even when the instruction already names the duration, the ticket and the
   text: "log 30m on AR-4 as DSM" is a request to draft, not permission to send.
   It holds again when an approved draft then changes. A figure the user corrected is a
   new draft and needs its own yes, because what reaches Jira must be what they saw.
   Reads never need approval.
2. **Read before you write.** List existing comments or worklogs so you edit an entry
   rather than adding a near-duplicate.
3. **Never guess a status name.** Fetch the transitions and post the transition id.
4. **Never invent progress.** Describe only what the diff, the journal or the user
   actually says happened. If you cannot substantiate it, leave it out.
5. **Record what you wrote** in `docs/jira/<KEY>.md`, in the same turn, including the id
   the API returned and why the change was made. Never leave a Jira write unjournalled.
