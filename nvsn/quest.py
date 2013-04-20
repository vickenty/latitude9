import random
import items

class Quest (object):
    types = None
    def __init__(self, goals):
        self.goals = goals

    @classmethod
    def new_random(self, size=3):
        if Quest.types is None or len(Quest.types) == 0:
            Quest.types = list(items.GoalItem.types)
        goals = []
        for i in range(size):
            goal = random.choice(Quest.types)
            Quest.types.remove(goal)
            goals.append(goal)

        return self(goals)

