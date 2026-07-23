# PICO Modern Agriculture — website

A modern, mobile-first marketing site for PICO Modern Agriculture, a third-generation
Egyptian grower and exporter of fresh produce. Built as a self-contained static site
with **interactive 3D fruit** you can drag and spin.

> Independent concept. Company facts (7,000 acres, crops, certifications, export markets)
> are drawn from public sources; contact details are placeholders pending real info.

## Features

- **Interactive 3D fruit** (Three.js) — a draggable strawberry in the hero, plus a
  strawberry / mango / citrus showcase you can rotate and switch between. Auto-rotates
  when idle, pauses when off-screen, and honours `prefers-reduced-motion`.
- **Bilingual EN / AR** with full right-to-left layout, localised numerals, and a
  one-tap language switch (remembered across visits).
- **Light / dark theme** that follows the system preference and can be toggled.
- **Fully responsive** down to small phones, with touch-friendly rotation.
- **Accessible**: skip link, keyboard focus states, reduced-motion fallbacks, ARIA labels.
- **Easter eggs** (subtle & delightful):
  - Tap the hero strawberry **5×** to make it spin and rain fruit.
  - The **Konami code** (`↑ ↑ ↓ ↓ ← → ← → b a`) triggers a fruit storm.
  - Honk the **🚜 tractor** in the footer and watch it drive off.
  - A hidden message in the browser **console**.

## Run it

It's plain HTML/CSS/JS — no build step.

```bash
# any static server works
python3 -m http.server 8099
# then open http://localhost:8099
```

Or open `index.html` directly (a server is only needed so the browser fetches the
CDN libraries over http/https). Deploys as-is to GitHub Pages, Netlify, Vercel, etc.

## Structure

```
index.html          # markup + section content
css/styles.css      # design system (green palette, light/dark, RTL, responsive)
js/i18n.js          # EN/AR translations + language/RTL switching
js/fruits3d.js      # procedural Three.js fruit models + viewer
js/main.js          # nav, theme, reveals, counters, form, easter eggs
```

## Dependencies (via CDN, loaded in the browser)

- [Three.js r128](https://threejs.org/) + OrbitControls — the 3D fruit
- Google Fonts: Sora, Plus Jakarta Sans, Tajawal (Arabic)

## To make it production-ready

- Replace placeholder **contact details** (email, phone, address) with the real ones.
- Swap the heritage photo for a licensed PICO farm photograph.
- Wire the contact form to a real endpoint (Formspree, an email service, or a backend).
- Add the official PICO logo in place of the placeholder leaf mark.
