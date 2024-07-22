import requests  # Import the requests library for making HTTP requests
import json      # Import json module for handling JSON data
from merkle_tree import MerkleTree  # Import the MerkleTree class from merkle_tree module

class Client:
    def __init__(self, server_url):
        self.server_url = server_url  # Initialize the Client class with the server URL
        self.root_hash = None         # Initialize root_hash attribute to None

    def upload_files(self, files):
        # Method to upload files to the server
        response = requests.post(f"{self.server_url}/upload", json={"files": files})  # Send POST request to upload files to server
        self.root_hash = response.json()["root_hash"]  # Extract and store the root hash received from the server
        
        with open("root_hash.txt", "w") as f:
            f.write(self.root_hash)  # Write the root hash to a file named root_hash.txt
        
        print(f"Files uploaded. Root hash: {self.root_hash}")  # Print confirmation message with the root hash

    def get_file(self, index):
        # Method to get and verify a file from the server
        response = requests.get(f"{self.server_url}/get_file/{index}")  # Send GET request to retrieve file and proof from server
        data = response.json()  # Parse the JSON response
        
        if "error" in data:
            print(f"Error: {data['error']}")  # Print error message if there's an error in the response
            return None

        file_content = data["file"]  # Extract file content from the response
        proof = data["proof"]        # Extract Merkle proof from the response

        with open("root_hash.txt", "r") as f:
            stored_root_hash = f.read().strip()  # Read and strip the stored root hash from root_hash.txt file

        print(f"Client: Verifying file {index}")
        print(f"Client: Stored root hash: {stored_root_hash}")
        print(f"Client: Received proof: {proof}")

        # Debug information
        print(f"Client: File content: {file_content}")
        print(f"Client: Index: {index}")

        # Verify file integrity using MerkleTree.verify_proof method
        if MerkleTree.verify_proof(file_content, index, proof, stored_root_hash):
            print(f"File {index} verified successfully.")
            return file_content  # Return file content if verification succeeds
        else:
            print(f"File {index} verification failed.")
            return None  # Return None if verification fails

def demo():
    client = Client("http://server:5000")  # Create an instance of Client class with server URL
    
    # Upload files
    files = {
        "file1.txt": "This is file 1",   # Define files to be uploaded with filename and content
        "file2.txt": "This is file 2",
        "file3.txt": "This is file 3",
        "file4.txt": "This is file 4",
        "file5.txt": "This is file 5",
        "file6.txt": "This is file 6",
        "file7.txt": "This is file 7",
        "file8.txt": "This is file 8",
        "file9.txt": "This is file 9",
        "file10.txt": "This is file 10"
    }
    client.upload_files(files)  # Call upload_files method to upload the defined files to the server

    # Get and verify files
    for i in range(10):  # Iterate over the range of 10 (files) to get and verify each file
        retrieved_file = client.get_file(i)  # Call get_file method to retrieve and verify file at index i
        if retrieved_file:
            print(f"Retrieved file {i}: {retrieved_file}")  # Print retrieved file content if verification succeeds

if __name__ == "__main__":
    demo()  # Execute the demo function if this script is run directly
