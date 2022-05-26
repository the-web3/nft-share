import {  MintNft } from '../src/jsNextMint';


describe('NFT test', ()=>{
    test('mint nft', async () => {
        const nftInfo = await MintNft("")
        console.log("nftInfo===", nftInfo)
    });
});