from avl.node import Nodo

class ArbolAVL:
    def obtener_altura(self, nodo):
        if nodo is None:
            return 0
        return nodo.altura

    def obtener_factor_equilibrio(self, nodo):
        if nodo is None:
            return 0
        return self.obtener_altura(nodo.izquierdo) - self.obtener_altura(nodo.derecho)

    def actualizar_altura(self, nodo):
        nodo.altura = 1 + max(
            self.obtener_altura(nodo.izquierdo),
            self.obtener_altura(nodo.derecho)
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
        # Mantenemos tu método original para cuando el modo automático esté activo sin animar pasos
        if raiz is None: return Nodo(valor)
        if valor < raiz.valor: raiz.izquierdo = self.insertar(raiz.izquierdo, valor)
        elif valor > raiz.valor: raiz.derecho = self.insertar(raiz.derecho, valor)
        else: return raiz

        self.actualizar_altura(raiz)
        factor = self.obtener_factor_equilibrio(raiz)

        if factor > 1 and valor < raiz.izquierdo.valor: return self.rotacion_derecha(raiz)
        if factor < -1 and valor > raiz.derecho.valor: return self.rotacion_izquierda(raiz)
        if factor > 1 and valor > raiz.izquierdo.valor:
            raiz.izquierdo = self.rotacion_izquierda(raiz.izquierdo)
            return self.rotacion_derecha(raiz)
        if factor < -1 and valor < raiz.derecho.valor:
            raiz.derecho = self.rotacion_derecha(raiz.derecho)
            return self.rotacion_izquierda(raiz)
        return raiz

    def buscar_con_recorrido(self, raiz, valor):
        recorrido = []
        actual = raiz
        encontrado = False
        while actual is not None:
            recorrido.append(actual)
            if valor == actual.valor:
                encontrado = True
                break
            actual = actual.izquierdo if valor < actual.valor else actual.derecho
        return encontrado, recorrido

    # --- NUEVO MÉTODO PARA PASO A PASO ---
    def calcular_pasos_insercion(self, raiz, valor):
        """
        Simula la inserción de forma controlada y genera una lista de 'eventos'
        Cada evento es un diccionario: {'tipo': 'visita/balanceo', 'nodo': nodo, 'msg': 'texto'}
        """
        pasos = []
        
        def _insercion_recursiva(nodo, v):
            if nodo is None:
                nuevo = Nodo(v)
                pasos.append({'tipo': 'crear', 'nodo': nuevo, 'msg': f"Creado nuevo nodo {v}"})
                return nuevo
            
            pasos.append({'tipo': 'evaluar', 'nodo': nodo, 'msg': f"Evaluando nodo {nodo.valor}"})
            
            if v < nodo.valor:
                nodo.izquierdo = _insercion_recursiva(nodo.izquierdo, v)
            elif v > nodo.valor:
                nodo.derecho = _insercion_recursiva(nodo.derecho, v)
            else:
                pasos.append({'tipo': 'duplicado', 'nodo': nodo, 'msg': f"El valor {v} ya existe"})
                return nodo

            self.actualizar_altura(nodo)
            factor = self.obtener_factor_equilibrio(nodo)
            pasos.append({'tipo': 'revisar_fe', 'nodo': nodo, 'msg': f"Verificando equilibrio en {nodo.valor} (FE={factor})"})

            # Caso Izquierda-Izquierda
            if factor > 1 and v < nodo.izquierdo.valor:
                pasos.append({'tipo': 'rotar', 'nodo': nodo, 'msg': f"Desbalance Izq-Izq en {nodo.valor}. Rotación Derecha."})
                return self.rotacion_derecha(nodo)

            # Caso Derecha-Derecha
            if factor < -1 and v > nodo.derecho.valor:
                pasos.append({'tipo': 'rotar', 'nodo': nodo, 'msg': f"Desbalance Der-Der en {nodo.valor}. Rotación Izquierda."})
                return self.rotacion_izquierda(nodo)

            # Caso Izquierda-Derecha
            if factor > 1 and v > nodo.izquierdo.valor:
                pasos.append({'tipo': 'rotar', 'nodo': nodo, 'msg': f"Desbalance Izq-Der en {nodo.valor}. Doble Rotación."})
                nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)
                return self.rotacion_derecha(nodo)

            # Caso Derecha-Izquierda
            if factor < -1 and v < nodo.derecho.valor:
                pasos.append({'tipo': 'rotar', 'nodo': nodo, 'msg': f"Desbalance Der-Izq en {nodo.valor}. Doble Rotación."})
                nodo.derecho = self.rotacion_derecha(nodo.derecho)
                return self.rotacion_izquierda(nodo)

            return nodo

        nueva_raiz = _insercion_recursiva(raiz, valor)
        return nueva_raiz, pasos
    def obtener_estadisticas(self, raiz):
        """Calcula métricas y recorridos del árbol para los reportes."""
        if raiz is None:
            return {
                "total_nodos": 0, "altura": 0, "balanceado": True,
                "inorden": [], "preorden": [], "postorden": []
            }

        inorden, preorden, postorden = [], [], []

        def _recorridos(nodo):
            if nodo:
                preorden.append(nodo.valor)
                _recorridos(nodo.izquierdo)
                inorden.append(nodo.valor)
                _recorridos(nodo.derecho)
                postorden.append(nodo.valor)

        _recorridos(raiz)
        
        # Un árbol AVL ideal siempre está balanceado, pero verificamos si hay desvíos graves
        def _verificar_balance(nodo):
            if nodo is None: return True
            fe = self.obtener_factor_equilibrio(nodo)
            if abs(fe) > 1: return False
            return _verificar_balance(nodo.izquierdo) and _verificar_balance(nodo.derecho)

        return {
            "total_nodos": len(inorden),
            "altura": raiz.altura,
            "balanceado": _verificar_balance(raiz),
            "inorden": inorden,
            "preorden": preorden,
            "postorden": postorden
        }