# 🍌 BANANA ARTWORKS — TODO.md

> Alle Tasks beziehen sich ausschließlich auf das Projekt **banana-artworks.com**

---

## 🔴 PRIORITÄT 1 — Sofort umsetzen

### SEO: Meta-Tags
**Datei:** `index.html` → in `<head>` einfügen

```html
<title>Banana Artworks | AI Solutions Builder & Vibe Coder | DACH Market</title>
<meta name="description" content="Freelance AI-Entwickler für den DACH-Markt. Ich baue KI-Automatisierungen, Chatbots und Web-Apps mit FastAPI & Claude API. Verfügbar auf Upwork.">
<meta name="keywords" content="AI Freelancer DACH, Upwork KI-Entwickler, FastAPI, Claude API, Automatisierung, Vibe Coder">
<link rel="canonical" href="https://banana-artworks.com/">
```

### SEO: Open Graph Tags
**Datei:** `index.html` → in `<head>` einfügen

```html
<meta property="og:title" content="Banana Artworks | AI Solutions Builder">
<meta property="og:description" content="KI-Automatisierung für den DACH-Markt. FastAPI. Claude. Ergebnisse.">
<meta property="og:image" content="https://banana-artworks.com/og-image.jpg">
<meta property="og:url" content="https://banana-artworks.com">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Banana Artworks | AI Solutions Builder">
```

### SEO: Structured Data (Schema.org)
**Datei:** `index.html` → in `<head>` einfügen

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Banana Artworks",
  "jobTitle": "AI Solutions Builder & Freelance Developer",
  "url": "https://banana-artworks.com",
  "sameAs": [
    "https://github.com/banana-artworks",
    "https://www.upwork.com/freelancers/~banana-artworks"
  ],
  "knowsAbout": ["AI Development", "FastAPI", "Claude API", "Automation"]
}
</script>
```

### SEO: sitemap.xml
**Datei:** `sitemap.xml` → im Root-Verzeichnis neu erstellen

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://banana-artworks.com/</loc>
    <lastmod>2026-03-27</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://banana-artworks.com/portfolio</loc>
    <priority>0.8</priority>
  </url>
</urlset>
```

### SEO: robots.txt
**Datei:** `robots.txt` → im Root-Verzeichnis neu erstellen

```
User-agent: *
Allow: /
Sitemap: https://banana-artworks.com/sitemap.xml
```

### SEO: Google Search Console Verification
**Datei:** `index.html` → in `<head>` einfügen
> Code zuerst manuell holen unter: https://search.google.com/search-console

```html
<meta name="google-site-verification" content="DEIN_CODE_HIER">
```

---

### Hero: Availability Badge + Dual CTA
**Datei:** `index.html` → Hero-Section ersetzen

```html
<section class="hero">
  <div class="availability-banner">
    <span class="pulse-dot"></span>
    <strong>Verfügbar ab sofort</strong> — Noch <strong>2 Projektslots</strong> im April frei
  </div>

  <h1 class="hero-title">AI Solutions Builder</h1>
  <p class="hero-sub">
    Ich baue KI-Systeme, die Arbeit abnehmen —<br>
    kein Bullshit, nur funktionierende Produkte.
  </p>

  <div class="cta-group">
    <a href="https://upwork.com/freelancers/~banana-artworks"
       class="btn-primary"
       target="_blank">
      🚀 Jetzt auf Upwork kontaktieren
    </a>
    <a href="#portfolio" class="btn-ghost">
      Projekte ansehen ↓
    </a>
  </div>

  <div class="trust-bar">
    <span>⚡ FastAPI</span>
    <span>🤖 Claude API</span>
    <span>🐍 Python</span>
    <span>🔧 Automatisierung</span>
  </div>
</section>
```

---

### Security: .gitignore prüfen
**Datei:** `.gitignore` → folgende Einträge müssen vorhanden sein

```
.env
.env.local
*.env
__pycache__/
*.pyc
```

---

## 🟠 PRIORITÄT 2 — Nächste Woche

### CSS: Typografie
**Datei:** `style.css` → Orbitron nur für Headlines, Inter für Fließtext

```css
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Inter:wght@300;400;500&display=swap');

body { font-family: 'Inter', sans-serif; font-weight: 300; }
h1, h2, .brand { font-family: 'Orbitron', monospace; }
```

### CSS: Animierte Hero-Headline
**Datei:** `style.css` → hinzufügen

```css
.hero-title {
  background: linear-gradient(90deg, #F5C842, #00E5FF, #F5C842);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shine 4s linear infinite;
}

@keyframes shine {
  to { background-position: 200% center; }
}
```

### CSS: Pulse-Dot für Availability Badge
**Datei:** `style.css` → hinzufügen

```css
.availability-banner {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(0, 255, 100, 0.1);
  border: 1px solid rgba(0, 255, 100, 0.3);
  border-radius: 100px;
  font-size: 0.875rem;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background: #00FF64;
  border-radius: 50%;
  display: inline-block;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.5); }
}
```

### CSS: Premium Glassmorphism Cards
**Datei:** `style.css` → bestehendes `.card` ersetzen

```css
:root {
  --banana-gold: #F5C842;
  --cyber-cyan: #00E5FF;
  --deep-void: #050810;
}

.card {
  background: linear-gradient(
    135deg,
    rgba(245, 200, 66, 0.05) 0%,
    rgba(0, 229, 255, 0.03) 100%
  );
  backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(245, 200, 66, 0.15);
  border-radius: 16px;
  box-shadow:
    0 0 0 1px rgba(0, 229, 255, 0.05),
    0 20px 60px -10px rgba(0, 0, 0, 0.7),
    inset 0 1px 0 rgba(245, 200, 66, 0.1);
  transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
}

.card:hover {
  border-color: rgba(245, 200, 66, 0.4);
  box-shadow:
    0 0 30px rgba(245, 200, 66, 0.15),
    0 0 80px rgba(0, 229, 255, 0.05),
    0 30px 80px -15px rgba(0, 0, 0, 0.8);
  transform: translateY(-4px);
}
```

### CSS: Mobile-Fixes
**Datei:** `style.css` → hinzufügen

```css
@media (max-width: 768px) {
  .card { backdrop-filter: blur(8px); }
  h1 { font-size: clamp(1.5rem, 6vw, 3rem); }
  .hero-title { letter-spacing: 0.05em; }
}
```

### HTML: Trust Section
**Datei:** `index.html` → direkt nach der Hero-Section einfügen

```html
<section class="trust-section">
  <div class="proof-grid">
    <div class="proof-card">
      <span class="proof-icon">🏗️</span>
      <span class="proof-number">3</span>
      <span class="proof-label">Live Projekte gebaut</span>
    </div>
    <div class="proof-card">
      <span class="proof-icon">🤖</span>
      <span class="proof-number">50K+</span>
      <span class="proof-label">Claude API Tokens verarbeitet</span>
    </div>
    <div class="proof-card">
      <span class="proof-icon">⚡</span>
      <span class="proof-number">24h</span>
      <span class="proof-label">Antwortzeit garantiert</span>
    </div>
  </div>
  <div class="verify-bar">
    <a href="https://github.com/banana-artworks" class="verify-link">
      github.com/banana-artworks ✓
    </a>
  </div>
</section>
```

### HTML: Font-Preload Performance
**Datei:** `index.html` → in `<head>` einfügen

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@300;400&display=swap">
```

### Analytics einbinden
- [ ] Plausible oder Google Analytics Script in `index.html` `<head>` einfügen

---

## 🟢 PRIORITÄT 3 — Wenn Zeit ist

### JS: Cursor Trail Micro-Animation
**Datei:** `main.js` → hinzufügen

```javascript
const canvas = document.getElementById('cursor-trail');
const ctx = canvas.getContext('2d');
const particles = [];

document.addEventListener('mousemove', (e) => {
  particles.push({
    x: e.clientX,
    y: e.clientY,
    life: 1.0,
    size: Math.random() * 4 + 1,
    color: Math.random() > 0.5 ? '#F5C842' : '#00E5FF'
  });
});

function animateTrail() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  particles.forEach((p, i) => {
    p.life -= 0.04;
    p.y -= 0.5;
    if (p.life <= 0) { particles.splice(i, 1); return; }
    ctx.globalAlpha = p.life;
    ctx.fillStyle = p.color;
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.size * p.life, 0, Math.PI * 2);
    ctx.fill();
  });
  ctx.globalAlpha = 1;
  requestAnimationFrame(animateTrail);
}
animateTrail();
```

> Canvas-Element in `index.html` vor `</body>` einfügen:
> ```html
> <canvas id="cursor-trail" style="position:fixed;top:0;left:0;pointer-events:none;z-index:9999;width:100%;height:100%;"></canvas>
> ```

### Bilder optimieren
- [ ] Alle Bilder als `.webp` exportieren
- [ ] `loading="lazy"` auf alle `<img>` Tags setzen
- [ ] `width` und `height` Attribute auf allen `<img>` Tags setzen

### Blog-Sektion
- [ ] Artikel schreiben: *"Wie ich eine KI-Plattform in 72 Stunden gebaut habe"* → Long-tail SEO für DACH

---

## ✅ NACH DER UMSETZUNG — Manuelle Schritte

1. Öffne https://search.google.com/search-console
2. Property hinzufügen: `banana-artworks.com`
3. Verification-Code kopieren → in `index.html` eintragen (Priorität 1, letzter Task)
4. Seite deployen
5. In Search Console: Sitemap einreichen → `banana-artworks.com/sitemap.xml`
6. URL-Prüfung starten → Indexierung beantragen
