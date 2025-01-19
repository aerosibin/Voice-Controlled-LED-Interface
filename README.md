# Voice-Controlled RGB LED System

This project enables you to control an RGB LED using voice commands or manual inputs through a user-friendly web interface. The application is powered by AI-based speech recognition and Streamlit for an interactive experience.

## Features

- **Voice Control**: Use commands like "red," "green," "blue," or "off" to control the RGB LED.
- **Manual Control**: A set of buttons on the interface allows manual control of the LED.
- **Arduino Integration**: Upload the provided `.ino` file to your Arduino to set up serial communication with the system.
- **Web-Based Access**: The app is designed for local use with Streamlit, and cannot be deployed to the Streamlit Cloud due to the requirement to list and connect to serial ports.

## Hugging Face Transformers 

This project leverages the power of Hugging Face's **Transformers** library for automatic speech recognition (ASR) through the use of the **Whisper** model. The Whisper model, developed by OpenAI, is designed to perform transcription tasks by converting audio input into text. Here's how the model is utilized:

### How It Works:

1. **Speech Input**: When the user gives a voice command, the system records the audio through the microphone using the `sounddevice` library. The recorded audio is then saved as a `.wav` file.

2. **Model Inference**: The audio file is passed to the Whisper model from Hugging Face's Transformers library. The model is pre-trained for automatic speech recognition and is capable of transcribing various languages, accents, and speech styles.

3. **Text Output**: Once the audio is processed, Whisper transcribes the speech into text. The output text is then converted into lowercase and analyzed to recognize specific commands such as "red," "green," "blue," or "off."

4. **Action Triggering**: Based on the recognized command, the corresponding action is triggered, such as sending a signal to change the LED color or turn it off.

### Advantages of Using Hugging Face Transformers:

- **Pre-trained Models**: Whisper is a robust, pre-trained model that requires no additional fine-tuning, making it easy to integrate and use.
- **Multilingual Support**: The model is capable of recognizing and transcribing multiple languages, ensuring that the system can work in various linguistic environments.
- **Accuracy**: Whisper has been shown to perform well with different accents, background noise, and other common speech variations, ensuring that the voice commands are accurately recognized.

By integrating this powerful ASR tool, the project achieves high accuracy and flexibility in recognizing user voice commands, allowing for seamless control of the RGB LED system through natural speech.

## Usage

To run the app locally, use the following command in your terminal:

```bash
streamlit run pro4.py
```

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
- [PyTorch](https://pytorch.org/)

## License

This project is licensed under the [MIT License](LICENSE).

---

### Acknowledgments

This project leverages the power of AI and Streamlit for an innovative interface. Special thanks to Hugging Face for the speech recognition model.

Developed with ❤️ for LED enthusiasts.

### Contributors

- [Sibin Paulraj](https://github.com/aerosibin)
- [Naren Kumar)[https://github.com/narenkumarchandran)
- [Varsha Pillai](https://github.com/varsha-2024-snu)
