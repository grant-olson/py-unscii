#include "oled_text.h"

void setup() {
  // put your setup code here, to run once:

  // Setup OLED drivers
  oled_initialization_sequence();
  oled_clear();
}

void loop() {
  oled_send_command(OLED_OUTPUT_RAM);

  oled_set_page(0);
  oled_set_column(0);
  oled_print_you_died();
  
  oled_set_page(1);
  oled_set_column(0);
  oled_print_play_again();
  
  oled_set_page(2);
  oled_set_column(0);
  oled_print_no();

  oled_set_page(3);
  oled_set_column(0);
  oled_print_ten();

  delay(1000);
  oled_set_column(0);
  oled_print_nine();

  delay(1000);
  oled_set_column(0);
  oled_print_eight();

  delay(1000);
  oled_set_column(0);
  oled_print_seven();

  delay(1000);
  oled_set_column(0);
  oled_print_six();

  delay(1000);
  oled_set_column(0);
  oled_print_five();

  delay(1000);
  oled_set_column(0);
  oled_print_four();

  delay(1000);
  oled_set_column(0);
  oled_print_three();

  delay(1000);
  oled_set_column(0);
  oled_print_two();

  delay(1000);
  oled_set_column(0);
  oled_print_one();

  delay(1000);
  oled_clear();
  oled_set_page(2);
  oled_set_column(0);
  oled_print_game_over();

  delay(5000);
}
