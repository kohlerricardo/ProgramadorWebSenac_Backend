
class Database:
    def __init__(self):
        self.index = 0
        self.banco = {}

    def insert(self,id,objeto):
        self.banco[id]=objeto
        
    def retrieve(self):
        return self.banco
    def next_index(self):
        self.index+=1
        # yield torna uma função em um gerador, salvando o estado da função e retomando valores quando a função é chamada
        # retornando um valor por vez
        yield self.index