import tkinter as tk
from tkinter import filedialog
import os
import speech_recognition as sr
import wave
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import threading
import time

def is_audio_file(file_path):
    return file_path.lower().endswith('.wav')

def select_target_audio():
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav")])
    if is_audio_file(file_path):
        target_entry.delete(0, tk.END)
        target_entry.insert(0, file_path)
        plot_waveform(file_path, target_canvas_ref, "Target Audio File Waveform")
        recognize_display_text(file_path, target_text_label)
    else:
        target_entry.delete(0, tk.END)
        target_entry.insert(0, "Invalid audio file")

def select_input_audio():
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav")])
    if is_audio_file(file_path):
        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)
        plot_waveform(file_path, input_canvas_ref, "Input Audio Waveform")  # Set title for input audio waveform
        recognize_display_text(file_path, input_text_label)
    else:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, "Invalid audio file")

def start_recording():
    def recognize_and_display(audio_data):
        recognized_text = recognize_text_from_audio_data(audio_data)
        input_text_label.config(text="Recognized Text: " + recognized_text)

    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Recording started. Speak now...")
        audio = r.record(source, duration=5)  # Adjust duration as needed
        print("Recording ended.")

    file_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".wav"
    file_path = filedialog.asksaveasfilename(defaultextension=".wav", initialfile=file_name)
    if file_path:
        with open(file_path, "wb") as f:
            f.write(audio.get_wav_data())

        input_entry.delete(0, tk.END)
        input_entry.insert(0, file_path)
        plot_waveform(file_path, input_canvas_ref, "Recorded Input Audio Waveform", downsample_factor=10)

        # Start a thread to recognize and display text
        threading.Thread(target=recognize_and_display, args=(audio,)).start()

def recognize_text_from_audio_data(audio_data):
    r = sr.Recognizer()
    recognized_text = ""
    try:
        recognized_text = r.recognize_google(audio_data)
    except sr.UnknownValueError:
        recognized_text = "Google Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        recognized_text = "Could not request results from Google Speech Recognition service; {0}".format(e)
    return recognized_text

def recognize_and_compare():
    target_audio_file = target_entry.get()
    input_audio_file = input_entry.get()

    if is_audio_file(target_audio_file) and is_audio_file(input_audio_file):
        start_time = time.time()

        # Perform recognition and comparison
        count_from_recognition = recognize_sentence(target_audio_file, input_audio_file)
        target_count_label.config(text="Count from Speech Recognition: " + str(count_from_recognition))

        target_waveform = get_waveform_from_audio(target_audio_file)
        input_waveform = get_waveform_from_audio(input_audio_file)
        count_from_waveforms = compare_waveforms(target_waveform, input_waveform)
        target_comparison_label.config(text="Count from Waveform Comparison: " + str(count_from_waveforms))

        end_time = time.time()
        elapsed_time = end_time - start_time
        time_label.config(text="Time taken: {:.2f} seconds".format(elapsed_time))

    else:
        print("Please select valid audio files.")

def recognize_sentence(target_audio_file, input_audio_file):
    r = sr.Recognizer()

    with sr.AudioFile(target_audio_file) as source:
        target_audio = r.record(source)
    target_text = r.recognize_google(target_audio)

    with sr.AudioFile(input_audio_file) as source:
        input_audio = r.record(source)
    input_text = r.recognize_google(input_audio)

    count = input_text.count(target_text)
    return count

def get_waveform_from_audio(audio_file):
    spf = wave.open(audio_file, 'r')
    signal = spf.readframes(-1)
    signal = np.frombuffer(signal, dtype=np.int16)
    return signal

def plot_waveform(audio_file, canvas_ref, title, downsample_factor=10):
    signal = get_waveform_from_audio(audio_file)
    signal_downsampled = signal[::downsample_factor]

    # Clear the previous plot
    if canvas_ref[0] is not None:
        canvas_ref[0].get_tk_widget().destroy()

    fig, ax = plt.subplots(figsize=(6, 2))
    ax.plot(signal_downsampled, color='black')
    ax.set_title(title)
    ax.set_xlabel("Sample")
    ax.set_ylabel("Amplitude")

    canvas_ref[0] = FigureCanvasTkAgg(fig, root)
    canvas_ref[0].get_tk_widget().pack()


def compare_waveforms(target_waveform, input_waveform):
    correlation = np.convolve(target_waveform[::-1], input_waveform, mode='valid')
    similarity_threshold = 0.5
    count = np.count_nonzero(correlation > similarity_threshold)
    return count

def recognize_display_text(audio_file, label):
    r = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    recognized_text = r.recognize_google(audio)
    label.config(text="Recognized Text: " + recognized_text)

def close_window():
    root.destroy()

root = tk.Tk()
root.title("Audio File Comparison")
root.geometry("700x800")  # Set window dimensions

# Create another frame inside the canvas
second_frame = tk.Frame(root)
second_frame.pack(expand=True)

# Widgets inside the second_frame
target_label = tk.Label(second_frame, text="Target Audio File:")
target_label.pack(anchor="center")

target_entry = tk.Entry(second_frame, width=50)
target_entry.pack()

target_button = tk.Button(second_frame, text="Select Target Audio File", command=select_target_audio)
target_button.pack()

# Create references to FigureCanvasTkAgg objects
target_canvas_ref = [None]

target_canvas = FigureCanvasTkAgg(plt.figure(figsize=(6, 2)), root)
target_canvas.get_tk_widget().pack()
target_canvas_ref[0] = target_canvas

target_text_label = tk.Label(second_frame, text="Recognized Text: ")
target_text_label.pack()

input_label = tk.Label(second_frame, text="Input Audio File:")
input_label.pack()

input_entry = tk.Entry(second_frame, width=50)
input_entry.pack()

input_button = tk.Button(second_frame, text="Select Input Audio File", command=select_input_audio)
input_button.pack()

# Create references to FigureCanvasTkAgg objects
input_canvas_ref = [None]

input_canvas = FigureCanvasTkAgg(plt.figure(figsize=(6, 2)), root)
input_canvas.get_tk_widget().pack()
input_canvas_ref[0] = input_canvas

input_text_label = tk.Label(second_frame, text="Recognized Text: ")
input_text_label.pack()

start_recording_button = tk.Button(second_frame, text="Start Recording", command=start_recording)
start_recording_button.pack()

compare_button = tk.Button(second_frame, text="Compare", command=recognize_and_compare)
compare_button.pack()

target_count_label = tk.Label(root, text="Count from Speech Recognition: ")
target_count_label.pack()

target_comparison_label = tk.Label(root, text="Count from Waveform Comparison: ")
target_comparison_label.pack()

time_label = tk.Label(root, text="Time Taken for Waveform Comparison: ")
time_label.pack()

close_button = tk.Button(root, text="Close", command=close_window)
close_button.pack()

root.mainloop()
