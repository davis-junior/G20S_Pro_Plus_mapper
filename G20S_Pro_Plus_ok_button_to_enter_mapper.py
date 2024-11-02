"""
This program corrects a problem with the G20S Pro Plus remote where the OK button does not work in Windows.
No virtual key code or scan code is emitted (or at least recognized by Windows), so this program connects to
the USB HID device and watches for the event emitted when the OK button is pressed, and then the Enter key
is sent.

Simple exception handling is built in to avoid exceptions not anticipated or possible exceptions
from device disconnect/connect. The program runs in an infinite loop.

Requires: hidapi and pynput

Author: David Kornacki (davis_junior)
Data written: 2024-11-2
Version: 0.1
"""

import time
import traceback

import hid
from pynput.keyboard import Key, Controller


# G20S Pro Plus
HID_DEVICE_VENDOR_ID = 0x4842
PRODUCT_ID = 0x1
USAGE = 0x1
OK_BUTTON_PRESSED_DATA = [3, 65, 0]
ANY_BUTTON_RELEASED_DATA = [3, 0, 0]


def main():
    keyboard = Controller()

    while True:
        try:
            device = connect_to_device(HID_DEVICE_VENDOR_ID, PRODUCT_ID, USAGE)
            if device:
                while True:
                    try:
                        wait_for_event_and_send_key(
                            device,
                            keyboard,
                            OK_BUTTON_PRESSED_DATA,
                            ANY_BUTTON_RELEASED_DATA,
                        )
                    except:
                        traceback.print_exc()
                        time.sleep(2)
                        break

                device.close()
        except:
            traceback.print_exc()
            time.sleep(2)


def connect_to_device(vendor_id, product_id, usage):
    device = None

    device_info = hid.enumerate(vendor_id=vendor_id, product_id=product_id)
    for info in device_info:
        if info["usage"] == usage:

            print("Connecting to device:")
            print(info)
            device = hid.device()
            device.open_path(info["path"])

    return device


def wait_for_event_and_send_key(
    device, keyboard, ok_button_pressed_data, any_button_released_data
):
    # read up to 64 bytes of data
    data = device.read(64)

    if data:
        # process HID event
        print(data)  # log all data read
        if len(data) >= 3:
            if data == ok_button_pressed_data:
                print("OK button pressed. Pressing enter key...")
                keyboard.press(Key.enter)

                key_released = False
                start_time = time.time()

                # wait up to around 10 seconds for release, otherwise force release
                while time.time() - start_time <= 10:
                    data = device.read(64, timeout_ms=1000)
                    if data:
                        print(data)  # log all data read
                        if len(data) >= 3:
                            if data == any_button_released_data:
                                print("Button released. Releasing enter key...")
                                keyboard.release(Key.enter)
                                key_released = True
                                break

                if not key_released:
                    # ensure at least some time has passed
                    if time.time() - start_time <= 1:
                        time.sleep(0.05)

                    print("Likely 10 seconds has past, so force releasing enter key...")
                    keyboard.release(Key.enter)


if __name__ == "__main__":
    main()
