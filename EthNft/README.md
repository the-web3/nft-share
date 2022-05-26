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
npx hardhat verify --contract contracts/EthNft.sol:EthNft  --network bsctest 0x6983eccfFeF3fb3AC77604123F7aBEdE64797C66
```

### 4. script 脚本下面有一个 mint.js,

把文件上传到 IPFS，把文件的 URL 传入，执行下面命令 mint
```
node mint.js
```
