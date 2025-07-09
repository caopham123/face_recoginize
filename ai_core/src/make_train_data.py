from api.helpers.db_connection import QueryMember

class Trainer:
    def __init__(self):
        self.dbConn = QueryMember()

    def register_member(self, name = None, email = None, face = None):
        response = self.dbConn.create_member(name, email, face) 
        return response # True/False

    def update_member(self, id: int , name = None, email = None, face = None):
        # if id is None:
        #     return False
        self.dbConn.update_member(id, name, email, face)
        return True
    
    def delete_member(self, id: int):
        # if id is None:
        #     return False
        self.dbConn.delete_member(id)
        return True
    
        