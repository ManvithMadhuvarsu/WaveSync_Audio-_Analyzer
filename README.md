# **WaveSync: Audio Analyzer**

### **Overview**
WaveSync: Audio Analyzer is an interactive Python application designed for analyzing and comparing audio files. It provides features for waveform visualization, speech recognition, and audio similarity measurement. The application is equipped to handle `.wav` audio files and offers a user-friendly GUI for seamless interaction.

---

### **Key Features**
1. **Audio File Selection**:
   - Allows users to select and load `.wav` audio files for analysis.
   - Provides validation for input file types to ensure compatibility.

2. **Waveform Visualization**:
   - Plots waveforms of both the target and input audio files.
   - Interactive and real-time visualization using Matplotlib embedded in Tkinter.

3. **Speech Recognition**:
   - Extracts and displays recognized text from audio files using Google Speech Recognition API.
   - Supports text comparison between two audio files for similarity evaluation.

4. **Audio Recording**:
   - Enables users to record audio directly within the application.
   - Saves recorded audio as `.wav` files and integrates them into the analysis pipeline.

5. **Audio Comparison**:
   - Performs a dual comparison:
     - **Speech Recognition**: Compares the recognized text from two audio files.
     - **Waveform Analysis**: Computes waveform similarity using correlation and a threshold-based method.

6. **Event Logging**:
   - Displays time taken for waveform comparisons.
   - Logs results, including counts from text recognition and waveform analysis.

---

### **Usage**
#### **Step-by-Step Guide**:
1. **Select Audio Files**:
   - Use the "Select Target Audio File" and "Select Input Audio File" buttons to load `.wav` files.
   
2. **Visualize Waveforms**:
   - View the waveforms of the loaded files for a visual comparison.

3. **Perform Speech Recognition**:
   - Automatically recognize and display the text in the selected audio files.

4. **Record Audio**:
   - Use the "Start Recording" button to record a new `.wav` file.
   - Save the file and include it for analysis.

5. **Compare Audio Files**:
   - Use the "Compare" button to perform both text-based and waveform-based analysis.
   - View the results, including match counts and time taken for processing.

6. **Close Application**:
   - Use the "Close" button to exit the application.

---

### **Technical Details**
#### **Key Modules and Libraries**:
- **Tkinter**: For creating a graphical user interface (GUI).
- **Matplotlib**: For plotting and embedding waveforms into the GUI.
- **SpeechRecognition**: For converting speech to text using the Google Speech Recognition API.
- **Wave**: For reading `.wav` audio files.
- **NumPy**: For processing waveform data and computing correlations.

#### **Core Functionalities**:
1. **Waveform Visualization**:
   - Uses `wave` and `numpy` to extract audio signals.
   - Downsamples signals for efficient plotting and embeds them into the GUI using Matplotlib.

2. **Speech Recognition**:
   - Leverages `SpeechRecognition` to transcribe audio files.
   - Compares transcriptions to calculate the number of matches.

3. **Waveform Comparison**:
   - Computes correlation between waveforms of the target and input files.
   - Counts significant correlations exceeding a predefined threshold.

4. **Recording**:
   - Uses `SpeechRecognition`'s `Microphone` module to capture audio.
   - Saves audio data in `.wav` format.

---

### **Project Structure**
```plaintext
WaveSync/
├── main.py         # Contains the core application logic.
├── requirements.txt # Lists dependencies for the project.
└── README.md       # Documentation and usage guide.
```

---

### **Dependencies**
- Python 3.x
- Tkinter (pre-installed with Python)
- SpeechRecognition
- Matplotlib
- NumPy

To install the dependencies, run:
```bash
pip install speechrecognition matplotlib numpy
```

---

### **Future Enhancements**
- Support for additional audio file formats like `.mp3`.
- Advanced visualization features, including frequency spectrograms.
- Enhanced audio similarity metrics using machine learning techniques.
- Real-time audio processing and transcription.

