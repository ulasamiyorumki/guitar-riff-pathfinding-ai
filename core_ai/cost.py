class ErgonomicCost:
    """
    Calculates the physical effort required to move between two fretboard positions.
    """

    def __init__(self):
        self.FRET_STRETCH_WEIGHT = 1.0
        self.STRING_CHANGE_WEIGHT = 2.0
        self.OPEN_STRING_BONUS = -0.5
        self.MAX_REACHABLE_STRETCH = 4

        # Penalty applied ONCE for anatomical violations
        self.ANATOMICAL_PENALTY = 15.0

    def calculate_step_cost(self, pos1, pos2):
        """
        Calculates ergonomic movement cost between two positions.
        """

        s1, f1 = pos1
        s2, f2 = pos2

        fret_diff = abs(f1 - f2)
        string_diff = abs(s1 - s2)

        cost = (
            fret_diff * self.FRET_STRETCH_WEIGHT +
            string_diff * self.STRING_CHANGE_WEIGHT
        )

        # Anatomical constraint (soft)
        if not self.is_physically_possible(pos1, pos2):
            cost += self.ANATOMICAL_PENALTY
        else:
            # Open string bonus ONLY if physically reachable
            if f2 == 0:
                cost += self.OPEN_STRING_BONUS

        # Ensure strictly positive cost (A* requirement)
        return max(1.0, cost)

    def is_physically_possible(self, pos1, pos2):
        """
        Returns False if the fret stretch exceeds hand anatomy limits.
        """
        f1, f2 = pos1[1], pos2[1]
        return abs(f1 - f2) <= self.MAX_REACHABLE_STRETCH
