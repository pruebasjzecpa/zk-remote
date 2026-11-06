"""Aplica la marca ZK-REMOTE sobre el árbol de RustDesk antes de compilar.

Se ejecuta en la CI (y opcionalmente en local) sobre un checkout limpio.
Los archivos de upstream NO se modifican en el repo: este script los pisa
solo en el árbol de compilación, así los merges con upstream no generan conflictos.
Si un texto esperado no aparece (upstream lo cambió), el script falla a propósito.

Uso:  python zk/apply_branding.py
"""

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "zk" / "branding"

APP_NAME = "ZK-REMOTE"
SOURCE_URL = "https://github.com/pruebasjzecpa/zk-remote"

# Destino -> archivo de marca
ASSETS = {
    "res/icon.ico": "icon.ico",
    "res/tray-icon.ico": "tray-icon.ico",
    "flutter/windows/runner/resources/app_icon.ico": "icon.ico",
    # Recursos que el modo "cliente personalizado" de RustDesk busca en flutter_assets.
    "flutter/assets/icon.ico": "icon.ico",
    "flutter/assets/icon.png": "icon.png",
    "flutter/assets/logo.png": "logo.png",
}

# (archivo, texto original, reemplazo). Se conservan CompanyName y LegalCopyright
# de upstream porque son avisos de autoría (AGPL-3.0).
TEXT_PATCHES = [
    (
        "flutter/windows/runner/Runner.rc",
        '"FileDescription", "RustDesk Remote Desktop"',
        f'"FileDescription", "{APP_NAME} (based on RustDesk)"',
    ),
    (
        "flutter/windows/runner/Runner.rc",
        '"InternalName", "rustdesk"',
        '"InternalName", "zk-remote"',
    ),
    (
        "flutter/windows/runner/Runner.rc",
        '"OriginalFilename", "rustdesk.exe"',
        f'"OriginalFilename", "{APP_NAME}.exe"',
    ),
    (
        "flutter/windows/runner/Runner.rc",
        '"ProductName", "RustDesk"',
        f'"ProductName", "{APP_NAME}"',
    ),
    # Colores de marca: #01B0E9 (logo). Para botones con texto blanco se usan tonos
    # más oscuros del mismo celeste para mantener el contraste (≈4:1).
    (
        "flutter/lib/common.dart",
        "static const Color accent = Color(0xFF0071FF);",
        "static const Color accent = Color(0xFF0284C7);",
    ),
    (
        "flutter/lib/common.dart",
        "static const Color accent50 = Color(0x770071FF);",
        "static const Color accent50 = Color(0x770284C7);",
    ),
    (
        "flutter/lib/common.dart",
        "static const Color accent80 = Color(0xAA0071FF);",
        "static const Color accent80 = Color(0xAA0284C7);",
    ),
    (
        "flutter/lib/common.dart",
        "static const Color idColor = Color(0xFF00B6F0);",
        "static const Color idColor = Color(0xFF01B0E9);",
    ),
    (
        "flutter/lib/common.dart",
        "static const Color button = Color(0xFF2C8CFF);",
        "static const Color button = Color(0xFF0390D0);",
    ),
    (
        "flutter/lib/desktop/pages/desktop_setting_page.dart",
        "decoration: const BoxDecoration(color: Color(0xFF2c8cff)),",
        "decoration: const BoxDecoration(color: Color(0xFF0284C7)),",
    ),
    # "Acerca de": link al código fuente de este fork (obligación AGPL-3.0).
    (
        "flutter/lib/desktop/pages/desktop_setting_page.dart",
        """                    launchUrlString('https://rustdesk.com');
                  },
                  child: Text(
                    translate('Website'),
                    style: linkStyle,
                  ).marginSymmetric(vertical: 4.0)),
""",
        f"""                    launchUrlString('https://rustdesk.com');
                  }},
                  child: Text(
                    translate('Website'),
                    style: linkStyle,
                  ).marginSymmetric(vertical: 4.0)),
              InkWell(
                  onTap: () {{
                    launchUrlString('{SOURCE_URL}');
                  }},
                  child: Text(
                    '{APP_NAME}: código fuente (AGPL-3.0), basado en RustDesk',
                    style: linkStyle,
                  ).marginSymmetric(vertical: 4.0)),
""",
    ),
]


def main() -> int:
    for dst, src in ASSETS.items():
        src_path = BRAND / src
        if not src_path.is_file():
            print(f"ERROR: falta {src_path}")
            return 1
        shutil.copyfile(src_path, ROOT / dst)
        print(f"asset  {dst} <- zk/branding/{src}")

    for rel, old, new in TEXT_PATCHES:
        path = ROOT / rel
        # Runner.rc no es UTF-8 en todas las versiones; se preserva la codificación byte a byte.
        data = path.read_bytes()
        old_b, new_b = old.encode("utf-8"), new.encode("utf-8")
        if b"\r\n" in data:  # checkout con autocrlf (Windows)
            old_b = old_b.replace(b"\n", b"\r\n")
            new_b = new_b.replace(b"\n", b"\r\n")
        summary = new.strip().splitlines()[0]
        if new_b in data:
            print(f"skip   {rel}: ya aplicado ({summary})")
            continue
        if data.count(old_b) != 1:
            print(f"ERROR: se esperaba 1 aparición de {old!r} en {rel}, hay {data.count(old_b)} (¿cambió upstream?)")
            return 1
        path.write_bytes(data.replace(old_b, new_b))
        print(f"patch  {rel}: {summary}")

    print("Marca aplicada.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
