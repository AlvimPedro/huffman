
# f = open('a.txt')
# byte = f.read()

# byte = 'ABBBBBBBBBBBBBBBBBBBBBBBBBBCCAAAAADDCCCCCCCCCCCCCGGGHHHHUZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ'

# Criação dos nós
from ast import While


class NodeTree(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s_%s' % (self.left, self.right)


# Função principal para codificar
def huffman_code_tree(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
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


#É feito um mapeamento de cada simbolo com a frequência e ordenado
contBytesMapped = []
for i in range(256):
    if contBytes[i] > 0:
        contBytesMapped.append((str(i), contBytes[i]))

def takeSecond(elem):
    return elem[1]
contBytesMapped.sort(reverse=True, key=takeSecond)

# print(contBytesMapped)


freq = contBytesMapped

nodes = freq

while len(nodes) > 1:
    (key1, c1) = nodes[-1]
    (key2, c2) = nodes[-2]
    nodes = nodes[:-2]
    node = NodeTree(key1, key2)
    nodes.append((node, c1 + c2))

    nodes = sorted(nodes, key=lambda x: x[1], reverse=True)


huffmanCode = huffman_code_tree(nodes[0][0])


print(' Chars | Huffman Tree ')
print('----------------------')
for (char, frequency) in freq:
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

#Caso falte bits no último byte, preencher até ser um byte
#No Header do arquivo comprimido vai ter essa quantidade de bits que deve ser descartado do final
contBitsFinal = 0
while len(nextBinByte) < 8:
    contBitsFinal += 1
    nextBinByte += '1'

compressedBytes.append(int(nextBinByte, base=2))

print(compressedBytes)
compressedBytesArray = bytearray(compressedBytes)
compressedFile.write(compressedBytesArray)

#Agora dá início a parte do código que decodifica os dados salvos no arquivo .pphuffman
encodedFile = open('compressed.pphuff', 'rb')
encodedData = encodedFile.read(1)

def huffmanDecoding(encodedData, huffmanTree):  
    treeHead = huffmanTree  
    decodedOutput = []  
    for x in encodedData:  
        if x == '1':  
            huffmanTree = huffmanTree.right     
        elif x == '0':  
            huffmanTree = huffmanTree.left  
        try:  
            if huffmanTree.left.symbol == None and huffmanTree.right.symbol == None:  
                pass  
        except AttributeError:  
            decodedOutput.append(huffmanTree.symbol)  
            huffmanTree = treeHead  
          
    string = ''.join([str(item) for item in decodedOutput])  
    return string

print('Aqui vai o arquivo decodificado')