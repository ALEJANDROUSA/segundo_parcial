from mesa import Agent, Model
from mesa.time import RandomActivation
import re
import math

# Agente base de operación

class OperacionAgente(Agent):
    def __init__(self, unique_id, model, simbolo, funcion):
        super().__init__(unique_id, model)
        self.simbolo = simbolo
        self.funcion = funcion
        self.tareas = []

    def step(self):
        if not self.tareas:
            return
        tarea = self.tareas.pop(0)
        tid = tarea["id"]
        a, b = tarea["a"], tarea["b"]
        try:
            resultado = self.funcion(a, b)
            self.model.resultados[tid] = {"ok": True, "valor": resultado}
        except Exception as e:
            self.model.resultados[tid] = {"ok": False, "error": str(e)}


# Agente de Entrada/Salida

class IOAgente(Agent):
    TOKEN = re.compile(r"\s*(?:(\d+(?:\.\d+)?)|([\+\-\*\/\^\(\)]))")

    def __init__(self, unique_id, model, mapa_ops):
        super().__init__(unique_id, model)
        self.mapa_ops = mapa_ops
        self.precedencia = {'^': 4, '*': 3, '/': 3, '+': 2, '-': 2}
        self.derecha_asoc = {'^'}

    def tokenizar(self, expr):
        tokens, pos = [], 0
        while pos < len(expr):
            m = self.TOKEN.match(expr, pos)
            if not m:
                raise ValueError(f"Token inválido cerca de: {expr[pos:]}")
            num, op = m.groups()
            tokens.append(num if num else op)
            pos = m.end()
        return tokens

    def a_rpn(self, tokens):
        salida, pila = [], []
        for t in tokens:
            if re.fullmatch(r"\d+(?:\.\d+)?", t):
                salida.append(t)
            elif t in self.precedencia:
                while pila and pila[-1] in self.precedencia:
                    top = pila[-1]
                    if ((t in self.derecha_asoc and self.precedencia[t] < self.precedencia[top]) or
                        (t not in self.derecha_asoc and self.precedencia[t] <= self.precedencia[top])):
                        salida.append(pila.pop())
                    else:
                        break
                pila.append(t)
            elif t == '(':
                pila.append(t)
            elif t == ')':
                while pila and pila[-1] != '(':
                    salida.append(pila.pop())
                if not pila:
                    raise ValueError("Paréntesis desbalanceados")
                pila.pop()
        while pila:
            if pila[-1] in ('(', ')'):
                raise ValueError("Paréntesis desbalanceados")
            salida.append(pila.pop())
        return salida

    def buscar_agente(self, aid):
        agentes = getattr(self.model.schedule, 'agents', [])
        if isinstance(agentes, list):
            for ag in agentes:
                if getattr(ag, 'unique_id', None) == aid:
                    return ag
        return None

    def solicitar_operacion(self, simbolo, a, b):
        if simbolo not in self.mapa_ops:
            raise ValueError(f"Operador no soportado: {simbolo}")
        tid = f"t{len(self.model.resultados)}"  # ID simple sin uuid
        aid = self.mapa_ops[simbolo]
        agente = self.buscar_agente(aid)
        if agente is None:
            raise RuntimeError("Agente no encontrado")
        agente.tareas.append({"id": tid, "a": a, "b": b})
        self.model.resultados[tid] = {"ok": None}
        return tid

    def esperar_resultado(self, tid, max_pasos=500):
        pasos = 0
        while pasos < max_pasos:
            val = self.model.resultados.get(tid)
            if val and val["ok"] is not None:
                return val
            self.model.step()
            pasos += 1
        raise TimeoutError("Tiempo de espera agotado")

    def evaluar_rpn(self, rpn):
        pila = []
        for t in rpn:
            if re.fullmatch(r"\d+(?:\.\d+)?", t):
                pila.append(float(t))
            elif t in self.mapa_ops:
                if len(pila) < 2:
                    raise ValueError("Expresión inválida")
                b, a = pila.pop(), pila.pop()
                tid = self.solicitar_operacion(t, a, b)
                res = self.esperar_resultado(tid)
                if not res["ok"]:
                    raise ValueError(f"Error en operación: {res.get('error')}")
                pila.append(res["valor"])
            else:
                raise ValueError(f"Token desconocido: {t}")
        if len(pila) != 1:
            raise ValueError("Error en evaluación final")
        return pila[0]



# Modelo principal

class ModeloCalculadora(Model):
    def __init__(self):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.resultados = {}

        operaciones = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b if b != 0 else (_ for _ in ()).throw(ZeroDivisionError("División por cero")),
            '^': lambda a, b: math.pow(a, b),
        }

        self.mapa_ops = {}
        for i, (simbolo, funcion) in enumerate(operaciones.items()):
            aid = f"op_{i}_{simbolo}"
            agente = OperacionAgente(aid, self, simbolo, funcion)
            self.schedule.add(agente)
            self.mapa_ops[simbolo] = aid

        self.io_agente = IOAgente("io_1", self, self.mapa_ops)
        self.schedule.add(self.io_agente)

    def step(self):
        self.schedule.step()


# Interfaz de usuario

def main():
    print("Calculadora distribuida basada en agentes (MESA)")
    print("Ejemplo: (2 + 3) * 4 - 5 / 2")
    print("Escribe 'salir' para terminar.\n")

    modelo = ModeloCalculadora()

    while True:
        expr = input("Ingresa expresión: ").strip()
        if expr.lower() in ("salir", "exit", "q"):
            print("Saliendo...")
            break
        try:
            tokens = modelo.io_agente.tokenizar(expr)
            rpn = modelo.io_agente.a_rpn(tokens)
            resultado = modelo.io_agente.evaluar_rpn(rpn)
            print(f"Resultado: {resultado}\n")
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
