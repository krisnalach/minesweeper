# Taken from tutorial video: https://www.youtube.com/watch?v=L8ypSXwyBds

import matplotlib.pyplot as plt
from IPython import display

plt.ion()


def plot(scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title("Training...")
    plt.xlabel("Number of Game sets (of 100)")
    plt.ylabel("Win Rate over game set")
    plt.plot(scores)
    plt.ylim(ymin=0)
    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.pause(0.05)
