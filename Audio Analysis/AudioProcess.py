import librosa
from python_speech_features import mfcc
import scipy.io.wavfile as wav
import numpy

def readAudio(file):
	y, sr = librosa.load(file)
	mfcc_feat = mfcc(y, sr)
	print mfcc_feat.shape

filename = librosa.util.example_audio_file()
readAudio(filename)
