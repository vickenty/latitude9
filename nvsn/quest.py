import random
import items

class Quest (object):
    def __init__(self, goals):
        self.goals = goals

    @classmethod
    def new_random(self, size=3):
        types = items.GoalItem.types
        goals = []
        for i in range(size):
            goal = random.choice(types)
            types.remove(goal)
            goals.append(goal)

        return self(goals)

