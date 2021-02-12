arquivo = open("entrada.txt", "r")
numLinha = 0
tokens = []
for linha in arquivo:
    numLinha = numLinha + 1
    linha = linha.rstrip()
    i = 0
    tam = len(linha)
    while i < tam:
        if ((linha[i] >= "a" and linha[i] <= "z") or (linha[i] >= "A" and linha[i] <= "Z")):
            j = i + 1
            temp = linha[i]
            while (j < tam):
                if ((linha[j] >= "a" and linha[j] <= "z") or (linha[j] >= "A" and linha[j] <= "Z")):
                    temp = temp + linha[j]
                    j = j + 1
                else:
                    break
            tokens.append(" " + temp)
            i = j
        elif (linha[i] >= "0" and linha[i] <= "9"):
            j = i + 1
            temp = linha[i]
            flutuante = False
            while (j < tam):
                if (linha[j] >= "0" and linha[j] <= "9"):
                    temp = temp + linha[j]
                    j = j + 1
                elif (linha[j] == "." and flutuante == False):
                    temp = temp + linha[j]
                    j = j + 1
                    flutuante = True
                else:
                    break
            tokens.append(" " + temp)
            i = j
        elif linha[i] == ":" and linha[i+1] == "=":
            tokens.append(" :=")
            i = i + 2
        elif linha[i] == "<" and linha[i+1] == ">":
            tokens.append(" <>")
            i = i + 2
        elif linha[i] == ">" and linha[i+1] == "=":
            tokens.append(" >=")
            i = i + 2
        elif linha[i] == "<" and linha[i+1] == "=":
            tokens.append(" <=")
            i = i + 2
        elif linha[i] == "/" and linha[i+1] == "*":
            tokens.append(" /*")
            i = i + 2
        elif linha[i] == "*" and linha[i+1] == "/":
            tokens.append(" */")
            i = i + 2
        elif linha[i] == "v" and linha[i+1] == "a" and linha[i+2] == "r":
            tokens.append(" var")
            i = i + 3
        elif linha[i] == "i" and linha[i+1] == "n" and linha[i+2] == "t" and linha[i+3] == "e" \
                and linha[i+4] == "g" and linha[i+5] == "e" and linha[i+6] == "r":
            tokens.append(" integer")
            i = i + 7
        elif linha[i] == "r" and linha[i+1] == "e" and linha[i+2] == "a" and linha[i+3] == "l":
            tokens.append(" real")
            i = i + 4
        elif linha[i] == "," or linha[i] == ";" or linha[i] == "+" or linha[i] == ":" or linha[i] == "(" or linha[i] == ")" or linha[i] == "*" or linha[i] == "/" or linha[i] == "-" or linha[i] == ">" or linha[i] == "<" or linha[i] == "$" or linha[i] == "{" or linha[i] == "}" or linha[i] == ".":
            tokens.append(" " + linha[i])
            i = i + 1
        elif linha[i] == "i" and linha[i+1] == "f":
            tokens.append(" if")
            i = i + 2
        elif linha[i] == "t" and linha[i+1] == "h" and linha[i+2] == "e" and linha[i+3] == "n":
            tokens.append(" then")
            i = i + 4
        elif linha[i] == "w" and linha[i+1] == "h" and linha[i+2] == "i" and linha[i+3] == "l" and linha[i+4] == "e":
            tokens.append(" while")
            i = i + 5
        elif linha[i] == "d" and linha[i+1] == "o":
            tokens.append(" do")
            i = i + 2
        elif linha[i] == "w" and linha[i+1] == "r" and linha[i+2] == "i" and linha[i+3] == "t" and linha[i+4] == "e":
            tokens.append(" write")
            i = i + 5
        elif linha[i] == "r" and linha[i+1] == "e" and linha[i+2] == "a" and linha[i+3] == "d":
            tokens.append(" read")
            i = i + 4
        elif linha[i] == "e" and linha[i+1] == "l" and linha[i+2] == "s" and linha[i+3] == "e":
            tokens.append(" else")
            i = i + 4
        elif linha[i] == "b" and linha[i+1] == "e" and linha[i+2] == "g" and linha[i+3] == "i" and linha[i+4] == "n":
            tokens.append(" begin")
            i = i + 5
        elif linha[i] == "e" and linha[i+1] == "n" and linha[i+2] == "d":
            tokens.append(" end")
            i = i + 4
        elif linha[i] == " ":
            i = i + 1
            continue
        else:
            print("Erro lexico, caracter " + linha[i] + " nao conhecido na linha " + str(numLinha))
            exit()
tokens[0] = tokens[0].replace(" ", "")
print(tokens)
arqSintatico = open("entradaSintatico.txt", "w")
arqSintatico.writelines(tokens)
arqSintatico.close()
arquivo.close()
