
from solcx import compile_source
from helper import get_provider_and_account

w3, acct = get_provider_and_account()

# solidity source code
compiled_target = compile_source(
"""
pragma solidity ^0.4.21;
contract GuessTheSecretNumberChallenge {
    bytes32 answerHash = 0xdb81b4d58595fbbbb592d3661a34cdca14d7ab379441400cbfa1b78bc447c365;

    function GuessTheSecretNumberChallenge() public payable {
        require(msg.value == 1 ether);
    }
    
    function isComplete() public view returns (bool) {
        return address(this).balance == 0;
    }

    function guess(uint8 n) public payable {
        require(msg.value == 1 ether);

        if (keccak256(n) == answerHash) {
            msg.sender.transfer(2 ether);
        }
    }
}
"""
)

contract_id, contract_interface = compiled_target.popitem()

# get abi
abi = contract_interface["abi"]

# brute force the hash
answer_hash = "0xdb81b4d58595fbbbb592d3661a34cdca14d7ab379441400cbfa1b78bc447c365"
num = 0

while num < 256: # uint8.max
    hash = w3.solidityKeccak(["uint8"], [num]).hex()
    if hash == answer_hash:
        break
    else:    
        num  += 1

# initialize contract at deployed address
guessing_game = w3.eth.contract(
    address="0xA0968A4DE7a0978443750144300c872cfEC3d6F7",
    abi=abi
)    

# send transaction to contract invoking guess with uint8 value that has identical hash to answer 
tx_hash = guessing_game.functions.guess(num).transact({'value': w3.toWei(1, 'ether')})
print(f"View on Etherscan: https://ropsten.etherscan.io/tx/{tx_hash.hex()}")

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Completed: {guessing_game.functions.isComplete().call()}")