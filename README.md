# Usage

Provision a free node on Infura and set it to ropsten. Copy the project id. 

```
pip3 install web3
pip3 install py-solc-x
echo "INFURA_PROJECT_ID=$your_infura_key \nPRIVATE_KEY=$your_key" >> .env
python3 [script.py]
```