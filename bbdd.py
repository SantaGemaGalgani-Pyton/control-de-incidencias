import sqlite3

# Conexión a la base de datos (archivo local)
conn = sqlite3.connect("incidencias.db")
cursor = conn.cursor()

# Crear tabla Estado
cursor.execute("""
CREATE TABLE IF NOT EXISTS Estado (
    Numero INTEGER PRIMARY KEY,
    Nombre TEXT NOT NULL
)
""")

# Crear tabla Niveles
cursor.execute("""
CREATE TABLE IF NOT EXISTS Niveles (
    Numero INTEGER PRIMARY KEY,
    Descripcion_Detallada TEXT NOT NULL
)
""")

# Crear tabla Incidencia
cursor.execute("""
CREATE TABLE IF NOT EXISTS Incidencia (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Titulo TEXT NOT NULL,
    Descripcion_Detallada TEXT,
    Nivel INTEGER,
    Fecha_y_Hora TEXT NOT NULL,
    Estado INTEGER,
    FOREIGN KEY (Nivel) REFERENCES Niveles(Numero),
    FOREIGN KEY (Estado) REFERENCES Estado(Numero)
)
""")

# Insertar datos de ejemplo en Estado
estados = [
    (1, "Pendiente"),
    (2, "En Proceso"),
    (3, "Resuelto")
]
cursor.executemany("INSERT OR IGNORE INTO Estado (Numero, Nombre) VALUES (?, ?)", estados)

# Insertar datos de ejemplo en Niveles
niveles = [
    (1, "Bajo"),
    (2, "Medio"),
    (3, "Alto")
]
cursor.executemany("INSERT OR IGNORE INTO Niveles (Numero, Descripcion_Detallada) VALUES (?, ?)", niveles)

# Insertar datos de ejemplo en Incidencia
incidencias = [
    ("Falla de conexión", "No se puede conectar a internet", 2, "2025-10-10 09:00:00", 1),
    ("Error de software", "El programa se cierra solo", 3, "2025-10-10 10:15:00", 2)
]
cursor.executemany("""
INSERT INTO Incidencia (Titulo, Descripcion_Detallada, Nivel, Fecha_y_Hora, Estado)
VALUES (?, ?, ?, ?, ?)
""", incidencias)

# Confirmar cambios y cerrar conexión
conn.commit()
conn.close()

print("Base de datos creada con éxito.")
