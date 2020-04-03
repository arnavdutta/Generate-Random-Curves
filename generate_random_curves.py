
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from itertools import combinations
import random
import numpy as np
import cv2


def generate_random_curves_arr():
    def draw_curve(point1, point2):
        try:
            den = abs(np.cosh(point2[0]) - np.cosh(point1[0]))
            if den == 0:
                den = 0.001
            a = abs(point2[1] - point1[1]) / den
            b = point1[1] - a * np.cosh(point1[0])
            x = np.linspace(point1[0], point2[0], 900)
            y = a * np.cosh(x) + abs(b)
        except Exception as e:
            print(e)
        return (x, y)

    # random curves image array dimensions
    img_rows, img_cols = 32, 60

    x_coords = [random.randint(1, img_rows) for x in range(random.randint(2, 5000))]
    y_coords = [random.randint(1, img_cols) for y in range(len(x_coords))]

    coordinates = list(zip(x_coords, y_coords))
    combination = list(combinations(coordinates, 2))
    if len(combination) > 5:
        combination = random.sample(combination, 5)
    fig, ax = plt.subplots()
    for c in combination:
        x, y = draw_curve(c[0], c[1])
        ax.plot(x, y, 'k', linewidth=random.randint(1, 8))
        ax.axis('off')
        canvas = FigureCanvas(fig)
        canvas.draw()
        plot_img_arr = np.frombuffer(canvas.tostring_rgb(), dtype='uint8').reshape(fig.canvas.get_width_height()[::-1] + (3,))
        plt.close()
        plot_img_arr = cv2.cvtColor(plot_img_arr, cv2.COLOR_BGR2GRAY)

    ax.clear()
    fig.delaxes(ax)
    random_curves_arr = plot_img_arr
    random_curves_arr = cv2.resize(random_curves_arr, (img_cols, img_rows), interpolation=cv2.INTER_AREA)
    random_curves_arr = cv2.threshold(random_curves_arr, 0, 255, cv2.THRESH_OTSU)[1]
    return random_curves_arr
