arquivo = open("entradaSintatico.txt", "r")
tokens = arquivo.read()
tokens = tokens.split(" ")
posInicial = 0
posFinal = 0
tempAtual = 0
tabSimb = []
verificacoes = []
cod3End = []
linhaCod = 1

def programa(ch, pos):
    if ch == "program":
        ch, pos = proxsimb(ch, pos)
        if isIdent(ch):
            ch, pos = proxsimb(ch, pos)
            ch, pos = corpo(ch, pos)
            if ch == ".":
                print("Cadeia sintaticamente correta.")
            else:
                print("Erro, esperado . e encontrado %s no %dº token" %(ch, pos+1))
                exit()
        else:
            print("Erro, esperado identificador e encontrado %s no %dº token" %(ch, pos+1))
            exit()
    else:
        print("Erro, esperado program e encontrado %s no %dº token" %(ch, pos+1))
        exit()

def corpo(ch, pos):
    if ch == "begin":
        ch, pos = proxsimb(ch, pos)
        ch, pos = comandos(ch, pos)
        if ch == "end":
            ch, pos = proxsimb(ch, pos)
            return (ch, pos)
        else:
            print("Erro, esperado end e encontrado %s no %dº token" %(ch, pos+1))
            exit()
    elif ch == "var" or ch == "procedure":
        ch, pos = dc(ch, pos)
        if ch == "begin":
            ch, pos = proxsimb(ch, pos)
            ch, pos = comandos(ch, pos)
            if ch == "end":
                ch, pos = proxsimb(ch, pos)
                return (ch, pos)
            else:
                print("Erro, esperado end e encontrado %s no %dº token" %(ch, pos+1))
                exit()
        else:
            print("Erro, esperado begin e encontrado %s no %dº token" %(ch, pos+1))
            exit()
    else:
        print("Erro, esperado begin ou var ou procedure e encontrado %s no %dº token" %(ch, pos+1))
        exit()

def dc(ch, pos):
    if ch == "var":
        ch, pos = dc_v(ch, pos)
        ch, pos = mais_dc(ch, pos)
        return (ch, pos)
    elif ch == "procedure":
        ch, pos = dc_p(ch, pos)
        ch, pos = mais_dc(ch, pos)
        return (ch, pos)
    elif ch == "var":
        return (ch, pos)
    else:
        print("Erro, esperado var ou procedure e encontrado %s no %dº token" %(ch, pos+1))
        exit()

def mais_dc(ch, pos):
    if ch == ";":
        ch, pos = proxsimb(ch, pos)
        if ch == "var" or ch == "procedure":
            ch, pos = dc(ch, pos)
            return (ch, pos)
        else:
            print("Erro, esperado var ou procedure e encontrado %s no %dº token" %(ch, pos+1))
            exit()
    elif ch == "begin":
        return (ch, pos)
    else:
        print("Erro, esperado ; ou begin e encontrado %s no %dº token" %(ch, pos+1))
        exit()        

def dc_v(ch, pos):
    if ch == "var":
        ch, pos = proxsimb(ch, pos)
        if isIdent(ch):
            ch, pos = variaveis(ch, pos)
            if ch == ":":
                ch, pos = proxsimb(ch, pos)
                if ch == "real" or ch == "integer":
                    ch, pos = tipo_var(ch, pos)
                    return (ch, pos)
                else:
                    print("Erro, esperado real ou integer e encontrado %s no %dº token" %(ch, pos+1))
                    exit()  
            else:
                print("Erro, esperado : e encontrado %s no %dº token" %(ch, pos+1))
                exit()  
        else:
            print("Erro, esperado identificador ou begin e encontrado %s no %dº token" %(ch, pos+1))
            exit()    
    else:
        print("Erro, esperado ; ou begin e encontrado %s no %dº token" %(ch, pos+1))
        exit() 


def tipo_var(ch, pos):
    if ch == "real":
        ch, pos = proxsimb(ch, pos)
        return (ch, pos)
    elif ch == "integer":
        ch, pos = proxsimb(ch, pos)
        return (ch, pos)
    else:
        print("Erro, esperado real ou integer e encontrado %s no %dº token" %(ch, pos+1))
        exit()   

def variaveis(ch, pos):
    if isIdent(ch):
        ch, pos = proxsimb(ch, pos)
        if ch == "," or ch == ":" or ch == ")":
            ch, pos = mais_var(ch, pos)
            return (ch, pos)
        else:
            print("Erro, esperado , ou : ou ) e encontrado %s no %dº token" %(ch, pos+1))
            exit()
    else:
        print("Erro, esperado identificador e encontrado %s no %dº token" %(ch, pos+1))
        exit()

def mais_var(ch, pos):
    if ch == ",":
        ch, pos = proxsimb(ch, pos)
        if isIdent(ch):
            ch, pos = variaveis(ch, pos)
            return (ch, pos)
        else:
            print("Erro, esperado identificador e encontrado %s no %dº token" %(ch, pos+1))
            exit()
    elif ch == ":" or ch == ")":
        return (ch, pos)
    else:
        print("Erro, esperado , ou : ou ) e encontrado %s no %dº token" %(ch, pos+1))
        exit()

def dc_p(ch, pos):
    if ch == "procedure":
        ch, pos = proxsimb(ch, pos)
        if isIdent(ch):
            ch, pos = proxsimb(ch, pos)
            if ch == "(" or ch == "var" or ch == "begin":
                ch, pos = parametros(ch, pos)
                if ch == "var" or ch == "begin":
                    ch, pos = corpo_p(ch, pos)
                    return (ch, pos)
                else:
                    print("Erro, esperado var ou begin e encontrado %s no %dº token" %(ch, pos+1))
                    exit() 
            else:
                print("Erro, esperado ( ou var ou begin e encontrado %s no %dº token" %(ch, pos+1))
                exit() 
        else:
            print("Erro, esperado identificador e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    else:
        print("Erro, esperado procedure e encontrado %s no %dº token" %(ch, pos+1))
        exit() 
    
def parametros(ch, pos):
    if ch == "(":
        ch, pos = proxsimb(ch, pos)
        if isIdent(ch):
            ch, pos = lista_par(ch, pos)
            if ch == ")":
                ch, pos = proxsimb(ch, pos)
                return (ch, pos)
            else:
                print("Erro, esperado ) e encontrado %s no %dº token" %(ch, pos+1))
                exit() 
        else:
            print("Erro, esperado identificador e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    elif ch == "var" or ch == "begin":
        return (ch, pos)
    else:
        print("Erro, esperado ( ou var ou begin e encontrado %s no %dº token" %(ch, pos+1))
        exit()

def lista_par(ch, pos):
    if isIdent(ch) or ch == "begin":
        ch, pos = variaveis(ch, pos)
        if ch == ":":
            ch, pos = proxsimb(ch, pos)
            if ch == "real" or ch == "integer":
                ch, pos = tipo_var(ch, pos)
                if ch == ";" or ch == ")":
                    ch, pos = mais_par(ch, pos)
                    return (ch, pos)
                else:
                    print("Erro, esperado ; ou ) e encontrado %s no %dº token" %(ch, pos+1))
                    exit() 
            else:
                print("Erro, esperado real ou integer e encontrado %s no %dº token" %(ch, pos+1))
                exit() 
        else:
            print("Erro, esperado : e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    else:
        print("Erro, esperado identificador ou begin e encontrado %s no %dº token" %(ch, pos+1))
        exit() 

def mais_par(ch, pos):
    if ch == ";":
        ch, pos = proxsimb(ch, pos)
        if isIdent(ch):
            ch, pos = lista_par(ch, pos)
            return (ch, pos)
        else:
            print("Erro, esperado identificador e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    elif ch == ")":
        return (ch, pos)
    else:
        print("Erro, esperado ; ou ) e encontrado %s no %dº token" %(ch, pos+1))
        exit() 

def corpo_p(ch, pos):
    if ch == "var" or ch == "begin":
        ch, pos = dc_loc(ch, pos)
        if ch == "begin":
            ch, pos = proxsimb(ch, pos)
            if isIdent(ch) or ch == "read" or ch == "write" or ch == "while" or ch == "if":
                ch, pos = comandos(ch, pos)
                if ch == "end":
                    ch, pos = proxsimb(ch, pos)
                    return (ch, pos)
                else:
                    print("Erro, esperado end e encontrado %s no %dº token" %(ch, pos+1))
                    exit() 
            else:
                print("Erro, esperado read ou write ou while ou if e encontrado %s no %dº token" %(ch, pos+1))
                exit() 
        else:
            print("Erro, esperado begin e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    else:
        print("Erro, esperado var ou begin e encontrado %s no %dº token" %(ch, pos+1))
        exit() 

def dc_loc(ch, pos):
    if ch == "var":
        ch, pos = dc_v(ch, pos)
        if ch == ";" or ch == "begin":
            ch, pos = mais_dcloc(ch, pos)
            return (ch, pos)
        else:
            print("Erro, esperado ; ou begin e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    elif ch == "begin":
        return (ch, pos)
    else:
        print("Erro, esperado var ou begin e encontrado %s no %dº token" %(ch, pos+1))
        exit() 

def mais_dcloc(ch, pos):
    if ch == ";":
        ch, pos = proxsimb(ch, pos)
        if ch == "var" or ch == "begin":
            ch, pos = dc_loc(ch, pos)
            return (ch, pos)
        else:
            print("Erro, esperado var ou begin e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    elif ch == "begin":
        return (ch, pos)
    else:
        print("Erro, esperado procedure e encontrado %s no %dº token" %(ch, pos+1))
        exit() 

def lista_arg(ch, pos):
    if ch == "(":
        ch, pos = proxsimb(ch, pos)
        if isIdent(ch):
            ch, pos = argumentos(ch, pos)
            if ch == ")":
                ch, pos = proxsimb(ch, pos)
                return (ch, pos)
            else:
                print("Erro, esperado ) e encontrado %s no %dº token" %(ch, pos+1))
                exit() 
    elif ch == "end" or ch == ";" or ch == "else" or ch == "$":
        return (ch, pos)
    else:
        print("Erro, esperado ( ou end ou ; ou else ou $) e encontrado %s no %dº token" %(ch, pos+1))
        exit() 

def argumentos(ch, pos):
    if isIdent(ch):
        ch, pos = proxsimb(ch, pos)
        if ch == ";" or ch == ")":
            ch, pos = mais_ident(ch, pos)
            return (ch, pos)
        else:
            print("Erro, esperado ; ou ) e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    else:
        print("Erro, esperado identificador e encontrado %s no %dº token" %(ch, pos+1))
        exit() 

def mais_ident(ch, pos):
    if ch == ";":
        ch, pos = proxsimb(ch, pos)
        if isIdent(ch):
            ch, pos = argumentos(ch, pos)
            return (ch, pos)
        else:
            print("Erro, esperado identificador e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    elif ch == ")":
        return (ch, pos)
    else:
        print("Erro, esperado procedure e encontrado %s no %dº token" %(ch, pos+1))
        exit() 

def pfalsa(ch, pos):
    if ch == "else":
        ch, pos = proxsimb(ch, pos)
        if isIdent(ch) or ch == "read" or ch == "write" or ch =="while" or ch == "if":
            ch, pos = comandos(ch, pos)
            return (ch, pos)
        else:
            print("Erro, esperado identificador ou read ou write ou while ou if e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    elif ch == "$":
        return (ch, pos)
    else:
        print("Erro, esperado else ou $ e encontrado %s no %dº token" %(ch, pos+1))
        exit() 

def comandos(ch, pos):
    if isIdent(ch) or ch == "read" or ch == "write" or ch =="while" or ch == "if":
        ch, pos = comando(ch, pos)
        if ch == ";" or ch == "end" or ch == "else" or ch == "$":
            ch, pos = mais_comandos(ch, pos)
            return (ch, pos)
        else:
            print("Erro, esperado ; ou end ou else ou $ e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    else:
        print("Erro, esperado identificador ou read ou write ou while ou if e encontrado %s no %dº token" %(ch, pos+1))
        exit() 

def mais_comandos(ch, pos):
    if ch == ";":
        ch, pos = proxsimb(ch, pos)
        if isIdent(ch) or ch == "read" or ch == "write" or ch =="while" or ch == "if":
            ch, pos = comandos(ch, pos)
            return (ch, pos)
        else:
            print("Erro, esperado identificador ou read ou write ou while ou if e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    elif ch == "end" or ch == "else" or ch == "$":
        return (ch, pos)
    else:
        print("Erro, esperado ; ou end ou else ou $ e encontrado %s no %dº token" %(ch, pos+1))
        exit() 

def comando(ch, pos):
    if ch == "read":
        ch, pos = proxsimb(ch, pos)
        if ch == "(":
            ch, pos = proxsimb(ch, pos)
            if isIdent(ch):
                ch, pos = variaveis(ch, pos)
                if ch == ")":
                    ch, pos = proxsimb(ch, pos)
                    return (ch, pos)
                else:
                    print("Erro, esperado ) e encontrado %s no %dº token" %(ch, pos+1))
                    exit() 
            else:
                print("Erro, esperado identificador e encontrado %s no %dº token" %(ch, pos+1))
                exit() 
        else:
            print("Erro, esperado ) e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    elif ch == "write":
        ch, pos = proxsimb(ch, pos)
        if ch == "(":
            ch, pos = proxsimb(ch, pos)
            if isIdent(ch):
                ch, pos = variaveis(ch, pos)
                if ch == ")":
                    ch, pos = proxsimb(ch, pos)
                    return (ch, pos)
                else:
                    print("Erro, esperado ) e encontrado %s no %dº token" %(ch, pos+1))
                    exit() 
            else:
                print("Erro, esperado identificador e encontrado %s no %dº token" %(ch, pos+1))
                exit() 
        else:
            print("Erro, esperado ) e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    elif ch == "while":
        ch, pos = proxsimb(ch, pos)
        if isIdent(ch) or ch == "(" or ch == "+" or ch == "-" or isInt(ch) or isReal(ch):
            ch, pos = condicao(ch, pos)
            if ch == "do":
                ch, pos = proxsimb(ch, pos)
                if isIdent(ch) or ch == "read" or ch == "write" or ch == "while" or ch == "if":
                    ch, pos = comandos(ch, pos)
                    if ch == "$":
                        ch, pos = proxsimb(ch, pos)
                        return (ch, pos)
                    else:
                        print("Erro, esperado procedure e encontrado %s no %dº token" %(ch, pos+1))
                        exit() 
                else:
                    print("Erro, esperado identificador ou read ou write ou while ou if e encontrado %s no %dº token" %(ch, pos+1))
                    exit() 
            else:
                print("Erro, esperado do e encontrado %s no %dº token" %(ch, pos+1))
                exit() 
        else:
            print("Erro, esperado ( ou + ou - ou numero_int ou numero_real e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    elif ch == "if":
        ch, pos = proxsimb(ch, pos)
        if isIdent(ch) or ch == "(" or ch == "+" or ch == "-" or isInt(ch) or isReal(ch):
            ch, pos = condicao(ch, pos)
            if ch == "then":
                ch, pos = proxsimb(ch, pos)
                if isIdent(ch) or ch == "read" or ch == "write" or ch == "while" or ch == "if":
                    ch, pos = comandos(ch, pos)
                    if ch == "else" or ch == "$":
                        ch, pos = pfalsa(ch, pos)
                        if ch == "$":
                            ch, pos = proxsimb(ch, pos)
                            return (ch, pos)
                        else:
                            print("Erro, $ procedure e encontrado %s no %dº token" %(ch, pos+1))
                            exit() 
                    else:
                        print("Erro, esperado else ou $ e encontrado %s no %dº token" %(ch, pos+1))
                        exit() 
                else:
                    print("Erro, esperado identificador ou read ou write ou while ou if e encontrado %s no %dº token" %(ch, pos+1))
                    exit() 
            else:
                print("Erro, esperado then e encontrado %s no %dº token" %(ch, pos+1))
                exit() 
        else:
            print("Erro, esperado ( ou + ou - ou numero_int ou numero_real e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    elif isIdent(ch):
        ch, pos = proxsimb(ch, pos)
        if ch == "(" or ch == ":=" or ch == "else" or ch == "$" or ch == "end" or ch == ";":
            ch, pos = restoIdent(ch, pos)
            return (ch, pos)
        else:
            print("Erro, esperado ( ou := else ou $ ou end ou ; e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    else:
        print("Erro, esperado read ou write ou while o if ou identificador e encontrado %s no %dº token" %(ch, pos+1))
        exit() 

def restoIdent(ch, pos):
    if ch == ":=":
        ch, pos = proxsimb(ch, pos)
        if ch == "(" or isIdent(ch) or isInt(ch) or isReal(ch) or ch == "+" or ch == "-":
            ch, pos = expressao(ch, pos)
            return (ch, pos)
        else:
            print("Erro, esperado ( ou identificador ou numero_inteiro ou numero_real ou + ou - e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    elif ch == "(" or ch == "end" or ch == ";" or ch == "else" or ch == "$":
        ch, pos = lista_arg(ch, pos)
        return (ch, pos)
    else:
        print("Erro, esperado := ou ( end ou ; ou else oou $ e encontrado %s no %dº token" %(ch, pos+1))
        exit() 

def condicao(ch, pos):
    if ch == "(" or isIdent(ch) or isInt(ch) or isReal(ch) or ch == "+" or ch == "-":
        ch, pos = expressao(ch, pos)
        if ch == "=" or ch == "<>" or ch == ">=" or ch == "<=" or ch == ">" or ch == "<":
            ch, pos = relacao(ch, pos)
            if ch == "(" or isIdent(ch) or isInt(ch) or isReal(ch) or ch == "+" or ch == "-":
                ch, pos = expressao(ch, pos)
                return (ch, pos)
            else:
                print("Erro, esperado ( ou identificador ou numero_inteiro ou numero_real ou + ou - e encontrado %s no %dº token" %(ch, pos+1))
                exit() 
        else:
            print("Erro, esperado = ou <> ou >= ou <= ou > ou < e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    else:
        print("Erro, esperado ( ou identificador ou numero_inteiro ou numero_real ou + ou - e encontrado %s no %dº token" %(ch, pos+1))
        exit()     

def relacao(ch, pos):
    if ch == "=" or ch == "<>" or ch == ">=" or ch == "<=" or ch == ">" or ch == "<":
        ch, pos = proxsimb(ch, pos)
        return (ch, pos)
    else:
        print("Erro, esperado = ou <> ou >= ou <= ou > ou < e encontrado %s no %dº token" %(ch, pos+1))
        exit() 

def expressao(ch, pos):
    if isInt(ch) or isReal(ch) or ch == "+" or ch == "-" or isIdent(ch) or ch == "(":
        ch, pos = termo(ch, pos)
        if ch == "+" or ch == "-" or ch == "end" or ch == ";" or ch == ")" or ch == "else" or ch == "do" or ch == "$" or ch == "then" or ch == "=" or ch == "<>" or ch == ">=" or ch == "<=" or ch == ">" or ch == "<":
            ch, pos = outros_termos(ch, pos)
            return (ch, pos)
        else:
            print("Erro, esperado + ou - ou end ou ; ou ) ou else ou do ou $ ou then ou then ou = ou <> ou >= ou <= ou > ou < e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    else:
        print("Erro, esperado numero_inteiro ou numero_real ou + ou - ou identificador ou ( e encontrado %s no %dº token" %(ch, pos+1))
        exit()

def op_un(ch, pos):
    if ch == "+":
        ch, pos = proxsimb(ch, pos)
        return (ch, pos)
    elif ch == "-":
        ch, pos = proxsimb(ch, pos)
        return (ch, pos)
    elif isIdent(ch) or ch == "(" or isInt(ch) or isReal(ch):
        return (ch, pos)
    else:
        print("Erro, esperado + ou - ou ( ou numero_inteiro ou numero_real e encontrado %s no %dº token" %(ch, pos+1))
        exit() 

def outros_termos(ch, pos):
    if isIdent(ch) or ch == "(" or ch == "+" or ch == "-" or isInt(ch) or isReal(ch):
        ch, pos = op_ad(ch, pos)
        if isInt(ch) or isReal(ch) or ch == "+" or ch == "-" or isIdent(ch) or ch == "(":
            ch, pos = termo(ch, pos)
            ch, pos = outros_termos(ch, pos)
            return (ch, pos)
        else:
            print("Erro, esperado numero_inteiro ou numero_real ou + ou - ou identificador ou ( e encontrado %s no %dº token" %(ch, pos+1))
            exit()
    if ch == "end" or ch == ";" or ch == ch == ")" or ch == "else" or ch == "do" or ch == "$" or ch == "then" or ch == "=" or ch == "<>" or ch == ">=" or ch == "<=" or ch == ">" or ch == "<":
        return (ch, pos)
    else:
        print("Erro, esperado identificador, ou ( ou + ou - ou end ou ; ou ) ou else ou do ou $ ou then ou = ou <> ou >= ou <= ou > ou < e encontrado %s no %dº token" %(ch, pos+1))
        exit() 

def op_ad(ch, pos):
    if ch == "+" or ch == "-":
        ch, pos = proxsimb(ch, pos)
        return (ch, pos)
    else:
        print("Erro, esperado + ou - e encontrado %s no %dº token" %(ch, pos+1))
        exit() 

def termo(ch, pos):
    ch, pos = op_un(ch, pos)
    ch, pos = fator(ch, pos)
    ch, pos = mais_fatores(ch, pos)
    return (ch, pos)

def mais_fatores(ch, pos):
    if ch == "*" or ch == "/":
        ch, pos = op_mul(ch, pos)
        ch, pos = fator(ch, pos)
        ch, pos = mais_fatores(ch, pos)
        return (ch, pos)
    elif ch == "end" or ch == ";" or ch == ")" or ch == "else" or ch == "do" or ch == "$" or ch == "then" or ch == "=" or ch == "<>" or ch == ">=" or ch == "<=" or ch == ">" or ch == "<" or ch == "+" or ch == "-":
        return (ch, pos)
    else:
        print("Erro, esperado * ou / ou end ou ; ou ) ou else ou do ou $ ou then ou = ou <> ou >= ou <= ou > ou < ou + ou - e encontrado %s no %dº token" %(ch, pos+1))
        exit() 

def op_mul(ch, pos):
    if ch == "*" or ch == "/":
        ch, pos = proxsimb(ch, pos)
        return (ch, pos)
    else:
        print("Erro, esperado * ou / e encontrado %s no %dº token" %(ch, pos+1))
        exit() 

def fator(ch, pos):
    if isIdent(ch) or isInt(ch) or isReal(ch):
        ch, pos = proxsimb(ch, pos)
        return (ch, pos)
    elif ch == "(":
        ch, pos = proxsimb(ch, pos)
        ch, pos = expressao(ch, pos)
        if ch == ")":
            ch, pos = proxsimb(ch, pos)
            return (ch, pos)
        else:
            print("Erro, esperado ) e encontrado %s no %dº token" %(ch, pos+1))
            exit() 
    else:
        print("Erro, esperado identificador ou numero_real ou numero_inteiro ou ( e encontrado %s no %dº token" %(ch, pos+1))
        exit() 

def proxsimb(ch, pos):
    if pos < len(tokens)-1:
        return (tokens[pos + 1], pos + 1)
    else:
        return ("#", pos)

def isIdent(ch):
    if ch == "var" or ch == "integer" or ch == "real" or ch == "if" or ch == "then" or ch == "do" or ch == "(" or ch == ")" or ch == "*" or ch == "/" or ch == "+" or ch == "-" or ch == "<>" or ch == ">=" or ch == "<=" or ch == ">" or ch == "<" or ch == "=" or ch == "$" or ch == "while" or ch == "write" or ch == "real" or ch == ";" or ch == "else" or ch == "begin" or ch == "end" or ch == ":" or ch == ",":
        return False
    elif (ch[0] >= "a" and ch[0] <= "z") or (ch[0] >= "A" and ch[0] <= "Z"):
        return True
    else:
        return False

def isInt(ch):
    try: 
        int(ch)
        return True
    except ValueError:
        return False

def isReal(ch):
    try: 
        float(ch)
        return True
    except ValueError:
        return False

def addTabSimb(ch):
    global posFinal, tabSimb
    for i in range(0, len(tabSimb)):
        if tabSimb[i]['Cadeia'] == ch:
            print('Cadeia ' + ch + " ja existe na tabela de simbolos.")
            exit()
    posFinal = posFinal + 1
    conteudo = {'Cadeia': ch, 'Token': 'id', 'Categoria': 'var', 'Tipo': 'null'}
    tabSimb.append(conteudo)

def addTipo(ch, tipo):
    global posInicial, posFinal, tabSimb
    for i in range(posInicial, posFinal):
        tabSimb[i]['Tipo'] = tipo
    posInicial = posFinal

def addListaVerificacao(ch):
    global verificacoes, tabSimb
    for i in range(len(tabSimb)):
        if tabSimb[i]['Cadeia'] == ch:
            verificacoes.append(tabSimb[i]['Tipo'])

def verificaTipo(verificacoes):
    tipo = verificacoes[0]
    for i in verificacoes:
        if i != tipo:
            print("Impossivel operar real com inteiro")
            return False
    verificacoes = []
    return True

def existe(ch):
    global tabSimb
    for i in range(len(tabSimb)):
        if tabSimb[i]['Cadeia'] == ch:
            return True
    return False

def geraTemp(ch):
    global tabSimb, tempAtual
    for i in range(len(tabSimb)):
        if ch == tabSimb[i]['Cadeia']:
            tipo = tabSimb[i]['Tipo']
    tempAtual = tempAtual + 1
    conteudo = {'Cadeia': 't' + str(tempAtual), 'Token': 'id', 'Categoria': 'var', 'Tipo': tipo}
    tabSimb.append(conteudo)
    return 't' + str(tempAtual)

#Main
programa(tokens[0], 0)
arquivo.close()
