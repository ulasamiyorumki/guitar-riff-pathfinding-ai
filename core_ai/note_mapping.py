from music21 import note

class NoteMapper:
    """
    Handles the translation between musical notation (Pitch)
    and the physical coordinates of the guitar fretboard.
    """
    def __init__(self, num_frets=22):
        # Standard Guitar Tuning (E2, A2, D3, G3, B3, E4) in MIDI values
        self.tuning = {
            1: 64, # High E String (E4)
            2: 59, # B String (B3)
            3: 55, # G String (G3)
            4: 50, # D String (D3)
            5: 45, # A String (A2)
            6: 40  # Low E String (E2)
        }
        self.num_frets = num_frets # Standard fret count

    def note_to_midi(self, note_name):
        """
        Converts a note name (e.g., 'C4', 'G#3') into a MIDI number.
        """
        try:
            n = note.Note(note_name)
            return n.pitch.midi
        except Exception as e:
            print(f"Error converting note name: {e}")
            return None

    def find_positions_on_fretboard(self, midi_value):
        """
        Maps a single MIDI value to all possible (string, fret)
        locations available on the fretboard.
        """
        positions = []
        for string_num, open_note_midi in self.tuning.items():
            fret = midi_value - open_note_midi
            # Ensure the note is physically playable on this specific string
            if 0 <= fret <= self.num_frets:
                positions.append((string_num, fret))
        return positions

# Example Usage:
# mapper = NoteMapper()
# midi_val = mapper.note_to_midi("A3")
# possible_locations = mapper.find_positions_on_fretboard(midi_val)
# print(f"Locations for A3: {possible_locations}")
# Output might be: [(2, -2), (3, 2), (4, 7), (5, 12), (6, 17)] -> (2, -2) is filtered out.