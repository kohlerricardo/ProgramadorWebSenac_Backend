
class Database:
    def __init__(self):
        self.banco = {}

    def insert(self,id,objeto):
        self.banco[id]=objeto
        
    def retrieve(self):
        return self.banco