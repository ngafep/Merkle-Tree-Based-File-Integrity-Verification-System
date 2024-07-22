# Merkle Tree-Based File Integrity Verification System

## Description

This project provides a system for verifying the integrity of files using a Merkle tree. It comprises a server-side application built with Flask that handles file uploads, manages a Merkle tree, and provides file retrieval with Merkle proofs. Additionally, it includes a client-side application that interacts with the server to upload files, retrieve files, and verify their integrity using the Merkle tree.

## Features

- **Server**: 
  - Handles file uploads via a REST API.
  - Manages a Merkle tree to ensure the integrity of uploaded files.
  - Provides file retrieval with Merkle proofs.

- **Client**:
  - Uploads files to the server.
  - Retrieves files and their Merkle proofs from the server.
  - Verifies the integrity of retrieved files using the Merkle proofs.

## Installation

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/merkle-tree-verification.git
    cd merkle-tree-verification
    ```

2. Build and start the services using Docker Compose:
    ```sh
    docker-compose up --build
    ```

## Usage

### Server

The server provides two main endpoints:

- **Upload Files**: 
  - Endpoint: `/upload`
  - Method: `POST`
  - Description: Uploads files to the server and generates a Merkle tree from the file contents.

- **Retrieve File**:
  - Endpoint: `/get_file/<index>`
  - Method: `GET`
  - Description: Retrieves a file and its Merkle proof by index.

### Client

The client interacts with the server to upload files, retrieve files, and verify their integrity.

1. **Upload Files**:
    ```python
    client = Client("http://server:5000")
    files = {
        "file1.txt": "This is file 1",
        "file2.txt": "This is file 2",
        # Add more files as needed
    }
    client.upload_files(files)
    ```

2. **Retrieve and Verify Files**:
    ```python
    for i in range(len(files)):
        retrieved_file = client.get_file(i)
        if retrieved_file:
            print(f"Retrieved file {i}: {retrieved_file}")
    ```

## File Structure

- **docker-compose.yml**: Defines the server and client services.
- **Dockerfile**: Builds the Docker image for the server and client.
- **server.py**: Implements the server-side application using Flask.
- **client.py**: Implements the client-side application.
- **merkle_tree.py**: Implements the Merkle tree data structure and related functions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
