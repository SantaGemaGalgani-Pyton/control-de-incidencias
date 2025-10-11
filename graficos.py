import matplotlib.pyplot as plt

def GraficoTipoDeIncidencias(tipoIncidenciaYCuenta: list[tuple[str, int, str]], titulo:str):
    """ valoresX y valoresY son Arrays de numpy
    """

    labels = ["Bajo", "Medio", "Alto"]
    sizes = [33, 12, 4]
    colors = ["#75DAFF", "#FFFF88", "#FF8A96"]
    # Pastel azul, amarillo y rojo
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
    ax.set_title(titulo)
    ax.axis("equal")
    plt.show()
    return ax


def GraficoEstadoDeIncidencias(tipoIncidenciaYCuenta: list[tuple[str, int]], titulo: str):
    labels, sizes = zip(*tipoIncidenciaYCuenta)   

    fig, ax = plt.subplots()
    x_pos = range(len(labels))
    ax.bar(x_pos, sizes, color="#75DAFF")  # you can customize colors per bar if needed
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels)
    ax.set_title(titulo)
    plt.show()
    return ax

tipoIncidenciaYCuenta = [
    ("Bajo", 33),   # Blue
    ("Medio", 12),  # Yellow
    ("Alto", 4)     # Red
]

GraficoEstadoDeIncidencias(tipoIncidenciaYCuenta, "hola")
#GraficoLineas(10, 40, ["enero", "febrero","marzo","abril"], [1, 3, 1, 1])