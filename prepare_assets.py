#!/usr/bin/env python3
"""
=============================================================
  BANANA ARTWORKS GENESIS — Prepare Assets
  - Konvertiert alle Bilder zu PNG
  - Einheitliche Größe: 1000x1000px (quadratisch, kein Crop)
  - Benennt um: 0.png bis 100.png
  - Erstellt collection.png (erstes Bild als Cover)
  - Original-Dateien werden NICHT verändert
=============================================================
"""

from pathlib import Path
from PIL import Image, ImageOps
import shutil

# ============================================================
#  KONFIGURATION
# ============================================================

# Ordner mit deinen 101 ausgewählten Artworks
INPUT_DIR  = r"D:\nft-banana\meine artworks"

# Ziel: assets/ Ordner für Sugar CLI
OUTPUT_DIR = r"D:\nft-banana\assets"

# Ausgabegröße in Pixel (NFT Standard)
SIZE = 1000

# Hintergrundfarbe für Letterbox (falls Bild nicht quadratisch)
# Schwarz passt zu deinem Dark Art Style
BG_COLOR = (0, 0, 0)

# ============================================================

SUPPORTED = {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff', '.gif'}

def make_square(img, size, bg_color):
    """
    Bild quadratisch machen ohne zu croppen.
    Letterbox (schwarze Balken) wenn nötig.
    """
    img = img.convert("RGBA")
    w, h = img.size

    # Skalieren damit alles reinpasst
    ratio = min(size / w, size / h)
    new_w = int(w * ratio)
    new_h = int(h * ratio)
    img = img.resize((new_w, new_h), Image.LANCZOS)

    # Auf quadratische Canvas zentrieren
    canvas = Image.new("RGBA", (size, size), (*bg_color, 255))
    offset_x = (size - new_w) // 2
    offset_y = (size - new_h) // 2
    canvas.paste(img, (offset_x, offset_y), img)

    return canvas.convert("RGB")

def main():
    input_path  = Path(INPUT_DIR)
    output_path = Path(OUTPUT_DIR)

    # Eingabe prüfen
    if not input_path.exists():
        print(f"FEHLER: Eingabe-Ordner nicht gefunden: {INPUT_DIR}")
        return

    # Bilder sammeln und sortieren
    images = sorted([
        f for f in input_path.iterdir()
        if f.suffix.lower() in SUPPORTED
    ])

    if not images:
        print(f"FEHLER: Keine Bilder gefunden in: {INPUT_DIR}")
        return

    print("=" * 60)
    print("  BANANA ARTWORKS — Asset Preparation")
    print("=" * 60)
    print(f"\n  Eingabe : {INPUT_DIR}")
    print(f"  Ausgabe : {OUTPUT_DIR}")
    print(f"  Bilder  : {len(images)} gefunden")
    print(f"  Größe   : {SIZE}x{SIZE}px PNG")
    print()

    # Ausgabe-Ordner anlegen
    output_path.mkdir(parents=True, exist_ok=True)

    errors = []

    for idx, src in enumerate(images):
        dest_name = f"{idx}.png"
        dest = output_path / dest_name

        print(f"  [{idx:>3}/100] {src.name:<45} -> {dest_name}", end=" ", flush=True)

        try:
            img = Image.open(src)
            img = make_square(img, SIZE, BG_COLOR)
            img.save(dest, "PNG", optimize=True)
            print("OK")
        except Exception as e:
            print(f"FEHLER: {e}")
            errors.append((src.name, str(e)))

    # collection.png = erstes Bild als Cover
    first_output = output_path / "0.png"
    collection   = output_path / "collection.png"
    if first_output.exists():
        shutil.copy(first_output, collection)
        print(f"\n  collection.png erstellt (Kopie von 0.png)")

    # Zusammenfassung
    success = len(images) - len(errors)
    print()
    print("=" * 60)
    print(f"  FERTIG: {success}/{len(images)} Bilder konvertiert")
    if errors:
        print(f"\n  FEHLER bei {len(errors)} Dateien:")
        for name, err in errors:
            print(f"    {name}: {err}")
    print(f"\n  Ordner: {OUTPUT_DIR}")
    print(f"  Inhalt: 0.png bis {len(images)-1}.png + collection.png")
    print()
    print("  NAECHSTE SCHRITTE:")
    print("  1. python generate_metadata.py  (JSONs erstellen)")
    print("  2. sugar validate               (alles pruefen)")
    print("  3. sugar upload                 (zu Arweave hochladen)")
    print()

if __name__ == "__main__":
    main()
