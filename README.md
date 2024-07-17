# Promissory Note Blockchain Project

## Overview

This project demonstrates a possible implementation of electronic transferable values using blockchain technology as a registry. It focuses on the creation, encryption, and transfer of promissory notes, leveraging blockchain for secure and verifiable transactions.

It is composed of two API services:

1. A Blockchain service to register the transfer of the promissory note.
2. A XML processing service for adding ownership, encrypting and decrypting xml files (as a concept of a promissory note).

## Includes Ideas For

- **Blockchain Integration**: Utilize a custom blockchain for recording transactions and ensuring the integrity of promissory note transfers.
- **Secure Transactions**: Sign and encrypt promissory notes to ensure authenticity and confidentiality.
- **Transfer and Verification**: Support for transferring promissory notes between parties and verifying ownership and authenticity.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Pipenv or virtual environment setup

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repository/promissory-note-blockchain.git
   ```
2. Navigate to the project directory.
3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Create a private key and certification in your selected directory.

### Running the project

1. Activate the virtual environment:
   ```sh
   source bin/activate
   ```
2. Initialize the blockchain API service using `uvicorn` in port `8001` (since is hardcoded):
   ```sh
   uvicorn --app-dir src/blockchain/ blockchain_api:app --reload --port 8001
   ```
3. Initialize the xml processor API service `uvicorn` in port `8002` (since is hardcoded):
   ```sh
   uvicorn --app-dir src/processor/ xml_processor_api:app --reload --port 8002
   ```
4. Add the paths of your private key and certification to the environment file (`.env`).
5. Run the main script:
   ```sh
   python src/main.py
   ```

## Usage

The project can be used to simulate the creation, encryption and transfer of a promissory note using blockchain to register the transactions. Run `main.py` to see an example.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
