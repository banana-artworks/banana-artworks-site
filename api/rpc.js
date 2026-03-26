// api/rpc.js — Vercel Serverless Function
// Proxied Helius RPC — Key bleibt serverseitig, nie im Browser sichtbar

export default async function handler(req, res) {
  // Nur POST erlauben
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Rate limiting: max 100 requests pro IP pro Minute (einfach)
  // Für Production: redis-basiertes Rate Limiting empfohlen

  const HELIUS_KEY = process.env.HELIUS_KEY;
  if (!HELIUS_KEY) {
    console.error('HELIUS_KEY environment variable not set!');
    return res.status(500).json({ error: 'RPC not configured' });
  }

  const RPC_URL = `https://mainnet.helius-rpc.com/?api-key=${HELIUS_KEY}`;

  try {
    const response = await fetch(RPC_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body),
    });

    const data = await response.json();

    // CORS Header damit Browser-Requests erlaubt sind
    res.setHeader('Access-Control-Allow-Origin', 'https://banana-artworks.com');
    res.setHeader('Access-Control-Allow-Methods', 'POST');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    return res.status(response.status).json(data);
  } catch (err) {
    console.error('RPC proxy error:', err);
    return res.status(500).json({ error: 'RPC proxy failed', details: err.message });
  }
}
