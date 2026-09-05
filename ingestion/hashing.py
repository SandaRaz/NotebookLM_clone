import hashlib

# Pour verifier les doublons
def calculate_file_hash(file_content):
    return hashlib.sha256(file_content).hexdigest()