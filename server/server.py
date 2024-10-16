import csv
import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# CSV file path for keys storage
KEYS_CSV = 'D:/Cheat/server/keys.csv'

# CSV file path for user credentials

USERS_CSV = 'D:/Cheat/server/admins.csv'

def authenticate_user(username, password):
    with open(USERS_CSV, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                return True
    return False

# Function to check if a key is valid and set the expiration date if it is ready
def check_key_validity_and_set_expiration(key):
    updated_rows = []
    key_found = False
    expiration_date = None

    with open(KEYS_CSV, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['key'] == key:
                if row['type'] == 'ready':
                    # Calculate the expiration date based on key type
                    if row['expiration_date'] == '30_days':
                        expiration_date = datetime.datetime.now() + datetime.timedelta(days=30)
                    elif row['expiration_date'] == 'lifetime':
                        expiration_date = 'lifetime'
                    
                    row['expiration_date'] = expiration_date.strftime("%Y-%m-%d") if expiration_date != 'lifetime' else 'lifetime'
                    row['type'] = 'activated'
                    key_found = True
                elif row['type'] == 'activated':
                    expiration_date = row['expiration_date']
                    if expiration_date != 'lifetime':
                        expiration_date = datetime.datetime.strptime(expiration_date, "%Y-%m-%d")
                        if datetime.datetime.now() <= expiration_date:
                            key_found = True
                    else:
                        key_found = True
                updated_rows.append(row)
            else:
                updated_rows.append(row)

    with open(KEYS_CSV, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['key', 'type', 'expiration_date'])
        writer.writeheader()
        writer.writerows(updated_rows)

    return key_found, expiration_date

# Function to activate a key without setting an expiration date
def activate_key(key_type):
    updated_rows = []
    activated_key = None
    key_activated = False  # Flag to track if a key has been activated
    with open(KEYS_CSV, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['type'] == 'pending' and not key_activated:
                row['type'] = 'ready'
                row['expiration_date'] = key_type
                activated_key = row
                key_activated = True  # Mark key as activated
            updated_rows.append(row)
    
    with open(KEYS_CSV, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['key', 'type', 'expiration_date'])
        writer.writeheader()
        writer.writerows(updated_rows)

    return activated_key  # Return the details of the activated key

# Endpoint for key authentication and setting expiration date
@app.route('/authkey', methods=['GET'])
def authkey():
    key = request.args.get('key')
    if not key:
        return jsonify({'error': 'No key provided'}), 400

    key_valid, expiration_date = check_key_validity_and_set_expiration(key)
    if key_valid:
        return jsonify({
            'message': 'Customer key validated successfully',
            'expiration_date': expiration_date if expiration_date == 'lifetime' else expiration_date.strftime("%Y-%m-%d")
        }), 200
    else:
        return jsonify({'error': 'Invalid key or key already activated'}), 401

# Endpoint for activating a key
@app.route('/activate', methods=['POST'])
def activate_endpoint():
    data = request.json
    secret_key = data.get('secret_key')
    username = data.get('username')
    password = data.get('password')
    key_type = data.get('key_type')

    if secret_key != '7BB74954CE45D98A182BA5A8DC93C':  # Replace with your actual secret key
        return jsonify({'error': 'Invalid secret key'}), 401

    if not authenticate_user(username, password):
        return jsonify({'error': 'Invalid username or password'}), 401

    if key_type not in ['30_days', 'lifetime']:
        return jsonify({'error': 'Invalid key type'}), 400

    # Activate a pending key if available
    activated_key = activate_key(key_type)
    if not activated_key:
        return jsonify({'error': 'No pending keys available or already activated'}), 404

    return jsonify({
        'key': activated_key['key'],
        'type': activated_key['type'],
        'expiration_date': 'Not set',
        'message': f'Key {activated_key["key"]} activated and marked as ready for {username}'
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)