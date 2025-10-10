import sqlite3

def crear_bd():
    conn = sqlite3.connect("incidencias.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Estado (
        Numero INTEGER PRIMARY KEY,
        Nombre TEXT NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Niveles (
        Numero INTEGER PRIMARY KEY,
        Descripcion_Detallada TEXT NOT NULL UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Incidencia (
        ID INTEGER PRIMARY KEY,
        Titulo TEXT NOT NULL,
        Descripcion_Detallada TEXT,
        Nivel INTEGER,
        Fecha_y_Hora TEXT NOT NULL,
        Estado INTEGER,
        FOREIGN KEY (Nivel) REFERENCES Niveles(Numero),
        FOREIGN KEY (Estado) REFERENCES Estado(Numero)
    )
    """)

    # Insertar estados
    estados = ["Pendiente", "En Proceso", "Resuelto"]
    for estado in estados:
        cursor.execute("INSERT OR IGNORE INTO Estado (Nombre) VALUES (?)", (estado,))

    # Insertar niveles
    niveles = ["Bajo", "Medio", "Alto"]
    for nivel in niveles:
        cursor.execute("INSERT OR IGNORE INTO Niveles (Descripcion_Detallada) VALUES (?)", (nivel,))

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
    
    # Verificar si la incidencia existe
    cursor.execute("SELECT ID FROM Incidencia WHERE ID = ?", (id_incidencia,))
    if cursor.fetchone() is None:
        print(f"Error: No existe la incidencia con ID {id_incidencia}.")
        conn.close()
        return
    
    # Verificar si el nuevo estado existe
    cursor.execute("SELECT Numero FROM Estado WHERE Numero = ?", (nuevo_estado_num,))
    if cursor.fetchone() is None:
        print(f"Error: No existe el estado con ID {nuevo_estado_num}.")
        conn.close()
        return
    
    # Actualizar estado
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
    # Crear base de datos e insertar datos, obtener IDs insertados
    ids = crear_bd()

    print("\nTodas las incidencias:")
    for fila in consultar_todas():
        print(fila)

    print("\nIncidencias con estado 'Pendiente':")
    for fila in consultar_por_estado("Pendiente"):
        print(fila)

    print("\nIncidencias con nivel 'Alto':")
    for fila in consultar_por_nivel("Alto"):
        print(fila)

    # Obtener el ID del estado "Resuelto"
    conn = sqlite3.connect("incidencias.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Numero FROM Estado WHERE Nombre = ?", ("Resuelto",))
    resuelto_id = cursor.fetchone()[0]
    conn.close()

    if ids:
        id_a_actualizar = ids[0]  # Actualizamos la primera incidencia insertada
        print(f"\nActualizar estado de la incidencia ID={id_a_actualizar} a 'Resuelto' (ID estado={resuelto_id}):")
        actualizar_estado(id_a_actualizar, resuelto_id)

        if len(ids) > 1:
            print(f"\nEliminar la incidencia ID={ids[1]}:")
            borrar_incidencia(ids[1])
        else:
            print("No hay segunda incidencia para eliminar.")
    else:
        print("No hay incidencias para actualizar o eliminar.")

    print("\nTodas las incidencias tras modificaciones:")
    for fila in consultar_todas():
        print(fila)
