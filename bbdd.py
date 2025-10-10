import sqlite3

def crear_bd():
    conn = sqlite3.connect("incidencias.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Estado (
        Numero INTEGER PRIMARY KEY,
        Nombre TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Niveles (
        Numero INTEGER PRIMARY KEY,
        Descripcion_Detallada TEXT NOT NULL
    )
    """)

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

    estados = [
        (1, "Pendiente"),
        (2, "En Proceso"),
        (3, "Resuelto")
    ]
    cursor.executemany("INSERT OR IGNORE INTO Estado (Numero, Nombre) VALUES (?, ?)", estados)

    niveles = [
        (1, "Bajo"),
        (2, "Medio"),
        (3, "Alto")
    ]
    cursor.executemany("INSERT OR IGNORE INTO Niveles (Numero, Descripcion_Detallada) VALUES (?, ?)", niveles)

    incidencias = [
        ("Falla de conexión", "No se puede conectar a internet", 2, "2025-10-10 09:00:00", 1),
        ("Error de software", "El programa se cierra solo", 3, "2025-10-10 10:15:00", 2)
    ]
    cursor.executemany("""
    INSERT INTO Incidencia (Titulo, Descripcion_Detallada, Nivel, Fecha_y_Hora, Estado)
    VALUES (?, ?, ?, ?, ?)
    """, incidencias)

    conn.commit()
    conn.close()
    print("Base de datos creada con éxito.")

def consultar_todas():
    conn = sqlite3.connect("incidencias.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT i.ID, i.Titulo, i.Descripcion_Detallada, n.Descripcion_Detallada, i.Fecha_y_Hora, e.Nombre
    FROM Incidencia i
    LEFT JOIN Niveles n ON i.Nivel = n.Numero
    LEFT JOIN Estado e ON i.Estado = e.Numero
    """)
    filas = cursor.fetchall()
    conn.close()
    return filas

def consultar_por_estado(estado_nombre):
    conn = sqlite3.connect("incidencias.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT i.ID, i.Titulo, i.Descripcion_Detallada, n.Descripcion_Detallada, i.Fecha_y_Hora, e.Nombre
    FROM Incidencia i
    LEFT JOIN Niveles n ON i.Nivel = n.Numero
    LEFT JOIN Estado e ON i.Estado = e.Numero
    WHERE e.Nombre = ?
    """, (estado_nombre,))
    filas = cursor.fetchall()
    conn.close()
    return filas

def consultar_por_nivel(nivel_descripcion):
    conn = sqlite3.connect("incidencias.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT i.ID, i.Titulo, i.Descripcion_Detallada, n.Descripcion_Detallada, i.Fecha_y_Hora, e.Nombre
    FROM Incidencia i
    LEFT JOIN Niveles n ON i.Nivel = n.Numero
    LEFT JOIN Estado e ON i.Estado = e.Numero
    WHERE n.Descripcion_Detallada = ?
    """, (nivel_descripcion,))
    filas = cursor.fetchall()
    conn.close()
    return filas

def actualizar_estado(id_incidencia, nuevo_estado_num):
    conn = sqlite3.connect("incidencias.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Incidencia SET Estado = ? WHERE ID = ?", (nuevo_estado_num, id_incidencia))
    conn.commit()
    conn.close()
    print(f"Incidencia {id_incidencia} actualizada al estado {nuevo_estado_num}")

def borrar_incidencia(id_incidencia):
    conn = sqlite3.connect("incidencias.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Incidencia WHERE ID = ?", (id_incidencia,))
    conn.commit()
    conn.close()
    print(f"Incidencia {id_incidencia} eliminada")

if __name__ == "__main__":
    crear_bd()

    print("\nTodas las incidencias:")
    for fila in consultar_todas():
        print(fila)

    print("\nIncidencias con estado 'Pendiente':")
    for fila in consultar_por_estado("Pendiente"):
        print(fila)

    print("\nIncidencias con nivel 'Alto':")
    for fila in consultar_por_nivel("Alto"):
        print(fila)

    print("\nActualizar estado de la incidencia ID=1 a 'Resuelto' (3):")
    actualizar_estado(1, 3)

    print("\nEliminar la incidencia ID=2:")
    borrar_incidencia(2)

    print("\nTodas las incidencias tras modificaciones:")
    for fila in consultar_todas():
        print(fila)
