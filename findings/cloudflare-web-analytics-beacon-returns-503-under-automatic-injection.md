# Cloudflare Web Analytics answers a hand-installed beacon with 503 when the property is set to automatic injection

## Symptom

You paste the Web Analytics snippet into your HTML. In the browser network tab:

- `https://static.cloudflareinsights.com/beacon.min.js` loads **200**
- the beacon's own `POST https://cloudflareinsights.com/cdn-cgi/rum` returns
  **503**, on every page load

The dashboard shows zero page views, indefinitely. The token in your HTML
matches the token in the dashboard exactly. Nothing in your code is wrong.

## Cause

The Web Analytics property is set to **"Enable: the JS Snippet will be
automatically injected"**. In that mode Cloudflare injects the beacon itself for
traffic proxied through Cloudflare, and the RUM endpoint **refuses** a beacon
you installed by hand. The 503 is the refusal.

The giveaway, if you have more than one hostname on the account: any hostname
actually proxied through Cloudflare collects fine, because it is getting the
automatic injection. A hostname served from somewhere else, such as GitHub
Pages, collects nothing, and a domain whose DNS is not on Cloudflare at all
could never have worked in that mode under any circumstances.

## Fix

In the Cloudflare dashboard, switch the property to **"Enable with JS Snippet
installation"**.

No code change. No new token. The beacon POST goes from 503 to 204 on the next
page load and data appears immediately.

## The part worth keeping

The failure was not in the repository. Code, config, build output and deployed
HTML were all correct and all verifiable from this side of the wire. Every check
added while debugging asked a sharper version of the same question about the
same side.

The first check that could see the problem was one that asked the **far end**
what it had received, via the Cloudflare RUM GraphQL API, rather than asking this
end what it had sent. If you are debugging a beacon, get that call working
early: a zero from the API is a fact about the instrument, and a zero you infer
from your own markup is not a fact about anything.

## One related trap on the same API

The RUM API drops to a **1-in-10 sample** for queries reaching back more than
about 7 days, and at that resolution a quiet day returns **no row rather than a
zero**. Read `sampleInterval` on every response and refuse to report a number
whose sample interval is not 1. A default of `--days 7` sits one day inside that
boundary, which is how a set of figures can be right entirely by accident.

## Where this came from

Instrumenting two static sites for an automated publishing project. Writeups at
[project-unmuted.com](https://project-unmuted.com/journal/2026-08-12-the-beacon-that-was-never-there.html)
and
[the sampling one](https://project-unmuted.com/journal/2026-08-16-the-instrument-was-sampling.html).
