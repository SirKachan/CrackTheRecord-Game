class RebornSystem:
    def __init__(self):
        self.count = 0
        self.base_cost = 500000
        self.cost_growth = 2.5

    def get_cost(self):
        return int(self.base_cost * (self.cost_growth ** self.count))

    def get_multiplier(self):
        return 1 + self.count

    def can_reborn(self, current_balance):
        return current_balance >= self.get_cost()

    def do_reborn(self):
        self.count += 1