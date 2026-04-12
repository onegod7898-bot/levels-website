# Premium Event Brand Landing Page

This is a starter landing page for a luxury UK event planning brand, featuring a modern, responsive design with elegant styling.

## Usage

1. Open `index.html` in your web browser to view the page.
2. The page is fully self-contained with embedded styles and scripts.

### Local preview (recommended for video / fonts)

**Easiest:** double‑click **`preview.bat`** in this folder. It starts the server in a separate window and opens **http://127.0.0.1:8765/** in your browser. Close the **“Levels preview server”** window when you are finished.

Use **127.0.0.1** in the address bar if `localhost` ever misbehaves.

- **Alternative — npm:** from this folder, `npm install` once, then `npm run preview`.

If port **8765** is stuck, close the preview server window or run `netstat -ano | findstr :8765` and end that PID.

**Cursor:** open the **`levels-website`** folder as the workspace, then **Terminal → Run Task → “Preview Levels site (browser)”** (runs `preview.bat`).

## Features

- **Responsive Design**: Adapts to desktop, tablet, and mobile screens.
- **Sticky Header**: Navigation stays at the top while scrolling.
- **Reveal Animations**: Sections fade in as you scroll using Intersection Observer.
- **Luxury Styling**: Gold accents, serif typography, and soft gradients for a premium feel.
- **Contact Form**: Basic form structure (not functional; add backend for submission).
- **Sections**: Hero, Services, Portfolio, Process, Testimonials, Contact, Footer.

## Technologies

- **HTML5**: Semantic structure.
- **CSS3**: Custom properties, grid/flexbox, animations, media queries.
- **JavaScript**: Intersection Observer for scroll reveals.

## Customization

- Edit embedded `<style>` in `index.html` to adjust colours, fonts, or layout.
- Replace images in `images/` with your own; keep filenames or update paths.
- **`og-image.png`** — 1200×630 share image for Open Graph / Twitter. Replace the file in the project root and redeploy; meta tags point to `https://levels-website.vercel.app/og-image.png`.
- Add form handling (e.g., Formspree, Netlify Forms, or a small API) if you add a contact form later.

## Troubleshooting

- **Animations not working**: Ensure JavaScript is enabled in your browser.
- **Styling issues**: Check for CSS conflicts or missing fonts (Inter is loaded from Google Fonts).
- **Mobile view**: Test on actual devices; use browser dev tools for simulation.
- **Images not loading**: Placeholder images are from Unsplash; replace with local files if needed.

## Dependencies

- Google Fonts: Cormorant Garamond & DM Sans (loaded via CDN).
- No build tools required; open directly in browser.

## Deploy to Vercel

This site is static HTML (no framework build). To host it on [Vercel](https://vercel.com):

1. Push the **`levels-website`** folder to a Git repository (or make this folder the repo root).
2. In Vercel: **Add New Project** → import the repo.
3. **Framework preset:** Other (or “Other” with no framework). **Build command:** leave empty. **Output directory:** `.` (project root).
4. Deploy. Vercel will serve `index.html`, `robots.txt`, and `sitemap.xml` from the project root.
5. In **Project → Settings → Domains**, connect your custom domain when ready and follow DNS instructions from Vercel.
6. **SEO:** Rankings depend on content quality, backlinks, and competition — no host can guarantee “#1 on Google.” This project includes canonical URLs, meta tags, Open Graph, Twitter cards, `robots.txt`, `sitemap.xml`, and JSON-LD (`LocalBusiness` + `WebSite`). If you use a temporary `*.vercel.app` URL before the custom domain is live, update `canonical`, `og:url`, `sitemap.xml`, and `robots.txt` to match your final domain, or add redirects in Vercel so one primary URL is clear to search engines.

CLI (optional): install the [Vercel CLI](https://vercel.com/docs/cli), run `vercel` inside this folder, and follow the prompts.

## License

This is a starter template. Customize as needed for your project.