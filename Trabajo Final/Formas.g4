grammar Formas;

programa: instrucciones EOF;

instrucciones: instruccion*;

instruccion
    : asignacion
    | punto
    | recta
    | triangulo
    | cuadrado
    | pentagono
    | repetir
    | trasladar
    | mostrar
    | mostrarDetallado
    | mostrarAngulos
    | circulo
    ;

asignacion: ID IGUAL expr ;

repetir: REPETIR expr VECES LPAREN instruccion+ RPAREN ;

punto: PUNTO ID LPAREN expr COMA expr RPAREN colorOpcional ;

recta
    : RECTA ID LPAREN ID COMA ID RPAREN colorOpcional
    | RECTA ID LPAREN expr COMA expr COMA expr COMA expr RPAREN colorOpcional
    ;

triangulo
    : TRIANGULO ID LPAREN ID COMA ID COMA ID RPAREN colorOpcional
    | TRIANGULO ID LPAREN expr COMA expr COMA expr COMA expr COMA expr COMA expr RPAREN colorOpcional
    ;

cuadrado
    : CUADRADO ID LPAREN ID COMA ID COMA ID COMA ID RPAREN colorOpcional
    | CUADRADO ID LPAREN expr COMA expr COMA expr COMA expr COMA expr COMA expr COMA expr COMA expr RPAREN colorOpcional
    ;

pentagono
    : PENTAGONO ID LPAREN ID COMA ID COMA ID COMA ID COMA ID RPAREN colorOpcional
    | PENTAGONO ID LPAREN expr COMA expr COMA expr COMA expr COMA expr COMA expr COMA expr COMA expr COMA expr COMA expr RPAREN colorOpcional
    ;

circulo
    : CIRCULO ID LPAREN ID COMA expr RPAREN colorOpcional
    | CIRCULO ID LPAREN expr COMA expr (COMA expr)? RPAREN colorOpcional
    ;

colorOpcional
    : COLOR colorValor
    |
    ;

colorValor
    : ROJO
    | VERDE
    | AZUL
    | AMARILLO
    | NARANJA
    | MORADO
    | NEGRO
    | MARRON
    ;

trasladar
    : TRASLADAR LPAREN ID COMA expr COMA expr RPAREN
    ;

mostrar
    : MOSTRAR LPAREN ID RPAREN
    | MOSTRAR LPAREN ID DOT ID LPAREN NUM RPAREN RPAREN
    ;

mostrarDetallado
    : MOSTRAR_DETALLADO LPAREN ID RPAREN
    ;

mostrarAngulos
    : MOSTRAR_ANGULOS LPAREN ID RPAREN
    ;

expr
    : expr op=(MULT | DIV) expr
    | expr op=(MAS | MENOS) expr
    | NUM
    | ID
    | LPAREN expr RPAREN
    ;

REPETIR   : 'repetir';
VECES     : 'veces';
PUNTO     : 'punto';
RECTA     : 'recta';

TRIANGULO : 'triangulo';
CUADRADO  : 'cuadrado';
PENTAGONO : 'pentagono';
CIRCULO   : 'circulo';
TRASLADAR : 'trasladar';
MOSTRAR_ANGULOS : 'mostrar_angulos';
MOSTRAR_DETALLADO : 'mostrar_detallado';
MOSTRAR   : 'mostrar';
COLOR     : 'color';
ROJO      : 'rojo';
VERDE     : 'verde';
AZUL      : 'azul';
AMARILLO  : 'amarillo';
NARANJA   : 'naranja';
MORADO    : 'morado';
NEGRO     : 'negro';
MARRON    : 'marron';

IGUAL : '=';
DOT   : '.';
COMA  : ',';
LPAREN: '(';
RPAREN: ')';

MAS   : '+';
MENOS : '-';
MULT  : '*';
DIV   : '/';

ID  : [a-zA-Z][a-zA-Z0-9_]*;
NUM : [0-9]+ ('.' [0-9]+)?;

WS : [ \t\r\n]+ -> skip;
