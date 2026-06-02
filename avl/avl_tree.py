from avl.node import Nodo


class ArbolAVL:

    def obtener_altura(self, nodo):
        if nodo is None:
            return 0

        return nodo.altura

    def obtener_factor_equilibrio(self, nodo):
        if nodo is None:
            return 0

        return (
            self.obtener_altura(nodo.izquierdo)
            - self.obtener_altura(nodo.derecho)
        )

    def actualizar_altura(self, nodo):
        nodo.altura = (
            1 +
            max(
                self.obtener_altura(nodo.izquierdo),
                self.obtener_altura(nodo.derecho)
            )
        )

    def rotacion_derecha(self, nodo_y):

        nodo_x = nodo_y.izquierdo
        sub_arbol = nodo_x.derecho

        nodo_x.derecho = nodo_y
        nodo_y.izquierdo = sub_arbol

        self.actualizar_altura(nodo_y)
        self.actualizar_altura(nodo_x)

        return nodo_x

    def rotacion_izquierda(self, nodo_x):

        nodo_y = nodo_x.derecho
        sub_arbol = nodo_y.izquierdo

        nodo_y.izquierdo = nodo_x
        nodo_x.derecho = sub_arbol

        self.actualizar_altura(nodo_x)
        self.actualizar_altura(nodo_y)

        return nodo_y

    def insertar(self, raiz, valor):

        if raiz is None:
            return Nodo(valor)

        if valor < raiz.valor:
            raiz.izquierdo = self.insertar(
                raiz.izquierdo,
                valor
            )

        elif valor > raiz.valor:
            raiz.derecho = self.insertar(
                raiz.derecho,
                valor
            )

        else:
            return raiz

        self.actualizar_altura(raiz)

        factor = self.obtener_factor_equilibrio(raiz)

        # Caso Izquierda-Izquierda
        if (
            factor > 1 and
            valor < raiz.izquierdo.valor
        ):
            return self.rotacion_derecha(raiz)

        # Caso Derecha-Derecha
        if (
            factor < -1 and
            valor > raiz.derecho.valor
        ):
            return self.rotacion_izquierda(raiz)

        # Caso Izquierda-Derecha
        if (
            factor > 1 and
            valor > raiz.izquierdo.valor
        ):
            raiz.izquierdo = self.rotacion_izquierda(
                raiz.izquierdo
            )

            return self.rotacion_derecha(raiz)

        # Caso Derecha-Izquierda
        if (
            factor < -1 and
            valor < raiz.derecho.valor
        ):
            raiz.derecho = self.rotacion_derecha(
                raiz.derecho
            )

            return self.rotacion_izquierda(raiz)

        return raiz

    def buscar(self, raiz, valor):

        if raiz is None:
            return None

        if raiz.valor == valor:
            return raiz

        if valor < raiz.valor:
            return self.buscar(
                raiz.izquierdo,
                valor
            )

        return self.buscar(
            raiz.derecho,
            valor
        )