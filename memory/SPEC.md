# SPEC — Steicy Semi-Jóias · Catálogo Exclusivo (v3 lilás)

Single-page static catalog (pt-BR) for a fashion-jewelry reseller ("Revendedora Cristali").
Positioning: ALTO TICKET / exclusivity. v3 (pedido da cliente): SEM azul-marinho — fundo branco, lilás como cor principal (textos, títulos, botões, seleção), dourado champanhe nos detalhes. A paleta navy de /app/design_guidelines.json está OBSOLETA; vale a seção "Design system (v3)" abaixo.

## What the app does
- Editorial luxury catalog: products WITH photos (brincos, anéis, pulseiras, colares) — photo, name, metal chip (Banho de ouro / Prata 925), REF, price in BRL and a full-width "Comprar pelo WhatsApp" button per card (`product-buy-btn-<REF>`) opening wa.me/5551993614204 with: Olá Steicy! Quero comprar a peça "<nome>" (REF <ref>) no valor de R$ X,XX. Ela está disponível?
- Products WITHOUT a photo are HIDDEN (user decision): upfront-filtered via `WITHOUT_PHOTO` set (16 refs) in index.html. To re-list a piece: add `ref-<REF>.png` to the repo root and remove its REF from the set. Runtime safety: an image that 404s removes its own card and recounts.
- Category filter pills (Todos/Brincos/Anéis/Pulseiras/Colares) + live count "Exibindo X peças exclusivas" (#count).
- Ordering is off-site via WhatsApp deep links (wa.me/5551993614204) pre-filled with the product REF; nav button, per-card "Comprar pelo WhatsApp", section CTA, footer link and floating button.
- Faixa do topo ALTERNA a cada 5s (setInterval, `.promo > p` com `hidden`): slide 1 Natal Steicy, slide 2 "Grupo VIP" (`promo-group`) com chip "Quero participar" (`promo-group-link`) → https://chat.whatsapp.com/HXl4jzAJ6ASErMYgSikaJq.
- SACOLINHA DE PEDIDOS (client-side, localStorage key `steicy-sacolinha` = {ref: qty}): botão "+ Adicionar à sacolinha" em cada card (`product-add-bag-<REF>`), ícone de sacola na nav com contador (`bag-open`, `bag-count`), gaveta lateral (`bag-drawer`) com itens, +/− quantidade (`bag-plus-/bag-minus-<REF>`), total (`bag-total`), aviso de bilhetes do Natal = floor(total/100) (`bag-tickets`), "Enviar pedido pelo WhatsApp" (`bag-send`, wa.me/5551993614204 com lista "• Nx Nome (REF) — R$" + Total) e "Esvaziar" (`bag-clear`). Toast "foi para a sacolinha" + "Ver sacolinha". Esc/overlay fecham. Sem backend: o pedido só vale quando a cliente envia a mensagem.
- Promo banner enriquecido (Natal Steicy): faixa superior lilás com filete dourado e sparkles + contagem regressiva "Faltam N dias para o Natal" (JS client-side, aparece só a ≤90 dias, some após 25/12), atalho "Promoção" no menu, selo dourado no hero e seção dedicada `#natal` (mecânica: 1 bilhete a cada R$ 100; prêmio: conjunto de colar e brincos; CTA WhatsApp "Quero meus bilhetes"). O ano do alvo é sempre o próximo 25/12.
- `hl: true` products render a gold "Curadoria" badge (85516, 83620, 85098, 88274).
- Photo ref-87863.png now HAS a product entry: aneis · "Anel cinco gotas com pedra vermelha e zircônias" · Banho de ouro · R$ 199 (price/finish from the supplier card itself).

## Catálogo em PDF
- `/app/catalogo-steicy.pdf` (A4, 14 páginas, branco/lilás/dourado: capa branca c/ logo + Natal Steicy, páginas por categoria 3×2 com foto/metal/nome/REF/preço, página final "Como comprar" + WhatsApp).
- Gerado por `python3 /app/tools/build_catalog_pdf.py` (Pillow + fontes Playfair/Plus Jakarta em /app/tools/fonts). Lê PRODUCTS e WITHOUT_PHOTO direto do index.html → RODE DE NOVO após qualquer mudança de produto/preço/foto.
- Links de download: botão "Baixar catálogo em PDF" no hero (`pdf-download`) e link na seção Como comprar (`pdf-download-footer`).

## Design system (v3 — lilás + branco)
- Palette: fundo #FFFFFF, lilás #6B5B7B (principal/títulos), #5F4F6E (botões, pill ativa, faixa Natal), hover #74638A, texto #4E4060, muted #756C7D, tint #F7F3FA (seção Como comprar, card Natal), borda #ECE6F0, dourado #C8A86B (linhas/bordas/badges), dourado texto #9A7E3F, #F5E6CA. Botão flutuante segue verde WhatsApp #25D366. NUNCA reintroduzir azul-marinho.
- Type: Playfair Display (headings) + Plus Jakarta Sans (body/UI), Google Fonts <link>.
- Sections: faixa Natal lilás c/ filete dourado → nav branca glass → hero branco c/ brilho lilás + logo em disco dourado → card Natal (tint lilás, borda dourada) → catálogo (3→2→1 col, hover lift + borda dourada) → Como comprar (tint lilás) → footer branco → WA flutuante.
- Motion: fadeUp card entrance, hover lifts, prefers-reduced-motion respeitado.

## Stack & serving
- Static single file `index.html` (vanilla JS, no build step) + `logo.png` + photos `ref-<REF>.png` at repo root.
- Served by `frontend/server.js` (zero-dependency Node) via supervisor program `frontend` (`yarn dev`, PORT=3000, HOST=0.0.0.0). Preview ingress → port 3000.
- No backend, no database, no auth (supervisor `backend` stays FATAL by design — repo has none).
- No login/credentials anywhere.

## Data model
- `PRODUCTS` inline in index.html: `{ cat, ref, name, metal, price, hl? }` — 71 entries kept even when hidden (data preserved).
- Counts by category with photos: brincos 25, anéis 14, pulseiras 4, colares 13 → 56 visible. (Argola linha coração verde / 88242 é BRINCO, corrigido a pedido da cliente.)
- Adding a product: append to `PRODUCTS` + drop `ref-<REF>.png` at root (keep it OUT of `WITHOUT_PHOTO`).
