# Criação dos nós
class NodeTree(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s_%s' % (self.left, self.right)

# Função para criação da árvore de Huffman
def huffmanTree(fileName):
    f = open(fileName, 'rb')    #Abre o arquivo byte a byte
    byte = f.read(1)

    contBytes = [0] * 256       #Cada posição corresponde a um simbolo de 8 bits que será contado
    contTotal = 0

    #Conta a aparição de cada byte do arquivo
    while byte:
        contBytes[int.from_bytes(byte, 'big')] += 1
        contTotal += 1
        byte = f.read(1)
    f.close()

    #É feito um mapeamento de cada simbolo presente com a frequência e ordenado
    contBytesMapped = []
    for i in range(256):
        if contBytes[i] > 0:
            contBytesMapped.append((str(i), contBytes[i]))

    def takeSecond(elem):
        return elem[1]
    contBytesMapped.sort(reverse=True, key=takeSecond)

    nodes = contBytesMapped

    # print(nodes)
    while len(nodes) > 1:
        (key1, c1) = nodes[-1]          #Último elemento (Que tem a menor probabilidade)
        (key2, c2) = nodes[-2]          #Penúltimo elemento
        nodes = nodes[:-2]              #Retira eles da lista
        node = NodeTree(key1, key2)     #Cria um nó que coloca o left e right do nó
        nodes.append((node, c1 + c2))   #Coloca na lista novamente esse novo nó

        nodes = sorted(nodes, key=lambda x: x[1], reverse=True) #Ordena novamente colocando esse nó na lista

    return nodes[0][0] #Raiz da Árvore de Huffman

# Função para codificar a árvore em um dicionário com o mapeamento dos simbolos para bits
def huffmanDict(node, left=True, binString=''):
    if type(node) is str:               #Se for uma folha
        return {node: binString}        #Retorna a codeword final para atualizar o dicionário.
    (l, r) = node.children()
    d = dict()
    d.update(huffmanDict(l, True, binString + '1'))
    d.update(huffmanDict(r, False, binString + '0'))
    return d

# print(' Chars | Huffman Tree ')
# print('----------------------')
# for (char, frequency) in contBytesMapped:
#     print(' %-4r |%12s' % (char, huffmanCode[char]))

def compressFile(fileName, huffmanCode):
    #Criação do arquivo comprimido
    compressedFileName = fileName.split('.')[0] + '.pphuff'
    compressedFile = open(compressedFileName, 'wb')
    compressedBytes = []

    f = open(fileName, 'rb')
    byte = f.read(1)

    #Rodar o arquivo novamente com o dicionário de Huffman e assim codificar cada byte
    nextBinByte = '' #Próximo byte binário a ser escrito no arquivo
    while byte:
        readByte = str(int.from_bytes(byte, 'big'))
        codedBin = huffmanCode[readByte]

        while len(codedBin) > 0:
            if len(nextBinByte) < 8:
                nextBinByte += codedBin[:1]     #Primeio bit
                codedBin = codedBin[1:]
            else:
                compressedBytes.append(int(nextBinByte, base=2))
                nextBinByte = ''
        
        byte = f.read(1)
    f.close()

    #Caso falte bits no último byte, preencher até ser um byte
    #No Header do arquivo comprimido vai ter essa quantidade de bits que deve ser descartado do final
    contBitsFinal = 0
    while len(nextBinByte) < 8:
        contBitsFinal += 1
        nextBinByte += '1'
#####################################
####Colocar o contBitsFinal no Header

    compressedBytes.append(int(nextBinByte, base=2))
    compressedBytesArray = bytearray(compressedBytes)
    compressedFile.write(compressedBytesArray)
    compressedFile.close()

####Retirar depois do HEADER
    contBitsFinalTemp = contBitsFinal
    return contBitsFinalTemp

#Agora dá início a parte do código que decodifica os dados salvos no arquivo .pphuffman
def decompressFile(fileNamePphuff, raizTemp, contBitsFinalTemp):
    encodedFile = open(fileNamePphuff, 'rb')
    byte = encodedFile.read(1)
    binStr = ''
    while byte:
        byteInt = int.from_bytes(byte, 'big')       #Lê o número do byte
        binStr += format(byteInt, 'b').zfill(8)     #Adiciona os bits do número na string de binários
        byte = encodedFile.read(1)

#######################################
#####Pegar esse contBitsFinal do HEADER
    # binStr = binStr[:-contBitsFinal]
    binStr = binStr[:-contBitsFinalTemp]

####################################
####Pegar a árvore da raiz do HEADER
    decodedMessage = huffmanDecoding(binStr, raizTemp)

###############################################
####Pegar formato origianl do arquivo do HEADER
    decompressedFile = open('decompressed.txt', 'wb')
    decompressedBytesArray = bytearray(decodedMessage)
    decompressedFile.write(decompressedBytesArray)
    decompressedFile.close()

#Lê bit a bit e pecorre a árvore para decodificar
def huffmanDecoding(encodedDataBits, huffmanTree):  
    treeHead = huffmanTree  
    decodedOutput = []  
    for x in encodedDataBits:  
        if x == '0':  
            if type(huffmanTree.right) is str:
                decodedOutput.append(int(huffmanTree.right))
                huffmanTree = treeHead
            else:
                huffmanTree = huffmanTree.right     

        elif x == '1': 
            if type(huffmanTree.left) is str:
                decodedOutput.append(int(huffmanTree.left))
                huffmanTree = treeHead
            else:
                huffmanTree = huffmanTree.left  
         
    return decodedOutput



if __name__ == "__main__":

    raiz = huffmanTree('a.txt')
    huffmanCode = huffmanDict(raiz)
    bitsFinalTemp = compressFile('a.txt', huffmanCode)
    raizTemp = raiz
    decompressFile('a.pphuff', raizTemp, bitsFinalTemp)

    print(' Chars | Huffman Tree ')
    print('----------------------')
    for char in huffmanCode:
        print(' %-4r |%12s' % (char.zfill(3), huffmanCode[char]))