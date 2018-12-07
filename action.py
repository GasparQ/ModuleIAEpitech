PICK, PRE_POWER, MOVE, POST_POWER = 0, 1, 2, 3


class Action:
    def __init__(self, state, actions, next_state):
        self.state = state
        self.actions = actions
        self.next_state = next_state

    def Clone(self):
        actions = [self.actions[PICK], self.actions[PRE_POWER], self.actions[MOVE], self.actions[POST_POWER]]
        return Action(self.state, actions, self.next_state)

    def __repr__(self):
        return '(state: ' + str(self.state.board.GetStateHash()) + ', actions: ' + str(self.actions) + ', next_state: ' + str(self.next_state.board.GetStateHash()) + ')'
