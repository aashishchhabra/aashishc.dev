# aashishc.dev

Personal portfolio site for Aashish Chhabra — Senior Lead DevOps & Big Data Platform Engineer.

Single-page site built with plain HTML, CSS, and JavaScript — no build step, no local dependencies. Everything lives in `index.html`. The one exception is [Three.js](https://threejs.org/) (r128, loaded via `<script>` tags from jsDelivr) which drives the interactive 3D node cluster in the hero; if it fails to load, the hero gracefully falls back to a lightweight 2D canvas animation.

## Local preview

Just open the file directly, or serve it locally:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Deployment (GitHub Pages)

1. Push this repo to GitHub as `aashishc.dev`.
2. In the repo, go to **Settings → Pages**.
3. Under **Build and deployment → Source**, choose **Deploy from a branch**.
4. Branch: `main`, folder: `/ (root)`. Save.
5. The site is now live at `https://<username>.github.io/aashishc.dev/`.

There's currently **no `CNAME` file** in the repo, on purpose — the `aashishc.dev` domain isn't registered/pointed yet. GitHub Pages redirects the default `github.io` URL to whatever custom domain a `CNAME` file specifies, so adding one before DNS is configured would break the live site. Once the domain is ready:

1. Add a `CNAME` file back at the repo root containing just `aashishc.dev`.
2. Point the domain's DNS at GitHub Pages (see below).
3. In **Settings → Pages → Custom domain**, enter `aashishc.dev` and save.
4. Once DNS propagates, check **Enforce HTTPS**.
5. Update the `og:url` / `canonical` / `og:image` / `twitter:image` URLs in `index.html` and `case-study-kafka.html` from the `github.io` URL to `https://aashishc.dev/`.

### DNS (once you have the domain)

- `A` records for the apex domain (`aashishc.dev`) → GitHub Pages IPs (`185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`)
- Or a `CNAME` record if using a `www` subdomain, pointing to `<username>.github.io`

## Features

- 3D interactive node-cluster hero (Three.js + OrbitControls) — drag to rotate, click amber nodes for stats
- Working terminal ("Command Center") — explore experience, stack, and projects via real shell commands
- Simulated ops telemetry widget (clearly labeled illustrative, not real production data)
- Draggable career timeline scrubber with an animated growth metric
- Expandable project case-study cards, including a full deep-dive page for the Kafka Platform build
- Filterable tech stack, animated skill radar chart, scroll reveals throughout
- Light/dark theme toggle (persisted, defaults to system preference)
- Command palette (`⌘K` / `Ctrl+K`) — jump to any section or run an action from the keyboard
- One-click copy on email/phone with toast confirmation
- Downloadable PDF résumé, kept in sync with on-site content
- Open Graph / Twitter meta tags with a generated social preview image
- Placeholder cards in the footer for future `blog.aashishc.dev` / video subdomains

## Structure

- `index.html` — the main single-page site (HTML/CSS/JS inline)
- `case-study-kafka.html` — deep-dive case study for the Kafka Platform project, with an interactive architecture diagram
- `Aashish-Chhabra-Resume.pdf` — downloadable résumé (generated with reportlab; regenerate if site content changes)
- `og-image.png` — social share preview image (1200×630)
- `README.md` — this file

Note: there is no `CNAME` file right now — see **Deployment** above for why, and how to add it back once the domain is ready.
