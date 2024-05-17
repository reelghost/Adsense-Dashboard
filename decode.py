import base64

def encode_file_to_base64(file_path):
    with open(file_path, 'rb') as file:
        encoded_string = base64.b64encode(file.read()).decode('utf-8')
    return encoded_string

client_secrets_base64 = encode_file_to_base64('client_secrets.json')

print(f"Client Secrets Base64: {client_secrets_base64}")
