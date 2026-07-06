
lado = 120
radio = 45

punto A(120, 120) color rojo
punto B(240, 120) color azul
punto C(180, 240) color verde

triangulo T1(A, B, C) color morado

mostrar_detallado(A)
mostrar(B)
mostrar(C)
mostrar_angulos(T1)

circulo C1(A, 20) color naranja
circulo C2(B, 20) color amarillo
circulo C3(C, 20) color marron

mostrar(C1)
mostrar(C2)
mostrar(C3)

punto D(420, 100) color rojo
punto E(560, 100) color azul
punto F(560, 240) color verde
punto G(420, 240) color morado

cuadrado Q1(D, E, F, G) color naranja

mostrar(D)
mostrar(E)
mostrar(F)
mostrar(G)

mostrar_detallado(Q1)

recta R1(D, F) color amarillo
recta R2(E, G) color marron

mostrar(R1)
mostrar(R2)

punto H(760, 110) color rojo
punto I(860, 170) color azul
punto J(830, 290) color verde
punto K(690, 290) color morado
punto L(660, 170) color naranja

pentagono P1(H, I, J, K, L) color marron


mostrar_angulos(P1)

circulo Sol(980, 120) color amarillo

mostrar(Sol)

repetir 6 veces (
    trasladar(Sol, -15, 15)
    mostrar(Sol)
)

recta Camino1(100, 420, 300, 420) color rojo
recta Camino2(300, 420, 500, 500) color verde
recta Camino3(500, 500, 750, 420) color azul

mostrar_detallado(Camino1)
mostrar(Camino2)
mostrar(Camino3)

punto X1(880, 420) color negro
punto X2(980, 420) color negro
punto X3(980, 520) color negro
punto X4(880, 520) color negro

cuadrado Casa(X1, X2, X3, X4) color marron

mostrar_detallado(Casa)

triangulo Techo(880, 420, 980, 420, 930, 340) color naranja

mostrar_detallado(Techo)

circulo Ventana(930, 470, 20) color azul

mostrar_detallado(Ventana)
