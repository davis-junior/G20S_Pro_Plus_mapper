# G20S_Pro_Plus_mapper
Maps G20S Pro Plus OK button to Enter key via HID event monitoring.

## Description
This program corrects a problem with the G20S Pro Plus remote where the OK button does not work in Windows.
No virtual key code or scan code is emitted (or at least recognized by Windows), so this program connects to
the USB HID device and watches for the event emitted when the OK button is pressed, and then the Enter key
is sent.

Simple exception handling is built in to avoid exceptions not anticipated or possible exceptions
from device disconnect/connect. The program runs in an infinite loop.

Requires: hidapi and pynput
