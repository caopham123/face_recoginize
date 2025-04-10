from .face_detection import FaceDetection
from .setting import DB_FACE_PATH
import pandas as pd

class Trainer():
    def __init__(self):
        self.data = pd.read_json(DB_FACE_PATH)
        self.ids = self.data['id'].to_numpy().tolist()
        self.names = self.data['name'].to_numpy().tolist()
        self.emails = self.data['email'].to_numpy().tolist()
        self.faces = self.data['face'].to_numpy().tolist()
        print("openned file")

    def register_member(self, target_id: int = None, target_name = None, target_email = None, target_face = None):
        ## Case: Don't pass the id
        if target_id is None:
            return False
        ## Case: Have specified member on DB
        ## Find loc and update other fields
        if target_id in self.ids:
            index = self.ids.index(target_id)
            ## Update other fields
            self.emails[index] = target_email if target_email is not None else self.emails[index]
            self.names[index] = target_name if target_name is not None else self.names[index]
            self.faces[index] = target_face if target_face is not None else self.faces[index]
        ## Case: Not found Id on DB ==> Create a new
        else:
            if target_email is None:
                return False
            if target_name is None:
                return False
            if target_face is None:
                return False
            self.ids.append(target_id)
            self.emails.append(target_email)
            self.names.append(target_name)
            self.faces.append(target_face)
        
        ## Save db
        self.data = pd.DataFrame({
            "id": self.ids,
            "email": self.emails,
            "name": self.names,
            "face": self.faces
        })
        self.data.to_json(DB_FACE_PATH, indent=4, force_ascii=True)
        return True   

    def delete_member(self, target_id):
         ## Case: Don't pass the id
        if target_id is None:
            return False
        ## Case: Have specified member on DB
        ## Find loc and delete other fields
        if target_id not in self.ids:
            return False
        if target_id in self.ids:
            index = self.ids.index(target_id)
            ## Delete other fields
            self.ids.pop(index)
            self.emails.pop(index) 
            self.names.pop(index)
            self.faces.pop(index)

            ## Save db
            self.data = pd.DataFrame({
                "id": self.ids,
                "email": self.emails,
                "name": self.names,
                "face": self.faces
            })
            self.data.to_json(DB_FACE_PATH, indent=4, force_ascii=True)
            return True
    
if __name__ == "main":
    import cv2
    trainer = Trainer()
    face_detection = FaceDetection()
    image = cv2.imread("ai_core/pic/noo_phuoc_thinh_1.jpg")
    _, embedding = face_detection.dectect_face(image)
    
    # trainer.register_member(
    #     3, "test01", "test01@gmail.com", embedding
    # )
    # trainer.delete_member(5)
