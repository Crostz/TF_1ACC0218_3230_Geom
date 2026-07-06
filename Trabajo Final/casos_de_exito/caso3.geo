lado = 100
radio = 40
radio_escalado = radio * 1.5

punto A(80, 80) color rojo
punto B(80 + lado, 80) color azul
punto C(80 + lado, 80 + lado) color verde
punto D(80, 80 + lado) color morado

cuadrado Q(A, B, C, D) color naranja
mostrar(Q)

trasladar(Q, 220, 80)
mostrar(Q)

circulo CBase(520, 130, radio) color azul
circulo CEscalado(520, 130, radio_escalado) color verde

mostrar(CBase)
mostrar(CEscalado)
