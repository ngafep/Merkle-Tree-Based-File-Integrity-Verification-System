import hashlib  # Importing hashlib module for cryptographic hashing operations

class MerkleTree:
    def __init__(self, leaves):
        self.leaves = [self._hash(leaf) for leaf in leaves]  # Compute hash of each leaf and store in self.leaves
        self.tree = self._build_tree()  # Build the Merkle tree from the leaves upon initialization

    def _build_tree(self):
        tree = [self.leaves]  # Start with the leaves as the first level of the tree
        while len(tree[-1]) > 1:  # Continue building until we have computed the root
            level = []
            for i in range(0, len(tree[-1]), 2):
                left = tree[-1][i]
                right = tree[-1][i + 1] if i + 1 < len(tree[-1]) else left
                level.append(self._hash(left + right))  # Hash pairs of nodes to form the next level
            tree.append(level)  # Add the current level to the tree
        return tree  # Return the complete Merkle tree structure

    def get_root(self):
        return self.tree[-1][0]  # Return the root hash of the Merkle tree

    def get_proof(self, index):
        proof = []
        for i, level in enumerate(self.tree[:-1]):  # Iterate through each level except the root level
            is_right = index % 2
            if is_right:
                proof.append(level[index - 1])  # Add sibling hash to proof if current node is a right child
            elif index + 1 < len(level):
                proof.append(level[index + 1])  # Add sibling hash to proof if current node is a left child
            else:
                proof.append(level[index])  # Add current hash if it's the last leaf in an odd-numbered level
            index //= 2  # Move up to the parent node
        return proof  # Return the Merkle proof for the given leaf index

    @staticmethod
    def verify_proof(leaf, index, proof, root_hash):
        computed_hash = MerkleTree._hash(leaf)  # Compute hash of the provided leaf
        for i, sibling_hash in enumerate(proof):
            if index % 2 == 0:
                computed_hash = MerkleTree._hash(computed_hash + sibling_hash)  # Concatenate and hash if left child
            else:
                computed_hash = MerkleTree._hash(sibling_hash + computed_hash)  # Concatenate and hash if right child
            index //= 2  # Move up to the parent node
        return computed_hash == root_hash  # Return True if computed hash matches the root hash

    @staticmethod
    def _hash(data):
        if isinstance(data, str):
            data = data.encode()  # Convert string to bytes if it's not already
        elif isinstance(data, bytes):
            pass  # Use the data directly if it's already bytes
        else:
            data = str(data).encode()  # Convert non-string data to string and then to bytes
        return hashlib.sha256(data).hexdigest()  # Return the hexadecimal digest of the hashed data
