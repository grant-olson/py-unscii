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

cpp_driver_code = """
#include <Wire.h>

const byte OLED_DISPLAY_ADDRESS = 0x3C;

const byte OLED_COMMAND = 0x00;
const byte OLED_DATA = 0x40;

const byte OLED_SET_MUX_RATIO = 0xA8;
const byte OLED_SET_DISPLAY_OFFSET = 0xD3;
const byte OLED_SET_DISPLAY_START_LINE = 0x40;
const byte OLED_SET_SEGMENT_REMAP_0 = 0xA0;
const byte OLED_SET_COM_OUTPUT_SCAN_DIRECTION_INCREMENT = 0xC0;
const byte OLED_SET_COM_PINS = 0xDA;
const byte OLED_SET_CONTRAST = 0x81;
const byte OLED_ENTIRE_DISPLAY_ON = 0xA5;
const byte OLED_NORMAL_DISPLAY = 0xA6;
const byte OLED_ENABLE_CHARGE_PUMP_REGULATOR = 0x8D;
const byte OLED_DISPLAY_ON = 0xAF;
const byte OLED_SET_MEMORY_ADDRESSING_MODE = 0x20;
const byte OLED_OUTPUT_RAM = 0xA4;

  const byte oled_init_sequence[] = {  
  OLED_SET_MUX_RATIO, 0x3f,
  OLED_SET_DISPLAY_OFFSET, 0x00,
  OLED_SET_DISPLAY_START_LINE,
  OLED_SET_SEGMENT_REMAP_0,
  OLED_SET_COM_OUTPUT_SCAN_DIRECTION_INCREMENT,
  OLED_SET_COM_PINS, 0x02,
  OLED_SET_CONTRAST, 0x7f,
  OLED_ENTIRE_DISPLAY_ON,
  OLED_OUTPUT_RAM,
  OLED_NORMAL_DISPLAY,
   
  OLED_ENABLE_CHARGE_PUMP_REGULATOR, 0x14,
  OLED_DISPLAY_ON,
  OLED_SET_MEMORY_ADDRESSING_MODE, 0x02
};

void oled_send_command(byte cmd) {
  Wire.beginTransmission(OLED_DISPLAY_ADDRESS);
  Wire.write(OLED_COMMAND);
  Wire.write(cmd);
  Wire.endTransmission();
}
void oled_send_data(byte data) {
  Wire.beginTransmission(OLED_DISPLAY_ADDRESS);
  Wire.write(OLED_DATA);
  Wire.write(data);
  Wire.endTransmission();

}


void oled_initialization_sequence() {
  for(int i=0;i<sizeof(oled_init_sequence);i++) {
    oled_send_command(oled_init_sequence[i]);
  }  
}
"""

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
