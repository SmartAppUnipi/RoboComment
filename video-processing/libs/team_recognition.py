import numpy as np
import cv2
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from scipy.spatial import distance
import matplotlib.pyplot as plt

# todo define interaction between players tracking
# and this module (how many times to call this function)
"""
    Wrapper class for detecting teams
    from a frame given a set of detections.
    
"""


class TeamRecognizer:

    # todo choose dbscan values
    def __init__(self, classes: list = ['team_a', 'team_b', 'referee'], eps=1., min_samples=2):
        self.classes = classes
        self.dbscan = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine')
        self.kmeans = KMeans(n_clusters=3)
        self.old_centroids_labels = []

    def filter_labels(self):
        new_teams = self.kmeans.labels_
        centroids = self.kmeans.cluster_centers_
        self.old_centroids_labels.append((centroids, new_teams))
        if len(self.old_centroids_labels) > 1:
            match_index = []
            # copute distance matrix between old clusters i and new clusters
            dist = distance.cdist(self.old_centroids_labels[0][0], self.old_centroids_labels[1][0])
            # print("[DEBUG} COMPUTED CENTROIDS DISTANCES")
            # print(dist)
            for i, d in enumerate(dist):
                res = np.where(d == np.amin(d))
                match_index.append((i, res[0][0]))
            # print("[DEBUG] PAIRED CLUSTERS")
            # print(match_index)
            # print()
            new_teams_shift = np.array([x + 10 for x in new_teams])
            for m in match_index:
                for i, label in enumerate(new_teams_shift):
                    if label == m[1] + 10:
                        new_teams[i] = m[0] + 10
            new_teams = np.array([x - 10 for x in new_teams])
            # prepare self.old_centroids_labels or next iteration
            self.old_centroids_labels.pop(0)
            lst = list(self.old_centroids_labels[0])
            lst[1] = np.array([x - 10 for x in self.old_centroids_labels[0][1]])
            self.old_centroids_labels[0] = tuple(lst)
        return new_teams

    def detect_teams(self, frame, boxes, use_idf=True, value_search=False):
        """
        Performs clustering on players'
        jerseys HSV histograms to detect
        to which team each one belongs to.
        :param boxes: list of bounding boxes assumed to
            be of shape [x, y, w, h] with (x, y) top left corner point.
        :param frame: h, w, c
        :param use_idf:
        :return: a list containing one class
        for each entity and a list containing
        flags indicating whether an entity was
        recognized.
        """
        # get color histograms of each box (weighting with tf-idf)
        histograms = self.compute_weighted_histograms(frame, boxes, use_idf)
        # [print(h) for h in histograms]

        # force same ordering in clusters: init kmeans start centroids with previous
        if len(self.old_centroids_labels) > 0:
            self.kmeans = KMeans(n_clusters=3, init=self.old_centroids_labels[0][0], n_init=1)

        X = histograms
        # use dbscan to filter out noise (fans, refs..)
        # self.dbscan.fit(X)
        # print(self.dbscan.labels_)
        # filter out noise
        # X = [x for i, x in enumerate(X) if self.dbscan.labels_[i] != -1]

        unrecognized_players = []
        # for d in self.dbscan.labels_:
        #     if d == -1:
        #         unrecognized_players.append(False)
        #     else:
        #         unrecognized_players.append(True)

        if len(X) > 0:
            bsse = 1e11
            for _ in range(10):
                self.kmeans.fit(X)
                if self.kmeans.inertia_ < bsse:
                    bsse = self.kmeans.inertia_
                    kmeans = self.kmeans
                    kmeans.labels_ = self.filter_labels()
            print(kmeans.labels_)
            return kmeans.labels_, [True for _ in range(len(kmeans.labels_))]
        else:
            self.kmeans.labels_ = []
            self.kmeans.inertia_ = 1e11

        if value_search:
            return self.kmeans.labels_, unrecognized_players, self.kmeans.inertia_
        else:
            return self.kmeans.labels_, unrecognized_players

    def search_best_eps(self, bboxes, frame):

        best_sse = 1e10
        labels, ok_players = [], []
        iter_ = -1
        for c, i in enumerate(range(-5, 1)):
            eps = 1 / (1 + np.exp(-i))
            self.dbscan = DBSCAN(eps=eps, min_samples=2, metric='cosine')
            l, ok, sse = self.detect(bboxes, frame, value_search=True)
            labels.append(l)
            ok_players.append(ok)
            print(f'Sse value is {sse} with eps {eps}')
            if sse < best_sse:
                best_sse = sse
                iter_ = c

        print("Best SSE value:", best_sse)

        return labels[iter_], ok_players[iter_]

    # def compute_color_centroids(self, frame, boxes, yolo_cache=None, video_cap=None, max_k=6):
    def compute_weighted_histograms(self, frame, boxes, use_idf=True):
        """
        Compute color histograms for each detection
        provided in boxes and 'compare' with histogram
        of entire frame to establish importance of
        each box using tf-idf.
        This method helps to adjust for the fact that
        the color of the field will appear more often,
        therefore we want to give less importance to it.
        :param frame: h, w, c format.
        :param boxes: same boxes format as 'detect_teams'
        :return:
        """
        n_bins = (8, 12, 3)
        # convert to HSV
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # compute document frequency for normalization (hist of entire frame)
        # todo: here we're cutting top part of frame
        #  assuming stadium seats; might have to re-check for close-up images/zooms
        idf = self.compute_histogram(frame[-200:], n_bins)
        # compute smooth idf
        idf = np.log(1.0 + idf) + 1.0

        histograms = []
        # arrange detections in a proper format before clustering
        for box in boxes:
            [x, y, w, h] = box
            playerb = frame[y:y + h, x:x + w, :].astype('uint8')

            # crop heads
            ratio = int(playerb.shape[0] / 7)
            playerb = playerb[ratio:, :, :]
            # blur player detection
            # kernel = np.ones((3, 3), np.float32)/9
            # playerb = cv2.filter2D(playerb, -1, kernel)

            # compute histogram of player detection (term frequency part)
            try:
                hist = self.compute_histogram(playerb, n_bins)
            except:
                print("ERROR")
                print(x, y, w, h, playerb.shape)
            if use_idf:
                hist /= idf
            # normalize it
            hist /= np.linalg.norm(hist)
            histograms.append(hist)

        return histograms

    def compute_histogram(self, img, bins):
        return cv2.calcHist(cv2.split(img), [0, 1, 2], None, bins, [0, 180, 0, 256, 0, 256]).flatten()

    # !deprecated!
    def centroid_histograms(self, centroids_labels, boxes, idf):
        """
        Given K-means centroid assignments, compute
        the dominant color histogram for each box.
        :param centroids_labels: result of kmeans clustering,
            label for each point.
        :param boxes: list of detections.
        :return:
        """
        # grab the number of different clusters
        numLabels = np.arange(0, len(np.unique(centroids_labels)) + 1)
        hists = []
        pos = 0
        for i, box in enumerate(boxes):
            (hist, _) = np.histogram(centroids_labels[pos:pos + len(box)], bins=numLabels, density=False)
            hist = hist.astype("float")
            # divide by document frequency
            hist /= idf
            # normalize the histogram, such that it sums to one
            hist /= np.linalg.norm(hist)  # (hist**2).sum()

            pos += len(box)

            hists.append(hist)

        # return histograms
        return hists

    def plot_colors(self, hist, centroids):
        # initialize the bar chart representing the relative frequency
        # of each of the colors
        bar = np.zeros((50, 300, 3), dtype="uint8")
        startX = 0

        hist = hist.astype("float")
        hist /= hist.sum()
        # loop over the percentage of each cluster and the color of
        # each cluster
        for (percent, color) in zip(hist, centroids):
            # plot the relative percentage of each cluster
            endX = startX + (percent * 300)
            cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                          color.astype("uint8").tolist(), -1)
            startX = endX

        # display bar chart
        plt.figure()
        plt.axis("off")
        plt.imshow(bar)
        plt.show()

    # def detect(self, b_boxes, frame, n_bins=30, value_search=False):
    #
    #     histograms = []
    #
    #     for box in b_boxes:
    #         # assume each box is a vector [x, y, w, h]
    #         [x, y, w, h] = box
    #         playerb = frame[y:y + h, x:x + w, :].astype('uint8')
    #
    #         # blur player detection
    #         kernel = np.ones((3, 3), np.float32) / 9
    #         playerb = cv2.filter2D(playerb, -1, kernel)
    #
    #         # crop heads
    #         ratio = int(playerb.shape[0] / 7)
    #
    #         playerb = playerb[ratio:, :, :]
    #
    #
    #         # cv2.imshow('', playerb)
    #         # cv2.waitKey(0)
    #
    #         # let's do a more efficient histogram by
    #         # utilizing only 10 bins per-channel
    #         histograms.append([cv2.calcHist([playerb], channels=[i], mask=None, histSize=[n_bins], ranges=[0, 256])
    #                            for i in range(3)])
    #
    #     X = [np.array(h).flatten() for h in histograms]
    #     # for x in X:
    #     #     print(x)
    #     self.dbscan.fit(X)
    #     print(self.dbscan.labels_)
    #     # filter out noise
    #     X = [x for i, x in enumerate(X) if self.dbscan.labels_[i] != -1]
    #     unrecognized_players = []
    #     for d in self.dbscan.labels_:
    #         if d == -1:
    #             unrecognized_players.append(False)
    #         else:
    #             unrecognized_players.append(True)
    #
    #     if len(X) > 0:
    #         self.kmeans.fit(X)
    #         print(self.kmeans.labels_)
    #     else:
    #         self.kmeans.labels_ = []
    #         self.kmeans.inertia_ = 1e11
    #
    #     if value_search:
    #         return self.kmeans.labels_, unrecognized_players, self.kmeans.inertia_
    #     else:
    #         return self.kmeans.labels_, unrecognized_players

# t = TeamRecognizer(eps=.2)
# image = cv2.imread('/Volumes/Samsung128/Pictures/tesla.png')
# cv2.imshow('', image)
# cv2.waitKey(0)
# # t.detect([[600, i*10+100, 25, 25] for i in range(4)], image)
# t.detect_teams(image, [[600, i*10+100, 25, 25] for i in range(4)])
