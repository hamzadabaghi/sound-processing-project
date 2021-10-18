import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import scipy

# librosa to calculate mfcc , plt to plot , scipy for the euclidean distance


class Program(object):

    # DTW functions

    def dtw_table(self, x, y, distance=None):
        if distance is None:
            distance = scipy.spatial.distance.euclidean
        nx = len(x)
        ny = len(y)
        table = np.zeros((nx+1, ny+1))

        # Compute left column separately, i.e. j=0.
        table[1:, 0] = np.inf

        # Compute top row separately, i.e. i=0.
        table[0, 1:] = np.inf

        # Fill in the rest.
        for i in range(1, nx+1):
            for j in range(1, ny+1):
                d = distance(x[i-1], y[j-1])
                table[i, j] = d + \
                    min(table[i-1, j], table[i, j-1], table[i-1, j-1])
        return table

    def dtw(self, x, y, table):
        i = len(x)
        j = len(y)
        path = [(i, j)]
        while i > 0 or j > 0:
            minval = np.inf
            if table[i-1][j-1] < minval:
                minval = table[i-1, j-1]
                step = (i-1, j-1)
            if table[i-1, j] < minval:
                minval = table[i-1, j]
                step = (i-1, j)
            if table[i][j-1] < minval:
                minval = table[i, j-1]
                step = (i, j-1)
            path.insert(0, step)
            i, j = step
        return np.array(path)
