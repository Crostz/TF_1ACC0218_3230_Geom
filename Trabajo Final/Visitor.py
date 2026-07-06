
import math
if __name__ is not None and "." in __name__:
    from .FormasParser import FormasParser
    from .FormasVisitor import FormasVisitor
else:
    from FormasParser import FormasParser
    from FormasVisitor import FormasVisitor


class Visitor(FormasVisitor):
    COLOR_DEFAULT = "black"
    COLORES_VALIDOS = {
        "rojo": "red",
        "verde": "green",
        "azul": "blue",
        "amarillo": "yellow",
        "naranja": "orange",
        "morado": "purple",
        "negro": "black",
        "marron": "brown",
    }

    def __init__(self):
        self.variables = {}
        self.figuras = {}
        self.html = ""

    ### GET FIGURAS ###
    def getFiguras(self):
        return self.figuras

    ### GET HTML ###
    def getHtml(self):
        return self.html

    ### OBTENER COLOR ###
    def obtenerColor(self, ctx):
        color = ctx.colorOpcional()
        if color and color.colorValor():
            valor = color.colorValor().getText()
            if valor not in self.COLORES_VALIDOS:
                colores = ", ".join(sorted(self.COLORES_VALIDOS))
                raise Exception(f"Color no valido: {valor}. Colores permitidos: {colores}")
            return self.COLORES_VALIDOS[valor]
        return self.COLOR_DEFAULT

    ### FORMATEAR NUMERO ###
    def formatearNumero(self, valor):
        if isinstance(valor, float) and valor.is_integer():
            return str(int(valor))
        if isinstance(valor, float):
            return f"{valor:.2f}"
        return str(valor)

    ### ESCAPAR TEXTO JS ###
    def escaparTexto(self, texto):
        return texto.replace("\\", "\\\\").replace('"', '\\"')

    ### OBTENER PUNTOS DE FIGURA ###
    def obtenerPuntosFigura(self, figura):
        if figura["tipo"] == "punto":
            return [(figura["x"], figura["y"])]
        if figura["tipo"] == "recta":
            return [(figura["x1"], figura["y1"]), (figura["x2"], figura["y2"])]
        if figura["tipo"] in ["triangulo", "cuadrado", "pentagono"]:
            return figura["puntos"]
        if figura["tipo"] == "circulo":
            return [(figura["x"], figura["y"])]
        return []

    ### CALCULAR LADOS ###
    def calcularLados(self, puntos, cerrar=True):
        lados = []
        limite = len(puntos) if cerrar else len(puntos) - 1
        for i in range(limite):
            x1, y1 = puntos[i]
            x2, y2 = puntos[(i + 1) % len(puntos)]
            lados.append(math.dist((x1, y1), (x2, y2)))
        return lados

    ### GENERAR ETIQUETAS DE LADOS ###
    def generarDetalleFigura(self, nombre, figura):
        tipo = figura["tipo"]
        if tipo == "recta":
            puntos = self.obtenerPuntosFigura(figura)
            cerrar = False
        elif tipo in ["triangulo", "cuadrado", "pentagono"]:
            puntos = self.obtenerPuntosFigura(figura)
            cerrar = True
        else:
            return ""

        codigo = """
            ctx.save();
            ctx.fillStyle = "black";
            ctx.font = "12px Arial";
        """

        limite = len(puntos) if cerrar else len(puntos) - 1
        for i in range(limite):
            x1, y1 = puntos[i]
            x2, y2 = puntos[(i + 1) % len(puntos)]
            longitud = math.dist((x1, y1), (x2, y2))
            etiqueta = f"{self.formatearNumero(longitud)} m"
            x_medio = (x1 + x2) / 2
            y_medio = (y1 + y2) / 2
            codigo += f"""
            ctx.fillText("{self.escaparTexto(etiqueta)}", {x_medio} + 5, {y_medio} - 5);
            """

        codigo += """
            ctx.restore();
        """

        return codigo

    ### CALCULAR ANGULO INTERNO ###
    def calcularAnguloInterno(self, anterior, actual, siguiente):
        ax, ay = anterior
        bx, by = actual
        cx, cy = siguiente

        vector1 = (ax - bx, ay - by)
        vector2 = (cx - bx, cy - by)
        magnitud1 = math.hypot(vector1[0], vector1[1])
        magnitud2 = math.hypot(vector2[0], vector2[1])

        if magnitud1 == 0 or magnitud2 == 0:
            return 0

        producto = vector1[0] * vector2[0] + vector1[1] * vector2[1]
        coseno = max(-1, min(1, producto / (magnitud1 * magnitud2)))
        return math.degrees(math.acos(coseno))

    ### CALCULAR MARCA DE ANGULO ###
    def calcularMarcaAngulo(self, anterior, actual, siguiente, centro):
        ax, ay = anterior
        bx, by = actual
        cx, cy = siguiente
        centro_x, centro_y = centro

        longitud1 = math.dist(actual, anterior)
        longitud2 = math.dist(actual, siguiente)
        radio = max(14, min(30, longitud1 * 0.22, longitud2 * 0.22))

        inicio = math.atan2(ay - by, ax - bx)
        fin = math.atan2(cy - by, cx - bx)
        vuelta = 2 * math.pi
        delta_ccw = (fin - inicio) % vuelta

        medio_ccw = inicio + delta_ccw / 2
        medio_cw = inicio - (vuelta - delta_ccw) / 2

        punto_ccw = (bx + math.cos(medio_ccw) * radio, by + math.sin(medio_ccw) * radio)
        punto_cw = (bx + math.cos(medio_cw) * radio, by + math.sin(medio_cw) * radio)
        distancia_ccw = math.dist(punto_ccw, (centro_x, centro_y))
        distancia_cw = math.dist(punto_cw, (centro_x, centro_y))

        if distancia_ccw <= distancia_cw:
            return inicio, fin, False, medio_ccw, radio
        return inicio, fin, True, medio_cw, radio

    ### GENERAR ETIQUETAS DE ANGULOS ###
    def generarAngulosFigura(self, nombre, figura):
        if figura["tipo"] not in ["triangulo", "cuadrado", "pentagono"]:
            raise Exception("mostrar_angulos solo se puede usar con triangulo, cuadrado o pentagono")

        puntos = figura["puntos"]
        centro_x = sum(x for x, _ in puntos) / len(puntos)
        centro_y = sum(y for _, y in puntos) / len(puntos)

        codigo = """
            ctx.save();
            ctx.strokeStyle = "black";
            ctx.fillStyle = "black";
            ctx.font = "12px Arial";
            ctx.lineWidth = 1.5;
        """

        for i, punto in enumerate(puntos):
            anterior = puntos[i - 1]
            siguiente = puntos[(i + 1) % len(puntos)]
            angulo = self.calcularAnguloInterno(anterior, punto, siguiente)
            inicio, fin, antihorario, direccion_texto, radio = self.calcularMarcaAngulo(
                anterior,
                punto,
                siguiente,
                (centro_x, centro_y)
            )
            x, y = punto
            x_texto = x + math.cos(direccion_texto) * (radio + 10)
            y_texto = y + math.sin(direccion_texto) * (radio + 10)
            etiqueta = f"{self.formatearNumero(angulo)} grados"
            codigo += f"""
            ctx.beginPath();
            ctx.arc({x}, {y}, {radio}, {inicio}, {fin}, {str(antihorario).lower()});
            ctx.stroke();
            ctx.fillText("{self.escaparTexto(etiqueta)}", {x_texto}, {y_texto});
            """

        codigo += """
            ctx.restore();
        """

        return codigo

    ### CALCULAR LINEA NOTABLE
    def calcularLineaNotable(self, triangulo, tipo_linea):
        import math

        puntos = triangulo["puntos"]
        lineas = []

        for i in range(3):
            x1, y1 = puntos[i]
            x2, y2 = puntos[(i + 1) % 3]
            x3, y3 = puntos[(i + 2) % 3]

            if tipo_linea == "mediana":
                px = (x2 + x3) / 2
                py = (y2 + y3) / 2

            elif tipo_linea == "altura":
                dx = x3 - x2
                dy = y3 - y2
                t = ((x1 - x2) * dx + (y1 - y2) * dy) / (dx * dx + dy * dy)
                px = x2 + t * dx
                py = y2 + t * dy

            elif tipo_linea == "bisectriz":
                lado1 = math.dist((x1, y1), (x2, y2))
                lado2 = math.dist((x1, y1), (x3, y3))
                px = (lado2 * x2 + lado1 * x3) / (lado1 + lado2)
                py = (lado2 * y2 + lado1 * y3) / (lado1 + lado2)

            lineas.append([x1, y1, px, py])

        return lineas

    ### VISIT PROGRAMA ###
    def visitPrograma(self, ctx):
        return self.visit(ctx.instrucciones())

    ### VISIT INSTRUCCIONES ###
    def visitInstrucciones(self, ctx):
        for instruccion in ctx.instruccion():
            self.visit(instruccion)

    ### VISIT REPETIR ###
    def visitRepetir(self, ctx):
        num = self.visit(ctx.expr())
        for i in range(num):
            for instruccion in ctx.instruccion():
                self.visit(instruccion)

    ### VISIT ASIGNACION ###
    def visitAsignacion(self, ctx):
        nombre = ctx.ID().getText()
        valor = self.visit(ctx.expr())
        self.variables[nombre] = valor

    ### VISIT PUNTO ###
    def visitPunto(self, ctx):
        nombre = ctx.ID().getText()
        x = self.visit(ctx.expr(0))
        y = self.visit(ctx.expr(1))
        self.figuras[nombre] = {
            "tipo": "punto",
            "x": x,
            "y": y,
            "color": self.obtenerColor(ctx)
        }

    ### VISIT RECTA ###
    def visitRecta(self, ctx):
        nombre = ctx.ID(0).getText()
        color = self.obtenerColor(ctx)
        if len(ctx.ID()) == 3:
            p1 = ctx.ID(1).getText()
            p2 = ctx.ID(2).getText()
            punto1 = self.figuras[p1]
            punto2 = self.figuras[p2]
            self.figuras[nombre] = {
                "tipo": "recta",
                "x1": punto1["x"],
                "y1": punto1["y"],
                "x2": punto2["x"],
                "y2": punto2["y"],
                "color": color
            }
        else:
            self.figuras[nombre] = {
                "tipo": "recta",
                "x1": self.visit(ctx.expr(0)),
                "y1": self.visit(ctx.expr(1)),
                "x2": self.visit(ctx.expr(2)),
                "y2": self.visit(ctx.expr(3)),
                "color": color
            }

    ### VISIT TRIANGULO ###
    def visitTriangulo(self, ctx):
        nombre = ctx.ID(0).getText()
        color = self.obtenerColor(ctx)
        if len(ctx.ID()) == 4:
            p1 = self.figuras[ctx.ID(1).getText()]
            p2 = self.figuras[ctx.ID(2).getText()]
            p3 = self.figuras[ctx.ID(3).getText()]
            self.figuras[nombre] = {
                "tipo": "triangulo",
                "puntos": [
                    (p1["x"], p1["y"]),
                    (p2["x"], p2["y"]),
                    (p3["x"], p3["y"])
                ],
                "color": color
            }
        else:
            self.figuras[nombre] = {
                "tipo": "triangulo",
                "puntos": [
                    (self.visit(ctx.expr(0)), self.visit(ctx.expr(1))),
                    (self.visit(ctx.expr(2)), self.visit(ctx.expr(3))),
                    (self.visit(ctx.expr(4)), self.visit(ctx.expr(5)))
                ],
                "color": color
            }
    ### VISIT CUADRADO ###
    def visitCuadrado(self, ctx):
        nombre = ctx.ID(0).getText()
        color = self.obtenerColor(ctx)
        if len(ctx.ID()) == 5:
            p1 = self.figuras[ctx.ID(1).getText()]
            p2 = self.figuras[ctx.ID(2).getText()]
            p3 = self.figuras[ctx.ID(3).getText()]
            p4 = self.figuras[ctx.ID(4).getText()]
            self.figuras[nombre] = {
                "tipo": "cuadrado",
                "puntos": [
                    (p1["x"], p1["y"]),
                    (p2["x"], p2["y"]),
                    (p3["x"], p3["y"]),
                    (p4["x"], p4["y"])
                ],
                "color": color
            }
        else:
            self.figuras[nombre] = {
                "tipo": "cuadrado",
                "puntos": [
                    (self.visit(ctx.expr(0)), self.visit(ctx.expr(1))),
                    (self.visit(ctx.expr(2)), self.visit(ctx.expr(3))),
                    (self.visit(ctx.expr(4)), self.visit(ctx.expr(5))),
                    (self.visit(ctx.expr(6)), self.visit(ctx.expr(7)))
                ],
                "color": color
            }

    ### VISIT CIRCULO ###
    def visitCirculo(self, ctx):
        nombre = ctx.ID(0).getText()
        color = self.obtenerColor(ctx)

        if len(ctx.ID()) == 2:
            punto_id = ctx.ID(1).getText()
            centro = self.figuras[punto_id]
            x = centro["x"]
            y = centro["y"]
            radio = self.visit(ctx.expr(0))

        else:
            exprs = ctx.expr()
            x = self.visit(exprs[0])
            y = self.visit(exprs[1])
            radio = self.visit(exprs[2]) if len(exprs) == 3 else 30

        self.figuras[nombre] = {
            "tipo": "circulo",
            "x": x,
            "y": y,
            "radio": radio,
            "color": color
        }

    ### VISIT PENTAGONO ###
    def visitPentagono(self, ctx):
        nombre = ctx.ID(0).getText()
        color = self.obtenerColor(ctx)

        if len(ctx.ID()) == 6:
            p1 = self.figuras[ctx.ID(1).getText()]
            p2 = self.figuras[ctx.ID(2).getText()]
            p3 = self.figuras[ctx.ID(3).getText()]
            p4 = self.figuras[ctx.ID(4).getText()]
            p5 = self.figuras[ctx.ID(5).getText()]

            self.figuras[nombre] = {
                "tipo": "pentagono",
                "puntos": [
                    (p1["x"], p1["y"]),
                    (p2["x"], p2["y"]),
                    (p3["x"], p3["y"]),
                    (p4["x"], p4["y"]),
                    (p5["x"], p5["y"])
                ],
                "color": color
            }

        else:
            self.figuras[nombre] = {
                "tipo": "pentagono",
                "puntos": [
                    (self.visit(ctx.expr(0)), self.visit(ctx.expr(1))),
                    (self.visit(ctx.expr(2)), self.visit(ctx.expr(3))),
                    (self.visit(ctx.expr(4)), self.visit(ctx.expr(5))),
                    (self.visit(ctx.expr(6)), self.visit(ctx.expr(7))),
                    (self.visit(ctx.expr(8)), self.visit(ctx.expr(9)))
                ],
                "color": color
            }
    ### VISIT TRASLADAR ###
    def visitTrasladar(self, ctx):
        nombre = ctx.ID().getText()
        dx = self.visit(ctx.expr(0))
        dy = self.visit(ctx.expr(1))
        figura = self.figuras[nombre]

        if figura["tipo"] in ["punto", "circulo"]:
            figura["x"] += dx
            figura["y"] += dy
        elif figura["tipo"] == "recta":
            figura["x1"] += dx; figura["y1"] += dy
            figura["x2"] += dx; figura["y2"] += dy
        elif figura["tipo"] in ["triangulo", "cuadrado", "pentagono"]:
            nuevos = []
            for x, y in figura["puntos"]:
                nuevos.append((x + dx, y + dy))
            figura["puntos"] = nuevos

    ### VISIT MOSTRAR ###
    def visitMostrar(self, ctx):
        if len(ctx.ID()) == 1:
            nombre = ctx.ID(0).getText()
            figura = self.figuras[nombre]
            self.html += self.generarFigura(nombre, figura)

        elif len(ctx.ID()) == 2:
            nombre = ctx.ID(0).getText()
            figura = self.figuras[nombre]
            linea_notable = ctx.ID(1).getText()
            lineas = self.calcularLineaNotable(figura, linea_notable)
            figura[linea_notable] = lineas
            self.html += self.generarFigura(nombre, figura, int(ctx.NUM().getText()))

    ### VISIT MOSTRAR DETALLADO ###
    def visitMostrarDetallado(self, ctx):
        nombre = ctx.ID().getText()
        figura = self.figuras[nombre]
        self.html += self.generarFigura(nombre, figura)
        self.html += self.generarDetalleFigura(nombre, figura)

    ### VISIT MOSTRAR ANGULOS ###
    def visitMostrarAngulos(self, ctx):
        nombre = ctx.ID().getText()
        figura = self.figuras[nombre]
        self.html += self.generarFigura(nombre, figura)
        self.html += self.generarAngulosFigura(nombre, figura)

    ### GENERAR FIGURA ###
    def generarFigura(self, nombre, figura, id_ln=0):
        codigo = ""
        color = figura.get("color", self.COLOR_DEFAULT)
        if figura["tipo"] == "punto":
            x = figura["x"]
            y = figura["y"]
            codigo += f"""
            ctx.strokeStyle = "{color}";
            ctx.fillStyle = "{color}";
            ctx.beginPath();
            ctx.arc({x}, {y}, 5, 0, 2 * Math.PI);
            ctx.fill();
            ctx.fillText("{nombre}({x},{y})", {x}+10, {y}+10);
            """

        elif figura["tipo"] == "recta":
            x1 = figura["x1"]
            y1 = figura["y1"]
            x2 = figura["x2"]
            y2 = figura["y2"]
            codigo += f"""
            ctx.strokeStyle = "{color}";
            ctx.fillStyle = "{color}";
            ctx.beginPath();
            ctx.moveTo({x1}, {y1});
            ctx.lineTo({x2}, {y2});
            ctx.stroke();
            ctx.fillText("{nombre}", ({x1}+{x2})/2, ({y1}+{y2})/2 - 12);
            """

        elif figura["tipo"] == "triangulo":
            for tipo in ["mediana", "bisectriz", "altura"]:
                if tipo in figura and id_ln > 0:
                    ln = figura[tipo][id_ln - 1]
                    codigo += f"""
                    ctx.strokeStyle = "{color}";
                    ctx.fillStyle = "{color}";
                    ctx.beginPath();
                    ctx.moveTo({ln[0]}, {ln[1]});
                    ctx.lineTo({ln[2]}, {ln[3]});
                    ctx.stroke();
                    ctx.fillText("{tipo}", {ln[2]}, {ln[3]});
                    """

            p = figura["puntos"]
            codigo += f"""
            ctx.strokeStyle = "{color}";
            ctx.fillStyle = "{color}";
            ctx.beginPath();
            ctx.moveTo({p[0][0]}, {p[0][1]});
            ctx.lineTo({p[1][0]}, {p[1][1]});
            ctx.lineTo({p[2][0]}, {p[2][1]});
            ctx.closePath();
            ctx.stroke();
            ctx.fillText(
                "{nombre}",
                ({p[0][0]} + {p[1][0]} + {p[2][0]}) / 3,
                ({p[0][1]} + {p[1][1]} + {p[2][1]}) / 3
            );
            """

        elif figura["tipo"] == "cuadrado":
            p = figura["puntos"]
            codigo += f"""
            ctx.strokeStyle = "{color}";
            ctx.fillStyle = "{color}";
            ctx.beginPath();
            ctx.moveTo({p[0][0]}, {p[0][1]});
            ctx.lineTo({p[1][0]}, {p[1][1]});
            ctx.lineTo({p[2][0]}, {p[2][1]});
            ctx.lineTo({p[3][0]}, {p[3][1]});
            ctx.closePath();
            ctx.stroke();
            ctx.fillText(
                "{nombre}",
                ({p[0][0]} + {p[1][0]} + {p[2][0]} + {p[3][0]}) / 4,
                ({p[0][1]} + {p[1][1]} + {p[2][1]} + {p[3][1]}) / 4
            );
            """

        elif figura["tipo"] == "circulo":
            x = figura["x"]
            y = figura["y"]
            r = figura["radio"]
            codigo += f"""
            ctx.strokeStyle = "{color}";
            ctx.fillStyle = "{color}";
            ctx.beginPath();
            ctx.arc({x}, {y}, {r}, 0, 2 * Math.PI);
            ctx.stroke();
            ctx.fillText("{nombre}", {x} + {r} + 5, {y});
            """

        elif figura["tipo"] == "pentagono":
            p = figura["puntos"]

            codigo += f"""
            ctx.strokeStyle = "{color}";
            ctx.fillStyle = "{color}";
            ctx.beginPath();
            ctx.moveTo({p[0][0]}, {p[0][1]});
            ctx.lineTo({p[1][0]}, {p[1][1]});
            ctx.lineTo({p[2][0]}, {p[2][1]});
            ctx.lineTo({p[3][0]}, {p[3][1]});
            ctx.lineTo({p[4][0]}, {p[4][1]});
            ctx.closePath();
            ctx.stroke();

            ctx.fillText(
                "{nombre}",
                ({p[0][0]} + {p[1][0]} + {p[2][0]} + {p[3][0]} + {p[4][0]}) / 5,
                ({p[0][1]} + {p[1][1]} + {p[2][1]} + {p[3][1]} + {p[4][1]}) / 5
            );
            """

        return codigo

    ### VISIT EXPR ###
    def visitExpr(self, ctx):
        if ctx.NUM():
            n = ctx.NUM().getText()
            return float(n) if "." in n else int(n)

        if ctx.ID():
            nombre = ctx.ID().getText()
            return self.variables[nombre]

        if ctx.getChildCount() == 3:
            if ctx.getChild(0).getText() == "(":
                return self.visit(ctx.expr(0))

            izquierda = self.visit(ctx.expr(0))
            derecha = self.visit(ctx.expr(1))
            operador = ctx.getChild(1).getText()

            if operador == "+":
                return izquierda + derecha
            elif operador == "-":
                return izquierda - derecha
            elif operador == "*":
                return izquierda * derecha
            elif operador == "/":
                return izquierda / derecha
