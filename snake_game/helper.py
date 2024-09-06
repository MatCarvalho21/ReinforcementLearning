import matplotlib.pyplot as plt
import IPython.display as display

import matplotlib
matplotlib.use('TkAgg')

plt.ion()

def plot(scores, mean_scores, move_mean):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.plot(move_mean)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    plt.text(len(move_mean)-1, move_mean[-1], str(move_mean[-1]))
    plt.show(block=False)
    plt.pause(.1)