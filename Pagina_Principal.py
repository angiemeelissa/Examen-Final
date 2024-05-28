import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import graphviz

class Node:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, id, name):
        if self.root is None:
            self.root = Node(id, name)
        else:
            self._insert(self.root, id, name)

    def _insert(self, node, id, name):
        if id < node.id:
            if node.left is None:
                node.left = Node(id, name)
            else:
                self._insert(node.left, id, name)
        else:
            if node.right is None:
                node.right = Node(id, name)
            else:
                self._insert(node.right, id, name)

    def draw_tree(self):
        if not self.root:
            return None
        dot = graphviz.Digraph()
        self._add_edges(self.root, dot)
        dot.render('bst', format='png', view=True)

    def _add_edges(self, node, dot):
        if node:
            dot.node(str(node.id), f"{node.id}: {node.name}")
            if node.left:
                dot.edge(str(node.id), str(node.left.id))
                self._add_edges(node.left, dot)
            if node.right:
                dot.edge(str(node.id), str(node.right.id))
                self._add_edges(node.right, dot)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Estudiantes")
        self.geometry("440x500")
        self.student_id_counter = 15000
        self.students = []
        self.bst = BST()

        self.Crear_Botones()

    def Crear_Botones(self):
        style = ttk.Style(self)
        style.theme_use('alt')
        style.configure('TButton', font=("Times New Roman", 15, "bold"), padding=12, borderwidth=4, relief="groove")
        style.map('TButton',
                  background=[('active', '#DBB6EE'), ('!active', '#7F4CA5')],
                  foreground=[('active', 'white'), ('!active', 'white')])

        titulo_label = tk.Label(self, text="Gestión de Estudiantes", font=("Times New Roman", 20, "bold"),
                                bg=self.cget('background'))
        titulo_label.pack(pady=(40, 30))

        botones = [
            "Agregar Estudiante",
            "Buscar Estudiante",
            "Eliminar Estudiante",
            "Ver Árbol Binario",
            "Listar"
        ]

        for boton in botones:
            button = ttk.Button(self, text=boton, style='TButton',
                                command=lambda boton=boton: self.Abrir_Ventana(boton))
            button.pack(fill='x', padx=50, pady=(7, 7))

    def Abrir_Ventana(self, nombre_boton):
        if nombre_boton == "Agregar Estudiante":
            self.Agregar_Estudiante()
        elif nombre_boton == "Buscar Estudiante":
            self.Buscar_Estudiante()
        elif nombre_boton == "Eliminar Estudiante":
            self.Eliminar_Estudiante()
        elif nombre_boton == "Ver Árbol Binario":
            self.Ver_Arbol_Binario()
        elif nombre_boton == "Listar":
            self.Listar_Estudiantes()

    def Agregar_Estudiante(self):
        new_window = tk.Toplevel(self)
        new_window.title("Agregar Estudiante")
        new_window.geometry("300x500")

        tk.Label(new_window, text="Nombre:", font=("Times New Roman", 15)).pack(pady=5)
        nombre_entry = tk.Entry(new_window)
        nombre_entry.pack(pady=5)

        tk.Label(new_window, text="Apellidos:", font=("Times New Roman", 15)).pack(pady=5)
        apellidos_entry = tk.Entry(new_window)
        apellidos_entry.pack(pady=5)

        tk.Label(new_window, text="Fecha de Nacimiento:", font=("Times New Roman", 15)).pack(pady=5)
        fecha_entry = tk.Entry(new_window)
        fecha_entry.pack(pady=5)

        tk.Label(new_window, text="Correo Electrónico:", font=("Times New Roman", 15)).pack(pady=5)
        correo_entry = tk.Entry(new_window)
        correo_entry.pack(pady=5)

        tk.Label(new_window, text="Número Telefónico:", font=("Times New Roman", 15)).pack(pady=5)
        telefono_entry = tk.Entry(new_window)
        telefono_entry.pack(pady=5)

        def Guardar_Estudiante():
            nombre = nombre_entry.get()
            apellidos = apellidos_entry.get()
            fecha = fecha_entry.get()
            correo = correo_entry.get()
            telefono = telefono_entry.get()
            student_id = self.student_id_counter * 100 + 24
            self.student_id_counter += 1

            estudiante = {
                "ID": student_id,
                "Nombre": nombre,
                "Apellidos": apellidos,
                "Fecha de Nacimiento": fecha,
                "Correo Electrónico": correo,
                "Número Telefónico": telefono
            }

            self.students.append(estudiante)
            self.bst.insert(student_id, nombre)

            messagebox.showinfo("Estudiante Guardado",
                                f"ID: {student_id}\nNombre: {nombre}\nApellidos: {apellidos}\nFecha de Nacimiento: {fecha}\nCorreo Electrónico: {correo}\nNúmero Telefónico: {telefono}")

            new_window.destroy()

        guardar_button = ttk.Button(new_window, text="Guardar", command=Guardar_Estudiante, style='TButton')
        guardar_button.pack(pady=20)

    def Buscar_Estudiante(self):
        new_window = tk.Toplevel(self)
        new_window.title("Buscar Estudiante")
        new_window.geometry("300x200")

        def Buscar_por_Nombre():
            nombre_completo = simpledialog.askstring("Buscar por Nombre", "Ingrese el nombre completo del estudiante:")
            if nombre_completo:
                estudiante = next(
                    (est for est in self.students if f"{est['Nombre']} {est['Apellidos']}" == nombre_completo), None)
                if estudiante:
                    messagebox.showinfo("Estudiante Encontrado",
                                        f"ID: {estudiante['ID']}\nNombre: {estudiante['Nombre']}\nApellidos: {estudiante['Apellidos']}\nFecha de Nacimiento: {estudiante['Fecha de Nacimiento']}\nCorreo Electrónico: {estudiante['Correo Electrónico']}\nNúmero Telefónico: {estudiante['Número Telefónico']}")
                else:
                    messagebox.showwarning("No Encontrado", "No se encontró ningún estudiante con ese nombre completo.")

        def Buscar_por_ID():
            id_estudiante = simpledialog.askinteger("Buscar por ID", "Ingrese el ID del estudiante:")
            if id_estudiante:
                estudiante = next((est for est in self.students if est['ID'] == id_estudiante), None)
                if estudiante:
                    messagebox.showinfo("Estudiante Encontrado",
                                        f"ID: {estudiante['ID']}\nNombre: {estudiante['Nombre']}\nApellidos: {estudiante['Apellidos']}\nFecha de Nacimiento: {estudiante['Fecha de Nacimiento']}\nCorreo Electrónico: {estudiante['Correo Electrónico']}\nNúmero Telefónico: {estudiante['Número Telefónico']}")
                else:
                    messagebox.showwarning("No Encontrado", "No se encontró ningún estudiante con ese ID.")

        buscar_nombre_button = ttk.Button(new_window, text="Buscar por Nombre", command=Buscar_por_Nombre,
                                          style='TButton')
        buscar_nombre_button.pack(fill='x', padx=50, pady=10)

        buscar_id_button = ttk.Button(new_window, text="Buscar por ID", command=Buscar_por_ID, style='TButton')
        buscar_id_button.pack(fill='x', padx=50, pady=10)

    def Eliminar_Estudiante(self):
        new_window = tk.Toplevel(self)
        new_window.title("Eliminar Estudiante")
        new_window.geometry("300x200")

        tk.Label(new_window, text="ID del Estudiante:", font=("Times New Roman", 15)).pack(pady=5)
        id_entry = tk.Entry(new_window)
        id_entry.pack(pady=5)

        def Eliminar():
            id_estudiante = int(id_entry.get())
            estudiante = next((est for est in self.students if est['ID'] == id_estudiante), None)
            if estudiante:
                self.students.remove(estudiante)
                messagebox.showinfo("Estudiante Eliminado", f"El estudiante con ID {id_estudiante} ha sido eliminado.")
                new_window.destroy()
            else:
                messagebox.showwarning("No Encontrado", "No se encontró ningún estudiante con ese ID.")

        eliminar_button = ttk.Button(new_window, text="Eliminar", command=Eliminar, style='TButton')
        eliminar_button.pack(pady=20)

    def Ver_Arbol_Binario(self):
        self.bst.draw_tree()

    def Listar_Estudiantes(self):
        #LISTAR ESTUDIANTES
        pass


def iniciar_aplicacion():
    app = Application()
    app.mainloop()


iniciar_aplicacion()
