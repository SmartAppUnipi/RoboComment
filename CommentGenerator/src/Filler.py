

class Filler:

    def __init__(self, config=None):
        if config is not None:
            self._load_config(config)

    def update_comment(self, comment):

        return comment + ",fantastic!"

    def _load_config(self):
        return None