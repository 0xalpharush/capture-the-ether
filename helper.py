import os
from dotenv import load_dotenv
from web3 import Web3, HTTPProvider
from web3.middleware import construct_sign_and_send_raw_middleware
from eth_account import Account


def get_provider_and_account():
    """
    Establish connection with rpc endpoint and add signing/ gas estimation middleware for account
    """
    load_dotenv()
    pk = os.environ["PRIVATE_KEY"]
    project_id =os.environ["INFURA_PROJECT_ID"]
    w3 = Web3(HTTPProvider(f"https://ropsten.infura.io/v3/{project_id}"))
    acct = Account.from_key(pk)
    w3.middleware_onion.add(construct_sign_and_send_raw_middleware(acct))
    w3.eth.default_account = acct.address

    assert w3.isConnected() == True
    assert w3.eth.chain_id == 3

    return w3, acct
