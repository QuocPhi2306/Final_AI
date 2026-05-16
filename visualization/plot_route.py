import matplotlib.pyplot as plt


def plot_route(coords, path, title="TSP Route", save_path=None, show=True):
    if len(coords) == 0:
        raise ValueError("Coords list is empty")
    if len(path) == 0:
        raise ValueError("Path list is empty")

    x = [coords[i][0] for i in path] + [coords[path[0]][0]]
    y = [coords[i][1] for i in path] + [coords[path[0]][1]]

    fig, ax = plt.subplots()
    ax.plot(x, y, '-o', color='tab:blue', markersize=8)

    for idx, (xi, yi) in enumerate(coords):
        ax.text(xi, yi, str(idx), fontsize=10, ha='right', va='bottom')

    ax.set_title(title)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    if show:
        plt.show()
    plt.close(fig)
