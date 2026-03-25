#!/bin/bash
# ═══════════════════════════════════════════════════
#  Banana Artworks — vendor.js Build Script
#  Einmalig ausführen wenn Pakete aktualisiert werden
#  Voraussetzung: Node.js >= 18
# ═══════════════════════════════════════════════════

set -e

echo "🍌 Banana Artworks — vendor.js Build"
echo "═══════════════════════════════════"

# Temp-Ordner
BUILD_DIR=".vendor-build"
mkdir -p $BUILD_DIR

# Entry point
cat > $BUILD_DIR/entry.js << 'EOF'
export { createUmi }             from '@metaplex-foundation/umi-bundle-defaults';
export { publicKey, generateSigner, some, none } from '@metaplex-foundation/umi';
export { mplCandyMachine, fetchCandyMachine, fetchCandyGuard, mintV2 } from '@metaplex-foundation/mpl-candy-machine';
export { walletAdapterIdentity } from '@metaplex-foundation/umi-signer-wallet-adapters';
export { setComputeUnitLimit }   from '@metaplex-foundation/mpl-toolbox';
EOF

# package.json
cat > $BUILD_DIR/package.json << 'EOF'
{
  "name": "banana-vendor-build",
  "private": true,
  "type": "module",
  "dependencies": {
    "@metaplex-foundation/umi": "1.5.1",
    "@metaplex-foundation/umi-bundle-defaults": "1.5.1",
    "@metaplex-foundation/mpl-candy-machine": "6.1.0",
    "@metaplex-foundation/umi-signer-wallet-adapters": "1.5.1",
    "@metaplex-foundation/mpl-toolbox": "0.10.0"
  },
  "devDependencies": {
    "esbuild": "^0.21.0"
  }
}
EOF

echo "📦 Installing packages..."
cd $BUILD_DIR && npm install --silent && cd ..

echo "⚙️  Bundling..."
$BUILD_DIR/node_modules/.bin/esbuild $BUILD_DIR/entry.js \
  --bundle \
  --format=esm \
  --platform=browser \
  --target=es2020 \
  --outfile=vendor.js \
  --define:process.env.NODE_ENV=\"production\" \
  --minify

SIZE=$(wc -c < vendor.js)
echo "✅ vendor.js erstellt: $(( SIZE / 1024 )) KB"
echo ""
echo "Jetzt commiten:"
echo "  git add vendor.js index.html"
echo "  git commit -m 'build: vendor.js Metaplex bundle'"
echo "  git push"
