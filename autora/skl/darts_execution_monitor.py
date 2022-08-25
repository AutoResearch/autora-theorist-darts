from types import SimpleNamespace

import matplotlib.pyplot as plt
import numpy as np


class BasicExecutionMonitor:
    def __init__(self):
        self.arch_weight_history = list()
        self.loss_history = list()
        self.epoch_history = list()
        self.primitives = list()

    def execution_monitor(self, network, architect, epoch, **kwargs):
        # collect data for visualization
        self.epoch_history.append(epoch)
        self.arch_weight_history.append(
            network.arch_parameters()[0].detach().numpy().copy()[np.newaxis, :]
        )
        self.loss_history.append(architect.current_loss)
        self.primitives = network.primitives

    def display(self):

        loss_fig, loss_ax = plt.subplots(1, 1)
        loss_ax.plot(self.loss_history)

        loss_ax.set_ylabel("Loss", fontsize=14)
        loss_ax.set_xlabel("Epoch", fontsize=14)
        loss_ax.set_title("Training Loss")

        arch_weight_history_array = np.vstack(self.arch_weight_history)
        num_epochs, num_edges, num_primitives = arch_weight_history_array.shape

        subplots_per_side = int(np.ceil(np.sqrt(num_edges)))

        arch_fig, arch_axes = plt.subplots(
            subplots_per_side,
            subplots_per_side,
            sharex=True,
            sharey=True,
            figsize=(10, 10),
        )

        arch_fig.suptitle("Architecture Weights", fontsize=10)

        for (edge_i, ax) in zip(range(num_edges), arch_axes.reshape(-1)):
            for primitive_i in range(num_primitives):
                print(f"{edge_i}, {primitive_i}, {ax}")
                ax.plot(
                    arch_weight_history_array[:, edge_i, primitive_i],
                    label=f"{self.primitives[primitive_i]}",
                )

            ax.set_title("k{}".format(edge_i), fontsize=8)

            # there is no need to have the legend for each subplot
            if edge_i == 0:
                ax.legend(loc="upper center")
                ax.set_ylabel("Edge Weights", fontsize=8)
                ax.set_xlabel("Epoch", fontsize=8)

        return SimpleNamespace(
            loss_fig=loss_fig,
            loss_ax=loss_ax,
            arch_fig=arch_fig,
            arch_axes=arch_axes,
        )
