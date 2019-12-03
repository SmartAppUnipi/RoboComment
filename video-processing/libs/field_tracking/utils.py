import numpy as np
import math
import numba
from numba import prange


def load_npz(path, keys):
    X = np.load(path, allow_pickle=True)
    return [X[k] for k in keys]


@numba.jit(parallel=True, nogil=True, fastmath=True, nopython=True)
def _distance_matrix(D, X, Y):
    for i in prange(D.shape[0]):
        for j in prange(D.shape[1]):
            tmp = 0
            for k in range(X.shape[1]):
                tmp += (X[i, k] - Y[j, k]) ** 2
            D[i, j] = tmp


def distance_matrix(X, Y, squared=False):
    D = np.empty((X.shape[0], Y.shape[0]), dtype=np.float32)
    _distance_matrix(D, X, Y)
    if not squared:
        D = np.sqrt(D)
    return D


@numba.jit(parallel=True, nogil=True, fastmath=True, nopython=True)
def _norm(X, Y):
    for i in prange(X.shape[0]):
        tmp = 0
        for j in range(X.shape[1]):
            tmp += X[i, j] ** 2
        Y[i] = math.sqrt(tmp)


def norm(x):
    y = np.empty(x.shape[0], dtype=np.float32)
    _norm(x, y)
    return y
