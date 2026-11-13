# SPEC — Steicy Semi-Jóias · Catálogo Exclusivo (v2 redesign)

Single-page static catalog (pt-BR) for a fashion-jewelry reseller ("Revendedora Cristali").
Positioning: ALTO TICKET / exclusivity — "Royal Navy & Champagne Gold" design language per /app/design_guidelines.json.

## What the app does
- Editorial luxury catalog: 55 products WITH photos (brincos, anéis, pulseiras, colares) — photo, name, metal chip (Banho de ouro / Prata 925), REF, price in BRL, WhatsApp "Consultar" per card.
- Products WITHOUT a photo are HIDDEN (user decision): upfront-filtered via `WITHOUT_PHOTO` set (16 refs) in index.html. To re-list a piece: add `ref-<REF>.png` to the repo root and remove its REF from the set. Runtime safety: an image that 404s removes its own card and recounts.
- Category filter pills (Todos/Brincos/Anéis/Pulseiras/Colares) + live count "Exibindo X peças exclusivas" (#count).
- Ordering is off-site via WhatsApp deep links (wa.me/5551993614204) pre-filled with the product REF; nav button, per-card "Consultar", section CTA, footer link and floating button.
- Promo banner: "Natal Steicy · A cada R$ 100,00 em compras, ganhe um bilhete para concorrer a um conjunto de colar e brincos."
- `hl: true` products render a gold "Curadoria" badge (85516, 83620, 85098, 88274).
- Photo ref-87863.png exists but has NO product entry (user said ignore for now).

## Design system (v2)
- Palette: page #FCFAF6 ivory, navy #0C192C/#0A1320, panel #FFF, gold #C8A86B / #D4AF37 / #F5E6CA, border #EAE5DB, WhatsApp green #25D366. Harmonizes with supplier photos (cream ground + navy azulejo frames).
- Type: Playfair Display (headings) + Plus Jakarta Sans (body/UI), Google Fonts <link>.
- Sections: promo banner (navy) → glass sticky nav → navy gradient hero (logo disc w/ gold ring) → catalog (3-col grid → 2 → 1, hover translateY(-4px) + gold border) → navy "Como comprar" (3 serif-gold numbered steps + green WA CTA) → footer → floating WA button.
- Motion: fadeUp card entrance (staggered, capped at 8), hover lifts, prefers-reduced-motion fully disabled.

## Stack & serving
- Static single file `index.html` (vanilla JS, no build step) + `logo.png` + photos `ref-<REF>.png` at repo root.
- Served by `frontend/server.js` (zero-dependency Node) via supervisor program `frontend` (`yarn dev`, PORT=3000, HOST=0.0.0.0). Preview ingress → port 3000.
- No backend, no database, no auth (supervisor `backend` stays FATAL by design — repo has none).
- No login/credentials anywhere.

## Data model
- `PRODUCTS` inline in index.html: `{ cat, ref, name, metal, price, hl? }` — 71 entries kept even when hidden (data preserved).
- Counts by category with photos: brincos 24, anéis 14, pulseiras 4, colares 13 → 55 visible.
- Adding a product: append to `PRODUCTS` + drop `ref-<REF>.png` at root (keep it OUT of `WITHOUT_PHOTO`).
