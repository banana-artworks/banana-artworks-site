# 🍌 BANANA ARTWORKS — TODO.md
> Projekt: banana-artworks.com | Solana NFT Minting Page
> Stack: HTML/CSS/JS, Phantom Wallet, Candy Machine, Solana Mainnet
> Ziel: Von "gut" auf "Weltklasse" — alle Tasks sind direkt ausführbar

---

## ✅ BEREITS ERLEDIGT (nicht nochmal anfassen!)
- [x] SEO Meta-Tags, Open Graph, Twitter Card in `<head>`
- [x] `artwork-hero.png` (1200×630px) als OG-Image
- [x] Canonical URL
- [x] Anthropic API Key aus Code entfernt → in Vercel Environment Variables
- [x] Live Mint Counter (MINTED / TOTAL SUPPLY / REMAINING / MINT PRICE)
- [x] Phantom Wallet Integration (`window.solana`)
- [x] MINT NOW Button
- [x] NFT Gallery mit echten Assets
- [x] Trust Bar (Phantom Wallet · Solana Mainnet · SPL Token)

---

## 🔴 PRIORITÄT 1 — Sofort umsetzen

### TASK 1: Share-Button nach erfolgreichem Mint
**Ziel:** Nach jedem Mint erscheint ein Modal mit X/Twitter Share Button → viraler Mechanismus

**Anweisung für Claude Code:**
Finde die `mintNFT()` Funktion im JavaScript. Nach einem erfolgreichen Mint-Vorgang soll ein Modal erscheinen. Das Modal soll:
1. Die gemintete NFT-Nummer anzeigen (z.B. "Genesis #042")
2. Einen "Share on X" Button haben mit vorausgefülltem Tweet
3. Einen "View on Magic Eden" Link haben
4. Einen "Close" Button haben
5. Zum bestehenden Gold/Teal Design passen

**Tweet-Text:**
```
Just minted Banana Artworks Genesis 🍌 One of 101 original on-chain assets. Zero AI. 100% handmade. #BananaArtworks #Solana #NFT
https://banana-artworks.com
```

**CSS für das Modal — zum bestehenden Theme passend:**
```css
.mint-success-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  animation: fadeIn 0.3s ease;
}

.mint-success-modal {
  background: linear-gradient(135deg, #0a1f1a 0%, #0d2b24 100%);
  border: 1px solid rgba(212, 160, 23, 0.4);
  border-radius: 16px;
  padding: 40px;
  max-width: 480px;
  width: 90%;
  text-align: center;
  box-shadow: 0 0 60px rgba(212, 160, 23, 0.2);
  animation: slideUp 0.4s cubic-bezier(0.23, 1, 0.32, 1);
}

.mint-success-emoji {
  font-size: 4rem;
  margin-bottom: 16px;
}

.mint-success-title {
  font-family: inherit;
  font-size: 1.8rem;
  color: #D4A017;
  margin-bottom: 8px;
  letter-spacing: 0.05em;
}

.mint-success-sub {
  color: rgba(255,255,255,0.6);
  font-size: 0.9rem;
  margin-bottom: 32px;
}

.share-btn-x {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #000;
  color: #fff;
  border: 1px solid rgba(255,255,255,0.2);
  padding: 12px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.2s;
  margin-bottom: 12px;
  width: 100%;
  justify-content: center;
}

.share-btn-x:hover {
  background: #1a1a1a;
  border-color: rgba(255,255,255,0.4);
  transform: translateY(-2px);
}

.magic-eden-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  color: #D4A017;
  border: 1px solid rgba(212, 160, 23, 0.4);
  padding: 12px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-size: 0.95rem;
  transition: all 0.2s;
  margin-bottom: 12px;
  width: 100%;
  justify-content: center;
}

.magic-eden-btn:hover {
  background: rgba(212, 160, 23, 0.1);
  border-color: rgba(212, 160, 23, 0.7);
}

.close-modal-btn {
  background: none;
  border: none;
  color: rgba(255,255,255,0.3);
  font-size: 0.85rem;
  cursor: pointer;
  margin-top: 8px;
  padding: 8px;
  transition: color 0.2s;
}

.close-modal-btn:hover { color: rgba(255,255,255,0.7); }

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp { from { transform: translateY(30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
```

**JavaScript für das Modal:**
```javascript
function showMintSuccessModal(mintNumber) {
  const tweetText = encodeURIComponent(
    `Just minted Banana Artworks Genesis 🍌 One of 101 original on-chain assets. Zero AI. 100% handmade. #BananaArtworks #Solana #NFT\nhttps://banana-artworks.com`
  );
  
  const overlay = document.createElement('div');
  overlay.className = 'mint-success-overlay';
  overlay.innerHTML = `
    <div class="mint-success-modal">
      <div class="mint-success-emoji">🍌</div>
      <h2 class="mint-success-title">GENESIS MINTED!</h2>
      <p class="mint-success-sub">You are now part of Banana Artworks history.<br>101 unique. On-chain. Forever.</p>
      <a href="https://twitter.com/intent/tweet?text=${tweetText}" 
         target="_blank" 
         class="share-btn-x">
        ✕ Share on X
      </a>
      <a href="https://magiceden.io/marketplace/banana_artworks" 
         target="_blank" 
         class="magic-eden-btn">
        View on Magic Eden
      </a>
      <button class="close-modal-btn" onclick="this.closest('.mint-success-overlay').remove()">
        Close
      </button>
    </div>
  `;
  
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) overlay.remove();
  });
  
  document.body.appendChild(overlay);
}
```

---

### TASK 2: NFT Card Hover-Effekte
**Ziel:** Die NFT-Cards in der Gallery sollen beim Hover eine Premium-Reaktion zeigen.

**Anweisung für Claude Code:**
Finde die CSS-Klasse der NFT-Cards in der Gallery-Section. Füge folgende Hover-Effekte hinzu:

```css
/* Zur bestehenden NFT-Card CSS hinzufügen */
.nft-card {
  transition: all 0.35s cubic-bezier(0.23, 1, 0.32, 1);
  cursor: pointer;
}

.nft-card:hover {
  transform: translateY(-8px) scale(1.03);
  box-shadow: 
    0 0 25px rgba(212, 160, 23, 0.25),
    0 20px 50px rgba(0, 0, 0, 0.5);
  border-color: rgba(212, 160, 23, 0.5);
  z-index: 10;
}

.nft-card img {
  transition: transform 0.35s cubic-bezier(0.23, 1, 0.32, 1);
}

.nft-card:hover img {
  transform: scale(1.05);
}
```

---

### TASK 3: sitemap.xml erstellen
**Ziel:** Google kann die Seite vollständig indexieren.

**Anweisung für Claude Code:**
Erstelle eine neue Datei `sitemap.xml` im Root-Verzeichnis des Projekts:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://banana-artworks.com/</loc>
    <lastmod>2026-03-27</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

---

### TASK 4: robots.txt erstellen
**Anweisung für Claude Code:**
Erstelle eine neue Datei `robots.txt` im Root-Verzeichnis:

```
User-agent: *
Allow: /
Sitemap: https://banana-artworks.com/sitemap.xml
```

---

### TASK 5: Alt-Texte auf allen NFT-Bildern
**Ziel:** SEO und Accessibility verbessern.

**Anweisung für Claude Code:**
Finde alle `<img>` Tags der NFT-Gallery. Füge bei jedem Bild ein `alt` Attribut, `loading="lazy"` und `width`/`height` hinzu.

Format: `alt="Banana Artworks Genesis #001 — [kurze Beschreibung], Solana NFT"`

Beispiel:
```html
<!-- Vorher -->
<img src="assets/1.png">

<!-- Nachher -->
<img src="assets/1.png" 
     alt="Banana Artworks Genesis #001 — Chrome-metallische Banane, Solana NFT"
     loading="lazy"
     width="500" 
     height="500">
```

---

## 🟠 PRIORITÄT 2 — Nächste Woche

### TASK 6: Mobile Optimierung prüfen
**Anweisung für Claude Code:**
Prüfe ob die 4 Counter-Boxen (MINTED / TOTAL SUPPLY / REMAINING / MINT PRICE) auf Mobile korrekt dargestellt werden. Auf Smartphones unter 480px Breite sollen sie in einem 2×2 Grid angeordnet sein, nicht in einer Reihe.

```css
@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }
  
  .stat-number {
    font-size: 1.5rem;
  }
  
  .mint-btn {
    width: 100%;
    padding: 16px;
    font-size: 1rem;
  }
}
```

---

### TASK 7: NFT Lightbox — Klick auf NFT öffnet Vollbild
**Ziel:** User können einzelne NFTs in voller Größe betrachten.

**Anweisung für Claude Code:**
Füge eine einfache Lightbox hinzu. Wenn ein User auf ein NFT-Bild klickt, öffnet sich ein Modal mit dem Bild in voller Größe, dem Namen (z.B. "Genesis #001") und einem Close-Button.

```javascript
function openLightbox(imgSrc, nftName) {
  const lightbox = document.createElement('div');
  lightbox.className = 'lightbox-overlay';
  lightbox.innerHTML = `
    <div class="lightbox-content">
      <img src="${imgSrc}" alt="${nftName}" class="lightbox-img">
      <p class="lightbox-title">${nftName}</p>
      <button class="lightbox-close" onclick="this.closest('.lightbox-overlay').remove()">✕</button>
    </div>
  `;
  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) lightbox.remove();
  });
  document.body.appendChild(lightbox);
}
```

```css
.lightbox-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.95);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  cursor: zoom-out;
}

.lightbox-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  text-align: center;
}

.lightbox-img {
  max-width: 100%;
  max-height: 80vh;
  object-fit: contain;
  border: 1px solid rgba(212, 160, 23, 0.3);
  border-radius: 8px;
}

.lightbox-title {
  color: #D4A017;
  margin-top: 12px;
  font-size: 1rem;
  letter-spacing: 0.1em;
}

.lightbox-close {
  position: absolute;
  top: -40px;
  right: 0;
  background: none;
  border: none;
  color: rgba(255,255,255,0.6);
  font-size: 1.5rem;
  cursor: pointer;
  padding: 8px;
  transition: color 0.2s;
}

.lightbox-close:hover { color: #fff; }
```

---

### TASK 8: Mint Button Pulse-Animation wenn Wallet verbunden
**Ziel:** Wenn die Wallet connected ist, pulsiert der Mint-Button subtil → visueller Sog.

**Anweisung für Claude Code:**
Finde die Stelle im JavaScript wo die Wallet erfolgreich verbunden wird (`onlyIfTrusted` oder nach `connectWallet()`). Füge dort die Klasse `wallet-connected` zum Mint-Button hinzu.

```css
@keyframes mintGlow {
  0%, 100% { 
    box-shadow: 0 0 0 0 rgba(0, 229, 200, 0.4);
  }
  50% { 
    box-shadow: 0 0 0 12px rgba(0, 229, 200, 0);
  }
}

.mint-btn.wallet-connected {
  animation: mintGlow 2s infinite;
}
```

---

## 🟢 PRIORITÄT 3 — Wenn Zeit ist

### TASK 9: Fehler-Handling verbessern
**Anweisung für Claude Code:**
Stelle sicher dass alle möglichen Fehler beim Minting eine klare, benutzerfreundliche Meldung zeigen:

```javascript
function showMintError(errorCode) {
  const messages = {
    'USER_REJECTED': '❌ Transaktion abgebrochen. Bitte bestätige in deinem Wallet.',
    'INSUFFICIENT_FUNDS': '❌ Nicht genug SOL. Du brauchst mindestens 0.25 SOL + Gas.',
    'SOLD_OUT': '❌ Sold out! Alle 101 NFTs sind geminted.',
    'WALLET_NOT_CONNECTED': '⚠️ Bitte verbinde zuerst deine Phantom Wallet.',
    'DEFAULT': '❌ Fehler beim Minting. Bitte versuche es erneut.'
  };
  
  const msg = messages[errorCode] || messages['DEFAULT'];
  
  // Zeige Fehlermeldung unter dem Mint-Button
  const errorDiv = document.getElementById('mint-error') || createErrorDiv();
  errorDiv.textContent = msg;
  errorDiv.style.display = 'block';
  
  setTimeout(() => { errorDiv.style.display = 'none'; }, 5000);
}
```

---

### TASK 10: Bilder zu WebP konvertieren (Performance)
**Anweisung für Claude Code:**
Prüfe ob Python und Pillow verfügbar sind. Konvertiere alle PNG-Dateien im `/assets/` Ordner zu WebP Format für schnellere Ladezeiten. Behalte die Originale.

```python
from PIL import Image
import os

assets_dir = './assets'
for filename in os.listdir(assets_dir):
    if filename.endswith('.png'):
        img_path = os.path.join(assets_dir, filename)
        webp_path = img_path.replace('.png', '.webp')
        if not os.path.exists(webp_path):
            img = Image.open(img_path)
            img.save(webp_path, 'WebP', quality=85)
            print(f"Converted: {filename} → {filename.replace('.png', '.webp')}")
```

---

## 📋 NACH DER UMSETZUNG — Manuelle Schritte

1. **Deploy:** `git add . && git commit -m "feat: share modal, hover effects, SEO fixes" && git push`
2. **Vercel:** Auto-Deploy läuft nach Push
3. **Google Search Console:** 
   - https://search.google.com/search-console aufrufen
   - Property `banana-artworks.com` hinzufügen
   - Sitemap einreichen: `banana-artworks.com/sitemap.xml`
4. **X/Twitter erster Post** nach erfolgreichem Test

---

## 🎯 ANWEISUNG FÜR CLAUDE CODE — START

```
Du bist mein Senior Developer für das Projekt banana-artworks.com.
Das ist eine Solana NFT Minting Page mit Phantom Wallet, Candy Machine 
und einer Gallery mit 101 NFT Assets.

Lies zuerst alle Projektdateien (index.html, CSS, JS).
Dann arbeite diese TODO.md Schritt für Schritt ab — 
beginne mit PRIORITÄT 1, TASK 1 (Share Modal nach Mint).

Zeige mir vor jeder Änderung was du vorhast.
Warte auf meine Bestätigung bevor du schreibst.
```
