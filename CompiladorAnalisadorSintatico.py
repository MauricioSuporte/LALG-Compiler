from CompiladorLexico import *

rodarLexico()

arquivo = open("entradaSintatico.txt", "r")
tokens = arquivo.read()
tokens = tokens.split(" ")

arqLinhas = open("linhas.txt", "r")
linhas = arqLinhas.read()
linhas = linhas.split(" ")

#Tabela de Símbolos
cat = ""
posInicial = 0
posFinal = 0
tempAtual = 0
tabSimb = []
procedimentos = []
verificacoes = []
verificacoesReadWrite = []
vemDeComando = False
param = False
escopo = {'Cadeia': "", 'PosInicial': 0}
contadorNumParam = 0
tiposParam = []
procSendoAnalisado = ""

#Maquina Hipotética
desvio = ""
posDesvio = 0
posDSVI = 0
posDSVF = 0
posPUSHER = 0
listaVariaveis = []
areadeCodigo = []
operador = ""
readWrite = ""
DSVIProc = 0
DSVFProc = 0
contadorDESM = 0
isProcedimento = False
listaCodProcedimentos = []

def programa(ch, pos):
    global areadeCodigo
    if ch == "program":
        areadeCodigo.append("INPP")
        ch, pos = proxsimb(pos)
        if isIdent(ch):
            addTabSimbNomeProg(ch)
            ch, pos = proxsimb(pos)
            ch, pos = corpo(ch, pos)
            if ch == ".":
                areadeCodigo.append("PARA")
                imprimeTabSimb()
                print("\nCadeia sintaticamente correta.")
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
        global cat
        cat = "var"
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
        addTipo(ch)
        ch, pos = proxsimb(pos)
        return (ch, pos)
    else:
        print("Erro sintatico, esperado real ou integer e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit()   

def variaveis(ch, pos):
    if isIdent(ch):
        global cat, vemDeComando, areadeCodigo, readWrite, contadorDESM, isProcedimento
        if (vemDeComando) and (not existeVar(ch)):
            print("Identificador %s na linha %d nao declarado" %(ch, linha(pos+1)))
            exit()
        if vemDeComando:
            addVerificacaoReadWrite(ch)
            if readWrite == "write":
                areadeCodigo.append("CRVL %d" %(posVar(ch)))
                areadeCodigo.append("IMPR")
            elif readWrite == "read":
                areadeCodigo.append("LEIT")
                areadeCodigo.append("ARMZ %d" %(posVar(ch)))
            else:
                areadeCodigo.append("ARMZ %d" %(posVar(ch)))
        if not vemDeComando and cat != "param":
            areadeCodigo.append("ALME 1")
        if not vemDeComando and isProcedimento:
            contadorDESM += 1
        addTabSimbVar(ch, cat)
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
            global areadeCodigo, DSVIProc, isProcedimento, listaCodProcedimentos
            isProcedimento = True
            areadeCodigo.append("DSVI")
            DSVIProc = len(areadeCodigo)-1
            listaCodProcedimentos.append({'Cadeia': ch, 'LinhaInicioCod': DSVIProc+1})
            addTabSimbNomeProg(ch)
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
        global cat
        cat = "param"
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
            global areadeCodigo, DSVIProc, contadorDESM, isProcedimento
            areadeCodigo.append("DESM %d" %(contadorDESM))
            areadeCodigo.append("RTPR")
            areadeCodigo[DSVIProc] = "DSVI %d" %(len(areadeCodigo))
            contadorDESM = 0
            isProcedimento = False
            imprimeTabSimb()
            deletarEscopoAtual()
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
        global param, areadeCodigo, contadorNumPara
        if not existeVar(ch):
            print("Identificador %s na linha %d nao declarado" %(ch, linha(pos+1)))
            exit()
        if param:
            addListaVerificacaoParam(ch)
            areadeCodigo.append("PARAM %d" %(posVar(ch)))
        addListaVerificacao(ch)
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
        global areadeCodigo, posPUSHER, procSendoAnalisado, listaCodProcedimentos
        areadeCodigo.append("CHPR %d" %(inicioCod(procSendoAnalisado)))
        areadeCodigo[posPUSHER] = "PUSHER %d" %(len(areadeCodigo))
        verificaParam(pos+1)
        return (ch, pos)
    else:
        print("Erro sintatico, esperado ; ou ) e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def pfalsa(ch, pos):
    if ch == "else":
        global areadeCodigo, posDSVI, posDSVF
        areadeCodigo.append("DSVI")
        posDSVI = len(areadeCodigo)-1
        areadeCodigo[posDSVF] = ("DSVF %d" %(len(areadeCodigo)))
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
    global vemDeComando, verificacoesReadWrite, areadeCodigo, desvio, readWrite, posDesvio, posDSVF, posDSVI
    if ch == "read":
        readWrite = ch
        ch, pos = proxsimb(pos)
        if ch == "(":
            ch, pos = proxsimb(pos)
            vemDeComando = True
            ch, pos = variaveis(ch, pos)
            verificaTipoReadWrite(pos+1)
            vemDeComando = False
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
        readWrite = ch
        ch, pos = proxsimb(pos)
        if ch == "(":
            ch, pos = proxsimb(pos)
            vemDeComando = True
            ch, pos = variaveis(ch, pos)
            verificaTipoReadWrite(pos+1)
            vemDeComando = False
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
        desvio = ch
        posDesvio = len(areadeCodigo)
        ch, pos = proxsimb(pos)
        ch, pos = condicao(ch, pos)
        if ch == "do":
            areadeCodigo.append("DSVF ")
            posDSVF = len(areadeCodigo)-1
            ch, pos = proxsimb(pos)
            ch, pos = comandos(ch, pos)
            if ch == "$":
                areadeCodigo.append("DSVI %d" %(posDesvio))
                areadeCodigo[posDSVF] = "DSVF %d" %(len(areadeCodigo))
                desvio = ""
                ch, pos = proxsimb(pos)
                return (ch, pos)
            else:
                print("Erro sintatico, esperado $ e encontrado %s na linha %d" %(ch, linha(pos+1)))
                exit() 
        else:
            print("Erro sintatico, esperado do e encontrado %s na linha %d" %(ch, linha(pos+1)))
            exit() 
    elif ch == "if":
        desvio = ch
        posDesvio = len(areadeCodigo)
        ch, pos = proxsimb(pos)
        ch, pos = condicao(ch, pos)
        if ch == "then":
            areadeCodigo.append("DSVF ")
            posDSVF = len(areadeCodigo)-1
            ch, pos = proxsimb(pos)
            ch, pos = comandos(ch, pos)
            ch, pos = pfalsa(ch, pos)
            if ch == "$":
                areadeCodigo[posDSVI] = ("DSVI %d" %(len(areadeCodigo)))
                desvio = ""
                ch, pos = proxsimb(pos)
                return (ch, pos)
            else:
                print("Erro sintatico, esperado $ e encontrado %s na linha %d" %(ch, linha(pos+1)))
                exit() 
        else:
            print("Erro sintatico, esperado then e encontrado %s na linha %d" %(ch, linha(pos+1)))
            exit() 
    elif isIdent(ch):
        global param, procSendoAnalisado, posPUSHER
        if (not existeVar(ch)) and (not existeNomeProg(ch)):
            print("Identificador %s na linha %d nao declarado" %(ch, linha(pos+1)))
            exit()
        if (existeNomeProg(ch)) and (not existeVar(ch)):
            procSendoAnalisado = ch
            param = True
            areadeCodigo.append("PUSHER")
            posPUSHER = (len(areadeCodigo)-1)
        addListaVerificacao(ch)
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
        global operador
        operador = ch
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
        if ch == "-":
            global operador
            operador = "INVE"
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
        global verificacoes, areadeCodigo, listaVariaveis, operador
        if len(verificacoes) != 0:
            if not verificaTipo(verificacoes, pos+1):
                exit()
            verificacoes = []
            if (len(listaVariaveis) == 1) or ((len(listaVariaveis) > 1) and (not isOp(ch))):
                areadeCodigo.append("ARMZ %d" %(posVar(listaVariaveis[0])))
                listaVariaveis = []
        return (ch, pos)
    else:
        print("Erro sintatico, esperado identificador ou ( ou + ou - ou numero_inteiro ou numero_real ou end ou ; ou ) ou else ou do ou $ ou then ou = ou <> ou >= ou <= ou > ou < e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def op_ad(ch, pos):
    if ch == "+" or ch == "-":
        global operador
        operador = ch
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
        global verificacoes, areadeCodigo, listaVariaveis, operador, desvio
        if len(verificacoes) != 0:
            if not verificaTipo(verificacoes, pos+1):
                exit()
            verificacoes = []
            if (len(listaVariaveis) == 1) or ((len(listaVariaveis) > 1) and (not isOp(ch))):
                if desvio == "":
                    areadeCodigo.append("ARMZ %d" %(posVar(listaVariaveis[0])))
                listaVariaveis = []
            elif (len(listaVariaveis) > 1) and (isOp(ch)):
                operador = ch
        return (ch, pos)
    else:
        print("Erro sintatico, esperado * ou / ou end ou ; ou ) ou else ou do ou $ ou then ou = ou <> ou >= ou <= ou > ou < ou + ou - e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def op_mul(ch, pos):
    if ch == "*" or ch == "/":
        global operador
        operador = ch
        ch, pos = proxsimb(pos)
        return (ch, pos)
    else:
        print("Erro sintatico, esperado * ou / e encontrado %s na linha %d" %(ch, linha(pos+1)))
        exit() 

def fator(ch, pos):
    global areadeCodigo, operador, listaVariaveis
    if isIdent(ch) or isInt(ch) or isReal(ch):
        if (isIdent(ch)) and (not existeVar(ch)):
            print("Identificador %s na linha %d nao declarado" %(ch, linha(pos+1)))
            exit()
        if isInt(ch) or isReal(ch):
            areadeCodigo.append("CRCT " + ch)
            addTabSimbNum(ch)
        if isIdent(ch):
            areadeCodigo.append("CRVL %d" %(posVar(ch)))
        if operador != "":
            incluirOp()
        addListaVerificacao(ch)
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
        if i != len(linhas)-1:
            if (pos >= int(linhas[i])) and (pos < int(linhas[i+1])):
                return i+1
        else:
            return i+1

def addParametros(ch):
    global procedimentos
    auxiliar = []

    auxiliar.extend(procedimentos[len(procedimentos)-1])
    if len(auxiliar) == 1:
        auxiliar.append(1) #1º Parametro, então qnt param = 1
    else:
        auxiliar[1] = len(auxiliar) - 1 #Calcula a qnt de parametros do procedimento atual
    auxiliar.append(ch)
    procedimentos.pop()
    procedimentos.append(auxiliar)

    return

def addTabSimbNomeProg(ch):
    global posInicial, posFinal, tabSimb, escopo, procedimentos
    
    #Relação posições dadosProcedimento
    #[0] = Cadeia | [1] = Qnt de parametros | [2]..[n-1] = Tipo do Parâmetro
    dadosProcedimento = []

    if existeNomeProg(ch):
        print("Proc de cadeia %s ja existe na tabela de simbolos." %(ch))
        exit()

    dadosProcedimento.append(ch)
 
    conteudo = {'Cadeia': ch, 'Token': 'id', 'Categoria': 'proc', 'Tipo': '', 'Valor': ''}
    escopo = {'Cadeia': ch, 'PosInicial': posFinal}
    posFinal += 1
    posInicial = posFinal
    tabSimb.append(conteudo)
    procedimentos.append(dadosProcedimento)

def existeNomeProg(ch):
    global procedimentos

    for i in range(1, len(procedimentos)):
        if procedimentos[i][0] == ch:
            return True
    return False

def addTabSimbVar(ch, cat):
    global posFinal, tabSimb, vemDeComando, escopo

    if vemDeComando:
        return

    if existeVar(ch):
        print("Cadeia %s ja existe na tabela de simbolos do escopo %s." %(ch, escopo['Cadeia']))
        exit()

    posFinal = posFinal + 1
    conteudo = {'Cadeia': ch, 'Token': 'id', 'Categoria': cat, 'Tipo': 'null', 'Valor': ''}
    tabSimb.append(conteudo)

def existeVar(ch):
    global tabSimb, escopo

    for i in range(escopo['PosInicial'], len(tabSimb)):
        if tabSimb[i]['Cadeia'] == ch:
            return True
    return False

def posVar(ch):
    global tabSimb, escopo

    posicao = -2
    for i in range(escopo['PosInicial'], len(tabSimb)):
        posicao += 1
        if tabSimb[i]['Cadeia'] == ch:
            return posicao

def addTabSimbNum(ch):
    global posFinal, tabSimb

    if existeNum(ch):
        return

    tipo = ""
    if isInt(ch):
        tipo = "integer"
    else:
        tipo = "real"

    posFinal = posFinal + 1
    conteudo = {'Cadeia': ch, 'Token': 'num', 'Categoria': '', 'Tipo': tipo, 'Valor': ch}
    tabSimb.append(conteudo)

def existeNum(ch):
    global tabSimb, escopo

    for i in range(escopo['PosInicial'], len(tabSimb)):
        if i != escopo['PosInicial']:
            if tabSimb[i]['Cadeia'] == ch:
                return True
    return False

def addTipo(tipo):
    global posInicial, posFinal, tabSimb
    for i in range(posInicial, posFinal):
        tabSimb[i]['Tipo'] = tipo
        if tabSimb[i]['Categoria'] == "param":
            addParametros(tipo)

    posInicial = posFinal
    
def addListaVerificacaoParam(ch):
    global tabSimb, contadorNumParam, tiposParam

    contadorNumParam += 1

    for i in range(1, len(tabSimb)):
        if tabSimb[i]['Cadeia'] == ch:
            tiposParam.append(tabSimb[i]['Tipo'])

def verificaParam(pos):
    global procedimentos, contadorNumParam, param, procSendoAnalisado, tiposParam

    for i in range(len(procedimentos)):
        if procedimentos[i][0] == procSendoAnalisado: 
            if procedimentos[i][1] != contadorNumParam: #Verifica qnt de parametros
                print("Esperado %d parametros na chamada de procedimento %s, nao %d como foi chamado na linha %d." %(procedimentos[i][1], procSendoAnalisado, contadorNumParam, linha(pos)))
                exit()
            copiaProcedimento = []
            copiaProcedimento.extend(procedimentos[i])
            for j in range(2, len(copiaProcedimento)):
                if copiaProcedimento[j] != tiposParam[j-2]: #Verifica tipos e ordem de parametros
                    print("Esperado parametros de tipo(os) %s no procedimento %s, mas foi chamado tipo(os) %s na linha %d." %(copiaProcedimento[2:], procSendoAnalisado, tiposParam, linha(pos)))
                    exit()
   
    #zera variaveis de verificacoes dos parametros
    param = False
    contadorNumParam = 0
    procSendoAnalisado = ""
    tiposParam = []

def addListaVerificacao(ch):
    global verificacoes, tabSimb, escopo, listaVariaveis

    listaVariaveis.append(ch)
    if isIdent(ch):
        for i in range(escopo['PosInicial']+1, len(tabSimb)):
            if tabSimb[i]['Cadeia'] == ch:
                verificacoes.append(tabSimb[i]['Tipo'])
                break
    elif isInt(ch):
        verificacoes.append('integer')
    else:
        verificacoes.append('real')

def verificaTipo(verificacoes, pos):
    tipo = verificacoes[0]
    for i in verificacoes:
        if i != tipo:
            print("Impossivel operar real com inteiro na linha " + str(linha(pos)))
            return False
    return True

def addVerificacaoReadWrite(ch):
    global verificacoesReadWrite, tabSimb, escopo

    if isIdent(ch):
        for i in range(escopo['PosInicial']+1, len(tabSimb)):
            if tabSimb[i]['Cadeia'] == ch:
                verificacoesReadWrite.append(tabSimb[i]['Tipo'])
                break
    elif isInt(ch):
        verificacoesReadWrite.append('integer')
    else:
        verificacoesReadWrite.append('real')

def verificaTipoReadWrite(pos):
    global verificacoesReadWrite
    tipo = verificacoesReadWrite[0]
    for i in verificacoesReadWrite:
        if i != tipo:
            print("Impossivel realizar comando read ou write com variaveis de tipos diferentes na linha " + str(linha(pos)))
            exit()
    verificacoesReadWrite = []
    return True

def deletarEscopoAtual():
    global escopo, posInicial, posFinal, tabSimb

    for i in range(escopo['PosInicial'], len(tabSimb)):
        tabSimb.pop()
    posInicial = escopo['PosInicial']
    posFinal = posInicial
    escopo = {'Cadeia': tabSimb[0]['Cadeia'], 'PosInicial': 0}

def imprimeTabSimb():
    global escopo, tabSimb
    print("\n=-=-=-=-=-=-=-=-=-=-=-=-TABELA DE SIMBOLOS %s=-=-=-=-=-=-=-=-=-=-=-=-" %(escopo['Cadeia']))
    for i in range(escopo['PosInicial'], len(tabSimb)):
        print(tabSimb[i])

def incluirOp():
    global operador, areadeCodigo, listaVariaveis

    if operador == "+":
        areadeCodigo.append("SOMA")
    elif operador == "-":
        areadeCodigo.append("SUBT")
    elif operador == "*":
        areadeCodigo.append("MULT")
    elif operador == "/":
        areadeCodigo.append("DIVI")
    elif operador == "<":
        areadeCodigo.append("CPME")
    elif operador == ">":
        areadeCodigo.append("CPMA")
    elif operador == "=":
        areadeCodigo.append("CPIG")
    elif operador == "<>":
        areadeCodigo.append("CDES")
    elif operador == "<=":
        areadeCodigo.append("CPMI")
    elif operador == ">=":
        areadeCodigo.append("CMAI")
    elif operador == "INVE":
        areadeCodigo.append("INVE")

    operador = ""

def isOp(ch):
    if ch == "*" or ch == "/" or ch == "+" or ch == "-" or ch == "<>" or ch == ">=" or ch == "<=" or ch == ">" or ch == "<" or ch == "=":
        return True
    else:
        return False

def inicioCod(ch):
    global listaCodProcedimentos

    for i in range(len(listaCodProcedimentos)):
        if listaCodProcedimentos[i]['Cadeia'] == ch:
            return listaCodProcedimentos[i]['LinhaInicioCod']

#Main
programa(tokens[0], 0)
arquivo.close()
for i in range(len(areadeCodigo)):
    print("%d: %s" %(i, areadeCodigo[i]))

arqCod = open("codigo.txt", "w")
for i in range(len(areadeCodigo)):
    arqCod.write(areadeCodigo[i] + "\n")
arqCod.close()
