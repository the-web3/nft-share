### 1.合约测试
```
npx hardhat test
```

### 2. 合约部署 ropsten
```
npx hardhat run --network bsctest scripts/deploy.js
```

### 3. 合约 verify 和 publish
```
npx hardhat verify --contract contracts/SteNft.sol:SteNft  --network bsctest 0x6983eccfFeF3fb3AC77604123F7aBEdE64797C66
```

