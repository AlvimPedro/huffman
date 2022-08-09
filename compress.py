f = open('a.txt', 'rb')

byte = f.read(1)

contBytes = [0] * 256 
contTotal = 0


# Contagem byte a byte alocada na posição do array que representa seu valor em um byte (0 - 255)
while byte:
    contBytes[int.from_bytes(byte, 'big')] += 1
    contTotal += 1

    byte = f.read(1)

# Probabilidade de cada byte
probBytes = [c/contTotal for c in contBytes]

# Colocando em ordem descrescente e adicionando um indice, que é o valor do byte original
descProbBytes = [[i, probBytes[i]] for i in range(len(probBytes))]
def takeSecond(elem):
    return elem[1]
descProbBytes.sort(reverse=False, key=takeSecond)

#print(descProbBytes)

# Criando a árvore binária
# for p in descProbBytes:
#     # print(p[1])
#     if p[1] > 0:




class HuffmanTree:

    # Primeiro vai
    def __init__(self, value, left, right):
        self.left = left
        self.right = right
        self.value = value

    def insert(self, value):
        if self.value:
            if value < self.value:
                if self.left is None:
                    self.left = Node(value)
                else:
                    self.left.insert(value)
            elif value > self.value:
                if self.right is None:
                    self.right = Node(value)
            else:
                self.right.insert(value)
        else:
            self.value = value


#print(contTotal)
#print(contBytes)
#print(probBytes)