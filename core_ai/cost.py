import math

class ErgonomicCost:
    """
    Calculates the physical effort required to move between two fretboard positions.
    Used as the step cost g(n) in the A* Search Algorithm.
    """

    def __init__(self):
        # Weight factors to tune the 'difficulty' of different movements
        self.FRET_STRETCH_WEIGHT = 1.0  # Horizontal distance
        self.STRING_CHANGE_WEIGHT = 2.0  # Vertical distance (string crossing)
        self.OPEN_STRING_BONUS = -0.5  # Open strings (fret 0) are easier to play
        self.MAX_REACHABLE_STRETCH = 4  # Maximum fret distance for a single hand position

    def calculate_step_cost(self, pos1, pos2):
        """
        Calculates the cost from position 1 (string1, fret1) to position 2 (string2, fret2).
        """
        s1, f1 = pos1
        s2, f2 = pos2

        # 1. Horizontal Distance (Fret difference)
        fret_diff = abs(f1 - f2)

        # 2. Vertical Distance (String difference)
        string_diff = abs(s1 - s2)

        # Base movement cost calculation
        cost = (fret_diff * self.FRET_STRETCH_WEIGHT) + (string_diff * self.STRING_CHANGE_WEIGHT)

        # 3. Open String Advantage
        # If the target note is an open string, it's generally easier (zero fret hand effort)
        if f2 == 0:
            cost += self.OPEN_STRING_BONUS

        return max(0, cost)

    def is_physically_possible(self, pos1, pos2):
        """
        Constraint Satisfaction (CSP) Check:
        Prunes moves that are anatomically impossible (e.g., extreme hand stretches).
        """
        f1, f2 = pos1[1], pos2[1]

        # Ignore stretch constraint if one of the notes is an open string
        if f1 == 0 or f2 == 0:
            return True

        return abs(f1 - f2) <= self.MAX_REACHABLE_STRETCH