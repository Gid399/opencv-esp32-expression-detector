#include <LiquidCrystal.h>

//Define LCD pins
// LCD pins: RS, E, D4, D5, D6, D7
LiquidCrystal lcd(27, 26, 33, 32, 25, 13);

//Declare a string variable that will hold the received message
String receivedMessage = "";

//Create a function for dispalying the received message from python
void displayExpression(String expression) {
  lcd.setCursor(0, 1);

  // Clear the previous message on row 2
  lcd.print("                ");
  lcd.setCursor(0, 1);

  lcd.print(expression);
}

void setup() {
  Serial.begin(9600);

  lcd.begin(16, 2);

  lcd.setCursor(0, 0);
  lcd.print("Expression:");

  displayExpression("Waiting...");

  //This asks the string to reserve enough capacity for atleast 32 characters
  receivedMessage.reserve(32);
}

void loop() {
  while (Serial.available() > 0) {
    char incomingChar = Serial.read();

    // Python sends a newline after each message
    if (incomingChar == '\n') {
      receivedMessage.trim(); //Removes whitespaces at the beginning and end of an arduino string

      if (receivedMessage.length() > 0) {
        if (receivedMessage == "SMILE") {
          displayExpression("SMILE");
        }
        else if (receivedMessage == "NEUTRAL") {
          displayExpression("NEUTRAL");
        }
        else if (receivedMessage == "NO FACE") {
          displayExpression("NO FACE");
        }
        else if (receivedMessage == "SHOCKED"){
          displayExpression("SHOCKED");
        }

        // Useful for checking communication in Serial Monitor
        Serial.println("Received: " + receivedMessage);
      }

      receivedMessage = "";
    }
    else if (incomingChar != '\r') {
      if (receivedMessage.length() < 32) {
        receivedMessage += incomingChar;
      }
    }
  }
}
