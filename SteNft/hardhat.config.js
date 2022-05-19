require("@nomiclabs/hardhat-waffle");

// APIKey
const ALCHEMY_API_KEY = "KE3V4NLUN3fgvie0lbTHyQ8Q2zSSnfo2";
const ROPSTEN_PRIVATE_KEY = "a1724a3be3134c9e64d9243428926088c1f4a236e777c19e3c7a974e0da6dba3";

module.exports = {
  solidity: "0.8.1",
  networks: {
    ropsten: {
      url: `https://eth-ropsten.alchemyapi.io/v2/${ALCHEMY_API_KEY}`,
      accounts: [`${ROPSTEN_PRIVATE_KEY}`]
    },
    bsctest: {
      url: `https://data-seed-prebsc-1-s1.binance.org:8545/`,
      accounts: [`${ROPSTEN_PRIVATE_KEY}`]
    },
    teletest: {
      url: `https://evm-rpc.testnet.teleport.network`,
      accounts: [`${ROPSTEN_PRIVATE_KEY}`]
    },
  }
};