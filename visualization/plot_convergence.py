import matplotlib.pyplot as plt


def plot_convergence(history, title="BA Convergence", save_path=None, show=True):
    if not history:
        raise ValueError("History list is empty")

    fig, ax = plt.subplots()
    ax.plot(range(len(history)), history, marker='o', color='tab:orange')
    ax.set_title(title)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Best Cost')
    ax.grid(True)

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if show:
        plt.show()
    plt.close(fig)
