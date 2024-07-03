#!/bin/python3
import evdev
from evdev import InputDevice, ecodes, UInput
import time
import threading

device = InputDevice('/dev/input/event5')

caps = {
    ecodes.EV_KEY: [ecodes.BTN_RIGHT]
}


ui = UInput(caps)

BUTTON_CODE = ecodes.BTN_SIDE  # Replace with the actual code for your extra button
RIGHT_CLICK_CODE = ecodes.BTN_RIGHT
runThread = 0



# def right_click():
#     ui.write(ecodes.EV_KEY, ecodes.BTN_RIGHT, 1)
#     ui.write(ecodes.EV_KEY, ecodes.BTN_RIGHT, 0)
#     ui.syn()


def right_click():
    # print("Sending right click")
    ui.write(ecodes.EV_KEY, RIGHT_CLICK_CODE, 1)
    ui.write(ecodes.EV_SYN, ecodes.SYN_REPORT, 0)  # Ensure event synchronization
    print("press func")
    time.sleep(0.1)  # Small delay to simulate click duration
    ui.write(ecodes.EV_KEY, RIGHT_CLICK_CODE, 0)
    ui.write(ecodes.EV_SYN, ecodes.SYN_REPORT, 0)  # Ensure event synchronization
    print("release func")
    # time.sleep(0.01)



def test():
    global runThread
    while True:
        if runThread == 1:
            right_click()
            time.sleep(0.001)
        elif runThread == 2:
            while True:
                if runThread == 1:
                    break
                elif runThread == 3:
                    return
                    

thread = threading.Thread(target=test).start()


try:
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY and event.code == BUTTON_CODE:
            if event.value == 1:
                # print("button pressed")
                runThread = 1
            elif event.value == 0:
                # print("button released")
                runThread = 2
except KeyboardInterrupt:
    print("Exiting!")
    runThread = 3
    ui.close()
    exit(0)
finally:
    ui.close()
