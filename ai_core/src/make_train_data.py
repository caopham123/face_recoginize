from api.helpers.db_connection import QueryMember

class Trainer:
    def __init__(self):
        self.dbConn = QueryMember()

    def register_member(self, name = None, email = None, face = None):
        response = self.dbConn.create_member(name, email, face) 
        return response # True/False

    def update_member(self, id: int, email = None, name = None, face = None):
        self.dbConn.update_member(id, email, name, face)
        return True
    
    def delete_member(self, id: int):
        self.dbConn.delete_member(id)
        return True
    
    def search_member_by_name(self, name: str):
        result= self.dbConn.search_by_name(name)
        return result

    def search_member_by_email(self, email: str):
        result= self.dbConn.search_by_email(email)
        return result
    
        