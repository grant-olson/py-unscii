# UNSCII for Python

This provides a wrapper around the collection of bitmapped fonts known
as [UNSCII](http://pelulamu.net/unscii/).

The original motivation was to create a lightweight way to get text on to small
displays such as OLEDs and LCD Screens that may be attached to devices such as
a Raspberry Pi or Arduino. There are other libraries out there that do this, but
most push the work to Pillow by providing it with .ttf fonts. I wanted a more
lightweight way to quickly get text on to the screens without using so many
resources, particularly on an Arduino.

Future versions will have a command line utility to generate the minimum amount
of code to get strings for python and C++ to make this more useful with C++
and CircuitPython embedded stacks.
