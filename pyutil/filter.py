class PT1():
    def __init__(self, T):
        self.T = T
        self.set = 0
        self.cur = 0

    def tick(self, dt):
        self.cur += ((self.set-self.cur)/self.T)*dt