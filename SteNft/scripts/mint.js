const Web3 = require("web3")

const contract = require("../artifacts/contracts/SteNft.sol/SteNft.json");
const API_URL = "https://evm-rpc.testnet.teleport.network"
const ADDRESS = "0xECF09D36f07EC396f97DD448D9E4bcb19fE4Ec3A"
const PRIVATE_KEY = "a1724a3be3134c9e64d9243428926088c1f4a236e777c19e3c7a974e0da6dba3"


async function mintNFT(tokenURI) {
    const web3 = new Web3(Web3.givenProvider || API_URL );
    const contract = require("../artifacts/contracts/SteNft.sol/SteNft.json")
    const contractAddress = "0x75192e880eAad55696b22a1efCA36eff5E889cC9"
    const nftContract = new web3.eth.Contract(contract.abi, contractAddress)
    const nonce = await web3.eth.getTransactionCount(ADDRESS, "latest")
    console.log("nonce is:",  nonce)
    const tx = {
        from: ADDRESS,
        to: contractAddress,
        nonce: nonce,
        gas: 500000,
        data: nftContract.methods.mint(ADDRESS, tokenURI).encodeABI(),
    }
    const signPromise = web3.eth.accounts.signTransaction(tx, PRIVATE_KEY)
    signPromise.then((signedTx) => {
        web3.eth.sendSignedTransaction(
            signedTx.rawTransaction,
            function (err, hash) {
                if (!err) {
                    console.log("success hash is = ", hash)
                } else {
                    console.log( "mint failure error is", err)
                }
            }
        )
    })
    .catch((err) => {
        console.log("Promise failed:", err)
    })
}

mintNFT("ipfs://QmecKFh9YamJpS6VmntCpZm65oKtv7WHu7tEwsCquYSrSD")
