# Generated from Formas.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .FormasParser import FormasParser
else:
    from FormasParser import FormasParser

# This class defines a complete generic visitor for a parse tree produced by FormasParser.

class FormasVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by FormasParser#programa.
    def visitPrograma(self, ctx:FormasParser.ProgramaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormasParser#instrucciones.
    def visitInstrucciones(self, ctx:FormasParser.InstruccionesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormasParser#instruccion.
    def visitInstruccion(self, ctx:FormasParser.InstruccionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormasParser#asignacion.
    def visitAsignacion(self, ctx:FormasParser.AsignacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormasParser#repetir.
    def visitRepetir(self, ctx:FormasParser.RepetirContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormasParser#punto.
    def visitPunto(self, ctx:FormasParser.PuntoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormasParser#recta.
    def visitRecta(self, ctx:FormasParser.RectaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormasParser#triangulo.
    def visitTriangulo(self, ctx:FormasParser.TrianguloContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormasParser#cuadrado.
    def visitCuadrado(self, ctx:FormasParser.CuadradoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormasParser#pentagono.
    def visitPentagono(self, ctx:FormasParser.PentagonoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormasParser#circulo.
    def visitCirculo(self, ctx:FormasParser.CirculoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormasParser#colorOpcional.
    def visitColorOpcional(self, ctx:FormasParser.ColorOpcionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormasParser#colorValor.
    def visitColorValor(self, ctx:FormasParser.ColorValorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormasParser#trasladar.
    def visitTrasladar(self, ctx:FormasParser.TrasladarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormasParser#mostrar.
    def visitMostrar(self, ctx:FormasParser.MostrarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormasParser#mostrarDetallado.
    def visitMostrarDetallado(self, ctx:FormasParser.MostrarDetalladoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormasParser#mostrarAngulos.
    def visitMostrarAngulos(self, ctx:FormasParser.MostrarAngulosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by FormasParser#expr.
    def visitExpr(self, ctx:FormasParser.ExprContext):
        return self.visitChildren(ctx)



del FormasParser