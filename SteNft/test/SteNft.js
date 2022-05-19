const { expect } = require("chai");


describe("Test SteNft", function() {
    it("It should deploy the contract, mint a token, and resolve to the right URI", async function() {
        const NFT = await ethers.getContractFactory("SteNft");
        const nft = await NFT.deploy();
        const URI = "ipfs://QmecKFh9YamJpS6VmntCpZm65oKtv7WHu7tEwsCquYSrSD";
        await nft.deployed();
        await nft.mint("0xECF09D36f07EC396f97DD448D9E4bcb19fE4Ec3A", URI)
        expect(await nft.tokenURI(1)).to.equal(URI)
    });
});

