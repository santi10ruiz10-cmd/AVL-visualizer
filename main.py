import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys

# Importación de la lógica del árbol
from avl.avl_tree import ArbolAVL

# Importación condicional para PDF
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
except ImportError:
    pass


class AplicacionAVL:

    def __init__(self):
        # 1. Inicialización de la ventana raíz
        self.ventana = tk.Tk()
        self.ventana.title("Árbol AVL Interactivo Avanzado")
        self.ventana.geometry("1200x820")

        # 2. Inicialización del árbol lógico
        self.arbol = ArbolAVL()
        self.raiz = None

        # 3. Variables de control de animación y modos
        self.modo_automatico = tk.BooleanVar(value=True)
        self.en_pausa = False
        self.cola_pasos = []
        self.indice_paso = 0
        self.nodo_resaltado_actual = None
        self.color_resaltado = "lightblue"
        self.raiz_temporal = None  

        # 4. Construcción de los componentes visuales
        self.crear_componentes()

    def crear_componentes(self):
        titulo = tk.Label(self.ventana, text="Árbol AVL Interactivo", font=("Arial", 18, "bold"))
        titulo.pack(pady=5)

        # ---- BARRA DE CONTROL PRINCIPAL ----
        barra = tk.Frame(self.ventana)
        barra.pack(fill="x", padx=10, pady=5)

        tk.Label(barra, text="Valor:").pack(side="left", padx=2)
        self.entrada_valor = tk.Entry(barra, width=8)
        self.entrada_valor.pack(side="left", padx=5)

        tk.Button(barra, text="Insertar", command=self.insertar_nodo, bg="#4CAF50", fg="white").pack(side="left", padx=3)
        tk.Button(barra, text="Buscar", command=self.buscar_nodo).pack(side="left", padx=3)
        tk.Button(barra, text="Reiniciar", command=self.reiniciar_arbol, bg="#f44336", fg="white").pack(side="left", padx=3)
        tk.Button(barra, text="Cargar Ejemplo", command=self.cargar_ejemplo).pack(side="left", padx=3)
        
        # ¡BOTÓN ALEATORIO INTEGRADO AQUÍ!
        tk.Button(barra, text="🎲 Generar Aleatorio", command=self.generar_aleatorios, bg="#FF9800", fg="white").pack(side="left", padx=3)

        # ---- PANEL DE MODOS Y ANIMACIÓN ----
        panel_animacion = tk.LabelFrame(self.ventana, text=" Controles de Balanceo / Simulación ")
        panel_animacion.pack(fill="x", padx=10, pady=5)

        chk_auto = tk.Checkbutton(panel_animacion, text="Balanceo Automático", variable=self.modo_automatico, command=self.actualizar_visibilidad_controles)
        chk_auto.pack(side="left", padx=10)

        self.btn_pausa = tk.Button(panel_animacion, text="Pausar", command=self.toggle_pausa, state="disabled")
        self.btn_pausa.pack(side="left", padx=5)

        self.btn_siguiente = tk.Button(panel_animacion, text="Siguiente Paso ➡️", command=self.ejecutar_siguiente_paso, state="disabled")
        self.btn_siguiente.pack(side="left", padx=5)

        tk.Label(panel_animacion, text="Velocidad (ms):").pack(side="left", padx=(15, 2))
        self.slider_velocidad = tk.Scale(panel_animacion, from_=200, to=2000, orient="horizontal", length=150)
        self.slider_velocidad.set(800)
        self.slider_velocidad.pack(side="left", padx=5)

        # ---- PANEL DE EXPORTACIÓN ----
        panel_export = tk.LabelFrame(self.ventana, text=" Reportes y Salidas ")
        panel_export.pack(side="top", fill="x", padx=10, pady=5)

        tk.Button(panel_export, text="📷 Exportar Imagen (PNG)", command=self.exportar_png, bg="#2196F3", fg="white").pack(side="left", padx=10, pady=5)
        tk.Button(panel_export, text="📄 Exportar PDF (Métricas)", command=self.exportar_pdf, bg="#9C27B0", fg="white").pack(side="left", padx=10, pady=5)
        tk.Button(panel_export, text="🖨️ Imprimir Estructura", command=self.imprimir_arbol, bg="#607D8B", fg="white").pack(side="left", padx=10, pady=5)

        # Canvas de dibujo
        self.canvas = tk.Canvas(self.ventana, bg="white", height=380)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=5)

        # Consola de logs
        self.log = tk.Text(self.ventana, height=5, bg="#222", fg="#00FF00")
        self.log.pack(fill="x", padx=10, pady=5)

        self.escribir_log("Aplicación inicializada. Modo Automático Activo.")

    def generar_aleatorios(self):
        """Genera entre 5 y 20 nodos con valores únicos aleatorios."""
        import random
        
        self.reiniciar_arbol()
        cantidad = random.randint(5, 20)
        valores = random.sample(range(1, 100), cantidad)
        
        self.escribir_log(f"🎲 Generando {cantidad} nodos aleatorios: {valores}")
        
        if self.modo_automatico.get():
            for valor in valores:
                self.raiz = self.arbol.insertar(self.raiz, valor)
            self.dibujar_arbol()
            self.escribir_log("✨ Estructura aleatoria generada e insertada automáticamente.")
        else:
            self.escribir_log("⚠️ Modo Paso a Paso activo. Se iniciará la animación del PRIMER elemento generado.")
            self.entrada_valor.delete(0, tk.END)
            self.entrada_valor.insert(0, str(valores[0]))
            self.insertar_nodo()
            self.escribir_log(f"Resto de la secuencia disponible para pruebas manuales: {valores[1:]}")

    def exportar_png(self):
        """Exporta el Canvas a PNG usando captura directa de pixeles para evitar dependencias de Ghostscript."""
        if self.raiz is None:
            messagebox.showwarning("Exportar PNG", "El árbol está vacío. No hay nada que exportar.")
            return
            
        fichero = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Imagen PNG", "*.png")])
        if not fichero:
            return

        try:
            from PIL import ImageGrab
            self.ventana.update()
            
            x_inicial = self.canvas.winfo_rootx()
            y_inicial = self.canvas.winfo_rooty()
            x_final = x_inicial + self.canvas.winfo_width()
            y_final = y_inicial + self.canvas.winfo_height()
            
            imagen_arbol = ImageGrab.grab(bbox=(x_inicial, y_inicial, x_final, y_final))
            imagen_arbol.save(fichero, "png")
            
            self.escribir_log(f"Imagen exportada exitosamente en: {fichero}")
            messagebox.showinfo("Éxito", f"Imagen guardada como PNG:\n{fichero}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar la imagen: {str(e)}")

    def exportar_pdf(self):
        if 'reportlab' not in sys.modules:
            messagebox.showerror("Falta Dependencia", "Por favor instala reportlab ejecutando: pip install reportlab")
            return
        if self.raiz is None:
            messagebox.showwarning("Exportar PDF", "El árbol está vacío. Inserta nodos para generar métricas.")
            return

        fichero = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Documento PDF", "*.pdf")])
        if not fichero: return

        try:
            stats = self.arbol.obtener_estadisticas(self.raiz)
            doc = SimpleDocTemplate(fichero, pagesize=letter)
            estilos = getSampleStyleSheet()
            
            estilo_titulo = ParagraphStyle('DocTitle', parent=estilos['Title'], fontName='Helvetica-Bold', fontSize=24, textColor=colors.HexColor("#2196F3"), spaceAfter=20)
            estilo_h2 = ParagraphStyle('SectionHeader', parent=estilos['Heading2'], fontSize=14, textColor=colors.HexColor("#333333"), spaceBefore=15, spaceAfter=10)
            
            historia = [
                Paragraph("Reporte Analítico: Árbol AVL", estilo_titulo),
                Spacer(1, 10),
                Paragraph("Métricas Generales de la Estructura", estilo_h2)
            ]

            datos_tabla = [
                [Paragraph("<b>Métrica</b>", estilos['Normal']), Paragraph("<b>Valor Actual</b>", estilos['Normal'])],
                ["Altura Máxima del Árbol", str(stats["altura"])],
                ["Número Total de Nodos", str(stats["total_nodos"])],
                ["Estado de Balanceo Estricto", "Correcto (Balanced)" if stats["balanceado"] else "Desbalanceado"]
            ]
            
            t = Table(datos_tabla, colWidths=[200, 250])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (1,0), colors.HexColor("#E0E0E0")),
                ('GRID', (0,0), (-1,-1), 1, colors.grey),
                ('PADDING', (0,0), (-1,-1), 8),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F9F9F9")])
            ]))
            historia.append(t)
            historia.append(Spacer(1, 20))
            
            historia.append(Paragraph("Recorridos de Exploración", estilo_h2))
            historia.append(Paragraph(f"<b>Inorden (Ordenado):</b> {', '.join(map(str, stats['inorden']))}", estilos['Normal']))
            historia.append(Spacer(1, 5))
            historia.append(Paragraph(f"<b>Preorden:</b> {', '.join(map(str, stats['preorden']))}", estilos['Normal']))
            historia.append(Spacer(1, 5))
            historia.append(Paragraph(f"<b>Postorden:</b> {', '.join(map(str, stats['postorden']))}", estilos['Normal']))

            doc.build(historia)
            self.escribir_log(f"Reporte analítico PDF guardado en: {fichero}")
            messagebox.showinfo("Éxito", f"Reporte PDF guardado con éxito:\n{fichero}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo construir el PDF: {str(e)}")

    def imprimir_arbol(self):
        if self.raiz is None:
            messagebox.showwarning("Imprimir", "Estructura vacía. No hay datos para enviar a impresión.")
            return

        stats = self.arbol.obtener_estadisticas(self.raiz)
        texto_impresion = (
            "=========================================\n"
            "       REPORTE DE IMPRESIÓN ÁRBOL AVL    \n"
            "=========================================\n\n"
            f"Altura Máxima: {stats['altura']}\n"
            f"Total de Nodos: {stats['total_nodos']}\n"
            f"Recorrido Inorden: {stats['inorden']}\n\n"
            "Historial Reciente del Log:\n"
            "-----------------------------------------\n"
            f"{self.log.get('1.0', tk.END)}"
        )

        try:
            temp_file = "temp_print_avl.txt"
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(texto_impresion)

            if sys.platform == "win32":
                os.startfile(temp_file, "print")
            elif sys.platform == "darwin":
                os.system(f"lpr {temp_file}")
            else:
                os.system(f"lp {temp_file}")
                
            self.escribir_log("Documento enviado a la cola de impresión del sistema...")
            messagebox.showinfo("Impresora", "Enviado a la cola de impresión.")
        except Exception as e:
            messagebox.showerror("Error de Impresión", f"No se pudo imprimir: {str(e)}")

    def actualizar_visibilidad_controles(self):
        if self.modo_automatico.get():
            self.escribir_log("Modo cambiado a: Automático")
            self.btn_pausa.config(state="disabled")
            self.btn_siguiente.config(state="disabled")
        else:
            self.escribir_log("Modo cambiado a: Paso a Paso")

    def escribir_log(self, mensaje):
        self.log.insert(tk.END, mensaje + "\n")
        self.log.see(tk.END)

    def insertar_nodo(self):
        try:
            valor = int(self.entrada_valor.get())
            self.entrada_valor.delete(0, tk.END)

            if self.modo_automatico.get():
                self.raiz = self.arbol.insertar(self.raiz, valor)
                self.escribir_log(f"Nodo {valor} insertado automáticamente.")
                self.dibujar_arbol()
            else:
                self.raiz_temporal, self.cola_pasos = self.arbol.calcular_pasos_insercion(self.raiz, valor)
                self.indice_paso = 0
                self.en_pausa = False
                self.btn_pausa.config(state="normal", text="Pausar")
                self.btn_siguiente.config(state="disabled")
                self.reproducir_animacion_insercion()
        except ValueError:
            self.escribir_log("Ingrese un número válido.")

    def reproducir_animacion_insercion(self):
        if self.en_pausa: return
        if self.indice_paso >= len(self.cola_pasos):
            self.raiz = self.raiz_temporal
            self.nodo_resaltado_actual = None
            self.dibujar_arbol()
            self.escribir_log("Balanceo paso a paso finalizado. ✨")
            self.btn_pausa.config(state="disabled")
            self.btn_siguiente.config(state="disabled")
            return
        self.ejecutar_siguiente_paso()
        self.ventana.after(self.slider_velocidad.get(), self.reproducir_animacion_insercion)

    def ejecutar_siguiente_paso(self):
        if self.indice_paso >= len(self.cola_pasos): return
        paso = self.cola_pasos[self.indice_paso]
        self.escribir_log(f"[Paso {self.indice_paso + 1}]: {paso['msg']}")
        
        self.nodo_resaltado_actual = paso['nodo']
        if paso['tipo'] in ['evaluar', 'revisar_fe']: self.color_resaltado = "#FFDE59"
        elif paso['tipo'] == 'crear': self.color_resaltado = "#4CAF50"
        elif paso['tipo'] == 'rotar': self.color_resaltado = "#FF5722"

        self.dibujar_arbol(nodo_resaltado=self.nodo_resaltado_actual)
        self.indice_paso += 1

    def toggle_pausa(self):
        self.en_pausa = not self.en_pausa
        if self.en_pausa:
            self.btn_pausa.config(text="Reanudar ▶️")
            self.btn_siguiente.config(state="normal")
        else:
            self.btn_pausa.config(text="Pausar")
            self.btn_siguiente.config(state="disabled")
            self.reproducir_animacion_insercion()

    def buscar_nodo(self):
        try:
            valor = int(self.entrada_valor.get())
            self.entrada_valor.delete(0, tk.END)
            encontrado, recorrido = self.arbol.buscar_con_recorrido(self.raiz, valor)
            self.animar_busqueda(recorrido, 0, valor, encontrado)
        except ValueError:
            self.escribir_log("Ingrese un número válido.")

    def animar_busqueda(self, recorrido, idx, valor, encontrado):
        if idx >= len(recorrido):
            self.escribir_log(f"Resultado: Nodo {valor} " + ("Encontrado 🎉" if encontrado else "No encontrado ❌"))
            self.dibujar_arbol()
            return
        self.color_resaltado = "#9C27B0"
        self.dibujar_arbol(nodo_resaltado=recorrido[idx])
        self.ventana.after(self.slider_velocidad.get(), lambda: self.animar_busqueda(recorrido, idx + 1, valor, encontrado))

    def dibujar_arbol(self, nodo_resaltado=None):
        self.canvas.delete("all")
        if self.raiz is not None:
            self.dibujar_nodo(self.raiz, 600, 40, 240, nodo_resaltado)

    def dibujar_nodo(self, nodo, x, y, separacion, nodo_resaltado=None):
        if nodo is None: return
        radio = 26
        fe = self.arbol.obtener_factor_equilibrio(nodo)
        texto = f"{nodo.valor}\nh={nodo.altura}\nFE={fe}"

        bg_color = "lightblue"
        if nodo_resaltado and nodo.valor == nodo_resaltado.valor:
            bg_color = self.color_resaltado

        self.canvas.create_oval(x - radio, y - radio, x + radio, y + radio, fill=bg_color, outline="black", width=2)
        self.canvas.create_text(x, y, text=texto, font=("Arial", 8, "bold"), justify="center")

        if nodo.izquierdo:
            nx, ny = x - separacion, y + 85
            self.canvas.create_line(x, y + radio, nx, ny - radio, width=2)
            self.dibujar_nodo(nodo.izquierdo, nx, ny, max(separacion // 2, 25), nodo_resaltado)
        if nodo.derecho:
            nx, ny = x + separacion, y + 85
            self.canvas.create_line(x, y + radio, nx, ny - radio, width=2)
            self.dibujar_nodo(nodo.derecho, nx, ny, max(separacion // 2, 25), nodo_resaltado)

    def reiniciar_arbol(self):
        self.raiz = None
        self.cola_pasos = []
        self.canvas.delete("all")
        self.escribir_log("Árbol limpiado por completo.")

    def cargar_ejemplo(self):
        self.reiniciar_arbol()
        secuencia = [50, 30, 80, 20, 40, 70, 90, 35, 38, 36, 37, 39]
        for v in secuencia: self.raiz = self.arbol.insertar(self.raiz, v)
        self.dibujar_arbol()
        self.escribir_log("Árbol base de ejemplo cargado.")

    def ejecutar(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    app = AplicacionAVL()
    app.ejecutar()