C = [] #Lista da área de código
i = 0 #Posição da lista da área de código
D = [] #Pilha da área de dados
s = -1 #Posição da pila da área de dados
nLinha = -1
comando = ""
valor = ""
enderecoVariaveis = []

#Funções Cod Hipotetico
#carrega constante k no topo da pilha D
def CRCT(k):
    global D, s
    s += 1
    D.append(0)
    D[s] = k

#carrega valor de endereço n no topo da pilha D
def CRVL(n):
    global D, s, enderecoVariaveis
    s = s+1
    D.append(D[enderecoVariaveis[n]])

#soma o elemento antecessor com o topo da pilha
def SOMA():
    global D, s
    D[s-1] = D[s-1] + D[s]
    s = s-1
    D.pop()

#subtrai o antecessor pelo elemento do topo
def SUBT():
    global D, s
    D[s-1] = D[s-1] - D[s]
    s = s-1
    D.pop()

#multiplica elemento antecessor pelo elemento do topo
def MULT():
    global D, s
    D[s-1] = D[s-1] * D[s]
    s = s-1
    D.pop()

#divide o elemento antecessor pelo elemento do topo
def DIVI():
    global D, s
    if D[s] == 0:
        print("Impossivel dividir por 0")
        exit()
    D[s-1] = D[s-1] / D[s]
    s = s-1
    D.pop()

#inverte sinal do topo
def INVE():
    global D, s
    D[s] = - D[s]

#comparação de menor entre o antecessor e o topo
def CPME():
    global D, s
    if D[s-1] < D[s]:
        D[s-1] = 1
    else:
        D[s-1] = 0
    s = s-1
    D.pop()

#comparação de maior
def CPMA():
    global D, s
    if D[s-1] > D[s]:
        D[s-1] = 1
    else:
        D[s-1] = 0
    s = s-1
    D.pop()

#comparação de igualdade
def CPIG():
    global D, s
    if D[s-1] == D[s]:
        D[s-1] = 1
    else:
        D[s-1] = 0
    s = s-1
    D.pop()

#comparação de desigualdade
def CDES():
    global D, s
    if D[s-1] != D[s]:
        D[s-1] = 1
    else:
        D[s-1] = 0
    s = s-1
    D.pop()

#comparação menor-igual
def CPMI():
    global D, s
    if D[s-1] <= D[s]:
        D[s-1] = 1
    else:
        D[s-1] = 0
    s = s-1
    D.pop()

#comparação maior-igual
def CMAI():
    global D, s
    if D[s-1] >= D[s]:
        D[s-1] = 1
    else:
        D[s-1] = 0
    s = s-1
    D.pop()

#armazena o topo da pilha no endereço n de D
def ARMZ(n):
    global D, s, enderecoVariaveis
    D[enderecoVariaveis[n]] = D[s]
    s = s-1
    D.pop()

#desvio incondicional para a instrução de endereço p
def DSVI(p):
    global i
    i = p - 1

#desvio condicional para a instrução de endereço p; o desvio será
#executado caso a condição resultante seja falsa; o valor da
#condição estará no topo
def DSVF(p):
    global i, s, D
    if D[s] == 0:
        i = p - 1
    s = s-1
    D.pop()

#lê um dado de entrada para o topo da pilha
def LEIT():
    global s, D
    s = s+1
    D.append(input("Digite o valor da entrada: "))
    if isInt(D[s]):
        D[s] = int(D[s])
    else:
        D[s] = float(D[s])

#imprime valor o valor do topo da pilha na saída
def IMPR():
    global s, D
    print(D[s])
    s = s-1
    D.pop()

#reserva m posições na pilha D; m depende do tipo da variável
def ALME(m):
    global s, D, enderecoVariaveis
    s = s + m
    D.append(0)
    enderecoVariaveis.append(s)

#inicia programa – será sempre a 1ª instrução
def INPP():
    global s
    s = -1

#termina a execução do programa
def PARA():
    exit()

#aloca memória e copia valor da posição n para o topo de D
def PARAM(n):
    global s, D, enderecoVariaveis
    s = s+1
    D.append(0)
    D[s] = D[enderecoVariaveis[n]]
    enderecoVariaveis.append(s)#TODO

#empilha o índice e da instrução seguinte à chamada do
#procedimento, como endereço de retorno, no array C
def PUSHER(e):
    global s, D
    s = s + 1
    D.append(0)
    D[s] = e

#desvia para instrução de índice p no array C, obtido na TS
def CHPR(p):
    global i
    i = p - 1

#desaloca m posições de memória, a partir do topo s de D
def DESM(m):
    global s, D, enderecoVariaveis
    s = s - m
    for j in range(m):
        D.pop()
        enderecoVariaveis.pop()

#retorna do procedimento – endereço de retorno estará no topo
#de D – e desempilha o endereço
def RTPR():
    global i, s, D
    i = D[s]
    i = i - 1
    s = s-1
    D.pop()

#verifica se é identificador
def isIdent(ch):
    if (ch[0] >= "a" and ch[0] <= "z") or (ch[0] >= "A" and ch[0] <= "Z"):
        return True
    else:
        return False

#verifica se é inteiro
def isInt(ch):
    try: 
        int(ch)
        return True
    except ValueError:
        return False

#verifica se é real
def isReal(ch):
    try: 
        float(ch)
        return True
    except ValueError:
        return False

#Trata arquivo de entrada para variavel C
arquivo = open("codigo.txt", "r")
arquivo = arquivo.readlines()
for j in range(len(arquivo)):
    instrucao = arquivo[j].replace("\n","")
    instrucao = instrucao.split(" ")
    C.append(instrucao)

#for i in range(len(C)):
while i < len(C):

    comando = C[i][0]
    if len(C[i]) != 1:
        comando = C[i][0]
        if (isInt(C[i][1])):
            valor = int(C[i][1])
        else:
            valor = float(C[i][1])

    if comando == "CRCT":
        CRCT(valor)
    elif comando == "CRVL":
        CRVL(valor)
    elif comando == "SOMA":
        SOMA()
    elif comando == "SUBT":
        SUBT()
    elif comando == "MULT":
        MULT()
    elif comando == "DIVI":
        DIVI()
    elif comando == "INVE":
        INVE()
    elif comando == "CPME":
        CPME()
    elif comando == "CPMA":
        CPMA()
    elif comando == "CPIG":
        CPIG()
    elif comando == "CDES":
        CDES()
    elif comando == "CPMI":
        CPMI()
    elif comando == "CMAI":
        CMAI()
    elif comando == "ARMZ":
        ARMZ(valor)
    elif comando == "DSVI":
        DSVI(valor)
    elif comando == "DSVF":
        DSVF(valor)
    elif comando == "LEIT":
        LEIT()
    elif comando == "IMPR":
        IMPR()
    elif comando == "ALME":
        ALME(valor)
    elif comando == "INPP":
        INPP()
    elif comando == "PARA":
        PARA()
    elif comando == "PARAM":
        PARAM(valor)
    elif comando == "PUSHER":
        PUSHER(valor)
    elif comando == "CHPR":
        CHPR(valor)
    elif comando == "DESM":
        DESM(valor)
    elif comando == "RTPR":
        RTPR()
    else:
        print("Erro, instrucao %s desconhecida." %(comando))
        exit()

    i += 1
