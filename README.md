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
5. Under **Custom domain**, enter `aashishc.dev` and save (this reads the `CNAME` file already in the repo).
6. Once DNS propagates, check **Enforce HTTPS**.

### DNS

Point your domain's DNS records at GitHub Pages:

- `A` records for the apex domain (`aashishc.dev`) → GitHub Pages IPs (`185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`)
- Or a `CNAME` record if using a `www` subdomain, pointing to `<username>.github.io`

## Features

- 3D interactive node-cluster hero (Three.js + OrbitControls) — drag to rotate, click amber nodes for stats
- Working terminal ("Command Center") — explore experience, stack, and projects via real shell commands
- Simulated ops telemetry widget (clearly labeled illustrative, not real production data)
- Draggable career timeline scrubber with an animated growth metric
- Expandable project case-study cards, including a full deep-dive page for Kafka-as-a-Service
- Filterable tech stack, animated skill radar chart, scroll reveals throughout
- Light/dark theme toggle (persisted, defaults to system preference)
- Command palette (`⌘K` / `Ctrl+K`) — jump to any section or run an action from the keyboard
- One-click copy on email/phone with toast confirmation
- Downloadable PDF résumé, kept in sync with on-site content
- Open Graph / Twitter meta tags with a generated social preview image
- Placeholder cards in the footer for future `blog.aashishc.dev` / video subdomains

## Structure

- `index.html` — the main single-page site (HTML/CSS/JS inline)
- `case-study-kafka.html` — deep-dive case study for the Kafka-as-a-Service project, with an interactive architecture diagram
- `Aashish-Chhabra-Resume.pdf` — downloadable résumé (generated with reportlab; regenerate if site content changes)
- `og-image.png` — social share preview image (1200×630)
- `CNAME` — custom domain for GitHub Pages
- `README.md` — this file
