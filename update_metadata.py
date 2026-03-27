#!/usr/bin/env python3
"""
=============================================================
  BANANA ARTWORKS GENESIS — Individual Names & Descriptions
  Liest mapping.csv + results.csv und trägt individuelle
  Namen und Beschreibungen in alle 101 JSONs ein.
=============================================================
"""

import csv
import json
from pathlib import Path

# ============================================================
#  KONFIGURATION
# ============================================================

MAPPING_CSV = r"D:\nft-banana\mapping.csv"
RESULTS_CSV = r"D:\nft-banana\results.csv"
ASSETS_DIR  = r"D:\nft-banana\assets"

# Collection Name
COLLECTION  = "Banana Artworks Genesis"

# ============================================================
#  Kurze englische Titel aus deutschen Beschreibungen ableiten
#  Schlüsselwörter → Titel
# ============================================================

KEYWORD_TITLES = {
    "Totenkopf": "Skull",
    "Schädel": "Skull",
    "skull": "Skull",
    "Skull": "Skull",
    "Banane": "Banana",
    "Bananen": "Banana",
    "banana": "Banana",
    "Spirale": "Spiral",
    "Spiralen": "Spiral",
    "spiral": "Spiral",
    "Glitch": "Glitch",
    "glitch": "Glitch",
    "Neon": "Neon",
    "neon": "Neon",
    "Gothic": "Gothic",
    "gothic": "Gothic",
    "Cyber": "Cyber",
    "cyber": "Cyber",
    "Kreatur": "Creature",
    "Maske": "Mask",
    "Symmetrie": "Symmetry",
    "Feuer": "Fire",
    "Roboter": "Robot",
    "Skelett": "Skeleton",
    "Schmetterling": "Butterfly",
    "Gesicht": "Face",
    "Affe": "Ape",
    "Chamäleon": "Chameleon",
    "Pilz": "Mushroom",
    "Stier": "Bull",
    "Armillarsphäre": "Armillary",
    "Skyline": "Skyline",
    "Chromosomen": "Chromosome",
    "Röntgen": "X-Ray",
    "Gasmaske": "Gasmask",
    "Altar": "Altar",
    "Totempunk": "Totempunk",
    "Totempilz": "Totem",
    "X-Form": "X-Shape",
    "Biomechanisch": "Biomech",
    "biomechanische": "Biomech",
    "Surreal": "Surreal",
    "surreal": "Surreal",
    "Psychedelisch": "Psychedelic",
    "psychedelisch": "Psychedelic",
    "Hypnotisch": "Hypnotic",
    "hypnotisch": "Hypnotic",
    "hypnotische": "Hypnotic",
    "Dystopisch": "Dystopian",
    "dystopisch": "Dystopian",
    "Okkulte": "Occult",
    "okkulte": "Occult",
}

def derive_title(description, nummer):
    """Leitet einen kurzen englischen Titel aus der deutschen Beschreibung ab."""
    for german, english in KEYWORD_TITLES.items():
        if german in description:
            return english
    # Fallback: erstes Substantiv aus Beschreibung
    words = description.split()
    for word in words:
        if len(word) > 4 and word[0].isupper():
            return word[:12]
    return f"Genesis"

def load_mapping(path):
    """Lädt nummer → original_filename."""
    mapping = {}
    with open(path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mapping[int(row["nummer"])] = row["original"]
    return mapping

def load_results(path):
    """Lädt original_filename → {verdict, grund}."""
    results = {}
    with open(path, "r", encoding="utf-8-sig") as f:
        # Semikolon-getrennt
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            results[row["datei"]] = {
                "verdict": row["verdict"],
                "grund": row["grund"]
            }
    return results

def main():
    mapping = load_mapping(MAPPING_CSV)
    results = load_results(RESULTS_CSV)
    assets  = Path(ASSETS_DIR)

    print("=" * 60)
    print("  BANANA ARTWORKS — Individual Metadata Update")
    print("=" * 60)
    print(f"\n  Mapping : {len(mapping)} Einträge")
    print(f"  Results : {len(results)} Einträge")
    print()

    updated = skipped = errors = 0

    for nummer, original in sorted(mapping.items()):
        json_path = assets / f"{nummer}.json"

        if not json_path.exists():
            print(f"  [{nummer:>3}] JSON nicht gefunden — übersprungen")
            skipped += 1
            continue

        # Beschreibung aus results holen
        result = results.get(original)
        if not result:
            print(f"  [{nummer:>3}] {original:<40} — kein Ergebnis in CSV")
            skipped += 1
            continue

        description = result["grund"]
        nft_number  = nummer + 1  # #1 bis #101

        # Titel ableiten
        title = derive_title(description, nummer)
        name  = f"{title} #{nft_number} — {COLLECTION}"

        # JSON laden und updaten
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)

            metadata["name"]        = name
            metadata["description"] = (
                f"{description}. "
                f"Original mixed media artwork by Banana Artworks — "
                f"handpainted and digitally processed, zero AI. "
                f"Dark art from Chiang Rai, Thailand."
            )

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            print(f"  [{nummer:>3}] {original:<40} → {name}")
            updated += 1

        except Exception as e:
            print(f"  [{nummer:>3}] FEHLER: {e}")
            errors += 1

    print()
    print("=" * 60)
    print(f"  Aktualisiert : {updated}")
    print(f"  Übersprungen : {skipped}")
    if errors:
        print(f"  Fehler       : {errors}")
    print()
    print("  BEISPIEL NFT #1:")
    try:
        with open(assets / "0.json", "r", encoding="utf-8") as f:
            sample = json.load(f)
        print(f"  Name        : {sample['name']}")
        print(f"  Description : {sample['description'][:80]}...")
    except:
        pass
    print()
    print("  Fertig! Alle JSONs haben jetzt individuelle Namen.")
    print("  Naechster Schritt: sugar upload (Mainnet)")

if __name__ == "__main__":
    main()
