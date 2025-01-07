import tempfile
import json

def create_temp_key_file(service_account_key):
    # Create a temporary file to store the service account JSON key
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json')
    
    # Write the service account key to the file
    with open(temp_file.name, 'w') as key_file:
        json.dump(service_account_key, key_file)
    
    return temp_file.name