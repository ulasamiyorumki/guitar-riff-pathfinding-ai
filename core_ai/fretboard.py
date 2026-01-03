class Fretboard:
    """
    Represents the physical dimensions and properties of the guitar fretboard.
    Acts as the environment for the AI agent.
    """

    def __init__(self, num_frets=22):
        self.num_strings = 6
        self.num_frets = num_frets  # Standard range is usually 22 or 24

    def is_valid_position(self, string, fret):
        """
        Validates if a (string, fret) coordinate exists on this fretboard.
        """
        # String 1 is high E, String 6 is low E
        is_string_valid = 1 <= string <= self.num_strings
        is_fret_valid = 0 <= fret <= self.num_frets

        return is_string_valid and is_fret_valid

    def get_fretboard_size(self):
        """Returns the dimensions of the search grid."""
        return self.num_strings, self.num_frets



