import { clusterApiUrl, Connection, Keypair, LAMPORTS_PER_SOL } from  "@solana/web3.js";
import { createMint, getOrCreateAssociatedTokenAccount, mintTo, setAuthority, transfer } from  "@solana/spl-token";


(async () => {
    const connection = new Connection(clusterApiUrl("devnet"), "confirmed");
    const fromWallet = Keypair.generate();
    const fromAirdropSignature = await connection.requestAirdrop(
        fromWallet.publicKey,
        LAMPORTS_PER_SOL
    );
    await connection.confirmTransaction(fromAirdropSignature);
    const mint = await createMint(
        connection,
        fromWallet,
        fromWallet.publicKey,
        null,
        0
    );
    const fromTokenAccount = await getOrCreateAssociatedTokenAccount(
        connection,
        fromWallet,
        mint,
        fromWallet.publicKey
    );
    const toWallet = Keypair.generate();
    const toTokenAccount = await getOrCreateAssociatedTokenAccount(
        connection,
        fromWallet,
        mint,
        toWallet.publicKey
    );
    let signature = await mintTo(
        connection,
        fromWallet,
        mint,
        fromTokenAccount.address,
        fromWallet.publicKey,
        1
    );
    await setAuthority(
        connection,
        fromWallet,
        mint,
        fromWallet.publicKey,
        0,
        null
    );
    signature = await transfer(
        connection,
        fromWallet,
        fromTokenAccount.address,
        toTokenAccount.address,
        fromWallet.publicKey,
        1
    );
    console.log("SIGNATURE", signature);
})();