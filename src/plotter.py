import matplotlib.pyplot as plt
import IPython.display as display

plt.ion()

def plot(scores, avg_scores):
    display.display(plt.gcf())
    display.clear_output(wait=True)
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Episodes')
    plt.ylabel('Score')
    plt.plot(scores, color='darkturquoise')
    plt.plot(avg_scores, color='darkorange')
    plt.ylim(ymin=0)
    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.text(len(avg_scores) - 1, avg_scores[-1], str(avg_scores[-1]))
