"""Genera los íconos de ZK-REMOTE a partir de zk/branding/source/logo.webp.

Uso (requiere Pillow):  python zk/tools/make_icons.py
Los archivos generados se versionan en zk/branding/ y los aplica apply_branding.py.
"""

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "branding" / "source" / "logo.webp"
OUT = ROOT / "branding"

BRAND = (1, 176, 233, 255)  # #01B0E9, color medido del logo
ICO_SIZES = [16, 20, 24, 32, 40, 48, 64, 128, 256]


def load_logo() -> Image.Image:
    logo = Image.open(SRC).convert("RGBA")
    return logo.crop(logo.getbbox())


def white_logo(logo: Image.Image) -> Image.Image:
    white = Image.new("RGBA", logo.size, (255, 255, 255, 0))
    white.putalpha(logo.getchannel("A"))
    return Image.alpha_composite(Image.new("RGBA", logo.size, (255, 255, 255, 0)), white)


def app_icon(size: int, logo_white: Image.Image) -> Image.Image:
    """Cuadrado redondeado en color de marca con el logo en blanco."""
    scale = 4  # supersampling para bordes suaves
    big = size * scale
    canvas = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    radius = int(big * 0.22)
    ImageDraw.Draw(canvas).rounded_rectangle((0, 0, big - 1, big - 1), radius, fill=BRAND)
    pad = 0.14 if size >= 32 else 0.08
    max_w = int(big * (1 - 2 * pad))
    w, h = logo_white.size
    ratio = max_w / w
    lw, lh = max_w, int(h * ratio)
    resized = logo_white.resize((lw, lh), Image.LANCZOS)
    canvas.alpha_composite(resized, ((big - lw) // 2, (big - lh) // 2))
    return canvas.resize((size, size), Image.LANCZOS)


def main() -> None:
    logo = load_logo()
    logo_w = white_logo(logo)

    icons = {s: app_icon(s, logo_w) for s in ICO_SIZES + [512]}
    icons[256].save(OUT / "icon.ico", sizes=[(s, s) for s in ICO_SIZES],
                    append_images=[icons[s] for s in ICO_SIZES])
    icons[256].save(OUT / "tray-icon.ico", sizes=[(s, s) for s in (16, 20, 24, 32, 48)],
                    append_images=[icons[s] for s in (16, 20, 24, 32, 48)])
    icons[512].save(OUT / "icon.png")

    # Logo horizontal para la pantalla principal (Flutter lo limita a 300x60).
    h = 120
    w = int(logo.width * h / logo.height)
    logo.resize((w, h), Image.LANCZOS).save(OUT / "logo.png")
    print("OK:", sorted(p.name for p in OUT.iterdir() if p.is_file()))


if __name__ == "__main__":
    main()
