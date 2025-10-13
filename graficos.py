import matplotlib.pyplot as plt
import csv
from matplotlib.figure import Figure
import os;

def GraficoNivelDeIncidencias(tipoIncidenciaYCuenta: list[tuple[str, int, str]]):
    """Devuelve un gráfico circular con las incidencias categorizadas por su tipo
    \ntipoIncidenciaYCuenta es una lista de 'tipo','numero','color'
    """
    labels, sizes, colors = zip(*tipoIncidenciaYCuenta)   

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
    ax.set_title("Incidencias de este último mes por gravedad")
    ax.axis("equal")
    plt.show()

    ExportarAPDF(fig)
    ExportarACSV(["Tipo","Numero","Color"], tipoIncidenciaYCuenta)

    return ax


def GraficoEstadoDeIncidencias(tipoIncidenciaYCuenta: list[tuple[str, int]]):
    """Devuelve un gráfico de barras con las incidencias categorizadas por su nivel
    \ntipoIncidenciaYCuenta es una lista de 'estado','numero'
    """
    labels, sizes = zip(*tipoIncidenciaYCuenta)   

    fig, ax = plt.subplots()
    x_pos = range(len(labels))
    ax.bar(x_pos, sizes, color="#75DAFF")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels)
    ax.set_title("Incidencias de este último mes por estado")
    plt.show()
    return ax

def ExportarAPDF(figura: Figure):
    """Exporta la figura del gráfico a pdf, automáticamente a la carpeta descargas, bajo el nombre 'grafico.pdf'
    """
    carpetaDescargas = os.path.join(os.path.expanduser("~"), "Downloads")
    ruta = os.path.join(carpetaDescargas, "grafico.pdf")
    figura.savefig(ruta, format="pdf")


def ExportarACSV(encabezado, contenido):
    """Exporta el contenido del gráfico a csv, automáticamente a la carpeta descargas, bajo el nombre 'grafico.csv'
    """
    carpetaDescargas = os.path.join(os.path.expanduser("~"), "Downloads")
    ruta = os.path.join(carpetaDescargas, "grafico.csv")
    f = open(ruta, "w", newline="", encoding="utf-8")
    writer = csv.writer(f)
    writer.writerow(encabezado)
    writer.writerows(contenido)
    f.close()

tipoIncidenciaYCuenta = [
    ("Resuelto", 33),
    ("En proceso", 12),
    ("Sin resolver", 4)
]

#GraficoEstadoDeIncidencias(tipoIncidenciaYCuenta)
tipoIncidenciaYCuenta2 = [
    ("Bajo", 12, "#FF0000"),
    ("Medio", 15, "#00FF00"),
    ("Alto", 40, "#0000FF")
]

GraficoNivelDeIncidencias(tipoIncidenciaYCuenta2)