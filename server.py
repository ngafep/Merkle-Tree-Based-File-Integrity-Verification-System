from flask import Flask, jsonify, request  # Import necessary Flask modules
from merkle_tree import MerkleTree  # Import MerkleTree class from local module
import os  # Import os module for operating system related functionalities

app = Flask(__name__)  # Create a Flask application instance
files = {}  # Initialize an empty dictionary to store uploaded files
merkle_tree = None  # Initialize a variable to hold the Merkle tree object

@app.route('/upload', methods=['POST'])  # Define a route for uploading files via POST method
def upload_files():
    global files, merkle_tree  # Access global variables files and merkle_tree
    files = request.json['files']  # Extract uploaded files from the request JSON data
    merkle_tree = MerkleTree(list(files.values()))  # Create a Merkle tree from the file contents
    root_hash = merkle_tree.get_root()  # Get the root hash of the Merkle tree
    print(f"Server: Root hash generated: {root_hash}")  # Print the generated root hash to console
    print(f"Server: Tree structure: {merkle_tree.tree}")  # Print the Merkle tree structure to console
    return jsonify({"root_hash": root_hash})  # Return the root hash as JSON response

@app.route('/get_file/<int:index>', methods=['GET'])  # Define a route for retrieving files by index via GET method
def get_file(index):
    if index < 0 or index >= len(files):  # Check if the requested index is valid
        return jsonify({"error": "Invalid file index"}), 400  # Return error response for invalid index

    file_content = list(files.values())[index]  # Get the content of the file at the requested index
    proof = merkle_tree.get_proof(index)  # Get the Merkle proof for the file at the requested index
    print(f"Server: Sending file {index} with content: {file_content}")  # Print file content to console
    print(f"Server: Proof for file {index}: {proof}")  # Print Merkle proof to console
    return jsonify({"file": file_content, "proof": proof})  # Return file content and proof as JSON response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run the Flask application on host 0.0.0.0 and port 5000
