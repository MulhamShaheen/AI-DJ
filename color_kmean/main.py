from sklearn.cluster import KMeans
import numpy as np
from collections import Counter
import cv2

NOTES_COLORS = {"C": [255, 0, 0],  # C
                "F": [171, 0, 52],  # F
                "Bb":[169, 103, 124],  # Bb
                "Eb":[183, 70, 139],  # Eb
                "Ab":[187, 117, 252],  # Ab
                "Db":[144, 0, 255],  # Db
                "Gb":[127, 139, 253],  # F#/Gb
                "B": [142, 201, 255],  # B
                "E": [195, 242, 255],  # E
                "A": [51, 204, 51],  # A
                "D": [255, 255, 0],  # D
                "G": [255, 127, 0]}  # G


def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))


def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


def get_colors(image, number_of_colors, show_chart):
    modified_image = cv2.resize(image, (600, 400), interpolation=cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0] * modified_image.shape[1], 3)

    clf = KMeans(n_clusters=number_of_colors)
    labels = clf.fit_predict(modified_image)

    counts = Counter(labels)
    # sort to ensure correct color percentage
    counts = dict(sorted(counts.items()))

    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]

    return rgb_colors


def get_notes(color):
    diffs = []
    notes_values = list(NOTES_COLORS.values())
    notes_keys = list(NOTES_COLORS.keys())
    for i in range(len(NOTES_COLORS)):

        diff = notes_values[i] - color
        diff = np.abs(diff)
        diff = sum(diff)
        diffs.append(diff)
    index = diffs.index(min(diffs))
    return notes_keys[i]


# rgb_colors = get_colors(get_image('sample_image.jpg'), 8, False)
# print(get_notes(rgb_colors[1]))
