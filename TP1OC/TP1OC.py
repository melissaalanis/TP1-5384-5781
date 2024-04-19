import sys

''' EXTRAS IMPLEMENTADOS
- Instruções addi, sub e xori

- Pseudo Instruções:
Pseudo-Instrucao : Instrucao do riscv : Funcionalidade
[nop]            : [addi x0, x0, 0]   : Nao realiza operacao
[mv rd, rs]      : [addi rd, rs, 0]   : Copia oq esta em rs para rd
[not rd, rs]     : [xori rd, rs, -1]  : Inverte os bits do numero
[neg: rd, rs]    : [sub rd, x0, rs]   : Complemento de 2 do rs

- Saida em binario ou hexa

'''

def Complemento_Dois(valor_decimal):
    if valor_decimal < 0:
        valor_binario = format(valor_decimal*(-1), '012b') # Convertendo para binário, multiplica o valor decimal por -1 pq tem 
        #que pegar o numero positivo para as transformações

        numero_invertido = "".join('1' if bit == '0' else '0' for bit in valor_binario) #O join vai concatenar os valores, e a 
        #parte interna do join tranforma inverte os bsits

        valor_complemento_dois = bin(int(numero_invertido, 2) + 1)[2:] #Como python não permite somar em binário, eu tranformo 
        #meu valor em decimal, somo 1 transformo em binario

        return str(valor_complemento_dois) #Retorno meu valor como string para facilitar a concatenação
    else:
        valor_binario = format(valor_decimal, '012b') # Convertendo para binário
        return str(valor_binario)

def Binario(valor_decimal):
    valor_binario = format(valor_decimal, '05b') # Convertendo para binário
    return str(valor_binario)


funct3 = {"andi": "111", "xori":"100", "or": "110", "iguais": "001", "addi": "000","add": "000","sub":"000" } #iguais: sh, bne, lh e sll
#apesar de termos addi, add e sub com a mesma funct3, optamos por deixar o nome da instrucaSo, para nao ter confilto com o grupo nomeado iguais

opcode = {"sh": "0100011", "bne": "1100011", "lh": "0000011", "iguaisR":"0110011", "iguaisI": "0010011"} #iguaisR: add, or, sub e sll __ iguaisI: xori, addi, andi

funct7 = {"iguais":"0000000", "sub":"0100000"} #usada para add, or e sll, além da função extra sub


def FormatoR(instrucao,rd, rs1, rs2): # Formato R: funct7, rs2, rs1, funct3, rd, opcode
    rd = Binario(int(rd))
    rs1 = Binario(int(rs1))
    rs2 = Binario(int(rs2))

    if(instrucao == "sll"):
        funct3r = funct3["iguais"]
    else:
        funct3r = funct3[instrucao]
    
    if(instrucao == "add" or instrucao == "or" or instrucao == "sll"):
        funct7r = funct7["iguais"]
    else:
        funct7r = funct7["sub"]
        
    resultadoR = funct7r + rs2 + rs1 + funct3r + rd + opcode["iguaisR"]
    return resultadoR

def FormatoS(instrucao, rs2, rs1, imm): #FormatoS: imm[11:5], rs2, rs1, funct3, imm[4:0], opcode
    #tivemos que mudar a indices do imm, pq em binario vai de 11-0 e o vetor vai de 0-11
    imm = Complemento_Dois(int(imm))
    rs1 = Binario(int(rs1))
    rs2 = Binario(int(rs2)) 

    resultadoS = imm[:7] + rs2 + rs1 + funct3["iguais"] + imm[7:] + opcode[instrucao]
    return resultadoS

def FormatoI(instrucao,rd, rs1,imm): # Formato I: imm, rs1, funct3, rd, opcode

    imm = Complemento_Dois(int(imm))
    rs1 = Binario(int(rs1))
    rd = Binario(int(rd))


    if(instrucao == "lh"):
        funct3r = funct3["iguais"]
        opcoder = opcode[instrucao] 
    else:
        funct3r = funct3[instrucao]
        opcoder = opcode["iguaisI"] 


    resultadoI = imm + rs1 + funct3r+ rd + opcoder
    return resultadoI

# Saidas
# Nome do arquivo de entrada
nome_arquivo = sys.argv[1]

base = 2 #se meu usuario nao informar a base, ela sera 2

# Se o usuário fornecer um arquivo de saída, abra o arquivo para escrita
if len(sys.argv) > 3 and sys.argv[2] == "-o": #para reconhecer um arquivo de saida precisa do -o, e len(sys.argv) > 3 indica que pessoa informou um arquivo de saida ou base para printar no terminal
    nome_arquivo_saida = sys.argv[3]

    if(len(sys.argv) == 5):#A pessoa digita arquivo.py entrada.asm -o saida base
        base = int(sys.argv[4])

    saida = open(nome_arquivo_saida+".asm", "w") #"w" significa que cria um arquivo com o nome fornecido ou, caso já exista um com esse nome, subreescreve o conteudo

elif(len(sys.argv) == 3): #A pessoa digita arquivo.py entrada.asm base
    base = int(sys.argv[2])


with open(nome_arquivo, "r") as arq: # Leitura do arquivo
    
    for linha in arq:
        palavras = linha.replace(',',' ') # Retirando as Vírgulas
        palavras = palavras.replace('(',' ') # Retirando os colchetes
        palavras = palavras.replace(')',' ') # Retirando as colchetes
        palavras = palavras.replace('x', ' ') # Retirando o X
        palavras = palavras.split() # Separando os elementos
        if(palavras[0] == "ori"):
            palavras[0] = "x"+palavras[0]

        # Comparando a primeira string de cada linha p/ identificar o tipo
        if(palavras[0] == "add" or palavras[0] == "sll" or palavras[0] == "or" or palavras[0]== "sub"):  
            resultado = FormatoR(palavras[0], palavras[1], palavras[2], palavras[3]) #instrucao rd rs1 rs2
        
        elif(palavras[0]=="andi" or palavras[0]=="addi" or palavras[0]=="xori"):
            resultado = FormatoI(palavras[0], palavras[1], palavras[2], palavras[3]) #instrucao rd rs1 imm

        elif(palavras[0]=="lh"):
            resultado = FormatoI(palavras[0], palavras[1], palavras[3], palavras[2]) #instrucao rd imm(rs1)

        elif(palavras[0]== "sh"):
            resultado = FormatoS(palavras[0], palavras[1], palavras[3], palavras[2]) #instrucao rs1 imm(rs2)

        elif(palavras[0]=="bne"):
            resultado = FormatoS(palavras[0], palavras[1], palavras[2], palavras[3]) #instrucao rs1 rs2 imm


        #pseudo instrucoes:
        elif(palavras[0]=="nop"): #nop
            resultado = FormatoI("addi", "0", "0", "0") #addi x0, x0, 0
        elif(palavras[0]=="mv"): #mv rd, rs
            resultado = FormatoI("addi", palavras[1], palavras[2], "0") #addi rd, rs, 0
        elif(palavras[0]=="not"): #not rd, rs
            resultado = FormatoI("xori", palavras[1], palavras[2], "-1") #xori rd, rs, -1
        elif(palavras[0] == "neg"): #neg: rd, rs
            resultado = FormatoR("sub", palavras[1], "0", palavras[2]) #sub rd, x0, rs
        
        if(base == 16):
            resultado = format(int(resultado, 2), '08x')
        if len(sys.argv) > 3:
            saida.write(resultado + '\n') 
        else:
            print(resultado)


# Se um arquivo de saída foi fornecido, ele será fechado
if len(sys.argv) > 3:
    saida.close()