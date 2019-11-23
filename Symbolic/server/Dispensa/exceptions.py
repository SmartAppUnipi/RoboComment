class EmptyQueueError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class InvalidIndexError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class NotFoundElementError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)