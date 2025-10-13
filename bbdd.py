from datetime import date, timedelta
import sqlite3

class BaseDeDatos():
    def __init__(self):
        self.crear_bbdd()
        pass


    def crear_bbdd(self):
        conn = sqlite3.connect('incidencias.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Estado'")
        foundEstado = cursor.fetchone()
        if (not foundEstado):
            cursor.execute("""
            CREATE TABLE Estado (
                Numero INTEGER PRIMARY KEY,
                Nombre TEXT NOT NULL UNIQUE )""")
            conn.commit()
            
            estados = ["Pendiente", "En Proceso", "Resuelto"]
            for estado in estados:
                cursor.execute("INSERT OR IGNORE INTO Estado (Nombre) VALUES (?)", (estado,))
            print("Estados insertados")


        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Niveles'")
        foundEstado = cursor.fetchone()
        if (not foundEstado):
            cursor.execute("""
            CREATE TABLE Niveles (
                Numero INTEGER PRIMARY KEY,
                Descripcion_Detallada TEXT NOT NULL UNIQUE )""")
            conn.commit()
            
            niveles = ["Bajo", "Medio", "Alto"]
            for nivel in niveles:
                cursor.execute("INSERT OR IGNORE INTO Niveles (Descripcion_Detallada) VALUES (?)", (nivel,))

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Incidencia'")
        foundEstado = cursor.fetchone()
        if (not foundEstado):
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Incidencia (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Titulo TEXT NOT NULL,
            Descripcion_Detallada TEXT,
            Nivel INTEGER,
            Fecha_y_Hora TEXT NOT NULL,
            Estado INTEGER,
            FOREIGN KEY (Nivel) REFERENCES Niveles(Numero),
            FOREIGN KEY (Estado) REFERENCES Estado(Numero) )""")
            conn.commit()

            self.crear_incidencia("Titulo 1", "Descripcion detallada 1", 1, "2025-10-01 09:15:00", 1)
            self.crear_incidencia("Titulo 2", "Descripcion detallada 2", 2, "2025-10-03 11:30:00", 2)
            self.crear_incidencia("Titulo 3", "Descripcion detallada 3", 3, "2025-10-05 14:45:00", 3)
            self.crear_incidencia("Titulo 4", "Descripcion detallada 4", 1, "2025-10-07 08:20:00", 2)
            self.crear_incidencia("Titulo 5", "Descripcion detallada 5", 2, "2025-10-10 16:10:00", 1)

        conn.close()

        print("Base de datos creada con éxito.")
        pass

    def consultar_todas(self):
        conn = sqlite3.connect("incidencias.db")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT i.Titulo, i.Descripcion_Detallada, n.Descripcion_Detallada, i.Fecha_y_Hora, e.Nombre
        FROM Incidencia i
        LEFT JOIN Niveles n ON i.Nivel = n.Numero
        LEFT JOIN Estado e ON i.Estado = e.Numero
        """)
        filas = cursor.fetchall()
        conn.close()
        return filas

    def consultar_por_estado(self, estado_nombre):
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

    def consultar_por_nivel(self, nivel_descripcion):
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

    def actualizar_estado(self, id_incidencia, nuevo_estado_num):
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

    def borrar_incidencia(self, id_incidencia):
        conn = sqlite3.connect("incidencias.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Incidencia WHERE ID = ?", (id_incidencia,))
        conn.commit()
        conn.close()
        print(f"Incidencia {id_incidencia} eliminada")

    def crear_incidencia(self, titulo, descripcion_detallada, nivel, fecha_y_hora, estado):
        conn = sqlite3.connect("incidencias.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Incidencia (Titulo, Descripcion_Detallada, Nivel, Fecha_y_Hora, Estado)
            VALUES (?, ?, ?, ?, ?)""",                       
            (titulo, descripcion_detallada, nivel, fecha_y_hora, estado))
        conn.commit()
        conn.close()

    def diasDelMesHastaHoy(self):
        hoy = date.today()
        cur = hoy.replace(day=1)
        dias = []
        while cur <= hoy:
            dias.append(cur.strftime('%Y-%m-%d'))
            cur += timedelta(days=1)

        print(dias)
        return dias