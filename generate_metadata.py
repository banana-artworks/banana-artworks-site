#!/usr/bin/env python3
"""
=============================================================
  BANANA ARTWORKS GENESIS — Metadata Generator
  Metaplex NFT Standard (Candy Machine v3 / Sugar CLI)
  100 Items · Solana
=============================================================

ANLEITUNG:
  1. Konfiguration unten anpassen (DEINE Wallet, Royalties etc.)
  2. traits_catalog befüllen — optional, kannst du auch leer lassen
  3. python generate_metadata.py ausführen
  4. Output-Ordner enthält: 0.json bis 99.json + collection.json

ORDNERSTRUKTUR DANACH (für Sugar CLI):
  assets/
    0.png     ← dein Artwork #1
    0.json    ← generiert von diesem Script
    1.png
    1.json
    ...
    99.png
    99.json
    collection.png    ← dein Collection-Cover
    collection.json   ← generiert von diesem Script
=============================================================
"""

import json
import os
import random
from pathlib import Path

# ============================================================
#  KONFIGURATION — hier anpassen
# ============================================================

CONFIG = {
    # Collection-Name (erscheint bei jedem einzelnen NFT)
    "collection_name": "Banana Artworks Genesis",

    # Symbol (max 10 Zeichen, erscheint in Wallets)
    "symbol": "BAG",

    # Beschreibung (erscheint auf Magic Eden)
    "description": (
        "100 original Mixed Media artworks by Banana Artworks — "
        "handpainted and digitally processed, zero AI. "
        "Dark art from Chiang Rai, Thailand. Genesis Collection."
    ),

    # Deine Solana Creator-Wallet (Phantom-Adresse)
    # WICHTIG: Hier deine echte Adresse eintragen!
    "creator_wallet": "Dw1mTq978joHLnEm3fsVjBPFeFm7VQjGgZbU8Xmy4Dya",

    # Royalties bei Weiterverkauf
    # 500 = 5%  |  750 = 7.5%  |  1000 = 10%
    "seller_fee_basis_points": 500,

    # Deine Website
    "external_url": "https://banana-artworks.com",

    # Anzahl NFTs
    "item_count": 101,

    # Output-Ordner (wird angelegt falls nicht vorhanden)
    "output_dir": "assets",

    # Bildformat deiner Artworks
    "image_extension": "png",

    # Kategorie für Magic Eden (image, video, audio, html, vr)
    "category": "image",
}

# ============================================================
#  TRAITS / ATTRIBUTES
#  Jeder NFT bekommt zufällige Traits aus dieser Liste.
#  Traits machen NFTs filterbar auf Magic Eden.
#
#  Format: { "trait_type": [("Wert", Gewichtung), ...] }
#  Höhere Gewichtung = häufiger = Common
#  Niedrige Gewichtung = seltener = Rare/Legendary
#
#  Anpassen oder leer lassen {} wenn du keine Traits willst.
# ============================================================

TRAITS_CATALOG = {
    "Medium": [
        ("Acrylic on Canvas", 40),
        ("Ink on Paper", 25),
        ("Mixed Media", 20),
        ("Watercolor", 10),
        ("Oil on Board", 5),
    ],
    "Style": [
        ("Dark Gothic", 35),
        ("Abstract", 25),
        ("Surreal", 20),
        ("Expressionist", 15),
        ("Minimalist", 5),
    ],
    "Palette": [
        ("Black & White", 40),
        ("Monochrome Red", 20),
        ("Dark Tones", 20),
        ("High Contrast", 15),
        ("Greyscale", 5),
    ],
    "Edition": [
        ("Genesis", 100),  # alle sind Genesis
    ],
    "Rarity": [
        ("Common", 60),
        ("Uncommon", 25),
        ("Rare", 12),
        ("Legendary", 3),
    ],
}

# ============================================================
#  SPEZIELLE ARTWORKS (optional)
#  Hier kannst du einzelnen NFTs feste Namen oder Traits geben.
#  Index ist 0-basiert (NFT #1 = Index 0)
#
#  Format: { index: { "name": "...", "traits": {...} } }
# ============================================================

SPECIAL_ITEMS = {
    # Beispiel: NFT #1 bekommt einen besonderen Namen
    0: {
        "name": "Genesis Prime",
        "traits": {
            "Medium": "Mixed Media",
            "Style": "Dark Gothic",
            "Palette": "Black & White",
            "Edition": "Genesis",
            "Rarity": "Legendary",
            "Special": "1 of 1",
        }
    },
    # Beispiel: NFT #50 bekommt einen anderen Namen
    49: {
        "name": "Skull Throne",
        "traits": None  # None = zufällige Traits generieren
    },
}

# ============================================================
#  SCRIPT-LOGIK — ab hier nichts ändern nötig
# ============================================================

def weighted_choice(options):
    """Wählt einen Wert basierend auf Gewichtung."""
    values = [v for v, _ in options]
    weights = [w for _, w in options]
    return random.choices(values, weights=weights, k=1)[0]


def generate_traits(index):
    """Generiert zufällige Traits für einen NFT."""
    if not TRAITS_CATALOG:
        return []

    # Prüfen ob Special-Item mit festen Traits
    if index in SPECIAL_ITEMS and SPECIAL_ITEMS[index].get("traits") is not None:
        traits_dict = SPECIAL_ITEMS[index]["traits"]
        return [{"trait_type": k, "value": v} for k, v in traits_dict.items()]

    # Zufällige Traits aus Katalog
    attributes = []
    for trait_type, options in TRAITS_CATALOG.items():
        value = weighted_choice(options)
        attributes.append({
            "trait_type": trait_type,
            "value": value
        })

    return attributes


def generate_nft_metadata(index):
    """Generiert ein einzelnes NFT-Metadaten-JSON."""
    cfg = CONFIG
    number = index + 1  # NFT #1 bis #100

    # Name bestimmen
    if index in SPECIAL_ITEMS and SPECIAL_ITEMS[index].get("name"):
        name = f"{SPECIAL_ITEMS[index]['name']} #{number}"
    else:
        name = f"{cfg['collection_name']} #{number}"

    # Bildpfad (wird nach Upload durch Arweave/IPFS-URI ersetzt von Sugar CLI)
    image = f"{index}.{cfg['image_extension']}"

    # Traits generieren
    attributes = generate_traits(index)

    metadata = {
        "name": name,
        "symbol": cfg["symbol"],
        "description": cfg["description"],
        "seller_fee_basis_points": cfg["seller_fee_basis_points"],
        "image": image,
        "external_url": cfg["external_url"],
        "attributes": attributes,
        "collection": {
            "name": cfg["collection_name"],
            "family": "Banana Artworks"
        },
        "properties": {
            "files": [
                {
                    "uri": image,
                    "type": f"image/{cfg['image_extension']}"
                }
            ],
            "category": cfg["category"],
            "creators": [
                {
                    "address": cfg["creator_wallet"],
                    "share": 100
                }
            ]
        }
    }

    return metadata


def generate_collection_metadata():
    """Generiert die Collection-Metadaten (collection.json)."""
    cfg = CONFIG
    return {
        "name": cfg["collection_name"],
        "symbol": cfg["symbol"],
        "description": cfg["description"],
        "seller_fee_basis_points": cfg["seller_fee_basis_points"],
        "image": f"collection.{cfg['image_extension']}",
        "external_url": cfg["external_url"],
        "properties": {
            "files": [
                {
                    "uri": f"collection.{cfg['image_extension']}",
                    "type": f"image/{cfg['image_extension']}"
                }
            ],
            "category": cfg["category"],
            "creators": [
                {
                    "address": cfg["creator_wallet"],
                    "share": 100
                }
            ]
        }
    }


def analyze_rarity(all_metadata):
    """Gibt eine Rarity-Übersicht aus."""
    trait_counts = {}

    for item in all_metadata:
        for attr in item.get("attributes", []):
            tt = attr["trait_type"]
            val = attr["value"]
            if tt not in trait_counts:
                trait_counts[tt] = {}
            trait_counts[tt][val] = trait_counts[tt].get(val, 0) + 1

    total = len(all_metadata)
    print("\n📊 RARITY ÜBERSICHT:")
    print("=" * 50)
    for trait_type, values in trait_counts.items():
        print(f"\n  {trait_type}:")
        for value, count in sorted(values.items(), key=lambda x: x[1]):
            pct = (count / total) * 100
            bar = "█" * int(pct / 5)
            print(f"    {value:<20} {count:>3}x  {pct:>5.1f}%  {bar}")


def main():
    cfg = CONFIG
    output_dir = Path(cfg["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("  BANANA ARTWORKS GENESIS — Metadata Generator")
    print("=" * 60)
    print(f"\n  Collection : {cfg['collection_name']}")
    print(f"  Symbol     : {cfg['symbol']}")
    print(f"  Items      : {cfg['item_count']}")
    print(f"  Royalties  : {cfg['seller_fee_basis_points'] / 100:.1f}%")
    print(f"  Output     : ./{cfg['output_dir']}/")
    print()

    # Wallet-Warnung
    if cfg["creator_wallet"] == "DEINE_PHANTOM_WALLET_ADRESSE_HIER":
        print("⚠️  WARNUNG: Creator-Wallet noch nicht eingetragen!")
        print("   Öffne das Script und trage deine Phantom-Adresse ein.")
        print()

    all_metadata = []

    # NFT JSONs generieren
    print(f"Generiere {cfg['item_count']} Metadaten-Dateien...")
    for i in range(cfg["item_count"]):
        metadata = generate_nft_metadata(i)
        all_metadata.append(metadata)

        filepath = output_dir / f"{i}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        # Fortschritt
        if (i + 1) % 10 == 0:
            print(f"  {i + 1}/{cfg['item_count']} ✓")

    # Collection JSON
    collection_meta = generate_collection_metadata()
    collection_path = output_dir / "collection.json"
    with open(collection_path, "w", encoding="utf-8") as f:
        json.dump(collection_meta, f, indent=2, ensure_ascii=False)
    print(f"  collection.json ✓")

    # Rarity-Analyse
    analyze_rarity(all_metadata)

    # Nächste Schritte
    print("\n" + "=" * 60)
    print("✅ FERTIG!")
    print("=" * 60)
    print(f"\n  {cfg['item_count']} JSON-Dateien in: ./{cfg['output_dir']}/")
    print()
    print("NÄCHSTE SCHRITTE:")
    print()
    print("  1. Deine Artwork-Dateien benennen:")
    print(f"     0.{cfg['image_extension']}, 1.{cfg['image_extension']}, ..., 99.{cfg['image_extension']}")
    print(f"     + collection.{cfg['image_extension']} (dein Cover-Bild)")
    print()
    print("  2. Alle Dateien in den assets/ Ordner kopieren")
    print("     (Bild + JSON mit gleichem Namen nebeneinander)")
    print()
    print("  3. Sugar CLI: sugar validate")
    print("     (prüft ob alle JSONs korrekt sind)")
    print()
    print("  4. Sugar CLI: sugar upload")
    print("     (lädt alles zu Arweave/NFT.Storage hoch)")
    print()
    print("  5. Sugar CLI: sugar deploy")
    print("     (deployt die Candy Machine on-chain)")
    print()
    print("  Viel Erfolg mit dem Launch! 🍌🎨")
    print()


if __name__ == "__main__":
    # Seed für reproduzierbare Rarity-Verteilung setzen
    # Gleiche Zahl = gleiche Traits bei erneutem Ausführen
    random.seed(42)
    main()
