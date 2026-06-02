# 🌳 AVL Tree Visualizer

¡Bienvenido al **Visualizador Interactivo de Árboles AVL**! Esta es una aplicación de escritorio avanzada desarrollada en Python utilizando **Tkinter** que permite comprender de forma gráfica, interactiva y analítica cómo funcionan las estructuras de datos auto-balanceables (Árboles AVL).

La aplicación permite insertar, buscar y analizar nodos, mostrando en tiempo real los cambios en las alturas, factores de equilibrio y simulando paso a paso las rotaciones necesarias para mantener el árbol óptimo.

---

## ✨ Características Principales

* **Visualización Dinámica:** Cada nodo muestra explícitamente su **Valor**, su **Altura ($h$)** y su **Factor de Equilibrio ($FE$)** actualizados en tiempo real.
* **Dos Modos de Balanceo:**
    * **Modo Automático:** Las inserciones y rotaciones ocurren instantáneamente al presionar un botón.
    * **Modo Paso a Paso:** Una simulación interactiva completa que permite **Pausar/Reanudar**, avanzar manualmente mediante el botón de **Siguiente Paso** y controlar la velocidad del temporizador a través de un slider en milisegundos.
* **Generador Aleatorio:** Inserta conjuntos masivos de datos (entre 5 y 20 nodos concurrentes con valores únicos aleatorios) para poner a prueba el algoritmo de balanceo de forma inmediata.
* **Panel de Log (Consola):** Registro detallado tipo terminal que describe textualmente cada evaluación matemática y rotación ejecutada ($Izq-Izq$, $Der-Der$, $Izq-Der$, $Der-Izq$).
* **Módulo de Reportes y Salidas:**
    * 📷 **Exportación a PNG:** Guarda capturas de pantalla exactas de la estructura del árbol sin dependencias externas complejas.
    * 📄 **Exportación a PDF:** Genera un reporte analítico formal que incluye tablas de métricas de la estructura y los recorridos matemáticos (**Inorden**, **Preorden**, **Postorden**).
    * 🖨️ **Impresión Física:** Envía el estado del árbol y el historial de logs directamente a la cola de impresión de tu sistema operativo.

---

## 📦 Librerías del Sistema

El proyecto está construido combinando componentes nativos del lenguaje con librerías externas de la comunidad para la gestión avanzada de archivos y reportes:

### 1. Librerías Nativas (Vienen instaladas por defecto con Python)
* **`tkinter`**: Encargada de renderizar toda la interfaz gráfica de usuario (ventanas, botones, canvas y sliders).
* **`os` y `sys`**: Utilizadas para gestionar rutas de archivos temporales y detectar el sistema operativo al mandar a imprimir.
* **`random`**: Utilizada para seleccionar la cantidad de nodos y los valores numéricos únicos en el botón aleatorio.

### 2. Librerías Externas (Instalación Requerida)
* **`reportlab`** *(La librería para el PDF)*: Es el estándar de la industria en Python. Se encarga de maquetar, estructurar y generar el documento `.pdf` con tablas de diseño y texto estilizado para las estadísticas del árbol.
* **`pillow` (PIL)**: Utilizada por el módulo de imagen para capturar de forma nativa los píxeles del canvas (`ImageGrab`) y salvarlos directamente en formato `.png` de manera limpia.

---

## 🛠️ Instalación y Requisitos

La aplicación requiere **Python 3.11+** y la descarga de sus dos dependencias externas principales.

### 1. Clonar o ubicarse en el proyecto
Abre tu terminal o consola de comandos y navega hasta el directorio raíz del proyecto:
```bash
cd AVL-Visualizer