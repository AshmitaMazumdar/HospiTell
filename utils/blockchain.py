import json
import logging
from web3 import Web3
import os
from dotenv import load_dotenv

# Load environment variables (for sensitive information like private keys, contract address, etc.)
load_dotenv()

logger = logging.getLogger(__name__)

# Flag: set USE_BLOCKCHAIN=true in .env to enable blockchain writes. Default is false.
USE_BLOCKCHAIN = os.getenv("USE_BLOCKCHAIN", "false").lower() == "true"

# Kaleido RPC URL for Ethereum node
KALEIDO_RPC_URL = os.getenv("KALEIDO_RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Module-level state — populated lazily on first use
_w3 = None
_contract = None
_user_address = None
_blockchain_ready = False


def _init_blockchain():
    """Lazily initialize Web3, contract, and account. Returns True if ready."""
    global _w3, _contract, _user_address, _blockchain_ready

    if _blockchain_ready:
        return True

    if not USE_BLOCKCHAIN:
        logger.warning("Blockchain disabled (USE_BLOCKCHAIN != true). Skipping init.")
        return False

    if not KALEIDO_RPC_URL:
        logger.warning("KALEIDO_RPC_URL not set. Blockchain will be skipped.")
        return False

    try:
        w3 = Web3(Web3.HTTPProvider(KALEIDO_RPC_URL))
        if not w3.is_connected():
            logger.warning("Unable to connect to Kaleido. Blockchain features will be skipped.")
            return False

        # Load the contract ABI
        abi_path = os.path.join(os.path.dirname(__file__), 'ABI.json')
        with open(abi_path, 'r') as abi_file:
            contract_abi = json.load(abi_file)

        contract_address = Web3.to_checksum_address(CONTRACT_ADDRESS)
        account = w3.eth.account.from_key(PRIVATE_KEY)

        _w3 = w3
        _contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        _user_address = account.address
        _blockchain_ready = True
        logger.info(f"Blockchain ready. Derived user address: {_user_address}")
        return True

    except Exception as e:
        logger.warning(f"Blockchain init failed: {e}. Blockchain features will be skipped.")
        return False


def store_data_on_blockchain(prescription_hash, test_results_hash):
    """
    Store prescription and test results hash on the Kaleido blockchain.

    Arguments:
    - prescription_hash: The IPFS hash of the prescription file.
    - test_results_hash: The IPFS hash of the test results file.

    Returns:
    - Transaction hash as a string if successful, or None if there was an error.
    """
    if not _init_blockchain():
        logger.warning("store_data_on_blockchain called but blockchain is not ready. Returning None.")
        return None

    try:
        # Get the latest nonce for your account (needed for transaction)
        nonce = _w3.eth.get_transaction_count(_user_address)

        # Check the balance to ensure there are enough funds
        balance = _w3.eth.get_balance(_user_address)
        print(f"Account balance: {_w3.from_wei(balance, 'ether')} ETH")
        if balance == 0:
            raise ValueError("Insufficient funds in the account to cover gas fees")

        # Call the storeMedicalData function and build the transaction
        txn = _contract.functions.storeMedicalData(prescription_hash, test_results_hash).build_transaction({
            'chainId': 1337,  # Replace with Kaleido's actual chain ID (check the Kaleido console)
            'gas': 2000000,    # Gas limit for the transaction
            'gasPrice': _w3.to_wei('20', 'gwei'),  # Gas price in Gwei
            'nonce': nonce,    # Nonce value for transaction uniqueness
            'from': _user_address  # Use the derived address from the private key
        })

        # Sign the transaction with your private key
        signed_txn = _w3.eth.account.sign_transaction(txn, PRIVATE_KEY)

        # Send the signed transaction to the blockchain
        tx_hash = _w3.eth.send_raw_transaction(signed_txn.raw_transaction)

        # Print or return the transaction hash
        print(f"Transaction successful with hash: {tx_hash.hex()}")
        return tx_hash.hex()

    except Exception as e:
        print(f"An error occurred while storing data on the blockchain: {e}")
        return None
