arquivo = open("entradaSintatico.txt", "r")
tokens = arquivo.read()
tokens = tokens.split(" ")

arqLinhas = open("linhas.txt", "r")
linhas = arqLinhas.read()
linhas = linhas.split(" ")

posInicial = 0
posFinal = 0
tempAtual = 0
tabSimb = []
verificacoes = []
cod3End = []
linhaCod = 1

def programa(ch, pos):
    if ch == "program":
        ch, pos = proxsimb(pos)
        if isIdent(ch):
            ch, pos = proxsimb(pos)
            ch, pos = corpo(ch, pos)
            if ch == ".":
                print("Cadeia sintaticamente correta.")
            else:
                print("Erro sintatico, esperado . e encontrado %s na linha %d" %(ch, linha(pos+1)))
                exit()
        else:
            print("Erro sintatico, esperado identificador e encontrado %s na linha %d" %(ch, linha(pos+1)))
            exit()
    else:
        print("Erro sintatico, esperado program e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit()

def corpo(ch, pos):
    ch, pos = dc(ch, pos)
    if ch == "begin":
        ch, pos = proxsimb(pos)
        ch, pos = comandos(ch, pos)
        if ch == "end":
            ch, pos = proxsimb(pos)
            return (ch, pos)
        else:
            print("Erro sintatico, esperado end e encontrado %s na linha %d" %(ch, linha(pos+1)))
            exit()
    else:
        print("Erro sintatico, esperado begin e encontrado %s na linha %d" %(ch, linha(pos+1)))
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
    elif ch == "begin":
        return (ch, pos)
    else:
        print("Erro sintatico, esperado var ou procedure ou begin e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit()

def mais_dc(ch, pos):
    if ch == ";":
        ch, pos = proxsimb(pos)
        ch, pos = dc(ch, pos)
        return (ch, pos)
    elif ch == "begin":
        return (ch, pos)
    else:
        print("Erro sintatico, esperado ; ou begin e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit()        

def dc_v(ch, pos):
    if ch == "var":
        ch, pos = proxsimb(pos)
        ch, pos = variaveis(ch, pos)
        if ch == ":":
            ch, pos = proxsimb(pos)
            ch, pos = tipo_var(ch, pos)
            return (ch, pos)
        else:
            print("Erro sintatico, esperado : e encontrado %s na linha %d" %(ch, linha(pos+1)))
            exit()     
    else:
        print("Erro sintatico, esperado ; ou begin e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 


def tipo_var(ch, pos):
    if ch == "real" or ch == "integer":
        ch, pos = proxsimb(pos)
        return (ch, pos)
    else:
        print("Erro sintatico, esperado real ou integer e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit()   

def variaveis(ch, pos):
    if isIdent(ch):
        ch, pos = proxsimb(pos)
        ch, pos = mais_var(ch, pos)
        return (ch, pos)
    else:
        print("Erro sintatico, esperado identificador e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit()

def mais_var(ch, pos):
    if ch == ",":
        ch, pos = proxsimb(pos)
        ch, pos = variaveis(ch, pos)
        return (ch, pos)
    elif ch == ":" or ch == ")":
        return (ch, pos)
    else:
        print("Erro sintatico, esperado , ou : ou ) e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit()

def dc_p(ch, pos):
    if ch == "procedure":
        ch, pos = proxsimb(pos)
        if isIdent(ch):
            ch, pos = proxsimb(pos)
            ch, pos = parametros(ch, pos)
            ch, pos = corpo_p(ch, pos)
            return (ch, pos)
        else:
            print("Erro sintatico, esperado identificador e encontrado %s na linha %d" %(ch, linha(pos+1)))
            exit() 
    else:
        print("Erro sintatico, esperado procedure e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 
    
def parametros(ch, pos):
    if ch == "(":
        ch, pos = proxsimb(pos)
        ch, pos = lista_par(ch, pos)
        if ch == ")":
            ch, pos = proxsimb(pos)
            return (ch, pos)
        else:
            print("Erro sintatico, esperado ) e encontrado %s na linha %d" %(ch, linha(pos+1)))
            exit() 
    elif ch == "var" or ch == "begin":
        return (ch, pos)
    else:
        print("Erro sintatico, esperado ( ou var ou begin e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit()

def lista_par(ch, pos):
    ch, pos = variaveis(ch, pos)
    if ch == ":":
        ch, pos = proxsimb(pos)
        ch, pos = tipo_var(ch, pos)
        ch, pos = mais_par(ch, pos)
        return (ch, pos)
    else:
        print("Erro sintatico, esperado : e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def mais_par(ch, pos):
    if ch == ";":
        ch, pos = proxsimb(pos)
        ch, pos = lista_par(ch, pos)
        return (ch, pos)
    elif ch == ")":
        return (ch, pos)
    else:
        print("Erro sintatico, esperado ; ou ) e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def corpo_p(ch, pos):
    ch, pos = dc_loc(ch, pos)
    if ch == "begin":
        ch, pos = proxsimb(pos)
        ch, pos = comandos(ch, pos)
        if ch == "end":
            ch, pos = proxsimb(pos)
            return (ch, pos)
        else:
            print("Erro sintatico, esperado end e encontrado %s na linha %d" %(ch, linha(pos+1)))
            exit() 
    else:
        print("Erro sintatico, esperado begin e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def dc_loc(ch, pos):
    if ch == "var":
        ch, pos = dc_v(ch, pos)
        ch, pos = mais_dcloc(ch, pos)
        return (ch, pos)
    elif ch == "begin":
        return (ch, pos)
    else:
        print("Erro sintatico, esperado var ou begin e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def mais_dcloc(ch, pos):
    if ch == ";":
        ch, pos = proxsimb(pos)
        ch, pos = dc_loc(ch, pos)
        return (ch, pos)
    elif ch == "begin":
        return (ch, pos)
    else:
        print("Erro sintatico, esperado ; ou begin e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def lista_arg(ch, pos):
    if ch == "(":
        ch, pos = proxsimb(pos)
        ch, pos = argumentos(ch, pos)
        if ch == ")":
            ch, pos = proxsimb(pos)
            return (ch, pos)
        else:
            print("Erro sintatico, esperado ) e encontrado %s na linha %d" %(ch, linha(pos+1)))
            exit() 
    elif ch == "end" or ch == ";" or ch == "else" or ch == "$":
        return (ch, pos)
    else:
        print("Erro sintatico, esperado ( ou end ou ; ou else ou $) e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def argumentos(ch, pos):
    if isIdent(ch):
        ch, pos = proxsimb(pos)
        ch, pos = mais_ident(ch, pos)
        return (ch, pos)
    else:
        print("Erro sintatico, esperado identificador e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def mais_ident(ch, pos):
    if ch == ";":
        ch, pos = proxsimb(pos)
        ch, pos = argumentos(ch, pos)
        return (ch, pos)
    elif ch == ")":
        return (ch, pos)
    else:
        print("Erro sintatico, esperado ; ou ) e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def pfalsa(ch, pos):
    if ch == "else":
        ch, pos = proxsimb(pos)
        ch, pos = comandos(ch, pos)
        return (ch, pos)
    elif ch == "$":
        return (ch, pos)
    else:
        print("Erro sintatico, esperado else ou $ e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def comandos(ch, pos):
    ch, pos = comando(ch, pos)
    ch, pos = mais_comandos(ch, pos)
    return (ch, pos)

def mais_comandos(ch, pos):
    if ch == ";":
        ch, pos = proxsimb(pos)
        ch, pos = comandos(ch, pos)
        return (ch, pos)
    elif ch == "end" or ch == "else" or ch == "$":
        return (ch, pos)
    else:
        print("Erro sintatico, esperado ; ou end ou else ou $ e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def comando(ch, pos):
    if ch == "read":
        ch, pos = proxsimb(pos)
        if ch == "(":
            ch, pos = proxsimb(pos)
            ch, pos = variaveis(ch, pos)
            if ch == ")":
                ch, pos = proxsimb(pos)
                return (ch, pos)
            else:
                print("Erro sintatico, esperado ) e encontrado %s na linha %d" %(ch, linha(pos+1)))
                exit() 
        else:
            print("Erro sintatico, esperado ) e encontrado %s na linha %d" %(ch, linha(pos+1)))
            exit() 
    elif ch == "write":
        ch, pos = proxsimb(pos)
        if ch == "(":
            ch, pos = proxsimb(pos)
            ch, pos = variaveis(ch, pos)
            if ch == ")":
                ch, pos = proxsimb(pos)
                return (ch, pos)
            else:
                print("Erro sintatico, esperado ) e encontrado %s na linha %d" %(ch, linha(pos+1)))
                exit() 
        else:
            print("Erro sintatico, esperado ) e encontrado %s na linha %d" %(ch, linha(pos+1)))
            exit() 
    elif ch == "while":
        ch, pos = proxsimb(pos)
        ch, pos = condicao(ch, pos)
        if ch == "do":
            ch, pos = proxsimb(pos)
            ch, pos = comandos(ch, pos)
            if ch == "$":
                ch, pos = proxsimb(pos)
                return (ch, pos)
            else:
                print("Erro sintatico, esperado $ e encontrado %s na linha %d" %(ch, linha(pos+1)))
                exit() 
        else:
            print("Erro sintatico, esperado do e encontrado %s na linha %d" %(ch, linha(pos+1)))
            exit() 
    elif ch == "if":
        ch, pos = proxsimb(pos)
        ch, pos = condicao(ch, pos)
        if ch == "then":
            ch, pos = proxsimb(pos)
            ch, pos = comandos(ch, pos)
            ch, pos = pfalsa(ch, pos)
            if ch == "$":
                ch, pos = proxsimb(pos)
                return (ch, pos)
            else:
                print("Erro sintatico, esperado $ e encontrado %s na linha %d" %(ch, linha(pos+1)))
                exit() 
        else:
            print("Erro sintatico, esperado then e encontrado %s na linha %d" %(ch, linha(pos+1)))
            exit() 
    elif isIdent(ch):
        ch, pos = proxsimb(pos)
        ch, pos = restoIdent(ch, pos)
        return (ch, pos)
    else:
        print("Erro sintatico, esperado read ou write ou while o if ou identificador e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def restoIdent(ch, pos):
    if ch == ":=":
        ch, pos = proxsimb(pos)
        ch, pos = expressao(ch, pos)
        return (ch, pos)
    elif ch == "(" or ch == "end" or ch == ";" or ch == "else" or ch == "$":
        ch, pos = lista_arg(ch, pos)
        return (ch, pos)
    else:
        print("Erro sintatico, esperado := ou ( end ou ; ou else ou $ e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def condicao(ch, pos):
    ch, pos = expressao(ch, pos)
    ch, pos = relacao(ch, pos)
    ch, pos = expressao(ch, pos)
    return (ch, pos)

def relacao(ch, pos):
    if ch == "=" or ch == "<>" or ch == ">=" or ch == "<=" or ch == ">" or ch == "<":
        ch, pos = proxsimb(pos)
        return (ch, pos)
    else:
        print("Erro sintatico, esperado = ou <> ou >= ou <= ou > ou < e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def expressao(ch, pos):
    ch, pos = termo(ch, pos)
    ch, pos = outros_termos(ch, pos)
    return (ch, pos)

def op_un(ch, pos):
    if ch == "+" or ch == "-":
        ch, pos = proxsimb(pos)
        return (ch, pos)
    elif isIdent(ch) or ch == "(" or isInt(ch) or isReal(ch):
        return (ch, pos)
    else:
        print("Erro sintatico, esperado + ou - ou ( ou identificador ou numero_inteiro ou numero_real e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def outros_termos(ch, pos):
    if isIdent(ch) or ch == "(" or ch == "+" or ch == "-" or isInt(ch) or isReal(ch):
        ch, pos = op_ad(ch, pos)
        ch, pos = termo(ch, pos)
        ch, pos = outros_termos(ch, pos)
        return (ch, pos)
    elif ch == "end" or ch == ";" or ch == ch == ")" or ch == "else" or ch == "do" or ch == "$" or ch == "then" or ch == "=" or ch == "<>" or ch == ">=" or ch == "<=" or ch == ">" or ch == "<":
        return (ch, pos)
    else:
        print("Erro sintatico, esperado identificador ou ( ou + ou - ou numero_inteiro ou numero_real ou end ou ; ou ) ou else ou do ou $ ou then ou = ou <> ou >= ou <= ou > ou < e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def op_ad(ch, pos):
    if ch == "+" or ch == "-":
        ch, pos = proxsimb(pos)
        return (ch, pos)
    else:
        print("Erro sintatico, esperado + ou - e encontrado %s na linha %d" %(ch, linha(pos+1)))
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
        print("Erro sintatico, esperado * ou / ou end ou ; ou ) ou else ou do ou $ ou then ou = ou <> ou >= ou <= ou > ou < ou + ou - e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def op_mul(ch, pos):
    if ch == "*" or ch == "/":
        ch, pos = proxsimb(pos)
        return (ch, pos)
    else:
        print("Erro sintatico, esperado * ou / e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def fator(ch, pos):
    if isIdent(ch) or isInt(ch) or isReal(ch):
        ch, pos = proxsimb(pos)
        return (ch, pos)
    elif ch == "(":
        ch, pos = proxsimb(pos)
        ch, pos = expressao(ch, pos)
        if ch == ")":
            ch, pos = proxsimb(pos)
            return (ch, pos)
        else:
            print("Erro sintatico, esperado ) e encontrado %s na linha %d" %(ch, linha(pos+1)))
            exit() 
    else:
        print("Erro sintatico, esperado identificador ou numero_real ou numero_inteiro ou ( e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def proxsimb(pos):
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

def linha(pos):
    for i in range(len(linhas)):
        if (pos >= int(linhas[i])) and (pos < int(linhas[i+1])):
            return i+1

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
