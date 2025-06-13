import serial
import pygame
import time
from orchestra_ui import OrchestraUI  # Import your UI class
# Set serial port
ser = serial.Serial('COM5', 9600)
pygame.mixer.init()
ui = OrchestraUI()

current_sounds = {
    "LEFT": None,
    "RIGHT": None, 
    "UP": None,
    "DOWN": None
}
# Load sounds
sounds = {
    "LEFT": {
        "slow": pygame.mixer.Sound("data/string_slow.mp3"),
        "normal": pygame.mixer.Sound("data/string.mp3"),
        "fast": pygame.mixer.Sound("data/string_fast.mp3")
    },
    "RIGHT": {
        "slow": pygame.mixer.Sound("data/woodwind_slow.mp3"),
        "normal": pygame.mixer.Sound("data/woodwind.mp3"),
        "fast": pygame.mixer.Sound("data/woodwind_fast.mp3")
    },
    "UP": {
        "slow": pygame.mixer.Sound("data/brass_slow.mp3"),
        "normal": pygame.mixer.Sound("data/brass.mp3"),
        "fast": pygame.mixer.Sound("data/brass_fast.mp3")
    },
    "DOWN": {
        "slow": pygame.mixer.Sound("data/percussion_slow.mp3"),
        "normal": pygame.mixer.Sound("data/percussion.mp3"),
        "fast": pygame.mixer.Sound("data/percussion_fast.mp3")
    }
}

# Global tempo state
current_tempo = "normal"

print("Listening for gestures...")
print("LEFT/RIGHT/UP/DOWN = Orchestra sections")
print("FORWARD = Speed up | BACKWARD = Slow down")
print("Double UP/DOWN = Reset to normal tempo")

def stop_all_sounds():

    pygame.mixer.stop()
    for key in current_sounds:
        current_sounds[key] = None
        ui.update_section_status(key, False)  # Update UI

def change_tempo(new_tempo):
    global current_tempo
    old_tempo = current_tempo
    current_tempo = new_tempo
    
    # Update UI
    ui.update_tempo(current_tempo)
    
    tempo_names = {
        "slow": "SLOW",
        "normal": "NORMAL", 
        "fast": "FAST"
    }
    
    print(f"Tempo changed: {tempo_names[current_tempo]}")
    
    #  currently playing
    playing_sections = []
    for key, sound_obj in current_sounds.items():
        if sound_obj is not None and sound_obj.get_busy():
            playing_sections.append(key)
    
    stop_all_sounds()
    
    # Restart the playing sections with new tempo
    for section in playing_sections:
        start_section(section)

def start_section(gesture_key):
    section_names = {
        "LEFT": "STRINGS",
        "RIGHT": "WOODWINDS", 
        "UP": "BRASS",
        "DOWN": "PERCUSSION"
    }
    
    channel = sounds[gesture_key][current_tempo].play(loops=-1)
    current_sounds[gesture_key] = channel
    ui.update_section_status(gesture_key, True) 
    print(f"♪ Now playing: {section_names[gesture_key]} at {current_tempo.upper()} tempo ♪")

def toggle_section(gesture_key):
    section_names = {
        "LEFT": "STRINGS",
        "RIGHT": "WOODWINDS", 
        "UP": "BRASS",
        "DOWN": "PERCUSSION"
    }
    
    # Check if section is currently playing
    if current_sounds[gesture_key] is not None and current_sounds[gesture_key].get_busy():
        # Section is playing - stop it
        current_sounds[gesture_key].stop()
        current_sounds[gesture_key] = None
        ui.update_section_status(gesture_key, False)  # Update UI
        print(f"Stopped: {section_names[gesture_key]}")
    else:
        # Section is not playing - start it at current tempo
        start_section(gesture_key)

try:
    running = True
    while running:
        # Handle UI events 
        running = ui.handle_events()
        
        # Check for serial data
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            print(f"Raw received: '{line}'")
            
            line_upper = line.upper()
            print(f"Processed: '{line_upper}'")
            
            # Check for tempo control gestures
            if "FORWARD" in line_upper or "NEAR" in line_upper:
                print("Detected FORWARD gesture")
                if current_tempo == "slow":
                    change_tempo("normal")
                elif current_tempo == "normal":
                    change_tempo("fast")
                else:
                    print("Already at maximum speed!")
                    
            elif "BACKWARD" in line_upper or "BACK" in line_upper:
                print("Detected BACKWARD gesture")
                if current_tempo == "fast":
                    change_tempo("normal")
                elif current_tempo == "normal":
                    change_tempo("slow")
                else:
                    print("Already at minimum speed!")
                    
            elif "CLOCKWISE" in line_upper:
                print("Detected reset gesture")
                change_tempo("normal")
                
            else:
                # Match gesture keywords and toggle corresponding section
                gesture_found = False
                for key in sounds:
                    if key in line_upper:
                        print(f"Detected {key} gesture")
                        toggle_section(key)
                        gesture_found = True
                        break
                
                if not gesture_found:
                    print(f"Unknown gesture: '{line}'")
        
        # Update the display
        ui.update_display()
        
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\nThank you for conducting the Concert!")
    stop_all_sounds()
    ser.close()
    ui.close()

except Exception as e:
    print(f"Error: {e}")
    stop_all_sounds()
    ser.close()
    ui.close()
