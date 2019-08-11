# UNSCII for Python

This provides a wrapper around the collection of bitmapped fonts known
as [UNSCII](http://pelulamu.net/unscii/).

The original motivation was to create a lightweight way to get text on to small
displays such as OLEDs and LCD Screens that may be attached to devices such as
a Raspberry Pi or Arduino. There are other libraries out there that do this, but
most push the work to Pillow by providing it with .ttf fonts. I wanted a more
lightweight way to quickly get text on to the screens without using so many
resources, particularly on an Arduino.


## Arduino Resource Generator

One problem with OLED displays on the Arduino is that they take up
significant space in flash memory. Unscii includes a command line
utility that generates bare bones files to allow you to use the OLED
with minimal flash consumption.

See the arduino_example directory for an example. It contains a normal
project file, and a `oled_text.yaml` file which contains the text
resources to display. To complie the .yaml file into files for the
Arduino project, run:

```
bin/unscii-compile-resource arduino_example/oled_text.yaml
```

This will create a .h and .cpp file for use in your main project
file. The file
[arduino_example/arduino_example.ino](../arduino_example/arduino_example.ino)
shows an example of barebones setup for general usage.

Future versions will include a slimmed down codebase for CircuitPython
as well, where memory constraints are even more important.
