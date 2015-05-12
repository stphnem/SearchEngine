class Frequency():
    def __init__(self, word):
        self.word = word
        self.frequency = 0

    def __init__(self, word, frequency):
        self.word = word
        self.frequency = frequency

    def get_text(self):
        return self.word

    def get_frequency(self):
        return self.frequency

    def increment_frequecy(self):
        self.frequency += 1

    def __repr__(self):
        return "{}:{}".format(self.word, self.frequency)

    def __str__(self):
        return "{}:{}".format(self.word, self.frequency)
