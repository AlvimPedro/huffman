# Criação dos nós
class NodeTree(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s_%s' % (self.left, self.right)


# Função principal para codificar
def huffman_code_tree(node, left=True, binString=''):
    if type(node) is str:               #Se for uma folha
        return {node: binString}        #Retorna a codeword final para atualizar o dicionário.
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '1'))
    d.update(huffman_code_tree(r, False, binString + '0'))
    return d


f = open('a.txt', 'rb')
byte = f.read(1)

contBytes = [0] * 256 
contTotal = 0

#Conta a aparição de cada byte do arquivo
while byte:
    contBytes[int.from_bytes(byte, 'big')] += 1
    contTotal += 1

    byte = f.read(1)
f.close()


#É feito um mapeamento de cada simbolo com a frequência e ordenado
contBytesMapped = []
for i in range(256):
    if contBytes[i] > 0:
        contBytesMapped.append((str(i), contBytes[i]))

def takeSecond(elem):
    return elem[1]
contBytesMapped.sort(reverse=True, key=takeSecond)

# print(contBytesMapped)


nodes = contBytesMapped

print(nodes)
while len(nodes) > 1:
    (key1, c1) = nodes[-1]          #Último elemento (Que tem a menor probabilidade)
    (key2, c2) = nodes[-2]          #Penúltimo elemento
    nodes = nodes[:-2]              #Retira eles da lista
    node = NodeTree(key1, key2)     #Cria um nó que coloca o left e right do nó
    nodes.append((node, c1 + c2))   #Coloca na lista novamente esse novo nó

    nodes = sorted(nodes, key=lambda x: x[1], reverse=True) #Ordena para 

# print(nodes[0][0].children()[1].children())
print(nodes[0][0])

raiz = nodes[0][0]


huffmanCode = huffman_code_tree(raiz)


print(' Chars | Huffman Tree ')
print('----------------------')
for (char, frequency) in contBytesMapped:
    print(' %-4r |%12s' % (char, huffmanCode[char]))

#Criação do arquivo comprimido
compressedFile = open('compressed.pphuff', 'wb')
compressedBytes = []

f = open('a.txt', 'rb')
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

print(contBitsFinal)

compressedBytes.append(int(nextBinByte, base=2))

print(compressedBytes)
compressedBytesArray = bytearray(compressedBytes)
compressedFile.write(compressedBytesArray)
compressedFile.close()

#Agora dá início a parte do código que decodifica os dados salvos no arquivo .pphuffman
# encodedFile = open('compressed.pphuff', 'rb')
# encodedData = encodedFile.read(1)


encodedFile = open('compressed.pphuff', 'rb')
byte = encodedFile.read(1)
binStr = ''
while byte:
    byteInt = int.from_bytes(byte, 'big')       #Lê o número do byte
    binStr += format(byteInt, 'b').zfill(8)     #Adiciona os bits do número na string de binários

    byte = encodedFile.read(1)

binStr = binStr[:-contBitsFinal]
print(binStr)



def huffmanDecoding(encodedData, huffmanTree):  
    treeHead = huffmanTree  
    decodedOutput = []  
    for x in encodedData:  
        if x == '0':  
            print(type(huffmanTree), huffmanTree)
            if type(huffmanTree.right) is str:
                decodedOutput.append(int(huffmanTree.right))
                huffmanTree = treeHead
            else:
                huffmanTree = huffmanTree.right     

        elif x == '1': 
            print(type(huffmanTree), huffmanTree)
            if type(huffmanTree.left) is str:
                decodedOutput.append(int(huffmanTree.left))
                huffmanTree = treeHead
            else:
                huffmanTree = huffmanTree.left  
         
    return decodedOutput

decodedMessage = huffmanDecoding(binStr, raiz)
print(decodedMessage)

decompressedFile = open('decompressed.txt', 'wb')

decompressedBytesArray = bytearray(decodedMessage)
decompressedFile.write(decompressedBytesArray)
decompressedFile.close()


# decoded = huffmanDecoding()

print('Aqui vai o arquivo decodificado')