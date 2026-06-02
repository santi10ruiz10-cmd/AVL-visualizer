from avl.avl_tree import ArbolAVL


arbol = ArbolAVL()
raiz = None

secuencia = [
    50,
    30,
    80,
    20,
    40,
    70,
    90,
    35,
    38,
    36,
    37,
    39
]

for numero in secuencia:
    raiz = arbol.insertar(
        raiz,
        numero
    )

print("Árbol AVL construido correctamente")

resultado = arbol.buscar(
    raiz,
    37
)

if resultado:
    print(
        f"Nodo encontrado: {resultado.valor}"
    )
else:
    print("Nodo no encontrado")