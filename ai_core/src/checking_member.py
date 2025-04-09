import pandas as pd

from .setting import DB_RESULT_PATH

class CheckingMember():
    def __init__(self):
        self.df = pd.read_json(DB_RESULT_PATH)
        self.emails = self.df["email"].to_numpy().tolist()
        self.names = self.df["name"].to_numpy().tolist()
        self.times = self.df["time_checking"].to_numpy().tolist() 
        print("Opened result file")

    def check_member(self, target_email: str, target_time, target_name):
        ## Case: Not found email
        if target_email is None:
            return False
        
        ## Case: Insert into DB
        else:
            self.emails.append(target_email)
            self.names.append(target_name)
            self.times.append(str(target_time))
        
        ## Save db
        self.data = pd.DataFrame({
            "email": self.emails,
            "name": self.names,
            "time_checking": self.times
        })
        self.data.to_json(DB_RESULT_PATH, indent=4, force_ascii=True)
        return True  
if __name__ == "__main__":
    obj1 = CheckingMember()
