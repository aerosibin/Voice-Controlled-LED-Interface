// Pin definitions for RGB LED
const int redPin = 9;
const int greenPin = 10;
const int bluePin = 11;

void setup() {
  // Set RGB LED pins as outputs
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);

  // Initialize serial communication
  Serial.begin(9600);
}

void loop() {
  // Check if data is available on serial
  if (Serial.available() > 0) {
    // Read the incoming command
    String command = Serial.readStringUntil('\n');
    command.trim(); // Remove any extra whitespace or newline characters

    // Process the command
    if (command == "red") {
      setColor(255, 0, 0); // Full Red
    } else if (command == "green") {
      setColor(0, 255, 0); // Full Green
    } else if (command == "blue") {
      setColor(0, 0, 255); // Full Blue
    } else if (command == "off") {
      setColor(0, 0, 0); // Turn off LED
    }
  }
}

// Function to set RGB LED color
void setColor(int red, int green, int blue) {
  analogWrite(redPin, red);   // Set red LED brightness
  analogWrite(greenPin, green); // Set green LED brightness
  analogWrite(bluePin, blue);  // Set blue LED brightness
}
