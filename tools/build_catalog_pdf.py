"""Gera /app/catalogo-steicy.pdf a partir da lista PRODUCTS do index.html.

Uso:  python3 /app/tools/build_catalog_pdf.py
Rode de novo sempre que mudar produtos, preços ou fotos — o PDF segue o site.
"""
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path('/app')
FONTS = ROOT / 'tools' / 'fonts'
OUT = ROOT / 'catalogo-steicy.pdf'

# A4 em 150 dpi
W, H = 1240, 1754
M = 80  # margem

NAVY = (12, 25, 44)
NAVY_DEEP = (7, 14, 24)
IVORY = (252, 250, 246)
INK = (20, 29, 43)
MUTED = (92, 103, 121)
MUTED_NAVY = (186, 199, 213)
GOLD = (200, 168, 107)
GOLD_BRIGHT = (212, 175, 55)
GOLD_LIGHT = (245, 230, 202)
LINE = (234, 229, 219)

CATS = [('brincos', 'Brincos'), ('aneis', 'Anéis'), ('pulseiras', 'Pulseiras'), ('colares', 'Colares')]
WA_NUMBER = '(51) 99361-4204'


def font(name: str, size: int, weight: int) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(str(FONTS / name), size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def serif(size, weight=600):
    return font('PlayfairDisplay.ttf', size, weight)


def sans(size, weight=500):
    return font('PlusJakartaSans.ttf', size, weight)


def load_products():
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    pattern = re.compile(
        r"\{ cat: '(\w+)', ref: '(\d+)', name: '([^']*)', metal: '([^']*)', price: (\d+)(, hl: true)? \}"
    )
    products = [
        {'cat': c, 'ref': r, 'name': n, 'metal': m, 'price': int(p), 'hl': bool(h)}
        for c, r, n, m, p, h in pattern.findall(html)
    ]
    block = re.search(r'WITHOUT_PHOTO = new Set\(\[(.*?)\]\)', html, re.S)
    hidden = set(re.findall(r"'(\d+)'", block.group(1))) if block else set()
    return [p for p in products if p['ref'] not in hidden and (ROOT / f"ref-{p['ref']}.png").exists()]


def brl(v: int) -> str:
    return f'R$ {v:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def wrap(draw, text, f, max_w):
    lines, cur = [], ''
    for word in text.split():
        test = f'{cur} {word}'.strip()
        if draw.textlength(test, font=f) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def spaced(draw, xy, text, f, fill, tracking=3):
    """Texto com espaçamento entre letras (eyebrows em caixa alta)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textlength(ch, font=f) + tracking
    return x


def spaced_width(draw, text, f, tracking=3):
    return sum(draw.textlength(ch, font=f) + tracking for ch in text) - tracking


def footer(draw, page_no, dark=False):
    color = MUTED_NAVY if dark else MUTED
    draw.line([(M, H - 92), (W - M, H - 92)], fill=(40, 55, 80) if dark else LINE, width=1)
    f = sans(20, 500)
    draw.text((M, H - 70), 'Steicy Semi-Jóias · Revendedora Cristali', font=f, fill=color)
    right = f'WhatsApp {WA_NUMBER}   ·   {page_no:02d}'
    draw.text((W - M - draw.textlength(right, font=f), H - 70), right, font=f, fill=color)


def cover(products):
    page = Image.new('RGB', (W, H), NAVY)
    d = ImageDraw.Draw(page)
    # degradê radial simples
    glow = Image.new('RGB', (W, H), NAVY_DEEP)
    mask = Image.new('L', (W, H), 0)
    ImageDraw.Draw(mask).ellipse([W * 0.25, -H * 0.15, W * 1.35, H * 0.65], fill=150)
    from PIL import ImageFilter
    mask = mask.filter(ImageFilter.GaussianBlur(160))
    page = Image.composite(Image.new('RGB', (W, H), (22, 38, 61)), page, mask)
    d = ImageDraw.Draw(page)
    d.rectangle([40, 40, W - 40, H - 40], outline=GOLD, width=2)
    d.rectangle([52, 52, W - 52, H - 52], outline=(70, 70, 60), width=1)

    # logo em disco
    size = 460
    logo = Image.open(ROOT / 'logo.png').convert('RGB').resize((size, size), Image.LANCZOS)
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size, size], fill=255)
    cx, top = W // 2, 300
    d.ellipse([cx - size // 2 - 22, top - 22, cx + size // 2 + 22, top + size + 22], outline=GOLD, width=2)
    page.paste(logo, (cx - size // 2, top), mask)

    f = sans(22, 700)
    t = 'CATÁLOGO DE SEMIJOIAS'
    spaced(d, (cx - spaced_width(d, t, f, 6) / 2, 200), t, f, GOLD_BRIGHT, 6)

    f = serif(96, 600)
    t = 'Steicy Semi-Jóias'
    d.text((cx - d.textlength(t, font=f) / 2, 850), t, font=f, fill=IVORY)
    f = serif(44, 600)
    t = 'Revendedora Cristali'
    d.text((cx - d.textlength(t, font=f) / 2, 975), t, font=f, fill=GOLD_LIGHT)

    f = sans(26, 600)
    t = 'Banho de ouro  ·  Prata 925  ·  Curadoria Cristali'
    d.text((cx - d.textlength(t, font=f) / 2, 1070), t, font=f, fill=MUTED_NAVY)
    f = sans(24, 500)
    t = f'{len(products)} peças exclusivas'
    d.text((cx - d.textlength(t, font=f) / 2, 1118), t, font=f, fill=MUTED_NAVY)

    # caixa Natal Steicy
    bx0, by0, bx1, by1 = M + 40, 1230, W - M - 40, 1500
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=14, outline=GOLD, width=2, fill=(16, 30, 50))
    f = sans(22, 700)
    t = '—  NATAL STEICY  —'
    spaced(d, (cx - spaced_width(d, t, f, 5) / 2, by0 + 40), t, f, GOLD_BRIGHT, 5)
    f = serif(40, 600)
    t = 'A cada R$ 100,00 em compras, 1 bilhete'
    d.text((cx - d.textlength(t, font=f) / 2, by0 + 92), t, font=f, fill=IVORY)
    f = sans(26, 500)
    t = 'para concorrer a um conjunto de colar e brincos.'
    d.text((cx - d.textlength(t, font=f) / 2, by0 + 162), t, font=f, fill=MUTED_NAVY)

    f = sans(26, 700)
    t = f'Peça pelo WhatsApp  {WA_NUMBER}'
    d.text((cx - d.textlength(t, font=f) / 2, 1570), t, font=f, fill=GOLD_LIGHT)
    return page


def product_pages(products, start_no):
    pages = []
    cols, rows = 3, 2
    gap = 32
    cell_w = (W - 2 * M - gap * (cols - 1)) // cols
    img_size = cell_w
    cell_h = img_size + 200
    header_h = 220
    page_no = start_no
    for cat, label in CATS:
        items = [p for p in products if p['cat'] == cat]
        if not items:
            continue
        per = cols * rows
        chunks = [items[i:i + per] for i in range(0, len(items), per)]
        for ci, chunk in enumerate(chunks):
            page = Image.new('RGB', (W, H), IVORY)
            d = ImageDraw.Draw(page)
            f = sans(20, 700)
            d.line([(M, M + 18), (M + 50, M + 18)], fill=GOLD, width=2)
            spaced(d, (M + 66, M + 4), 'COLEÇÃO EXCLUSIVA', f, (154, 126, 63), 5)
            f = serif(64, 600)
            title = label if ci == 0 else f'{label} (cont.)'
            d.text((M, M + 46), title, font=f, fill=NAVY)
            f = sans(22, 500)
            t = f'{len(items)} peças'
            d.text((W - M - d.textlength(t, font=f), M + 82), t, font=f, fill=MUTED)

            for i, p in enumerate(chunk):
                col, row = i % cols, i // cols
                x = M + col * (cell_w + gap)
                y = M + header_h + row * (cell_h + 40)
                d.rectangle([x, y, x + cell_w, y + cell_h], fill=(255, 255, 255), outline=LINE, width=1)
                photo = Image.open(ROOT / f"ref-{p['ref']}.png").convert('RGB').resize((img_size, img_size), Image.LANCZOS)
                page.paste(photo, (x, y))
                if p['hl']:
                    f = sans(16, 700)
                    t = 'CURADORIA'
                    tw = spaced_width(d, t, f, 3)
                    d.rectangle([x + 14, y + 14, x + 14 + tw + 24, y + 48], fill=GOLD)
                    spaced(d, (x + 26, y + 20), t, f, INK, 3)
                ty = y + img_size + 16
                if p['metal']:
                    f = sans(15, 700)
                    t = p['metal'].upper()
                    tw = spaced_width(d, t, f, 2)
                    d.rounded_rectangle([x + 16, ty, x + 16 + tw + 22, ty + 30], radius=15,
                                        fill=(248, 242, 230), outline=(222, 205, 168), width=1)
                    spaced(d, (x + 27, ty + 6), t, f, NAVY, 2)
                    ty += 40
                f = sans(21, 600)
                for line in wrap(d, p['name'], f, cell_w - 32)[:2]:
                    d.text((x + 16, ty), line, font=f, fill=INK)
                    ty += 28
                f = sans(17, 500)
                d.text((x + 16, y + cell_h - 46), f"REF {p['ref']}", font=f, fill=MUTED)
                f = sans(28, 700)
                price = brl(p['price'])
                d.text((x + cell_w - 16 - d.textlength(price, font=f), y + cell_h - 54), price, font=f, fill=NAVY)
            footer(d, page_no)
            pages.append(page)
            page_no += 1
    return pages, page_no


def closing(page_no):
    page = Image.new('RGB', (W, H), NAVY_DEEP)
    d = ImageDraw.Draw(page)
    d.rectangle([40, 40, W - 40, H - 40], outline=GOLD, width=2)
    f = sans(22, 700)
    d.line([(M + 40, 318), (M + 90, 318)], fill=GOLD, width=2)
    spaced(d, (M + 106, 304), 'SEU PRÓXIMO PASSO', f, GOLD_BRIGHT, 5)
    d.text((M + 40, 350), 'Como comprar', font=serif(84, 600), fill=IVORY)
    d.text((M + 40, 480), 'Anote a referência, envie uma mensagem e combinamos', font=sans(28, 500), fill=MUTED_NAVY)
    d.text((M + 40, 520), 'os detalhes pelo WhatsApp.', font=sans(28, 500), fill=MUTED_NAVY)
    steps = [
        ('01', 'Escolha sua peça', 'Anote a referência de quem chamou sua atenção.'),
        ('02', 'Envie uma mensagem', 'Informe a referência escolhida no WhatsApp da Steicy.'),
        ('03', 'Combine os detalhes', 'Confirme disponibilidade, valor e entrega no atendimento.'),
    ]
    y = 650
    for num, title, desc in steps:
        d.line([(M + 40, y), (W - M - 40, y)], fill=(60, 66, 70), width=1)
        d.text((M + 40, y + 30), num, font=serif(72, 400), fill=GOLD_BRIGHT)
        d.text((M + 200, y + 40), title, font=serif(40, 600), fill=IVORY)
        d.text((M + 200, y + 100), desc, font=sans(26, 500), fill=MUTED_NAVY)
        y += 200
    by = y + 60
    d.rounded_rectangle([M + 40, by, W - M - 40, by + 120], radius=60, fill=(37, 211, 102))
    f = sans(38, 700)
    t = f'WhatsApp  {WA_NUMBER}'
    d.text((W / 2 - d.textlength(t, font=f) / 2, by + 36), t, font=f, fill=(255, 255, 255))
    f = sans(24, 500)
    t = 'wa.me/5551993614204'
    d.text((W / 2 - d.textlength(t, font=f) / 2, by + 150), t, font=f, fill=GOLD_LIGHT)
    footer(d, page_no, dark=True)
    return page


def main():
    products = load_products()
    pages = [cover(products)]
    body, next_no = product_pages(products, 2)
    pages += body
    pages.append(closing(next_no))
    pages[0].save(OUT, 'PDF', save_all=True, append_images=pages[1:], resolution=150, quality=82)
    counts = {c: sum(p['cat'] == c for p in products) for c, _ in CATS}
    print(f'{OUT} · {len(pages)} páginas · {len(products)} peças · {counts} · {OUT.stat().st_size // 1024} KB')


if __name__ == '__main__':
    main()
