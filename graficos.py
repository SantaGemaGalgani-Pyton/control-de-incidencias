import matplotlib.pyplot as plt

def GraficoTipoDeIncidencias(tipoIncidenciaYCuenta: list[tuple[str, int, str]], titulo):
    """ valoresX y valoresY son Arrays de numpy
    """

    labels = ["Bajo", "Medio", "Alto"]
    sizes = [33, 12, 4]
    colors = ["#75DAFF", "#FFFF88", "#FF8A96"]
    # Pastel azul, amarillo y rojo

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
    ax.title(titulo)
    ax.axis("equal")
    return ax

#GraficoLineas(10, 40, ["enero", "febrero","marzo","abril"], [1, 3, 1, 1])
