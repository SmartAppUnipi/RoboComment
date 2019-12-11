import os
import numpy as np


class YoloCache:
    def __init__(self, path):
        self.path = path
        if os.path.exists(path):
            x = np.load(path)
            frames, sizes = x["frames"], x["sizes"]
            self.data = []
            pos = 0
            for s in sizes:
                self.data.append(frames[pos:pos+s])
                pos += s
        else:
            self.data = []

        self.index = 0

    def add(self, predictions):
        self.data.append(predictions)

    def save(self):
        sizes = np.asarray([x.shape[0] for x in self.data], dtype=np.int32)
        np.savez(self.path, frames=np.vstack(self.data), sizes=sizes)

    def clear(self):
        self.data = []
        self.index = 0

    def predict(self, *args, **kwargs):
        y = self.data[self.index]
        self.index += 1
        return y

    def get_n_frames(self):
        return len(self.data)
