import random
import string
import csv

KEYS_CSV = 'keys.csv'

def generate_keys(n=100):
    keys = []
    while len(keys) < n:
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        if key not in [k['key'] for k in keys]:
            keys.append({'key': key, 'type': 'pending', 'expiration_date': '', 'hwid': ''})
    
    with open(KEYS_CSV, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['key', 'type', 'expiration_date', 'hwid'])
        writer.writeheader()
        writer.writerows(keys)

if __name__ == '__main__':
    generate_keys()
