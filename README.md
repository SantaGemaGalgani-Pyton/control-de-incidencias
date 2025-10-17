# control-de-incidencias


Sistema escrito en Python para gestionar incidencias (problemas, reclamaciones, eventos) mediante una interfaz gráfica y una base de datos local.

---

## Índice

- [Descripción](#descripción)  
- [Funcionalidades](#funcionalidades)  
- [Estructura del proyecto](#estructura-del-proyecto)  
- [Requisitos](#requisitos)  
- [Instalación](#instalación)  
- [Uso](#uso)  
- [Bases de datos](#bases-de-datos)  
- [Contribuciones](#contribuciones)  
- [Licencia](#licencia)  

---

## Descripción

Este proyecto permite:

- Registrar nuevos usuarios  
- Iniciar sesión  
- Crear, editar y eliminar incidencias  
- Visualizar gráficas de los estados de las incidencias  
- Conexion con una base de datos SQLite  
- Interfaz gráfica creada con módulos de Python  

Está pensado como una herramienta de aprendizaje o para proyectos pequeños de control interno de incidencias.

---

## Funcionalidades principales

- Registro y autenticación de usuarios  
- Alta, modificación y baja de incidencias  
- Consulta del historial de incidencias  
- Visualización gráfica de estadísticas  
- Interfaz de usuario GUI (ventana principal, formularios, gráficas)  
- Operaciones con arrays utilitarios  
- Gestión de borrado/limpieza  
- Uso de estructuras de datos como colas/circulares (según módulos)  
- Persistencia mediante archivo SQLite (`incidencias.db`)  

---

## Estructura del proyecto

```text
control-de-incidencias/
├── ArrayUtils.py
├── BorrarI.py
├── CircularG.py
├── Main.py
├── RegistroIncidencias.py
├── RegistroUsu.py
├── VentanaPrincipal.py
├── bbdd.py
├── graficos.py
├── incidencias.db
├── .gitignore
└── README.md
