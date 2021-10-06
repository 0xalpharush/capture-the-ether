from solcx import compile_source
from helper import get_provider_and_account

w3, acct = get_provider_and_account()

# solidity source code
compiled_target = compile_source(
    '''
    pragma solidity ^0.4.21;

    // Relevant part of the CaptureTheEther contract.
    contract CaptureTheEther {
        mapping (address => bytes32) public nicknameOf;

        function setNickname(bytes32 nickname) public {
            nicknameOf[msg.sender] = nickname;
        }
    }
    '''
)

# retrieve the contract interface
contract_id, contract_interface = compiled_target.popitem()

# get abi
abi = contract_interface["abi"]

# initialize contract at deployed address
nickname = w3.eth.contract(
    address="0x71c46Ed333C35e4E6c62D32dc7C8F00D125b4fee",
    abi=abi
)    

# send transaction to contract invoking setNickname with bytes value
tx_hash = nickname.functions.setNickname(b"alpharush").transact()
print(f"View on Etherscan: https://ropsten.etherscan.io/tx/{tx_hash.hex()}")

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# verify state of contract
new_nickname = nickname.functions.nicknameOf(acct.address).call().decode("utf-8")
print(f"Nickname set to: {new_nickname}")

