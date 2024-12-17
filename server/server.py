import csv
import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

KEYS_CSV = 'D:/CheatHWID/server/keys.csv'

USERS_CSV = 'D:/CheatHWID/server/admins.csv'

def authenticate_user(username, password):
    with open(USERS_CSV, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                return True
    return False

def activate_key(key_type):
    updated_rows = []
    activated_key = None
    key_activated = False
    with open(KEYS_CSV, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['type'] == 'pending' and not key_activated:
                row['type'] = 'ready'
                row['expiration_date'] = key_type
                activated_key = row
                key_activated = True
            updated_rows.append(row)

    with open(KEYS_CSV, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['key', 'type', 'expiration_date', 'hwid'])
        writer.writeheader()
        writer.writerows(updated_rows)

    return activated_key
    
def check_key_validity_and_set_expiration(key, hwid):
    updated_rows = []
    key_found = False
    expiration_date = None
    hwid_assigned = False

    with open(KEYS_CSV, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['key'] == key:
                key_found = True
                
                stored_hwid = row['hwid'].strip() if row['hwid'] else ''
                hwid = hwid.strip() if hwid else ''

                if row['type'] == 'activated':
                    
                    if stored_hwid == hwid:
                        expiration_date = row['expiration_date']
                        hwid_assigned = True
                    else:
                        hwid_assigned = False 
                elif row['type'] == 'ready':
                    row['hwid'] = hwid 
                    expiration_date = row['expiration_date']
                    row['type'] = 'activated'
                    hwid_assigned = True 
                updated_rows.append(row)
            else:
                updated_rows.append(row)

    with open(KEYS_CSV, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['key', 'type', 'expiration_date', 'hwid'])
        writer.writeheader()
        writer.writerows(updated_rows)

    return key_found, expiration_date, hwid_assigned

@app.route('/authkey', methods=['GET'])
def authkey():
    key = request.args.get('key')
    hwid = request.args.get('hwid')

    if not key:
        return jsonify({'error': 'No key provided'}), 400
    
    if not hwid:
        return jsonify({'error': 'No HWID provided'}), 400
        
    print(f'Received key: {key}, HWID: "{hwid}"')

    key_valid, expiration_date, hwid_assigned = check_key_validity_and_set_expiration(key, hwid)
    
    if key_valid and hwid_assigned:
        return jsonify({
            'message': 'Customer key validated successfully',
            'expiration_date': expiration_date if expiration_date == 'lifetime' else expiration_date.strftime("%Y-%m-%d")
        }), 200
    elif key_valid and not hwid_assigned:
        return jsonify({'error': 'HWID mismatch. Access denied.'}), 403
    else:
        return jsonify({'error': 'Invalid key or key already activated'}), 401
        
@app.route('/activate', methods=['POST'])
def activate_endpoint():
    data = request.json
    secret_key = data.get('secret_key')
    username = data.get('username')
    password = data.get('password')
    key_type = data.get('key_type')

    if secret_key != '7BB74954CE45D98A182BA5A8DC93C':
        return jsonify({'error': 'Invalid secret key'}), 401

    if not authenticate_user(username, password):
        return jsonify({'error': 'Invalid username or password'}), 401

    if key_type not in ['30_days', 'lifetime']:
        return jsonify({'error': 'Invalid key type'}), 400

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
