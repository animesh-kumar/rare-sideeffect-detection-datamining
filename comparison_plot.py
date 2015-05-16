__author__ = 'animeshk'
# !/usr/bin/env python
# a bar plot with errorbars
import numpy as np
import matplotlib.pyplot as plt


class ComparisonPlot:
    def plot_graph(self, userRanks, expertRanks, sideeffects):
        N = 10
        # userRanks = (20, 35, 30, 35, 27)

        ind = np.arange(N)  # the x locations for the groups
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, userRanks, width, color='r')


        # expertRanks = (25, 32, 34, 20, 25)
        rects2 = ax.bar(ind + width, expertRanks, width, color='y')

        # add some text for labels, title and axes ticks
        ax.set_ylabel('Ranking')
        ax.set_title('Comparison between user and expert rankings')
        ax.set_xticks(ind + width)
        # ax.set_xticklabels( ('G1', 'G2', 'G3', 'G4', 'G5') )
        ax.set_xticklabels(sideeffects, rotation=30)

        ax.legend((rects1[0], rects2[0]), ('User Ranking', 'Expert Ranking'))

        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height, '%d' % int(height),
                        ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)

        plt.show()
