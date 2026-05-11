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
    ;

asignacion: ID IGUAL expr ;

repetir: REPETIR expr VECES LPAREN instruccion+ RPAREN ;

punto: PUNTO ID LPAREN expr COMA expr RPAREN ;

recta
    : RECTA ID LPAREN ID COMA ID RPAREN
    | RECTA ID LPAREN expr COMA expr COMA expr COMA expr RPAREN
    ;

triangulo
    : TRIANGULO ID LPAREN ID COMA ID COMA ID RPAREN
    | TRIANGULO ID LPAREN expr COMA expr COMA expr COMA expr COMA expr COMA expr RPAREN
    ;

cuadrado
    : CUADRADO ID LPAREN ID COMA ID COMA ID COMA ID RPAREN
    | CUADRADO ID LPAREN expr COMA expr COMA expr COMA expr COMA expr COMA expr COMA expr COMA expr RPAREN
    ;

pentagono
    : PENTAGONO ID LPAREN ID COMA ID COMA ID COMA ID COMA ID RPAREN
    | PENTAGONO ID LPAREN expr COMA expr COMA expr COMA expr COMA expr COMA expr COMA expr COMA expr COMA expr COMA expr RPAREN
    ;

trasladar
    : TRASLADAR LPAREN ID COMA expr COMA expr RPAREN
    ;

mostrar
    : MOSTRAR LPAREN ID RPAREN
    | MOSTRAR LPAREN ID DOT ID LPAREN NUM RPAREN RPAREN 
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

TRASLADAR : 'trasladar';
MOSTRAR   : 'mostrar';

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
