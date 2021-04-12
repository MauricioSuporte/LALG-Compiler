arquivo = open("codigo.txt", "r")
pilhadeDados = []
nLinha = -1
comando = ""
valor = ""

#Funções Cod Hipotetico
#carrega constante k no topo da pilha D
def CRCT(k):
    return

#carrega valor de endereço n no topo da pilha D
def CRVL(n):
    return

#soma o elemento antecessor com o topo da pilha
def SOMA():
    return

#subtrai o antecessor pelo elemento do topo
def SUBT():
    return

#multiplica elemento antecessor pelo elemento do topo
def MULT():
    return

#divide o elemento antecessor pelo elemento do topo
def DIVI():
    return

#inverte sinal do topo
def INVE():
    return

#conjunção de valores lógicos. F=0; V=1
def CONJ():
    return

#disjunção de valores lógicos
def DISJ():
    return

#negação lógica
def NEGA():
    return

#comparação de menor entre o antecessor e o topo
def CPME():
    return

#comparação de maior
def CPMA():
    return

#comparação de igualdade
def CPIG():
    return

#comparação de desigualdade
def CDES():
    return

#comparação menor-igual
def CPMI():
    return

#comparação maior-igual
def CMAI():
    return

#armazena o topo da pilha no endereço n de D
def ARMZ(n):
    return

#desvio incondicional para a instrução de endereço p
def DSVI(p):
    return

#desvio condicional para a instrução de endereço p; o desvio será
#executado caso a condição resultante seja falsa; o valor da
#condição estará no topo
def DSVF(p):
    return

#lê um dado de entrada para o topo da pilha
def LEIT():
    return

#imprime valor o valor do topo da pilha na saída
def IMPR():
    return

#reserva m posições na pilha D; m depende do tipo da variável
def ALME(m):
    return

#inicia programa – será sempre a 1ª instrução
def INPP():
    return

#termina a execução do programa
def PARA():
    return

#aloca memória e copia valor da posição n para o topo de D
def PARAM(n):
    return

#empilha o índice e da instrução seguinte à chamada do
#procedimento, como endereço de retorno, no array C
def PUSHER(e):
    return

#desvia para instrução de índice p no array C, obtido na TS
def CHPR(p):
    return

#desaloca m posições de memória, a partir do topo s de D
def DESM(m):
    return

#retorna do procedimento – endereço de retorno estará no topo
#de D – e desempilha o endereço
def RTPR():
    return

for instrucao in arquivo:
    nLinha += 1
    instrucao = instrucao.replace("\n","")
    instrucao = instrucao.split(" ")

    if len(instrucao) == 1:
        comando = instrucao[0]
        print(nLinha, comando)
    else:
        comando = instrucao[0]
        valor = instrucao[1]
        print(nLinha, comando, valor)

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
    elif comando == "CONJ":
        CONJ()
    elif comando == "DISJ":
        DISJ()
    elif comando == "NEGA":
        NEGA()
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
