import os

from dotenv import load_dotenv
load_dotenv()

agent_abi = [
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "userAddress",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "data",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "max_hops",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "originalData",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "address[]",
				"name": "hops",
				"type": "address[]"
			}
		],
		"name": "IRISRequestAgentData",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "userAddress",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "data",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "max_hops",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "originalData",
				"type": "string"
			},
			{
				"internalType": "address[]",
				"name": "hops",
				"type": "address[]"
			}
		],
		"name": "requestData",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]

def call_contract_function(w3, wallet, input, original, hops, logger, to):
    try:
        agent = w3.eth.contract(address=to, abi=agent_abi)
        agent_function = agent.functions.requestData(w3.to_checksum_address(wallet), input, 20, original, hops)
        
        nonce = w3.eth.get_transaction_count(os.getenv('WALLET_ADDR'))
        tx = agent_function.build_transaction({
            'from': os.getenv('WALLET_ADDR'),
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
            'chainId': w3.eth.chain_id
        })
        
        signed_tx = w3.eth.account.sign_transaction(tx, os.getenv('WALLET_PKEY'))
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        logger.info(f"Transaction sent: {tx_hash.hex()}")
        
        logger.info("Waiting for transaction confirmation...")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt
        
    except Exception as e:
        logger.error(f"[bold red]Failed to call contract function: {e}[/]")
        logger.exception("Exception occurred while calling contract function.")