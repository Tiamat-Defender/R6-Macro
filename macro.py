import tkinter as tk
from tkinter import ttk
import requests
import win32api
import keyboard
import random
import pyautogui as pui
from ttkthemes import ThemedStyle


SERVER_URL = 'http://127.0.0.1'

screenWidth, screenHeight = pui.size()

base_vertical_sensitivity = 30
base_horizontal_sensitivity = 30
base_dpi = 1600

dpi_scaling_factor = 20.0
sensitivity_scaling_factor = 20.0

root = None

def authenticate(key):
    authkey_url = f'{SERVER_URL}/authkey'
    params = {'key': key}
    try:
        response = requests.get(authkey_url, params=params)
        if response.status_code == 200:
            print('Customer key validated successfully')
            return True
        else:
            print(f'Customer key validation failed with status code {response.status_code}')
            return False
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False
    
def execute_code():
    global root  

    primary = "primary"
    secondary = "secondary"
    
    movement_delay = 0.03

    toggle_button = '5' 

    enabled = True

    operators = {
        "Striker": {
            "primary1": {"vertical": [8.0], "horizontal": [-0.5]},
            "primary2": {"vertical": [6.0], "horizontal": [0.2]},
            "primary3": {"vertical": [0], "horizontal": [0]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0], "horizontal": [0]},
            "secondary3": {"vertical": [0], "horizontal": [0]}
        },
        "Sledge": {
            "primary1": {"vertical": [4.75], "horizontal":[0.15]},
            "primary2": {"vertical": [0], "horizontal": [0]},
            "primary3": {"vertical": [0], "horizontal": [0]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0], "horizontal": [0]},
            "secondary3": {"vertical": [0], "horizontal": [0]}
        },
        "Ash": {
            "primary1": {"vertical": [8.0], "horizontal": [0.5]},
            "primary2": {"vertical": [11], "horizontal": [-0.45]},
            "primary3": {"vertical": [0], "horizontal": [0]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0], "horizontal": [0]}
        },
        "Thermite": {
            "primary1": {"vertical": [0], "horizontal": [0]},
            "primary2": {"vertical": [5.15], "horizontal": [1.0]},
            "primary3": {"vertical": [0], "horizontal": [0]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0], "horizontal": [0]}
        },
        "Twitch": {
            "primary1": {"vertical": [13.0], "horizontal": [0.24]},
            "primary2": {"vertical": [0], "horizontal": [0]},
            "primary3": {"vertical": [0], "horizontal": [0]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0], "horizontal": [0]},
            "secondary3": {"vertical": [0], "horizontal": [0]}
        },
        "Montange": {
            "primary1": {"vertical": [0.01], "horizontal": [0.01]},
            "primary2": {"vertical": [0], "horizontal": [0]},
            "primary3": {"vertical": [0], "horizontal": [0]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0], "horizontal": [0]},
            "secondary3": {"vertical": [0], "horizontal": [0]}
        },
        "Glaz": {
            "primary1": {"vertical": [0.01], "horizontal": [0.01]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [5.5], "horizontal": [0.15]}
        },
        "Fuze": {
            "primary1": {"vertical": [7.5], "horizontal": [-0.45]},
            "primary2": {"vertical": [0], "horizontal": [0]},
            "primary3": {"vertical": [0], "horizontal": [0]},
            "secondary1": {"vertical": [0.01], "horizontal": [0]},
            "secondary2": {"vertical": [0], "horizontal": [0]},
            "secondary3": {"vertical": [0], "horizontal": [0]}
        },
        "Blitz": {
            "primary1": {"vertical": [0.01], "horizontal": [0]},
            "primary2": {"vertical": [0], "horizontal": [0]},
            "primary3": {"vertical": [0], "horizontal": [0]},
            "secondary1": {"vertical": [0.01], "horizontal": [0]},
            "secondary2": {"vertical": [0], "horizontal": [0]},
            "secondary3": {"vertical": [0], "horizontal": [0]}
        },
        "IQ": {
            "primary1": {"vertical": [4.0], "horizontal": [-0.03]},
            "primary2": {"vertical": [5.5], "horizontal": [-0.03]},
            "primary3": {"vertical": [8.0], "horizontal": [-0.03]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0], "horizontal": [0]},
            "secondary3": {"vertical": [0], "horizontal": [0]}
        },
        "Buck": {
            "primary1": {"vertical": [7.65], "horizontal": [-0.45]},
            "primary2": {"vertical": [0], "horizontal": [0]},
            "primary3": {"vertical": [0], "horizontal": [0]},
            "secondary1": {"vertical": [0], "horizontal": [0]},
            "secondary2": {"vertical": [0], "horizontal": [0]},
            "secondary3": {"vertical": [0], "horizontal": [0]}
        },
        "Black Beard": {
            "primary1": {"vertical": [3.5], "horizontal": [0.65]},
            "primary2": {"vertical": [0], "horizontal": [0]},
            "primary3": {"vertical": [0], "horizontal": [0]},
            "secondary1": {"vertical": [0], "horizontal": [0]},
            "secondary2": {"vertical": [0], "horizontal": [0]},
            "secondary3": {"vertical": [0], "horizontal": [0]}
        },
        "Capitao ": {
            "primary1": {"vertical": [7.0], "horizontal": [-0.35]},
            "primary2": {"vertical": [6.0], "horizontal": [0.2]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Hibana": {
            "primary1": {"vertical": [7.0], "horizontal": [-0.45]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [5.5], "horizontal": [0.15]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Jackal": {
            "primary1": {"vertical": [7.2], "horizontal": [-0.02]},
            "primary2": {"vertical": [7.2], "horizontal": [-0.02]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Ying": {
            "primary1": {"vertical": [7.8], "horizontal": [-0.02]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Zofia": {
            "primary1": {"vertical": [10.2], "horizontal": [0.03]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Dokkabaei": {
            "primary1": {"vertical": [0.01], "horizontal": [0.01]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [5.7], "horizontal": [-0.02]},
            "secondary2": {"vertical": [4.0], "horizontal": [-0.02]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Lion": {
            "primary1": {"vertical": [7.7], "horizontal": [-0.02]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Finka": {
            "primary1": {"vertical": [3.5], "horizontal": [0.10]},
            "primary2": {"vertical": [7.4], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Mavarick": {
            "primary1": {"vertical": [8.0], "horizontal": [-0.5]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Nomad": {
            "primary1": {"vertical": [5.8], "horizontal": [-0.03]},
            "primary2": {"vertical": [6.0], "horizontal": [-0.08]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Gridlock": {
            "primary1": {"vertical": [6.4], "horizontal": [-0.8]},
            "primary2": {"vertical": [6.7], "horizontal": [0.5]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Nokk": {
            "primary1": {"vertical": [3.65], "horizontal": [0.15]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Amarau": {
            "primary1": {"vertical": [8.0], "horizontal": [-0.03]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [5.0], "horizontal": [0.15]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Kali": {
            "primary1": {"vertical": [0.01], "horizontal": [0.01]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [3.25], "horizontal": [0.15]},
            "secondary2": {"vertical": [4.0], "horizontal": [-0.02]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Ianna": {
            "primary1": {"vertical": [6.0], "horizontal": [-0.8]},
            "primary2": {"vertical": [11.0], "horizontal": [-0.45]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Ace": {
            "primary1": {"vertical": [7.5], "horizontal": [-0.45]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Zero": {
            "primary1": {"vertical": [3.5], "horizontal": [0.25]},
            "primary2": {"vertical": [3.5], "horizontal": [0.025]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Flores": {
            "primary1": {"vertical": [4.75], "horizontal": [0.15]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Osa": {
            "primary1": {"vertical": [5.15], "horizontal": [1.0]},
            "primary2": {"vertical": [7.65], "horizontal": [-0.45]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Sense": {
            "primary1": {"vertical": [7.65], "horizontal": [0.07]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Grim": {
            "primary1": {"vertical": [5.5], "horizontal": [0.07]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Brava": {
            "primary1": {"vertical": [2.5], "horizontal": [-0.35]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Ram": {
            "primary1": {"vertical": [9.0], "horizontal": [0.045]},
            "primary2": {"vertical": [8.0], "horizontal": [-0.02]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Deimos": {
            "primary1": {"vertical": [5.8], "horizontal": [-0.03]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Sentry": {
            "primary1": {"vertical": [3.65], "horizontal": [0.15]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [4.0], "horizontal": [-0.02]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Smoke": {
            "primary1": {"vertical": [3.65], "horizontal": [0.15]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [5.0], "horizontal": [0.15]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Mute": {
            "primary1": {"vertical": [3.35], "horizontal": [0.15]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [5.0], "horizontal": [0.15]}
        },
        "Castle": {
            "primary1": {"vertical": [3.90], "horizontal": [0.10]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Pulse": {
            "primary1": {"vertical": [3.9], "horizontal": [0.1]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Doc": {
            "primary1": {"vertical": [6.95], "horizontal": [0.15]},
            "primary2": {"vertical": [7.45], "horizontal": [0.35]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Rook": {
            "primary1": {"vertical": [6.95], "horizontal": [0.15]},
            "primary2": {"vertical": [7.45], "horizontal": [0.35]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Kapkan": {
            "primary1": {"vertical": [2.85], "horizontal": [0.35]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Techankka": {
            "primary1": {"vertical": [2.85], "horizontal": [0.35]},
            "primary2": {"vertical": [1.5], "horizontal": [0.15]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Jager": {
            "primary1": {"vertical": [4.0], "horizontal": [0.15]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Bandit": {
            "primary1": {"vertical": [3.5], "horizontal": [0.25]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Frost": {
            "primary1": {"vertical": [5.0], "horizontal": [0.15]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Valk": {
            "primary1": {"vertical": [3.0], "horizontal": [0.15]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Caviera": {
            "primary1": {"vertical": [2.0], "horizontal": [0.25]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Echo": {
            "primary1": {"vertical": [2.75], "horizontal": [0.15]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [5.5], "horizontal": [0.15]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Mira": {
            "primary1": {"vertical": [4.25], "horizontal": [0.15]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Lesion": {
            "primary1": {"vertical": [3.5], "horizontal": [0.15]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Ela": {
            "primary1": {"vertical": [4.0], "horizontal": [0.55]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Vigil": {
            "primary1": {"vertical": [3.0], "horizontal": [0.1]},
            "primary2": {"vertical": [98.0], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Maestro": {
            "primary1": {"vertical": [3.0], "horizontal": [0.1]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Alibi": {
            "primary1": {"vertical": [4.35], "horizontal": [0.1]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Clash": {
            "primary1": {"vertical": [0.01], "horizontal": [0.01]},
            "primary2": {"vertical": [3.25], "horizontal": [0.15]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Kaid": {
            "primary1": {"vertical": [3.0], "horizontal": [0.15]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Mozzie": {
"primary1": {"vertical": [3.25], "horizontal": [0.15]},
            "primary2": {"vertical": [2.5], "horizontal": [0.15]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Warden": {
            "primary1": {"vertical": [0.01], "horizontal": [0.01]},
            "primary2": {"vertical": [3.0], "horizontal": [0.15]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Goyo": {
            "primary1": {"vertical": [4.25], "horizontal": [0.15]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Wamai": {
            "primary1": {"vertical": [4.0], "horizontal": [-0.02]},
            "primary2": {"vertical": [3.35], "horizontal": [0.15]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Oryx": {
            "primary1": {"vertical": [0.01], "horizontal": [0.01]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Melusi": {
            "primary1": {"vertical": [6.95], "horizontal": [0.15]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Aruni": {
            "primary1": {"vertical": [3.25], "horizontal": [0.15]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Thunder Bird": {
            "primary1": {"vertical": [3.5], "horizontal": [0.10]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Thorn": {
            "primary1": {"vertical": [3.5], "horizontal": [0.15]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Azami": {
            "primary1": {"vertical": [2.85], "horizontal": [0.35]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Solis": {
            "primary1": {"vertical": [7.45], "horizontal": [0.35]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [5.0], "horizontal": [0.15]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Fenrir": {
            "primary1": {"vertical": [3.5], "horizontal": [0.25]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        },
        "Tubarao": {
            "primary1": {"vertical": [3.0], "horizontal": [0.15]},
            "primary2": {"vertical": [0.01], "horizontal": [0.01]},
            "primary3": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary1": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary2": {"vertical": [0.01], "horizontal": [0.01]},
            "secondary3": {"vertical": [0.01], "horizontal": [0.01]}
        }
    }
    
    current_operator_index = 0
    current_weapon = "primary"
    current_operator = list(operators.keys())[current_operator_index]
    current_primary_weapon = "primary1"
    current_secondary_weapon = "secondary1"
    last_state = False 

    def is_mouse_down():
        lmb_state = win32api.GetKeyState(0x01)
        rmb_state = win32api.GetKeyState(0x02) 
        return lmb_state < 0 and rmb_state < 0  

    def switch_operator():
        nonlocal current_operator, current_primary_weapon, current_secondary_weapon
        selected_operator = operator_selector.get()
        if selected_operator in operators:
            current_operator = selected_operator
            primary_weapon_selector.set("primary1")
            secondary_weapon_selector.set("secondary1")
            weapon_selector.config(text=f"Primary Weapon: {current_operator}")

    def switch_weapon(weapon_type):
        nonlocal current_weapon, current_primary_weapon, current_secondary_weapon
        if weapon_type == 'primary':
            current_weapon = primary_weapon_selector.get()
            weapon_selector.config(text=f"Primary Weapon: {current_operator} - {current_weapon}")
        elif weapon_type == 'secondary':
            current_weapon = secondary_weapon_selector.get()
            weapon_selector.config(text=f"Secondary Weapon: {current_operator} - {current_weapon}")

    def update_configuration():
        global base_vertical_sensitivity, base_horizontal_sensitivity, base_dpi
        base_vertical_sensitivity = float(current_vertical_sensitivity_entry.get())
        base_horizontal_sensitivity = float(current_horizontal_sensitivity_entry.get())
        base_dpi = float(current_dpi_entry.get())
        toggle_button = toggle_button_entry.get()

        current_vertical_sensitivity_entry.delete(0, tk.END)
        current_vertical_sensitivity_entry.insert(0, str(base_vertical_sensitivity))

        current_horizontal_sensitivity_entry.delete(0, tk.END)
        current_horizontal_sensitivity_entry.insert(0, str(base_horizontal_sensitivity))

        current_dpi_entry.delete(0, tk.END)
        current_dpi_entry.insert(0, str(base_dpi))

    def anti_recoil_step():
        nonlocal enabled, current_operator, last_state

        key_down_toggle = keyboard.is_pressed(toggle_button)
        key_down_switch_1 = keyboard.is_pressed('1')
        key_down_switch_2 = keyboard.is_pressed('2')

        if key_down_toggle != last_state:
            last_state = key_down_toggle
            if last_state:
                enabled = not enabled
                if enabled:
                    print("Anti-recoil ENABLED")
                else:
                    print("Anti-recoil DISABLED")

        if enabled and is_mouse_down():
            current_operator_info = operators[current_operator]
            recoil_values = current_operator_info[current_weapon]
            rapid_fire = recoil_values.get("rapid_fire", False)

            if rapid_fire:
                mouseloc = pui.position()
                pui.click(mouseloc)
            else:
                vertical_distances = recoil_values["vertical"]
                horizontal_distances = recoil_values["horizontal"]
                vertical_distance = random.choice(vertical_distances)
                horizontal_distance = random.choice(horizontal_distances)

                adjusted_vertical_distance = int(vertical_distance * (dpi_scaling_factor * base_dpi / 1600) * (base_vertical_sensitivity / 30))
                adjusted_horizontal_distance = int(horizontal_distance * (dpi_scaling_factor * base_dpi / 1600) * (base_horizontal_sensitivity / 30))

                sensitivity_difference = base_vertical_sensitivity - float(current_vertical_sensitivity_entry.get())
                dpi_difference = base_dpi - float(current_dpi_entry.get())

                if sensitivity_difference > 0 and dpi_difference > 0:
                    adjusted_vertical_distance += abs(sensitivity_difference) * dpi_difference
                    adjusted_horizontal_distance += abs(sensitivity_difference) * dpi_difference
                elif sensitivity_difference < 0 and dpi_difference < 0:
                    adjusted_vertical_distance -= abs(sensitivity_difference) * dpi_difference
                    adjusted_horizontal_distance -= abs(sensitivity_difference) * dpi_difference

                win32api.mouse_event(0x0001, adjusted_horizontal_distance, adjusted_vertical_distance)

        if key_down_switch_1:
            switch_weapon('primary')

        if key_down_switch_2:
            switch_weapon('secondary')

        root.after(10, anti_recoil_step)

    root = tk.Tk()
    root.title("Operator Selector")
    root.configure(bg='black')

    root.overrideredirect(True)

    window_width = 500
    window_height = 500

    position_right = int((screenWidth - window_width) / 2)
    position_down = int((screenHeight - window_height) / 2)

    root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")

    style = ThemedStyle(root)
    style.set_theme("black")
    style.configure('TButton', font=('Helvetica', 10), borderwidth=0, relief="flat", background='black', foreground='white', padding=5)
    style.configure('TLabel', font=('Helvetica', 10), background='black', foreground='white')
    style.configure('TCombobox', font=('Helvetica', 10), background='black', foreground='white', fieldbackground='black', borderwidth=0)
    style.configure('TEntry', font=('Helvetica', 10), background='black', foreground='white', fieldbackground='black', borderwidth=0)

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    operator_tab = ttk.Frame(notebook)
    config_tab = ttk.Frame(notebook)

    notebook.add(operator_tab, text="Operator")
    notebook.add(config_tab, text="Configuration")

    operator_label = ttk.Label(operator_tab, text="Select Operator:")
    operator_label.grid(row=0, column=0, padx=5, pady=5)

    operator_selector = ttk.Combobox(operator_tab, values=list(operators.keys()))
    operator_selector.grid(row=0, column=1, padx=5, pady=5)

    switch_operator_button = ttk.Button(operator_tab, text="Choose Operator", command=switch_operator)
    switch_operator_button.grid(row=0, column=2, padx=5, pady=5)

    weapon_label = ttk.Label(operator_tab, text="Select Weapon:")
    weapon_label.grid(row=1, column=0, padx=5, pady=5)

    primary_weapon_selector = ttk.Combobox(operator_tab, values=["primary1", "primary2", "primary3"])
    primary_weapon_selector.grid(row=1, column=1, padx=5, pady=5)
    primary_weapon_selector.bind("<<ComboboxSelected>>", lambda event: switch_weapon('primary'))

    secondary_weapon_selector = ttk.Combobox(operator_tab, values=["secondary1", "secondary2", "secondary3"])
    secondary_weapon_selector.grid(row=1, column=2, padx=5, pady=5)
    secondary_weapon_selector.bind("<<ComboboxSelected>>", lambda event: switch_weapon('secondary'))

    weapon_selector = ttk.Label(operator_tab, text="Primary Weapon: Sledge")
    weapon_selector.grid(row=2, column=1, padx=5, pady=5)

    config_label = ttk.Label(config_tab, text="Configuration:")
    config_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

    current_vertical_sensitivity_label = ttk.Label(config_tab, text="Vertical offset:")
    current_vertical_sensitivity_label.grid(row=1, column=0, padx=5, pady=5)
    current_vertical_sensitivity_entry = ttk.Entry(config_tab)
    current_vertical_sensitivity_entry.insert(0, str(base_vertical_sensitivity))
    current_vertical_sensitivity_entry.grid(row=1, column=1, padx=5, pady=5)
    current_vertical_sensitivity_entry.bind("<FocusOut>", lambda event: update_configuration())

    current_horizontal_sensitivity_label = ttk.Label(config_tab, text="Horizontal offset:")
    current_horizontal_sensitivity_label.grid(row=2, column=0, padx=5, pady=5)
    current_horizontal_sensitivity_entry = ttk.Entry(config_tab)
    current_horizontal_sensitivity_entry.insert(0, str(base_horizontal_sensitivity))
    current_horizontal_sensitivity_entry.grid(row=2, column=1, padx=5, pady=5)
    current_horizontal_sensitivity_entry.bind("<FocusOut>", lambda event: update_configuration())

    current_dpi_label = ttk.Label(config_tab, text="DPI:")
    current_dpi_label.grid(row=3, column=0, padx=5, pady=5)
    current_dpi_entry = ttk.Entry(config_tab)
    current_dpi_entry.insert(0, str(base_dpi))
    current_dpi_entry.grid(row=3, column=1, padx=5, pady=5)
    current_dpi_entry.bind("<FocusOut>", lambda event: update_configuration())

    toggle_button_label = ttk.Label(config_tab, text="Toggle button:")
    toggle_button_label.grid(row=4, column=0, padx=5, pady=5)
    toggle_button_entry = ttk.Entry(config_tab)
    toggle_button_entry.insert(0, toggle_button)
    toggle_button_entry.grid(row=4, column=1, padx=5, pady=5)
    toggle_button_entry.bind("<FocusOut>", lambda event: update_configuration())

    def start_drag(event):
        root.x = event.x
        root.y = event.y

    def do_drag(event):
        x = root.winfo_pointerx() - root.x
        y = root.winfo_pointery() - root.y
        root.geometry(f"+{x}+{y}")

    root.bind("<ButtonPress-1>", start_drag)
    root.bind("<B1-Motion>", do_drag)

    root.after(10, anti_recoil_step)
    
    auth_root.destroy()

    root.mainloop()

auth_root = tk.Tk()
auth_root.title("Authentication")
auth_root.configure(background="black")

screen_width = auth_root.winfo_screenwidth()
screen_height = auth_root.winfo_screenheight()

window_width = 300
window_height = 150

x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)

auth_root.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')

auth_root.overrideredirect(True)

label = tk.Label(auth_root, text="Enter 20-digit key:", fg="white", bg="black")
label.pack(pady=10)

entry = tk.Entry(auth_root, width=30)
entry.pack()

status_label = tk.Label(auth_root, text="", bg="black", fg="white")
status_label.pack()

def authenticate_and_execute():
    key = entry.get()
    if authenticate(key):
        execute_code()
        status_label.config(text="Authentication successful", fg="green")
    else:
        status_label.config(text="Authentication failed", fg="red")

button = tk.Button(auth_root, text="Authenticate", command=authenticate_and_execute)
button.pack(pady=10)

auth_root.mainloop()