# Voice-Controlled RGB LED System

This project enables you to control an RGB LED using voice commands or manual inputs through a user-friendly web interface. The application is powered by AI-based speech recognition and Streamlit for an interactive experience.

## Features

- **Voice Control**: Use commands like "red," "green," "blue," or "off" to control the RGB LED.
- **Manual Control**: A set of buttons on the interface allows manual control of the LED.
- **Arduino Integration**: Upload the provided `.ino` file to your Arduino to set up serial communication with the system.
- **Web-Based Access**: The app is designed for local use with Streamlit, and cannot be deployed to the Streamlit Cloud due to the requirement to list and connect to serial ports.

## Usage

To run the app locally, use the following command in your terminal:

'''bash
streamlit run pro4.py'''

### Note:
Since the application requires access to serial ports to communicate with the Arduino, it cannot be deployed on Streamlit Cloud or other cloud environments that restrict access to hardware ports.

## Prerequisites

### Hardware
- RGB LED connected to an Arduino or similar microcontroller.
- USB cable for Arduino connection to your computer.

### Software
- Arduino IDE for uploading the `.ino` file.
- Python 3.8 or later for local development (optional).
  
## Commands Supported

| Command    | Description            |
|------------|------------------------|
| `red`      | Turns on the LED red      |
| `green`    | Turns on the LED green    |
| `blue`     | Turns on the LED blue     |
| `off`      | Turns off the LED      |

## Troubleshooting

- **Serial Connection Issues**:
  - Ensure the correct port is selected in the sidebar.
  - Verify that the microcontroller is connected and functioning.
- **Voice Recognition Errors**:
  - Ensure your microphone is working.
  - Try speaking more clearly or in a quieter environment.

## Dependencies

- [Streamlit](https://streamlit.io/)
- [SoundDevice](https://python-sounddevice.readthedocs.io/)
- [Transformers](https://huggingface.co/transformers/)
- [PySerial](https://pyserial.readthedocs.io/)
- [SciPy](https://www.scipy.org/)

## License

This project is licensed under the [MIT License](LICENSE).

---

### Acknowledgments

This project leverages the power of AI and Streamlit for an innovative interface. Special thanks to Hugging Face for the speech recognition model.

Developed with ❤️ for LED enthusiasts.
