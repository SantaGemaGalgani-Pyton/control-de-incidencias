from datetime import date, timedelta
import sqlite3

class BaseDeDatos():
    def __init__(self):
        self.crear_bbdd()
        pass


    def crear_bbdd(self):
        """
        Va creando una a una todas las tablas de la base de datos, metiéndole valores por defecto
        """
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
                cursor.execute("INSERT INTO Estado (Nombre) VALUES (?)", (estado,))
            conn.commit()
            print("Estados insertados")

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Usuarios'")
        foundUsuarios = cursor.fetchone()
        if (not foundUsuarios):
            cursor.execute("""
            CREATE TABLE Usuarios (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Nombre TEXT,
                Pass TEXT )""")
            conn.commit()
            cursor.execute("INSERT INTO Usuarios (Nombre, Pass) Values (?, ?)", ("Admin", "Admin123"))
            conn.commit()
            print("Admin insertado")


        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Niveles'")
        foundNiveles = cursor.fetchone()
        if (not foundNiveles):
            cursor.execute("""
            CREATE TABLE Niveles (
                Numero INTEGER PRIMARY KEY,
                Descripcion_Detallada TEXT NOT NULL UNIQUE ,
                Color TEXT )""")
            conn.commit()
            
            niveles = [("Bajo", "#75DAFF"), ("Medio", "#FFFF88"), ("Alto", "#FF8A96")]
            for nivel in niveles:
                cursor.execute("INSERT INTO Niveles (Descripcion_Detallada, Color) VALUES (?, ?)", (nivel[0], nivel[1]))
            conn.commit()
            print("Niveles insertados")

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Incidencia'")
        foundIncidencias = cursor.fetchone()
        if (not foundIncidencias):
            cursor.execute("""
            CREATE TABLE Incidencia (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Descripcion_Detallada TEXT,
            Nivel INTEGER,
            fecha_creacion TEXT NOT NULL,
            fecha_resolucion TEXT,
            Estado INTEGER,
            FOREIGN KEY (Nivel) REFERENCES Niveles(Numero),
            FOREIGN KEY (Estado) REFERENCES Estado(Numero) )""")
            conn.commit()

            self.crear_incidencia("Descripcion detallada 1", 1, date.today(), 2)
            self.crear_incidencia("Descripcion detallada 2", 2, date.today(), 3)
            self.crear_incidencia("Descripcion detallada 3", 3, date.today(), 3)
            self.crear_incidencia("Descripcion detallada 4", 1, date.today(), 3)
            self.crear_incidencia("Descripcion detallada 5", 2, date.today(), 1)

            print("Base de datos creada con éxito")

        conn.close()
        pass

    def todos_los_estados(self):
        conn = sqlite3.connect("incidencias.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Estado")
        filas = cursor.fetchall()
        conn.close()
        return filas


    def anadir_usuario(self, nombre: str, passw: str):
        """
        Añade usuarios a la base de datos
        """
        conn = sqlite3.connect("incidencias.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Usuarios VALUES (?, ?)", nombre, passw)
        conn.close()

    def consultar_todas(self):
        """
        Consulta todas las incidencias de la base de datos.
        \nDevuelve su descripción, la fecha de creación y de resolución, y los nombres de estados y niveles
        """
        conn = sqlite3.connect("incidencias.db")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT i.Descripcion_Detallada, n.Descripcion_Detallada, i.fecha_creacion, i.fecha_resolucion, e.Nombre
        FROM Incidencia i
        LEFT JOIN Niveles n ON i.Nivel = n.Numero
        LEFT JOIN Estado e ON i.Estado = e.Numero
        """)
        filas = cursor.fetchall()
        conn.close()
        return filas
    
    def consultar_todas_id(self):
        """
        Consulta todas las incidencias de la base de datos.
        \nDevuelve su id, su descripción, la fecha de creación y de resolución, y los nombres de estados y niveles
        """
        conn = sqlite3.connect("incidencias.db")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT i.ID, i.Descripcion_Detallada, n.Descripcion_Detallada, i.fecha_creacion, i.fecha_resolucion, e.Nombre
        FROM Incidencia i
        LEFT JOIN Niveles n ON i.Nivel = n.Numero
        LEFT JOIN Estado e ON i.Estado = e.Numero
        """)
        filas = cursor.fetchall()
        conn.close()
        return filas

    def consultar_por_estado(self, estado_nombre: str):
        """
        Devuelve todas las incidencias que tengan el estado indicado
        """
        conn = sqlite3.connect("incidencias.db")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT i.Descripcion_Detallada, n.Descripcion_Detallada, i.fecha_creacion, i.fecha_resolucion, e.Nombre
        FROM Incidencia i
        LEFT JOIN Niveles n ON i.Nivel = n.Numero
        LEFT JOIN Estado e ON i.Estado = e.Numero
        WHERE e.Nombre = ?
        """, (estado_nombre,))
        filas = cursor.fetchall()
        conn.close()
        return filas

    def consultar_por_nivel(self, nivel_descripcion: str):
        """
        Devuelve todas las incidencias que tengan el nivel de gravedad indicado
        """
        conn = sqlite3.connect("incidencias.db")
        cursor = conn.cursor()
        cursor.execute("""
        SELECT i.Descripcion_Detallada, n.Descripcion_Detallada, i.fecha_creacion, i.fecha_resolucion, e.Nombre
        FROM Incidencia i
        LEFT JOIN Niveles n ON i.Nivel = n.Numero
        LEFT JOIN Estado e ON i.Estado = e.Numero
        WHERE n.Descripcion_Detallada = ?
        """, (nivel_descripcion,))
        filas = cursor.fetchall()
        conn.close()
        return filas
    
    def borrar_incidencia(self, id: int):
        """
        Borra la incidencia con el ID especificado
        """
        conn = sqlite3.connect("incidencias.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Incidencias WHERE ID = ?", id)
        conn.close()

    def actualizar_estado(self, id_incidencia: int, nuevo_estado_num: int):
        """
        Actualiza el estado de la incidencia con el ID especificado al estado especificado
        """
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

    def borrar_incidencia(self, id_incidencia: int):
        """
        Borra la incidencia con el ID especificado
        """
        conn = sqlite3.connect("incidencias.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Incidencia WHERE ID = ?", (id_incidencia,))
        conn.commit()
        conn.close()
        print(f"Incidencia {id_incidencia} eliminada")

    def crear_incidencia(self, descripcion_detallada, nivel, fecha, estado=1):
        """
        Crea una nueva incidencia con la información especificada. El estado 1 es 'Pendiente'
        """
        conn = sqlite3.connect("incidencias.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Incidencia (Descripcion_Detallada, Nivel, fecha_creacion, fecha_resolucion, Estado)
            VALUES (?, ?, ?, ?, ?)""",                       
            (descripcion_detallada, nivel, fecha, None, estado))
        conn.commit()
        conn.close()

    def nombres_niveles(self):
        conn = sqlite3.connect("incidencias.db")
        cursor = conn.cursor()
        cursor.execute("SELECT Descripcion_Detallada from Niveles ORDER BY Numero")
        filas = cursor.fetchall()
        conn.close()
        return filas

    def incidencias_gravedad(self):
        conn = sqlite3.connect("incidencias.db")
        cursor = conn.cursor()
        dias = self.diasDelMesHastaHoy()
        diasQ = ",".join("?" * len(dias))
        cursor.execute(f"""
        SELECT n.Descripcion_Detallada, COUNT(*) AS total, n.Color
        FROM INCIDENCIA i
        LEFT JOIN Niveles n ON i.Nivel = n.Numero
        WHERE i.fecha_creacion IN({diasQ})
        GROUP BY i.Nivel
        """, self.diasDelMesHastaHoy())
        filas = cursor.fetchall()
        print(filas)
        conn.close()
        return filas

    def incidencias_estado(self):
        conn = sqlite3.connect("incidencias.db")
        cursor = conn.cursor()
        dias = self.diasDelMesHastaHoy()
        diasQ = ",".join("?" * len(dias))
        cursor.execute(f"""
        SELECT e.Nombre, COUNT(*) AS total
        FROM INCIDENCIA i
        LEFT JOIN Estado e ON i.Estado = e.Numero
        WHERE i.fecha_creacion IN({diasQ})
        GROUP BY i.Estado
        """, self.diasDelMesHastaHoy())
        filas = cursor.fetchall()
        print(filas)
        conn.close()
        return filas

    def usuario_password_existen(self, usuario :str, password :str):
        conn = sqlite3.connect("incidencias.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuarios WHERE Nombre=? AND Pass=?", (usuario, password))
        foundNiveles = cursor.fetchone()
        if (foundNiveles):
            return True
        else:
            return False
        
    def convertirFechaATexto(self, fecha: date):
        return fecha.strftime('%d-%m-%Y')

    def diasDelMesHastaHoy(self):
        hoy = date.today()
        cur = hoy.replace(day=1)
        dias = []
        while cur <= hoy:
            dias.append(self.convertirFechaATexto(cur))
            cur += timedelta(days=1)

        return dias