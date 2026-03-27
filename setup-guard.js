import { createUmi }    from '@metaplex-foundation/umi-bundle-defaults';
import {
  keypairIdentity, publicKey, some, sol, generateSigner,
} from '@metaplex-foundation/umi';
import {
  mplCandyMachine, fetchCandyMachine,
  createCandyGuard, updateCandyGuard,
  wrap, findCandyGuardPda,
} from '@metaplex-foundation/mpl-candy-machine';
import { readFileSync } from 'fs';

const CM_ID      = '6Myzztq28zM4385VxfGdeGxg1ygSWrnC6KwfT1KnNRsP';
const MINT_PRICE = 0.25;
const KEYPAIR_PATH = './authority-keypair.json';
const RPC = 'https://mainnet.helius-rpc.com/?api-key=fc7e345b-f4f3-44a2-84e3-25d8bd33c87c';

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function main() {
  console.log('🍌 Banana Artworks — Guard Setup v4');
  console.log('════════════════════════════════════');

  const secretKey = JSON.parse(readFileSync(KEYPAIR_PATH, 'utf8'));
  const umi = createUmi(RPC).use(mplCandyMachine());
  const keypair = umi.eddsa.createKeypairFromSecretKey(new Uint8Array(secretKey));
  umi.use(keypairIdentity(keypair));
  console.log('✅ Wallet: ' + keypair.publicKey);

  console.log('\n🔍 Lade Candy Machine...');
  const cm = await fetchCandyMachine(umi, publicKey(CM_ID));
  console.log('   mintAuthority: ' + JSON.stringify(cm.mintAuthority));

  const treasury = keypair.publicKey;
  const guardConfig = {
    solPayment: some({ lamports: sol(MINT_PRICE), destination: treasury }),
  };

  if (cm.mintAuthority?.__option === 'Some') {
    // Guard existiert — nur Preis updaten
    console.log('\n🔄 Guard existiert — update auf ' + MINT_PRICE + ' SOL...');
    const guardPDA = cm.mintAuthority.value;
    await updateCandyGuard(umi, {
      candyGuard: guardPDA,
      guards: guardConfig,
      groups: [],
    }).sendAndConfirm(umi, { confirm: { commitment: 'finalized' } });
    console.log('✅ Preis aktualisiert! Guard: ' + guardPDA);

  } else {
    // Schritt 1: Guard erstellen
    console.log('\n✨ Schritt 1/2: Erstelle Candy Guard...');
    const base = generateSigner(umi);
    console.log('   Base pubkey: ' + base.publicKey);

    await createCandyGuard(umi, {
      base,
      guards: guardConfig,
      groups: [],
    }).sendAndConfirm(umi, { confirm: { commitment: 'finalized' } });
    console.log('✅ Guard erstellt!');

    // PDA berechnen — findCandyGuardPda gibt [publicKey, bump] zurück
    const pda = findCandyGuardPda(umi, { base: base.publicKey });
    // PDA kann PublicKey oder [PublicKey, number] sein — beide Fälle abdecken
    const guardPDAKey = Array.isArray(pda) ? pda[0] : pda;
    console.log('   Guard PDA: ' + guardPDAKey);

    // Warte bis Guard on-chain sichtbar
    console.log('   Warte 5 Sekunden auf Bestätigung...');
    await sleep(5000);

    // Schritt 2: wrap
    console.log('\n🔗 Schritt 2/2: Verbinde Guard mit Candy Machine...');
    await wrap(umi, {
      candyMachine: publicKey(CM_ID),
      candyGuard: guardPDAKey,
    }).sendAndConfirm(umi, { confirm: { commitment: 'finalized' } });
    console.log('✅ Guard verbunden!');
  }

  console.log('\n🎉 FERTIG! Preis: ' + MINT_PRICE + ' SOL → ' + treasury);
  console.log('   Website neu laden → Preis erscheint!');
}

main()
  .then(() => process.exit(0))
  .catch(err => {
    console.error('\n❌ Fehler:', err?.message || err);
    if (err?.logs) console.error('Logs:\n' + err.logs.slice(-5).join('\n'));
    process.exit(1);
  });
