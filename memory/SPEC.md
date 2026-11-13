# SPEC — Steicy Semi-Jóias · Catálogo Exclusivo (v2 redesign)

Single-page static catalog (pt-BR) for a fashion-jewelry reseller ("Revendedora Cristali").
Positioning: ALTO TICKET / exclusivity — "Royal Navy & Champagne Gold" design language per /app/design_guidelines.json.

## What the app does
- Editorial luxury catalog: 55 products WITH photos (brincos, anéis, pulseiras, colares) — photo, name, metal chip (Banho de ouro / Prata 925), REF, price in BRL, WhatsApp "Consultar" per card.
- Products WITHOUT a photo are HIDDEN (user decision): upfront-filtered via `WITHOUT_PHOTO` set (16 refs) in index.html. To re-list a piece: add `ref-<REF>.png` to the repo root and remove its REF from the set. Runtime safety: an image that 404s removes its own card and recounts.
- Category filter pills (Todos/Brincos/Anéis/Pulseiras/Colares) + live count "Exibindo X peças exclusivas" (#count).
- Ordering is off-site via WhatsApp deep links (wa.me/5551993614204) pre-filled with the product REF; nav button, per-card "Consultar", section CTA, footer link and floating button.
- Promo banner enriquecido (Natal Steicy): faixa superior navy/gold com sparkles + contagem regressiva "Faltam N dias para o Natal" (JS client-side, aparece só a ≤90 dias, some após 25/12), atalho "Promoção" no menu, selo dourado no hero e seção dedicada `#natal` (mecânica: 1 bilhete a cada R$ 100; prêmio: conjunto de colar e brincos; CTA WhatsApp "Quero meus bilhetes"). O ano do alvo é sempre o próximo 25/12.
- `hl: true` products render a gold "Curadoria" badge (85516, 83620, 85098, 88274).
- Photo ref-87863.png now HAS a product entry: aneis · "Anel cinco gotas com pedra vermelha e zircônias" · Banho de ouro · R$ 199 (price/finish from the supplier card itself).

## Catálogo em PDF
- `/app/catalogo-steicy.pdf` (A4, 14 páginas: capa navy c/ logo + Natal Steicy, páginas por categoria 3×2 com foto/metal/nome/REF/preço, página final "Como comprar" + WhatsApp).
- Gerado por `python3 /app/tools/build_catalog_pdf.py` (Pillow + fontes Playfair/Plus Jakarta em /app/tools/fonts). Lê PRODUCTS e WITHOUT_PHOTO direto do index.html → RODE DE NOVO após qualquer mudança de produto/preço/foto.
- Links de download: botão "Baixar catálogo em PDF" no hero (`pdf-download`) e link na seção Como comprar (`pdf-download-footer`).

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
- Counts by category with photos: brincos 25, anéis 14, pulseiras 4, colares 13 → 56 visible. (Argola linha coração verde / 88242 é BRINCO, corrigido a pedido da cliente.)
- Adding a product: append to `PRODUCTS` + drop `ref-<REF>.png` at root (keep it OUT of `WITHOUT_PHOTO`).
