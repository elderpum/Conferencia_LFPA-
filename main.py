# Analizador léxico (Tokenizador)
def tokenizar(codigo):
    tokens = []
    i = 0
    while i < len(codigo):
        if codigo[i].isdigit():
            numero = ''
            while i < len(codigo) and (codigo[i].isdigit() or codigo[i] == '.'):
                numero += codigo[i]
                i += 1
            tokens.append(('NUMERO', numero))
        elif codigo[i] == '"':
            cadena = '"'
            i += 1
            while i < len(codigo) and codigo[i] != '"':
                cadena += codigo[i]
                i += 1
            cadena += '"'
            i += 1
            tokens.append(('CADENA', cadena))
        elif codigo[i].isalpha() or codigo[i] == '_':
            identificador = ''
            while i < len(codigo) and (codigo[i].isalnum() or codigo[i] == '_'):
                identificador += codigo[i]
                i += 1
            tokens.append(('ID', identificador))
        elif codigo[i] in '+-*/=<>!':
            operador = codigo[i]
            i += 1
            while i < len(codigo) and codigo[i] in '+-*/=<>!':
                operador += codigo[i]
                i += 1
            tokens.append(('OP', operador))
        elif codigo[i] in '();,{}':
            tokens.append(('PUNTUACION', codigo[i]))
            i += 1
        elif codigo[i] in ' \t\n':
            i += 1
        else:
            raise RuntimeError(f'Carácter inesperado: {codigo[i]}')
    return tokens

# Analizador sintáctico (Parser)
class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.indice_actual = 0
        self.avanzar_token()

    def avanzar_token(self):
        self.token_actual = self.tokens[self.indice_actual] if self.indice_actual < len(self.tokens) else (None, None)
        self.indice_actual += 1

    def consumir(self, tipo_esperado):
        if self.token_actual[0] == tipo_esperado:
            token = self.token_actual
            self.avanzar_token()
            return token
        else:
            raise SyntaxError(f'Se esperaba {tipo_esperado}, pero se encontró {self.token_actual[0]}')

    def analizar(self):
        while self.token_actual[0] is not None:
            if self.token_actual[0] == 'ID' and self.token_actual[1] == 'function':
                self.analizar_funcion()
            elif self.token_actual[0] == 'ID' and self.token_actual[1] in ['let', 'var', 'const']:
                self.analizar_declaracion_variable()
            else:
                raise SyntaxError(f'Token inesperado: {self.token_actual}')

    def analizar_funcion(self):
        self.consumir('ID')  # Consume 'function'
        nombre_funcion = self.consumir('ID')[1]  # Consume el nombre de la función
        self.consumir('PUNTUACION')  # Consume '('
        self.analizar_parametros()
        self.consumir('PUNTUACION')  # Consume ')'
        self.analizar_bloque()
        print(f"Función definida: {nombre_funcion}")

    def analizar_parametros(self):
        while self.token_actual[0] != 'PUNTUACION' or self.token_actual[1] != ')':
            if self.token_actual[0] == 'ID':
                self.consumir('ID')
            if self.token_actual[1] == ',':
                self.consumir('PUNTUACION')

    def analizar_bloque(self):
        self.consumir('PUNTUACION')  # Consume '{'
        while self.token_actual[1] != '}':
            if self.token_actual[0] == 'ID' and self.token_actual[1] in ['var', 'let', 'const']:
                self.analizar_declaracion_variable()
            elif self.token_actual[0] == 'ID' and self.token_actual[1] == 'return':
                self.analizar_declaracion_retorno()
            else:
                self.analizar_expresion()
            if self.token_actual[1] == ';':
                self.consumir('PUNTUACION')
        self.consumir('PUNTUACION')  # Consume '}'

    def analizar_declaracion_variable(self):
        tipo_var = self.consumir('ID')[1]  # Consume 'var', 'let' o 'const'
        nombre_var = self.consumir('ID')[1]  # Consume el nombre de la variable
        if self.token_actual[1] == '=':
            self.consumir('OP')  # Consume '='
            self.analizar_expresion()
        self.consumir('PUNTUACION')  # Consume ';'
        print(f"Variable declarada: {tipo_var} {nombre_var}")

    def analizar_declaracion_retorno(self):
        self.consumir('ID')  # Consume 'return'
        self.analizar_expresion()

    def analizar_expresion(self):
        # Esta es una implementación muy simplificada
        while self.token_actual[0] in ['ID', 'NUMERO', 'CADENA', 'OP']:
            self.avanzar_token()

# Ejemplo de uso
codigo = """
function sumar(a, b, c) {
    var resultado = a + b;
    return resultado;
}

let mensaje = "Hola, Mundo!";
const PI = 3.1416;
const texto = mensaje + " " + PI;
const texto2 = texto + " " + 10;
"""

tokens = tokenizar(codigo)
analizador = AnalizadorSintactico(tokens)
analizador.analizar()