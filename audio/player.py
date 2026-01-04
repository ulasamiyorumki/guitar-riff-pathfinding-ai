import numpy as np
import sounddevice as sd
import time
from music21 import note


class GuitarSoundPlayer:
    def __init__(self, fs=44100, volume=0.25):
        self.fs = fs
        self.volume = volume

    def note_to_freq(self, note_name: str) -> float:
        n = note.Note(note_name)
        midi = n.pitch.midi
        return 440.0 * (2 ** ((midi - 69) / 12))


    def generate_guitar_wave(self, freq, duration):
        t = np.linspace(0, duration, int(self.fs * duration), False)

        # Harmonic-rich waveform
        wave = (
            1.0 * np.sin(2 * np.pi * freq * t) +
            0.5 * np.sin(2 * np.pi * 2 * freq * t) +
            0.25 * np.sin(2 * np.pi * 3 * freq * t) +
            0.15 * np.sin(2 * np.pi * 4 * freq * t)
        )

        wave /= np.max(np.abs(wave))

        attack = int(0.01 * self.fs)
        decay = int(0.08 * self.fs)
        sustain_level = 0.3
        release = int(0.15 * self.fs)

        sustain = len(wave) - (attack + decay + release)
        sustain = max(0, sustain)

        envelope = np.concatenate([
            np.linspace(0, 1, attack),
            np.linspace(1, sustain_level, decay),
            np.full(sustain, sustain_level),
            np.linspace(sustain_level, 0, release)
        ])

        envelope = envelope[:len(wave)]
        wave *= envelope

        return wave

    def play_note(self, note_name, duration=0.5):
        freq = self.note_to_freq(note_name)
        wave = self.generate_guitar_wave(freq, duration)
        sd.play(self.volume * wave, self.fs)
        sd.wait()

    def play_notes(self, notes, duration=0.5):
        for n in notes:
            self.play_note(n, duration)
            time.sleep(0.03)


