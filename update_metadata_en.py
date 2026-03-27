#!/usr/bin/env python3
"""
=============================================================
  BANANA ARTWORKS GENESIS — Individual Names & Descriptions
  Übersetzt deutsche Beschreibungen auf Englisch via Claude API
  und trägt sie in alle 101 JSONs ein.
=============================================================
"""

import csv
import json
import time
from pathlib import Path
import os
import anthropic

API_KEY     = os.environ.get("ANTHROPIC_API_KEY", "")
MAPPING_CSV = r"D:\nft-banana\mapping.csv"
RESULTS_CSV = r"D:\nft-banana\results.csv"
ASSETS_DIR  = r"D:\nft-banana\assets"
COLLECTION  = "Banana Artworks Genesis"

KEYWORD_TITLES = {
    "Totenkopf": "Skull", "Schädel": "Skull", "Skull": "Skull",
    "Banane": "Banana", "Bananen": "Banana",
    "Spirale": "Spiral", "Spiralen": "Spiral",
    "Glitch": "Glitch", "Neon": "Neon", "Gothic": "Gothic",
    "Cyber": "Cyber", "Kreatur": "Creature", "Maske": "Mask",
    "Feuer": "Fire", "Roboter": "Robot", "Skelett": "Skeleton",
    "Schmetterling": "Butterfly", "Gesicht": "Face",
    "Affe": "Ape", "Chamäleon": "Chameleon", "Pilz": "Mushroom",
    "Stier": "Bull", "Armillarsphäre": "Armillary",
    "Skyline": "Skyline", "Chromosomen": "Chromosome",
    "Röntgen": "X-Ray", "Gasmaske": "Gasmask", "Altar": "Altar",
    "Totempilz": "Totem", "X-Form": "X-Shape",
    "biomechanische": "Biomech", "Biomechanisch": "Biomech",
    "surreal": "Surreal", "Surreal": "Surreal",
    "psychedelisch": "Psychedelic", "Psychedelisch": "Psychedelic",
    "hypnotisch": "Hypnotic", "hypnotische": "Hypnotic",
    "dystopisch": "Dystopian", "okkulte": "Occult",
}

def derive_title(description):
    for german, english in KEYWORD_TITLES.items():
        if german in description:
            return english
    words = description.split()
    for word in words:
        if len(word) > 4 and word[0].isupper():
            return word[:12]
    return "Genesis"

def translate_to_english(client, text):
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": (
                f"Translate this German art description to English. "
                f"Keep it short and punchy, max 12 words. "
                f"Only output the translation, nothing else:\n\n{text}"
            )
        }]
    )
    return msg.content[0].text.strip()

def load_mapping(path):
    mapping = {}
    with open(path, "r", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            mapping[int(row["nummer"])] = row["original"]
    return mapping

def load_results(path):
    results = {}
    with open(path, "r", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f, delimiter=";"):
            results[row["datei"]] = row["grund"]
    return results

def main():
    if API_KEY == "DEIN_ANTHROPIC_API_KEY_HIER":
        print("Fehler: API Key fehlt!")
        return

    mapping = load_mapping(MAPPING_CSV)
    results = load_results(RESULTS_CSV)
    assets  = Path(ASSETS_DIR)
    client  = anthropic.Anthropic(api_key=API_KEY)

    print("=" * 60)
    print("  BANANA ARTWORKS -- Metadata Update (English)")
    print("=" * 60)
    print(f"\n  {len(mapping)} NFTs werden aktualisiert...\n")

    updated = skipped = errors = 0

    for nummer, original in sorted(mapping.items()):
        json_path  = assets / f"{nummer}.json"
        nft_number = nummer + 1

        if not json_path.exists():
            print(f"  [{nft_number:>3}] JSON fehlt -- uebersprungen")
            skipped += 1
            continue

        german_desc = results.get(original)
        if not german_desc:
            print(f"  [{nft_number:>3}] {original:<35} -- kein Eintrag in CSV")
            skipped += 1
            continue

        try:
            print(f"  [{nft_number:>3}] {original:<40}", end=" ", flush=True)
            english_desc = translate_to_english(client, german_desc)

            title = derive_title(german_desc)
            name  = f"{title} #{nft_number} -- {COLLECTION}"

            full_description = (
                f"{english_desc}. "
                f"Original mixed media artwork by Banana Artworks -- "
                f"handpainted and digitally processed, zero AI. "
                f"Dark art from Chiang Rai, Thailand."
            )

            with open(json_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)

            metadata["name"]        = name
            metadata["description"] = full_description

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            print(f"OK")
            print(f"       {english_desc}")
            updated += 1

        except Exception as e:
            print(f"FEHLER: {e}")
            errors += 1

        time.sleep(0.3)

    print()
    print("=" * 60)
    print(f"  Aktualisiert : {updated}")
    print(f"  Uebersprungen: {skipped}")
    if errors:
        print(f"  Fehler       : {errors}")
    print()

    try:
        with open(assets / "0.json", "r", encoding="utf-8") as f:
            sample = json.load(f)
        print("  BEISPIEL #1:")
        print(f"  Name : {sample['name']}")
        print(f"  Desc : {sample['description'][:100]}...")
    except:
        pass

    print("\n  Fertig! Naechster Schritt: sugar upload (Mainnet)")

if __name__ == "__main__":
    main()
