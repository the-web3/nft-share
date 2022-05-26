import { Metaplex, keypairIdentity, bundlrStorage } from "@metaplex-foundation/js-next";
import { Connection, Keypair} from "@solana/web3.js";


export async function MintNft(privateKey) {
    const connection = new Connection("mainnet");
    console.log(await connection.getBlockHeight())
    const wallet = Keypair.fromSecretKey(new Uint8Array(Buffer.from(privateKey, "hex")));
    const metaplex = Metaplex.make(connection)
        .use(keypairIdentity(wallet))
        .use(bundlrStorage());
    const { uri } = await metaplex.nfts().uploadMetadata({
        name: "My NFT",
        description: "My description",
        image: "https://arweave.net/123",
    });
    const { nft } = await metaplex.nfts().create({
        uri: uri,
    });
    console.log(nft)
}

