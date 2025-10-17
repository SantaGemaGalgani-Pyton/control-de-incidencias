import matplotlib.pyplot as plt
import csv
from matplotlib.figure import Figure
import os;

def GraficoNivelDeIncidencias(tipoIncidenciaYCuenta: list[tuple[str, int, str]], mostrar:bool):
    """Devuelve un gráfico circular con las incidencias categorizadas por su tipo
    \ntipoIncidenciaYCuenta es una lista de 'tipo','numero','color'
    """
    labels, sizes, colors = zip(*tipoIncidenciaYCuenta)   

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
    ax.set_title("Incidencias de este último mes por gravedad")
    ax.axis("equal")
    if mostrar:
        plt.show()

    ExportarAPDF(fig)
    ExportarACSV(["Tipo","Numero","Color"], tipoIncidenciaYCuenta)

    return fig

def GraficoEstadoDeIncidencias(tipoIncidenciaYCuenta: list[tuple[str, int]], mostrar: bool):
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
    if mostrar:
        plt.show()
    return fig

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