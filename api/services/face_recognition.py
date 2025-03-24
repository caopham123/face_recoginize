from ai_core.src.face_recognize import FaceRecognition
from ai_core.src.make_train_data import Trainer
from fastapi.responses import JSONResponse
from fastapi import status


face_recognition = FaceRecognition()
trainer = Trainer()

def add_user(target_id: str = None, target_email = None, target_name = None, target_image = None):
    global face_recognition, trainer
    embedding = None

    if target_image is not None:
        _, embedding = face_recognition.recognize_face(target_image)
    message = trainer.register_member(target_id, target_email, target_name, embedding)
    face_recognition = FaceRecognition()
    response = {
        "code": status.HTTP_200_OK,
        "data": message
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)

def del_user(target_id: str = None):
    global face_recognition, trainer

    if target_id is None: return False

    msg = trainer.delete_member(target_id)
    face_recognition = FaceRecognition()
    response = {
        "status_code": status.HTTP_200_OK,
        "content": msg
    } 
    return JSONResponse(status_code=status.HTTP_200_OK, content={"response": response})