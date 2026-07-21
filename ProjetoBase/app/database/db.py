
class DB():
    def __init__(self):
        self.db = {}
    def insert(self,id,object):
        self.db[id]=object
    def update(self,id,object):
        self.db[id]=object
    def retrieve(self,id):
        return self.db.get(id,None)
    def delete(self,id):
        self.db.pop(id,None)

    def retrieve_all(self,):
        return self.db