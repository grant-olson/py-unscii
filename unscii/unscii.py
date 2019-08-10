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
        self.name = font_name

    def get_char(self, char):
        return self.raw_data[ord(char)] # Is this right for unicode?

    def size(self):
        return len(self.get_char("A")) / 8

    def transposed(self):
        return "_transposed" in self.name
    
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

class ResourceGenerator(object):
    def __init__(self, font_name):
        self.font = unscii(font_name)

    def cpp_resource_string(self, resource_name, resource_text, line_size=None):
        resource_declaration = "const byte %s[] = { \n" % resource_name
        for c in resource_text:
            for b in self.font.get_char(c):
                resource_declaration += "0x%2X, " % b
            resource_declaration += "// '%s'\n" % c
        resource_declaration += "};\n"
        
        return resource_declaration
