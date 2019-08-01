import importlib
from . import raw_unscii
import glob

cached_fonts = {}

class UnsciiFont(object):
    def __init__(self, font_name):
        if font_name not in cached_fonts:
            importlib.import_module("unscii.raw_unscii.%s" % font_name, "unscii")
            module = getattr(globals()['raw_unscii'], font_name)
            cached_fonts[font_name] = getattr(module, "%s_bytes" % font_name)
        self.raw_data = cached_fonts[font_name]

    def get_char(self, char):
        return self.raw_data[ord(char)] # Is this right for unicode?
        
def unscii(font_name):
    """
    Given a font name, return a font object for usage.
    """
    return UnsciiFont(font_name)

def fonts():
    """
    Provide list of installed unscii fonts that can be used.
    """
    return raw_unscii.raw_unscii_modules
