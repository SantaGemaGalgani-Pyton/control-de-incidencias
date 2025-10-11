import matplotlib.pyplot as plt

def GraficoTipoDeIncidencias(tipoIncidenciaYCuenta: list[tuple[str, int, str]], titulo):
    """ valoresX y valoresY son Arrays de numpy
    """

    labels = ["Bajo", "Medio", "Alto"]
    sizes = [33, 12, 4]
    colors = ["#75DAFF", "#FFFF88", "#FF8A96"]
    # Pastel azul, amarillo y rojo

    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
    plt.title(titulo)
    plt.axis("equal")
    plt.show()
    pass

GraficoTipoDeIncidencias(7, "Grafico de incidencias por tipo")

# plt.savefig('foo.png')
# plt.savefig('foo.pdf')