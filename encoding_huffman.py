# Criação dos nós
from cmath import exp


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


def compressFile(fileName, root):
    huffmanCode = huffmanDict(root)
    # print(len(huffmanCode))
    # print(' Chars | Huffman Tree ')
    # print('----------------------')
    
    # for char in huffmanCode:
    #     print(' %-4r |%12s' % (char.zfill(3), huffmanCode[char]))
    # print(root)

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
    

    #Criação do arquivo comprimido
    compressedFileName = fileName.split('.')[0] + '.pphuff'
    compressedFile = open(compressedFileName, 'wb')
###############################################################################################
###############################################################################################
    #Header
    arrTree = ['n'] * 6400140
    arrHuffmanTree = buildHeaderTree(1, root, arrTree)
    # print(arrHuffmanTree)
    headerBytes = buildHeader(arrHuffmanTree, contBitsFinal, fileName.split('.')[1])
    compressedFile.write(headerBytes)

    #Content
    compressedBytes.append(int(nextBinByte, base=2))
    compressedBytesArray = bytearray(compressedBytes)
    compressedFile.write(compressedBytesArray)
    compressedFile.close()



#Agora dá início a parte do código que decodifica os dados salvos no arquivo .pphuffman
def decompressFile(fileNamePphuff):
    encodedFile = open(fileNamePphuff, 'rb')

    #Ler o Header
    fileTree = encodedFile.readline()
    fileTree = fileTree.decode()
    arrTree = fileTree[:len(fileTree)-1].split()

    fileContBits = encodedFile.readline()
    fileContBits = fileContBits.decode()
    contBitsFinal = int(fileContBits[:len(fileContBits)-1])

    fileFormat = encodedFile.readline()
    fileFormat = fileFormat.decode()
    fileFormat = fileFormat[:len(fileFormat)-1]

    root = getHeaderTree(1, arrTree)

    byte = encodedFile.read(1)
    binStr = ''
    while byte:
        byteInt = int.from_bytes(byte, 'big')       #Lê o número do byte
        binStr += format(byteInt, 'b').zfill(8)     #Adiciona os bits do número na string de binários
        byte = encodedFile.read(1)

    binStr = binStr[:-contBitsFinal]

    decodedMessage = huffmanDecoding(binStr, root)

    decompressedFileName = 'd_' + fileNamePphuff.split('.')[0] + '.' + fileFormat

    decompressedFile = open(decompressedFileName, 'wb')
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

'''
           1
      2        3 
   4    5    6   7
 8   9
n=0 n=1 n=2 n=3 n=4 5   6   7   8   9

File format:
n   n   n   n   n   5   6   7   8   9

left = k * 2
right = (k * 2) + 1
'''
def buildHeaderTree(index, huffmanTree, arrTree):
    treeHead = huffmanTree

    if type(treeHead) is str:
        arrTree[index] = treeHead
        return arrTree
    else:
        arrTree[index] = 'n'
        arrLeft = buildHeaderTree(index * 2, treeHead.left, arrTree)
        arrRight = buildHeaderTree((index * 2) + 1, treeHead.right, arrLeft)
        return arrRight

def getHeaderTree(index, arrTree):
    #Se for letra (É um nó)
    # print(index)
    if not arrTree[index].isnumeric():
        node = NodeTree(getHeaderTree(index * 2, arrTree), getHeaderTree((index * 2) + 1, arrTree))
        return node
    else:
        leaf = arrTree[index]
        return leaf

def buildHeader(arrHuffmanTree, contBitsFinal, fileFormart):
    compactArrHuffmanTree = []
    i = len(arrHuffmanTree)
    # print(arrHuffmanTree[:200])
    while i != 0:
        i -= 1
        if arrHuffmanTree[i].isnumeric():
            compactArrHuffmanTree = arrHuffmanTree[:i+1]
            i = 0

    strTree = ' '.join(compactArrHuffmanTree)
    strBits = str(contBitsFinal)
    strFormat = fileFormart

    strHeader = strTree + '\n' + strBits + '\n' + strFormat + '\n'

    return bytearray(strHeader, 'utf-8')


if __name__ == "__main__":

    raiz = huffmanTree('a.txt')
    
    compressFile('a.txt', raiz)
    raizTemp = raiz
    decompressFile('a.pphuff')

    # print(' Chars | Huffman Tree ')
    # print('----------------------')
    # for char in huffmanCode:
    #     print(' %-4r |%12s' % (char.zfill(3), huffmanCode[char]))