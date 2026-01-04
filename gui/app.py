from gui.input_panel import InputPanel
from gui.fretboard_view import FretboardView
from core_ai.api import run_fingering_algorithm
from core_ai.fretboard import Fretboard
from audio.player import GuitarSoundPlayer
from core_ai.note_mapping import NoteMapper


class GuitarAIApp:
    def __init__(self, root):
        self.fretboard_model = Fretboard()
        self.root = root
        self.root.title("Guitar AI Pathfinding Dashboard")
        self.root.geometry("1200x650")
        self.root.configure(bg="#121212")
        self.sound_player = GuitarSoundPlayer()
        self.note_mapper = NoteMapper()
        self.current_path = []

        self.fretboard = FretboardView(self.root, self.fretboard_model)
        self.input_panel = InputPanel(
            self.root,
            self.on_solve,
            self.fretboard.next_step,
            self.fretboard.prev_step,
            self.fretboard.show_full_path,
            self.play_solution
        )

    def on_solve(self, riff_text):
        riff = riff_text.strip().split()
        if not riff:
            self.fretboard.load_path([])
            self.input_panel.update_stats({"stretch": 0, "string": 0, "pos": 0, "total": 0})
            self.input_panel.set_message("Please enter some notes.")
            return

        try:
            path, analysis = run_fingering_algorithm(riff)

            if len(path) < len(riff):
                self.input_panel.set_message("Warning: Some notes are out of range!", is_error=True)
            else:
                self.input_panel.set_message("Success: Path calculated.", is_error=False)

            if path:
                self.fretboard.load_path(path)
                self.fretboard.show_full_path()
                self.input_panel.update_stats(analysis)
                self.current_path = path

        except Exception as e:
            self.input_panel.set_message(f"Error: {str(e)}", is_error=True)

    def play_solution(self):
        if not self.current_path:
            return

        notes = []

        for string, fret in self.current_path:
            open_midi = self.note_mapper.tuning[string]
            midi = open_midi + fret
            note_name = self.note_mapper.midi_to_note_name(midi)
            notes.append(note_name)

        self.sound_player.play_notes(notes)
