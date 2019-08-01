import importlib
import raw_unscii
import glob

cached_fonts = {}

class UnsciiFont(object):
    def __init__(self, font_name):
        if font_name not in cached_fonts:
            print("LAZY LOADING FONT")
            importlib.import_module("unscii.raw_unscii.%s" % font_name, "unscii")
            print(repr(dir(globals()['raw_unscii'])))
            module = getattr(globals()['raw_unscii'], font_name)
            cached_fonts[font_name] = getattr(module, "%s_bytes" % font_name)
        self.raw_data = cached_fonts[font_name]

    def get_char(self, char):
        return self.raw_data(ord(char)) # Is this right for unicode?
        
def unscii(font_name):
    return UnsciiFont(font_name)
