# /// script
# dependencies = [
#   "streamlit",
#   "streamlit-webrtc",
#   "scipy",
#   "transformers",
#   "torch",
#   "serial",
#   "numpy",
# ]
# ///


import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import scipy.io.wavfile as wav
from transformers import pipeline
import serial.tools.list_ports
import serial
import os
import numpy as np

# Streamlit app title
st.title("Voice-Controlled LED Interface")
st.markdown("Control an RGB LED using voice commands or manual inputs.")

# Set up serial communication
ports = serial.tools.list_ports.comports()
ports_list = [str(port) for port in ports]
st.sidebar.subheader("Serial Port Configuration")
port_var = st.sidebar.selectbox("Select Port", options=ports_list)

baud_rate = st.sidebar.number_input("Baud Rate", min_value=9600, step=9600, value=9600)

# Initialize serial connection in session state
if "serial_inst" not in st.session_state:
    st.session_state.serial_inst = serial.Serial()

# Handle serial connection
if st.sidebar.button("Connect"):
    if port_var:
        st.session_state.serial_inst.port = port_var.split(" ")[0]  # Extract port (e.g., COM3)
        st.session_state.serial_inst.baudrate = baud_rate
        try:
            st.session_state.serial_inst.open()
            st.sidebar.success(f"Connected to {port_var}")
        except Exception as e:
            st.sidebar.error(f"Failed to connect: {e}")
    else:
        st.sidebar.error("No port selected.")

if st.sidebar.button("Disconnect"):
    if st.session_state.serial_inst.is_open:
        st.session_state.serial_inst.close()
        st.sidebar.success("Disconnected.")
    else:
        st.sidebar.warning("No active connection to close.")

# Define AudioProcessor to record and save audio
class AudioRecorder(AudioProcessorBase):
    def __init__(self):
        self.audio_data = []

    def recv_audio(self, frames):
        self.audio_data.extend(frames)
        return frames

    def get_audio(self):
        return np.array(self.audio_data)

def save_audio(audio_data, sample_rate, file_name):
    with wave.open(file_name, 'wb') as wf:
        wf.setnchannels(1)  # Mono audio
        wf.setsampwidth(2)  # 2 bytes per sample
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data)

# Function to capture and process voice
def capture_voice():
    whisper = pipeline("automatic-speech-recognition", model="openai/whisper-medium", device=0)
    sample_rate = 16000
    file_name = "live_audio.wav"
    try:
        st.info("Recording for 5 seconds...")

        webrtc_ctx = webrtc_streamer(
            key="audio-recorder",
            mode=WebRtcMode.SENDRECV,
            audio_receiver_size=256,
            media_stream_constraints={"audio": True},
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            audio_processor_factory=AudioRecorder,
        )

        if webrtc_ctx.audio_processor:
            st.warning("Recording... Please wait.")
            audio_recorder = webrtc_ctx.audio_processor
            st.time.sleep(5)  # Record for 5 seconds
            raw_audio = audio_recorder.get_audio()
            save_audio(raw_audio.tobytes(), sample_rate, file_name)
            st.success("Recording complete.")
        else:
            st.error("Audio recorder not initialized.")

    except Exception as e:
        st.error(f"Error during recording: {e}")
        return None

    try:
        result = whisper(file_name)
        os.remove(file_name)  # Cleanup audio file after processing
        return result["text"].lower()
    except Exception as e:
        st.error(f"Error during processing: {e}")
        return None

# Function to send command via serial
def send_command(command):
    if st.session_state.serial_inst.is_open:
        st.session_state.serial_inst.write(command.encode("utf-8"))
        st.success(f"Command sent: {command}")
    else:
        st.error("Serial connection not open. Please connect first.")

# Main interface
st.header("Voice Command")
if st.button("Record Voice"):
    text = capture_voice()
    if text:
        st.write(f"Recognized Text: {text}")
        if "red" in text:
            send_command("red")
        elif "green" in text:
            send_command("green")
        elif "blue" in text:
            send_command("blue")
        elif "off" in text:
            send_command("off")
        elif "exit" in text:
            st.warning("Exiting program...")
            if st.session_state.serial_inst.is_open:
                st.session_state.serial_inst.close()
        else:
            st.error("Command not recognized. Please say red, green, blue, or off.")

st.header("Manual Command Control")
col1, col2, col3, col4 = st.columns(4)

if col1.button("Red"):
    send_command("red")

if col2.button("Green"):
    send_command("green")

if col3.button("Blue"):
    send_command("blue")

if col4.button("Off"):
    send_command("off")

# Streamlit footer
st.sidebar.markdown("---")
st.sidebar.caption("Developed for controlling RGB LEDs using voice commands.")
