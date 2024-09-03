# ERC-20-Token-Transaction-Interface
ERC-20 Token Transaction Interface
Overview

This application provides a graphical user interface (GUI) for sending ERC-20 tokens on the Ethereum blockchain. It allows users to input transaction details, detect ERC-20 token information automatically, and handle transactions with real-time gas price fetching. The application is built using Python and Tkinter for the GUI, with Web3.py for interacting with the Ethereum blockchain and Rich for logging.
Features

    ERC-20 Token Detection: Automatically detects token details (name, symbol, decimals) based on the contract address entered.
    Transaction Handling: Send ERC-20 tokens with user-defined gas price and gas limit.
    Gas Price Fetching: Retrieve the current gas price from the Ethereum network and display it in the UI.
    Rich Logging: Provides detailed logging with the Rich console.
    Error Handling: Displays relevant error messages and transaction status in the UI.

Prerequisites

To run this application, you need:

    Python 3.7 or higher
    Required Python libraries: web3, eth-account, bitcoinlib, tkinter, rich

You can install the required libraries using pip:

bash

pip install web3 eth-account bitcoinlib rich

Installation

    Clone the Repository:

    bash

git clone https://github.com/yourusername/erc20-token-transaction-interface.git
cd erc20-token-transaction-interface

Install Dependencies:

Ensure that all required libraries are installed. You can use the provided requirements.txt:

bash

    pip install -r requirements.txt

Usage

    Run the Application:

    bash

    python app.py

    Enter Transaction Details:
        Token Contract Address: Input the ERC-20 token contract address. The application will automatically detect and display the token's name, symbol, and decimals.
        Sender Address: Enter the sender's Ethereum address.
        Private Key: Enter the sender's private key. This is required to sign the transaction.
        Recipient Address: Enter the recipient's Ethereum address.
        Amount to Send: Enter the amount of the token you wish to send.
        Gas Price (Gwei): Enter the gas price in Gwei. The application will fetch the current gas price if left empty.
        Gas Limit: Enter the gas limit for the transaction.

    Submit Transaction:

    Click the "Submit Transaction" button to initiate the transaction. The result, including any errors or the transaction hash, will be displayed in the output section.

Example

To send 1.5 million USDT with a gas price of 20 Gwei and a gas limit of 65,000, you would:

    Enter the USDT contract address: 0xdac17f958d2ee523a2206206994597c13d831ec7
    Input the amount as 1500000
    Set the gas price and gas limit accordingly
    Click "Submit Transaction"

License

This project is licensed under the MIT License. See the LICENSE file for details.
Contributing

Feel free to open issues and submit pull requests. Contributions to improve the functionality and features of this application are welcome!
Contact

For questions or support, please open an issue on the GitHub repository or contact me at @erickconstanza.
