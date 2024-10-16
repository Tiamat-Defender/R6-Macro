import tkinter as tk
from tkinter import ttk
import requests
import win32api
import keyboard
import pyautogui as pui
from ttkthemes import ThemedStyle
from dict import operators
import random
import subprocess


#base variables needed
SERVER_URL = 'http://127.0.0.1'

screenWidth, screenHeight = pui.size()

base_vertical_sensitivity = 30
base_horizontal_sensitivity = 30
base_dpi = 1600

root = None

def clean_hw_id(raw_hwid):
    #format HWID
    lines = raw_hwid.strip().splitlines()
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    return cleaned_lines[-1] if cleaned_lines else None

def GetHWID():
    try:
        # Try to get bios serial number
        output = subprocess.check_output('wmic bios get serialnumber', shell=True, text=True)
        hwid = clean_hw_id(output)

        # If BIOS serial number is not found find motherboard serial number
        if hwid is None or hwid == "SerialNumber":
            output = subprocess.check_output('wmic baseboard get serialnumber', shell=True, text=True)
            hwid = clean_hw_id(output)
        
        return hwid.upper() if hwid else None  # Return uppercase HWID or None if invalid
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving HWID: {e}")
        return None

def authenticate(key):
    hwid = GetHWID()
    if hwid is None:
        print("Failed to retrieve HWID. Exiting...")
        return False

    print(f'Authenticating with key: {key} and HWID: {hwid}')  # Correct format for this is key,hwid

    authkey_url = f'{SERVER_URL}/authkey'
    params = {'key': key, 'hwid': hwid}
    
    #if status code equals 200 then success else dont execute code
    try:
        response = requests.get(authkey_url, params=params)
        if response.status_code == 200:
            print('Customer key validated successfully')
            return True
        else:
            print(f'Customer key validation failed with status code {response.status_code}: {response.json().get("error")}')
            return False
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return False
    
def execute_code():
    global root  

    primary = "primary"
    secondary = "secondary"
    
    #movement delay will be different on each gun
    movement_delay = 0.03

    toggle_button = '5' 

    #must stay enabled or shit will be fucked
    enabled = True

    #simple and explains itself
    current_operator_index = 0
    current_weapon = "primary"
    current_operator = list(operators.keys())[current_operator_index]
    current_primary_weapon = "primary1"
    current_secondary_weapon = "secondary1"
    last_state = False 

    #will return true if shooting
    def is_mouse_down():
        lmb_state = win32api.GetKeyState(0x01)
        rmb_state = win32api.GetKeyState(0x02) 
        return lmb_state < 0 and rmb_state < 0  

    #switches dictonary element
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

    #note:Delete anything having to do with dpi as its useless
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
            
            movement_delay = operators[current_operator][current_weapon]["FireRate"]

            if rapid_fire:
                mouseloc = pui.position()
                pui.click(mouseloc)
            
            vertical_distances = recoil_values["vertical"]
            horizontal_distances = recoil_values["horizontal"]
            vertical_distance = random.choice(vertical_distances)
            horizontal_distance = random.choice(horizontal_distances)

            win32api.mouse_event(0x0001, int(horizontal_distance + base_horizontal_sensitivity), int(vertical_distance + base_vertical_sensitivity))

        if key_down_switch_1:
            switch_weapon('primary')

        if key_down_switch_2:
            switch_weapon('secondary')

        root.after(10, anti_recoil_step)

    #all things having to do with gui
    root = tk.Tk()
    root.title("Operator Selector")
    root.configure(bg='black')

    root.overrideredirect(True)

    window_width = 500
    window_height = 300

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