# https://www.wolframalpha.com/examples/mathematics/geometry/curves-and-surfaces/
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from itertools import combinations
import random


def generate_curves():
    img_rows, img_cols = 32, 64

    def draw_random_curve(point1, point2):
        try:
            den = abs(np.sinh(point2[0]) - np.cosh(point1[0]))
            if den == 0:
                den = 0.001
            a = abs(point2[1] - point1[1]) / den
            b = point1[1] - a * np.cosh(point1[0])
            x = np.linspace(point1[0], point2[0], 500)
            y = a * np.cosh(x) + abs(b)
            return x, y
        except Exception as e:
            print(e)

    x_coords = [random.randint(1, img_rows) for x in range(random.randint(2, 1000))]
    y_coords = [random.randint(1, img_cols) for y in range(len(x_coords))]

    coordinates = list(zip(x_coords, y_coords))
    combination = list(combinations(coordinates, 2))
    if len(combination) > 5:
        combination = random.sample(combination, 5)
    fig, ax = plt.subplots()
    for c in combination:
        x, y = draw_random_curve(c[0], c[1])
        ax.plot(x, y, 'k', linewidth=random.randint(5, 8))
        ax.axis('off')
        canvas = FigureCanvas(fig)
        canvas.draw()
        plot_img_arr = np.frombuffer(canvas.tostring_rgb(), dtype='uint8').reshape(fig.canvas.get_width_height()[::-1] + (3,))
        plt.close()
    plot_img_arr = cv2.cvtColor(plot_img_arr, cv2.COLOR_BGR2GRAY)
    combination.clear()
    ax.clear()
    fig.delaxes(ax)
    noise = plot_img_arr
    noise = cv2.resize(noise, (img_cols, img_rows), interpolation=cv2.INTER_AREA)
    noise = cv2.threshold(noise, 0, 255, cv2.THRESH_OTSU)[1]
    return noise
