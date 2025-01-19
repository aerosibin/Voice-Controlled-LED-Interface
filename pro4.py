# /// script
# dependencies = [
#   "streamlit",
#   "streamlit-webrtc",
#   "scipy",
#   "transformers",
#   "torch",
#   "pyserial",
# ]
# ///

import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
from transformers import pipeline
import serial.tools.list_ports
import serial
import os
import wave

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

# Whisper pipeline for speech recognition
whisper = pipeline("automatic-speech-recognition", model="openai/whisper-medium", device=0)

# Function to process audio frames
def process_audio(frames):
    audio_file = "live_audio.wav"
    with wave.open(audio_file, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(b"".join(frames))
    try:
        result = whisper(audio_file)
        os.remove(audio_file)  # Cleanup audio file after processing
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
frames_collected = []

# WebRTC audio streaming for live voice input
webrtc_ctx = webrtc_streamer(
    key="voice-control",
    mode=WebRtcMode.SENDONLY,
    client_settings=ClientSettings(
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"audio": True, "video": False},
    ),
)

if webrtc_ctx and webrtc_ctx.state.playing:
    audio_frame = webrtc_ctx.audio_receiver
    if audio_frame:
        frames_collected.append(audio_frame.to_ndarray().tobytes())

    if len(frames_collected) >= 16000 * 5:  # Collect 5 seconds of audio
        st.info("Processing voice command...")
        recognized_text = process_audio(frames_collected)
        frames_collected.clear()  # Reset frames
        if recognized_text:
            st.write(f"Recognized Text: {recognized_text}")
            if "red" in recognized_text:
                send_command("red")
            elif "green" in recognized_text:
                send_command("green")
            elif "blue" in recognized_text:
                send_command("blue")
            elif "off" in recognized_text:
                send_command("off")
            elif "exit" in recognized_text:
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
