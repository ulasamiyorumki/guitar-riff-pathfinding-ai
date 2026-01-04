from audio.player import GuitarSoundPlayer

player = GuitarSoundPlayer()

player.play_notes(["E4", "F4", "G4", "A4"])


if __name__ == "__main__":
    print("Çalıyor...")
    for note in riff:
        midi = note_to_midi(note)
        freq = midi_to_freq(midi)
        play_frequency(freq)
        time.sleep(0.03) # Notalar arası çok küçük boşluk