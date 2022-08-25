
# f = open('a.txt')
# byte = f.read()

# byte = 'ABBBBBBBBBBBBBBBBBBBBBBBBBBCCAAAAADDCCCCCCCCCCCCCGGGHHHHUZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ'

# Criação dos nós
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


# Cálculo da frequência de repetição dos caracteres 
# freq = {}
# for c in byte:
#     if c in freq:
#         freq[c] += 1
#     else:
#         freq[c] = 1

# freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
# print(freq)

f = open('a.txt', 'rb')

byte = f.read(1)

contBytes = [0] * 256 
contTotal = 0

while byte:
    contBytes[int.from_bytes(byte, 'big')] += 1
    contTotal += 1

    byte = f.read(1)

contBytesMapped = [(0,0)] * 256
for i in range(256):
    contBytesMapped[i] = (i, contBytes[i])


def takeSecond(elem):
    return elem[1]
contBytesMapped.sort(reverse=True, key=takeSecond)

print(contBytesMapped)


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