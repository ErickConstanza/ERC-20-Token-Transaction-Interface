import tkinter as tk
from tkinter import ttk, messagebox
from web3 import Web3
from eth_account import Account
import logging
from rich.console import Console
from rich.logging import RichHandler

# Initialize web3 with your provider
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/fc761b7e84964c72bb11a70878f17557'))

# Setup Rich Console and Logger
console = Console()
logging.basicConfig(level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler(console=console)])
logger = logging.getLogger("erc20-logger")

# ERC-20 transfer method signature
erc20_transfer_signature = web3.keccak(text="transfer(address,uint256)").hex()[:10]

def detect_token_details(token_contract_address):
    """Auto-detect token name, symbol, and decimals from the contract address."""
    try:
        token_contract = web3.eth.contract(address=Web3.to_checksum_address(token_contract_address), abi=[
            {
                "constant": True,
                "inputs": [],
                "name": "name",
                "outputs": [{"name": "", "type": "string"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function",
            },
            {
                "constant": True,
                "inputs": [],
                "name": "symbol",
                "outputs": [{"name": "", "type": "string"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function",
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function",
            },
        ])

        # Calling contract functions
        name = token_contract.functions.name().call()
        symbol = token_contract.functions.symbol().call()
        decimals = token_contract.functions.decimals().call()

        logger.info(f"Detected Token: {name} ({symbol}) with {decimals} decimals")
        return name, symbol, decimals

    except Exception as e:
        logger.error(f"Failed to detect token details: {e}")
        return None, None, None

def get_current_gas_price():
    """Fetch the current gas price in Gwei."""
    try:
        gas_price_wei = web3.eth.gas_price
        gas_price_gwei = web3.from_wei(gas_price_wei, 'gwei')
        logger.info(f"Current Gas Price: {gas_price_gwei} Gwei")
        return gas_price_gwei
    except Exception as e:
        logger.error(f"Failed to fetch gas price: {e}")
        return None

def send_erc20_transaction(token_contract_address, sender_address, private_key, recipient_address, amount_token, gas_price_gwei, gas_limit):
    """Send ERC-20 tokens to a recipient address."""
    try:
        logger.info("Starting ERC-20 transaction...")

        name, symbol, decimals = detect_token_details(token_contract_address)
        if not name or not symbol:
            raise ValueError("Token detection failed. Cannot proceed with transaction.")

        amount_in_wei = int(amount_token * 10**decimals)  # Adjust based on token decimals
        gas_price_wei = web3.to_wei(gas_price_gwei, 'gwei')
        transaction_fee = gas_price_wei * gas_limit

        sender_balance = web3.eth.get_balance(sender_address)
        if sender_balance < transaction_fee:
            raise ValueError('Insufficient ETH balance to cover the gas fees.')

        nonce = web3.eth.get_transaction_count(sender_address)
        data = (erc20_transfer_signature +
                recipient_address[2:].rjust(64, '0') +
                hex(amount_in_wei)[2:].rjust(64, '0'))

        transaction = {
            'to': token_contract_address,
            'value': 0,
            'gasPrice': gas_price_wei,
            'gas': gas_limit,
            'nonce': nonce,
            'data': data,
            'chainId': 1
        }

        signed_tx = Account.sign_transaction(transaction, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        logger.info(f"ERC-20 Transaction Sent: {web3.to_hex(tx_hash)}")
        return web3.to_hex(tx_hash)
    
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

def submit_transaction():
    try:
        token_contract_address = token_contract_address_entry.get()
        sender_address = sender_address_entry.get()
        private_key = private_key_entry.get()
        recipient_address = recipient_entry.get()
        amount_token = float(amount_entry.get())
        gas_price_gwei = float(gas_price_entry.get())
        gas_limit = int(gas_limit_entry.get())

        tx_hash = send_erc20_transaction(token_contract_address, sender_address, private_key, recipient_address, amount_token, gas_price_gwei, gas_limit)
        
        output_text_box.delete(1.0, tk.END)
        output_text_box.insert(tk.END, f"Transaction Successful!\nTransaction Hash:\n{tx_hash}")
    
    except ValueError as e:
        output_text_box.delete(1.0, tk.END)
        output_text_box.insert(tk.END, f"Error: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        output_text_box.delete(1.0, tk.END)
        output_text_box.insert(tk.END, f"An unexpected error occurred: {str(e)}")

def on_contract_address_change(event=None):
    """Callback to handle the change of the token contract address entry."""
    token_contract_address = token_contract_address_entry.get()
    name, symbol, decimals = detect_token_details(token_contract_address)
    
    if name and symbol:
        output_text_box.delete(1.0, tk.END)
        output_text_box.insert(tk.END, f"Detected Token: {name} ({symbol})\nDecimals: {decimals}\n")
    else:
        output_text_box.delete(1.0, tk.END)
        output_text_box.insert(tk.END, "Failed to detect token details. Please check the contract address.")

# Create the main window
root = tk.Tk()
root.title("ERC-20 Token Transaction Interface by ErickConstanza")
root.geometry("400x600")
root.configure(bg='#ff4d4d')  # Red background

# Styling
style = ttk.Style()
style.configure('TLabel', background='#ff4d4d', foreground='white')
style.configure('TButton', background='#ff6666', foreground='white')
style.configure('TEntry', fieldbackground='#ffcccc')

# Token contract address
ttk.Label(root, text="Token Contract Address:").pack(pady=5)
token_contract_address_entry = ttk.Entry(root, width=50)
token_contract_address_entry.pack(pady=5)
token_contract_address_entry.bind("<FocusOut>", on_contract_address_change)  # Trigger detection on focus out

# Sender address
ttk.Label(root, text="Sender Address:").pack(pady=5)
sender_address_entry = ttk.Entry(root, width=50)
sender_address_entry.pack(pady=5)

# Private key
ttk.Label(root, text="Private Key:").pack(pady=5)
private_key_entry = ttk.Entry(root, width=50, show='*')  # Mask the private key input
private_key_entry.pack(pady=5)

# Recipient address
ttk.Label(root, text="Recipient Address:").pack(pady=5)
recipient_entry = ttk.Entry(root, width=50)
recipient_entry.pack(pady=5)

# Amount to send
ttk.Label(root, text="Amount to Send:").pack(pady=5)
amount_entry = ttk.Entry(root, width=20)
amount_entry.pack(pady=5)

# Gas price
ttk.Label(root, text="Gas Price (Gwei):").pack(pady=5)
gas_price_entry = ttk.Entry(root, width=20)
gas_price_entry.pack(pady=5)
current_gas_price = get_current_gas_price()
if current_gas_price:
    gas_price_entry.insert(0, str(current_gas_price))

# Gas limit
ttk.Label(root, text="Gas Limit:").pack(pady=5)
gas_limit_entry = ttk.Entry(root, width=20)
gas_limit_entry.pack(pady=5)

# Submit button
submit_button = ttk.Button(root, text="Submit Transaction", command=submit_transaction)
submit_button.pack(pady=20)

# Output Text Box
ttk.Label(root, text="Output:").pack(pady=5)
output_text_box = tk.Text(root, height=10, width=50, wrap=tk.WORD)
output_text_box.pack(pady=5)

# Run the application
root.mainloop()
