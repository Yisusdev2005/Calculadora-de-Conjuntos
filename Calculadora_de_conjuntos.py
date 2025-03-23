import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import re

class CalculadoraConjuntos:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Conjuntos")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Diccionario para almacenar los conjuntos
        self.conjuntos = {}
        self.universo = set()
        
        # Variable para los cardinalidad
        self.mostrar_cardinalidad = tk.BooleanVar()
        self.ordenar_elementos = tk.BooleanVar()
        
        self.crear_interfaz()
    
    def crear_interfaz(self):

        # Título
        titulo = tk.Label(self.root, text="Calculadora de conjuntos", font=("Arial", 18, "bold"), bg="#f0f0f0")
        titulo.pack(pady=10)
        
        # Botón de ayuda
        btn_ayuda = tk.Button(self.root, text="Ayuda", command=self.mostrar_ayuda,
                              bg="#333", fg="white", font=("Arial", 10))
        btn_ayuda.place(x=20, y=20)
        
        # Frame para opciones
        frame_opciones = tk.Frame(self.root, bg="#f0f0f0", highlightbackground="#ddd", 
                                  highlightthickness=1, bd=0)
        frame_opciones.pack(fill=tk.X, padx=20, pady=10)
        
        # Botón para mostrar la cardinalidad
        chk_cardinalidad = tk.Checkbutton(frame_opciones, text="Mostrar cardinalidad", 
                                         variable=self.mostrar_cardinalidad, 
                                         font=("Arial", 12), bg="#f0f0f0")
        chk_cardinalidad.pack(anchor=tk.W, pady=5, padx=10)
        
        # Botón para ordenar elementos
        chk_ordenar = tk.Checkbutton(frame_opciones, text="Ordenar elementos", 
                                    variable=self.ordenar_elementos, 
                                    font=("Arial", 12), bg="#f0f0f0")
        chk_ordenar.pack(anchor=tk.W, pady=5, padx=10)
        
        # Aŕea para entrada y botones de operación
        frame_principal = tk.Frame(self.root, bg="white", highlightbackground="#ddd", 
                                   highlightthickness=1, bd=0)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Área de entrada de texto
        self.txt_entrada = scrolledtext.ScrolledText(frame_principal, height=10, width=40, 
                                                    font=("Consolas", 12))
        self.txt_entrada.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botones de operaciones
        frame_botones = tk.Frame(frame_principal, bg="white")
        frame_botones.pack(fill=tk.X, padx=10, pady=10)
        
        # Botones de conjuntos
        botones_izq = [
            ('{', '}', '(', ')', '∅'),
            ('∩', 'U', '\\', 'C', '△', '×')
        ]
        
        botones_der = [
            ('?', '='),
            ('⊆', '⊂')
        ]
        
        # Área para los botones izquierdos
        frame_izq = tk.Frame(frame_botones, bg="white")
        frame_izq.pack(side=tk.LEFT)
        
        # Botones izquierdos
        for i, fila in enumerate(botones_izq):
            frame_fila = tk.Frame(frame_izq, bg="white")
            frame_fila.pack(pady=2)
            for texto in fila:
                btn = tk.Button(frame_fila, text=texto, width=3, height=1,
                               bg="#222", fg="white", font=("Arial", 12, "bold"),
                               command=lambda t=texto: self.insertar_simbolo(t))
                btn.pack(side=tk.LEFT, padx=2)
        
        # Arwea para los botones derechos
        frame_der = tk.Frame(frame_botones, bg="white")
        frame_der.pack(side=tk.RIGHT)
        
        # Botones derechos
        for i, fila in enumerate(botones_der):
            frame_fila = tk.Frame(frame_der, bg="white")
            frame_fila.pack(pady=3)
            for texto in fila:
                btn = tk.Button(frame_fila, text=texto, width=3, height=1,
                               bg="#222", fg="white", font=("Arial", 12, "bold"),
                               command=lambda t=texto: self.insertar_simbolo(t))
                btn.pack(side=tk.LEFT, padx=1)
        
        # Botón para calcular
        btn_calcular = tk.Button(frame_principal, text="Calcular", bg="#222", fg="white",
                                font=("Arial", 12, "bold"), command=self.calcular)
        btn_calcular.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Área de resultados
        self.frame_resultados = None
    
    def insertar_simbolo(self, simbolo):

        # Mapeo de símbolos
        simbolos_map = {
            'U': '∪',  # Unión
            'C': 'C',  # Complemento
            '∅': '∅',  # Conjunto vacío
        }
        
        # Si el símbolo está en el mapeo, usamos el valor mapeado
        simbolo_a_insertar = simbolos_map.get(simbolo, simbolo)
        
        # Insertar en la posición actual del cursor
        self.txt_entrada.insert(tk.INSERT, simbolo_a_insertar)
    
    def mostrar_ayuda(self):
        ventana_ayuda = tk.Toplevel(self.root)
        ventana_ayuda.title("Ayuda")
        ventana_ayuda.geometry("820x620")
        ventana_ayuda.configure(bg="#f0f0f0")
        
        texto_ayuda = """
Están soportadas las siguientes operaciones:

• Unión
• Intersección
• Diferencia
• Diferencia simétrica
• Complemento
• Producto cartesiano

¿Cómo se usa?
Primero define los conjuntos y luego realiza las operaciones. Solo se pueden definir conjuntos por
extensión. Se debe definir un conjunto por línea.

Ej.:

A={1,2,3,4}
B={5,6,7,8}
C={3,4,5,6}
A∪B
B∩C
(A∪C)\\B

Cuando termines presiona el botón «Calcular». Por defecto se crea el conjunto «vacío» y el conjunto
«Universo» (la letra «U» está reservada para el «Universo»).
El «Universo» tiene el contenido de todos los conjuntos que hayas creado.
Tomando el ejemplo anterior, el universo sería: U={1,2,3,4,5,6,7,8}.
También puedes agregar elementos que solo estarán en el «Universo».
        """
        
        lbl_ayuda = tk.Label(ventana_ayuda, text=texto_ayuda, justify=tk.LEFT, 
                            bg="#f0f0f0", font=("Arial", 11), padx=20, pady=20)
        lbl_ayuda.pack(fill=tk.BOTH, expand=True)
        
        btn_cerrar = tk.Button(ventana_ayuda, text="Cerrar", bg="#222", fg="white",
                              font=("Arial", 10), command=ventana_ayuda.destroy)
        btn_cerrar.pack(pady=10)
    
    def ordenar_elementos_conjunto(self, elementos):

        # Separar elementos por tipo
        numeros = []
        textos = []
        
        for e in elementos:
            if isinstance(e, (int, float)):
                numeros.append(e)
            else:
                textos.append(str(e))
        
        # Ordenar cada grupo y combinar
        return sorted(numeros) + sorted(textos)
    
    def mostrar_resultados(self, conjuntos, resultados):
        # Si ya existe un frame de resultados, lo destruimos
        if self.frame_resultados:
            self.frame_resultados.destroy()
        
        # Crear nuevo frame para resultados
        self.frame_resultados = tk.Toplevel(self.root)
        self.frame_resultados.title("Resultados")
        self.frame_resultados.geometry("600x400")
        self.frame_resultados.configure(bg="white")
        
        # Mostrar conjuntos
        lbl_conjuntos = tk.Label(self.frame_resultados, text="Conjuntos:", 
                                font=("Arial", 14, "bold"), bg="white", anchor="w")
        lbl_conjuntos.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        for nombre, elementos in conjuntos.items():
            # Formatear elementos como {1, 2, 3}
            if isinstance(elementos, set):
                # Convertir a lista para ordenar si es necesario
                if self.ordenar_elementos.get():
                    elementos_lista = self.ordenar_elementos_conjunto(elementos)
                else:
                    elementos_lista = list(elementos)
                
                elementos_str = "{" + ", ".join(map(str, elementos_lista)) + "}"
                if self.mostrar_cardinalidad.get():
                    elementos_str += f" |{nombre}| = {len(elementos)}"
            else:
                elementos_str = str(elementos)
            
            contenido = f"{nombre} = {elementos_str}"
            lbl = tk.Label(self.frame_resultados, text=contenido, font=("Arial", 12), 
                         bg="white", anchor="w", padx=20, pady=2)
            lbl.pack(fill=tk.X)
        
        # Mostrar resultados
        lbl_resultados = tk.Label(self.frame_resultados, text="Resultados:", 
                                 font=("Arial", 14, "bold"), bg="white", anchor="w")
        lbl_resultados.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        for nombre, elementos in resultados.items():
            if isinstance(elementos, set):
                # Convertir a lista para ordenar si es necesario
                if self.ordenar_elementos.get():
                    elementos_lista = self.ordenar_elementos_conjunto(elementos)
                else:
                    elementos_lista = list(elementos)
                
                elementos_str = "{" + ", ".join(map(str, elementos_lista)) + "}"
                if self.mostrar_cardinalidad.get():
                    elementos_str += f" |{nombre}| = {len(elementos)}"
            else:
                elementos_str = str(elementos)
            
            contenido = f"{nombre} = {elementos_str}"
            lbl = tk.Label(self.frame_resultados, text=contenido, font=("Arial", 12), 
                         bg="white", anchor="w", fg="#5050ff", padx=20, pady=2)
            lbl.pack(fill=tk.X)
        
        # Botón para volver
        btn_volver = tk.Button(self.frame_resultados, text="Volver", bg="#222", fg="white",
                              font=("Arial", 10), command=self.frame_resultados.destroy)
        btn_volver.pack(pady=20)
    
    def analizar_entrada(self, texto):
        lineas = texto.strip().split('\n')
        conjuntos = {'∅': set()}  # Conjunto vacío
        resultados = {}
        
        # Capturar definiciones de conjuntos
        for linea in lineas:
            linea = linea.strip()
            if not linea:
                continue
            
            # Buscar definiciones de conjuntos (ej. A={1,2,3})
            match = re.match(r'^([A-Za-z])\s*=\s*\{(.*)\}$', linea)
            if match:
                nombre = match.group(1)
                elementos_str = match.group(2)
                elementos = [e.strip() for e in elementos_str.split(',') if e.strip()]

                # Convertir a números si es posible
                elementos_convertidos = []
                for e in elementos:
                    try:
                        elementos_convertidos.append(int(e))
                    except ValueError:
                        try:
                            elementos_convertidos.append(float(e))
                        except ValueError:
                            elementos_convertidos.append(e)
                
                conjuntos[nombre] = set(elementos_convertidos)
                # Agregar al conjunto universo
                self.universo.update(conjuntos[nombre])
        
        # Asignar el universo
        conjuntos['U'] = self.universo
        
        # Segunda pasada: evaluación de operaciones
        for linea in lineas:
            linea = linea.strip()
            if not linea or '=' in linea and re.match(r'^[A-Za-z]', linea):
                continue  # Saltar definiciones de conjuntos ya procesadas
            
            try:
                # Reemplazar símbolos por operaciones de Python
                operacion = linea
                for nombre, conjunto in conjuntos.items():
                    operacion = operacion.replace(nombre, f"conjuntos['{nombre}']")
                
                # Reemplazar símbolos de operaciones
                operacion = operacion.replace('∪', '|')  # Unión
                operacion = operacion.replace('∩', '&')  # Intersección
                operacion = operacion.replace('\\', '-')  # Diferencia
                operacion = operacion.replace('△', '^')  # Diferencia simétrica
                
                # Evaluar y guardar resultado
                resultado = eval(operacion)
                resultados[linea] = resultado
            except Exception as e:
                resultados[linea] = f"Error: {str(e)}"
        
        return conjuntos, resultados
    
    def calcular(self):
        texto = self.txt_entrada.get("1.0", tk.END)
        try:
            conjuntos, resultados = self.analizar_entrada(texto)
            self.mostrar_resultados(conjuntos, resultados)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al procesar la entrada: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraConjuntos(root)
    root.mainloop()