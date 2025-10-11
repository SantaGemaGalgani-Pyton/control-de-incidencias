import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as n
import ArrayUtils as au

# set_title es un titulo encima del grafico
# X y Y son titulos en horizontal y diagonal respect

def GraficoLineas(sizeX, sizeY, meses, valoresY, titulo = None, tituloX = None, tituloY = None):
    """ valoresX y valoresY son Arrays de numpy
    """
    fig, ax = plt.subplots(figsize=(sizeX, sizeY))
    bars = ax.bar(meses, valoresY, color="#060061")

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height - 0.1,
            str(height),
            ha='center', va='top',
            color='white', fontsize=10
    )

    ax.set_title(titulo)
    ax.set_xlabel(tituloX)
    ax.set_ylabel(tituloY)
    ax.set_yticks([])
    ax.set_yticklabels([])
    plt.show()
    pass

#GraficoLineas(10, 40, ["enero", "febrero","marzo","abril"], [1, 3, 1, 1])
