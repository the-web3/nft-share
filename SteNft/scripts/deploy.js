const hre = require("hardhat");


async function main() {
    const NFT = await hre.ethers.getContractFactory("SteNft");
    const nft = await NFT.deploy();
    const URI = "ipfs://QmecKFh9YamJpS6VmntCpZm65oKtv7WHu7tEwsCquYSrSD";
    await nft.mint("0xECF09D36f07EC396f97DD448D9E4bcb19fE4Ec3A", URI)
    await nft.deployed();
    console.log("NFT deployed to:", nft.address);
}

main().then(() => process.exit(0)).catch(error => {
    console.error(error);
    process.exit(1);
});
