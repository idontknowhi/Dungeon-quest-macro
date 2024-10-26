import keyboard
import time
import threading as th

def get_ping():
    while True:
        user_input = input("Enter ping: ")
        try:
            ping_value = float(user_input)
            current_ping = ping_value / 1000
            print("Ping added.")
            return current_ping
        except ValueError:
            print("Invalid number, try again.")

def update_ping():
    global user_ping, delay_time, auto_heal_time, ability_cooldown_time
    new_ping = get_ping()
    user_ping = new_ping
    delay_time = user_ping + 5.9
    auto_heal_time = 3.6 + user_ping
    ability_cooldown_time = 3.6 + user_ping
    print(f"Updated ping to {new_ping * 1000:.0f} ms.")
    print(f"Updated delay time: {delay_time:.4f}, Auto heal time: {auto_heal_time:.4f}, Ability cooldown time: {ability_cooldown_time:.4f}")


user_ping = get_ping()


delay_time = user_ping + 5.9
toggle_chat_key = "c+v"
auto_heal_time = 3.6 + user_ping
ability_cooldown_time = 3.6 + user_ping
auto_heal_key = "alt+h"

healing_active = False
chat_mode_active = False
holding_e = False

def toggle_e_key():
    global holding_e
    if not chat_mode_active:
        holding_e = not holding_e
        if holding_e:
            print("Holding 'E'")
            while holding_e:
                if not chat_mode_active:
                    keyboard.press('e')
                time.sleep(0.05)
                if keyboard.is_pressed('q'):
                    stop_e_key()
                    break
                if keyboard.is_pressed('l'):
                    release_e_key()
                    break
                if keyboard.is_pressed(toggle_chat_key):
                    release_e_key()
                    break
    else:
        print("Chat mode. Press to exit.")

def stop_e_key():
    global holding_e
    print(f"Stopping 'E' for {delay_time:.4f} seconds")
    holding_e = False
    keyboard.release('e')
    time.sleep(delay_time)
    print("Using ability again.")
    toggle_e_key()

def release_e_key():
    global holding_e
    print("Stopping 'E'.")
    holding_e = False
    keyboard.release('e')

def toggle_chat_mode():
    global chat_mode_active
    chat_mode_active = not chat_mode_active
    if chat_mode_active:
        print("Chat mode activated.")
        release_e_key()
        time.sleep(1)
    else:
        print("Back to normal.")

def auto_heal():
    global healing_active
    healing_active = True
    print("Auto healing activated.")
    while healing_active:
        keyboard.press_and_release("e")
        time.sleep(auto_heal_time)
        if chat_mode_active:
            break
        keyboard.press_and_release("q")
        time.sleep(ability_cooldown_time)
    print("Auto healing deactivated.")

def start_healing():
    global healing_active
    if not healing_active:
        th.Thread(target=auto_heal, daemon=True).start()

def stop_healing():
    global healing_active
    healing_active = False


keyboard.add_hotkey('e', toggle_e_key)
keyboard.add_hotkey('q', stop_e_key)
keyboard.add_hotkey('l', release_e_key)
keyboard.add_hotkey(toggle_chat_key, toggle_chat_mode)
keyboard.add_hotkey(auto_heal_key, start_healing)
keyboard.add_hotkey('alt+s', stop_healing)
keyboard.add_hotkey('alt+p', update_ping)


print("Press 'E' to hold 'E'")
print(f"Press 'Q' to stop for {delay_time:.4f} seconds")
print("Press 'L' to stop holding 'E'")
print(f"Press {auto_heal_key} to auto heal (Alt+H) {3.6 + user_ping:.4f} seconds between using abilities")
print("Press Alt+S to stop healing.")
print(f"Press {toggle_chat_key} to pause everything.")
print("Press Alt+P to change ping YOU HAVE TO PAUSE EVERYTHING IF ANYTHING IS ALREADY ACTIVE.")


while True:
    if chat_mode_active:
        holding_e = False
    time.sleep(0.05)
