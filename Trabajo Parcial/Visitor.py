
import math
if __name__ is not None and "." in __name__:
    from .FormasParser import FormasParser
    from .FormasVisitor import FormasVisitor
else:
    from FormasParser import FormasParser
    from FormasVisitor import FormasVisitor


class Visitor(FormasVisitor):
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
        self.figuras[nombre] = {"tipo": "punto", "x": x, "y": y}

    ### VISIT RECTA ###
    def visitRecta(self, ctx):
        nombre = ctx.ID(0).getText()
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
                "y2": punto2["y"]
            }
        else:
            self.figuras[nombre] = {
                "tipo": "recta",
                "x1": self.visit(ctx.expr(0)),
                "y1": self.visit(ctx.expr(1)),
                "x2": self.visit(ctx.expr(2)),
                "y2": self.visit(ctx.expr(3))
            }

    ### VISIT TRIANGULO ###
    def visitTriangulo(self, ctx):
        nombre = ctx.ID(0).getText()
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
                ]
            }
        else:
            self.figuras[nombre] = {
                "tipo": "triangulo",
                "puntos": [
                    (self.visit(ctx.expr(0)), self.visit(ctx.expr(1))),
                    (self.visit(ctx.expr(2)), self.visit(ctx.expr(3))),
                    (self.visit(ctx.expr(4)), self.visit(ctx.expr(5)))
                ]
            }
    ### VISIT CUADRADO ###
    def visitCuadrado(self, ctx):
        nombre = ctx.ID(0).getText()
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
                ]
            }
        else:
            self.figuras[nombre] = {
                "tipo": "cuadrado",
                "puntos": [
                    (self.visit(ctx.expr(0)), self.visit(ctx.expr(1))),
                    (self.visit(ctx.expr(2)), self.visit(ctx.expr(3))),
                    (self.visit(ctx.expr(4)), self.visit(ctx.expr(5))),
                    (self.visit(ctx.expr(6)), self.visit(ctx.expr(7)))
                ]
            }
    
    ### VISIT CIRCULO ###
    def visitCirculo(self, ctx):
        nombre = ctx.ID(0).getText()
        
        if len(ctx.ID()) == 2:
            punto_id = ctx.ID(1).getText()
            centro = self.figuras[punto_id]
            x = centro["x"]
            y = centro["y"]
            radio = self.visit(ctx.expr(0))
        
        else:
            x = self.visit(ctx.expr(0))
            if ctx.expr(2):
                y = self.visit(ctx.expr(1))
                radio = self.visit(ctx.expr(2))
            else:
                y = self.visit(ctx.expr(1))
                radio = 30
                
        self.figuras[nombre] = {
            "tipo": "circulo",
            "x": x, 
            "y": y, 
            "radio": radio
        }
    
    ### VISIT PENTAGONO ###
    def visitPentagono(self, ctx):
        nombre = ctx.ID(0).getText()

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
                ]
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
                ]
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

    ### GENERAR FIGURA ###
    def generarFigura(self, nombre, figura, id_ln=0):
        codigo = ""
        if figura["tipo"] == "punto":
            x = figura["x"]
            y = figura["y"]
            codigo += f"""
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
                    ctx.beginPath();
                    ctx.moveTo({ln[0]}, {ln[1]});
                    ctx.lineTo({ln[2]}, {ln[3]});
                    ctx.stroke();
                    ctx.fillText("{tipo}", {ln[2]}, {ln[3]});
                    """

            p = figura["puntos"]
            codigo += f"""
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
            ctx.beginPath();
            ctx.arc({x}, {y}, {r}, 0, 2 * Math.PI);
            ctx.stroke();
            ctx.fillText("{nombre}", {x} + {r} + 5, {y});
            """

        elif figura["tipo"] == "pentagono":
            p = figura["puntos"]

            codigo += f"""
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
