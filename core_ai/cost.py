import math

class ErgonomicCost:
    """
    Calculates the physical effort required to move between two fretboard positions.
    Acts as the cost function for the global optimization agent.
    """

    def __init__(self):
        # Weight factors to tune the 'difficulty' of different movements
        self.FRET_STRETCH_WEIGHT = 1.0   # Penalty for horizontal movement
        self.STRING_CHANGE_WEIGHT = 2.0  # Penalty for vertical string jumps
        self.OPEN_STRING_BONUS = -0.5    # Reward for using open strings (easier)
        self.MAX_REACHABLE_STRETCH = 4   # Constraint: Max fret span for a hand position

    def calculate_step_cost(self, pos1, pos2):
        """
        Calculates the cost from position 1 to position 2.
        """
        if pos1 is None:
            return 0

        s1, f1 = pos1
        s2, f2 = pos2

        # 1. Distance calculations
        fret_diff = abs(f1 - f2)
        string_diff = abs(s1 - s2)

        # 2. Base cost calculation
        cost = (fret_diff * self.FRET_STRETCH_WEIGHT) + (string_diff * self.STRING_CHANGE_WEIGHT)

        # 3. Open String Advantage
        if f2 == 0:
            cost += self.OPEN_STRING_BONUS

        # 4. Anatomical Constraint Check
        # If the move is physically impossible, add a massive penalty to discourage the agent.
        if not self.is_physically_possible(pos1, pos2):
            cost += 15.0

        return max(0.1, cost)

    def is_physically_possible(self, pos1, pos2):
        """
        Constraint Satisfaction Check:
        Returns False if the fret distance exceeds human anatomical limits.
        """
        f1, f2 = pos1[1], pos2[1]

        # Ignore stretch constraint if one of the notes is an open string
        if f1 == 0 or f2 == 0:
            return True

        return abs(f1 - f2) <= self.MAX_REACHABLE_STRETCH