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

cpp_header_file = """
#ifndef OLED_CONTROL
#define OLED_CONTROL

#include <Arduino.h>

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
const byte OLED_ENABLE_BYTEGE_PUMP_REGULATOR = 0x8D;
const byte OLED_DISPLAY_ON = 0xAF;
const byte OLED_SET_MEMORY_ADDRESSING_MODE = 0x20;
const byte OLED_OUTPUT_RAM = 0xA4;

void oled_send_command(byte cmd);
void oled_send_data(byte data);
void oled_initialization_sequence();
void oled_set_page(byte page);
void oled_set_column(byte column);
void oled_clear();

"""

cpp_file = """
#include <Wire.h>

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
   
  OLED_ENABLE_BYTEGE_PUMP_REGULATOR, 0x14,
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
  Wire.begin();

  for(int i=0;i<sizeof(oled_init_sequence);i++) {
    oled_send_command(oled_init_sequence[i]);
  }  
}

void oled_set_page(byte page) {
  oled_send_command(0xB0 | page);
}

void oled_set_column(byte column) {
  byte high_nibble = (column & 0xF0) >> 4;
  byte low_nibble = column & 0x0F;


  oled_send_command(low_nibble);
  oled_send_command(high_nibble | 0x10);
}

void oled_print_resource(const byte data[], int size) {
  for(int i=0;i<size;i++) {
    oled_send_data(data[i]);
  };
}

void oled_clear() {
  for(int i=0;i<8;i++) {
    oled_set_page(i);
    oled_set_column(0);
    for(int j=0;j<128;j++) {
      oled_send_data(0x0);
    };
  };
}

"""

class ResourceGenerator(object):
    def __init__(self, font_name):
        self.font = unscii(font_name)

    def cpp_header_intro(self):
        return cpp_header_file

    def cpp_intro(self):
        return cpp_file
    
    def cpp_resource_string(self, resource_name, resource_text, line_size=None):
        resource_declaration = "const byte %s[] = { \n" % resource_name
        for c in resource_text:
            for b in self.font.get_char(c):
                resource_declaration += "0x%02X, " % b
            resource_declaration += "// '%s'\n" % c
        resource_declaration += "};\n"
        
        return resource_declaration

    def cpp_resource_helper(self, resource_name, header=True):
        signature = "void oled_print_%s()" % resource_name.lower()
        if header:
            return signature + ";\n"
        else:
            function = signature + " {\n"
            function += "    oled_print_resource(%s,sizeof(%s));\n}\n" % (resource_name, resource_name)
            return function
                
    def cpp_resources(self, resource_name, resource_text):
        resources = {}
        resources["string"] = self.cpp_resource_string(resource_name, resource_text)
        resources["helper_declaration"] = self.cpp_resource_helper(resource_name)
        resources["helper_function"] = self.cpp_resource_helper(resource_name, header=False)
        return resources
