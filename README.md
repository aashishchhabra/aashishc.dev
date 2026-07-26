# aashishc.dev

Personal portfolio site for Aashish Chhabra — Senior Lead DevOps & Big Data Platform Engineer.

Single-page site built with plain HTML, CSS, and JavaScript — no frameworks, no build step. Everything lives in `index.html`.

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

## Structure

- `index.html` — the entire site (HTML/CSS/JS inline)
- `CNAME` — custom domain for GitHub Pages
- `README.md` — this file
