from ai_core.src.face_recognize import FaceRecognition
from ai_core.src.face_recognize import FaceDetection
from ai_core.src.make_train_data import Trainer
from ai_core.src.checking_member import CheckingMember
from fastapi.responses import JSONResponse
from fastapi import status


face_recognition = FaceRecognition()
face_detection = FaceDetection()
trainer = Trainer()
checking_Member = CheckingMember()

def register_member(target_id: int = None, target_email = None, target_name = None, target_image = None):
    global face_recognition, trainer
    embedding = None

    if target_image is not None:
        _, embedding = face_detection.dectect_face(target_image)

    message = trainer.register_member(target_id, target_email, target_name, embedding)
    face_recognition = FaceRecognition()
    response = {
        "code": status.HTTP_200_OK,
        "data": message
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=response)

def del_user(target_id):
    global face_recognition, trainer

    msg = trainer.delete_member(target_id)
    face_recognition = FaceRecognition()
    response = {
        "status_code": status.HTTP_200_OK,
        "content": msg
    } 
    return JSONResponse(status_code=status.HTTP_200_OK, content={"response": response})

def check_image(image):
    crop_face, embedding = face_detection.dectect_face(image)
    if crop_face is not None and embedding is not None:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content= "Found faces on the image"
        )
    return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content= "Not found any faces on the image"
        )

def check_user(image):
    result = face_recognition.recognize_face(image)
    target_email = result['email']
    target_name = result['name']
    target_time = result['time']
    # id, email, name, time = result
    ## Trainer
    print(f"service dic: {target_email, target_name, target_time}")
    msg = checking_Member.check_member(target_email=target_email, target_name=target_name, target_time=target_time)

    if result is not None:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content= msg
        )
    return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content= "Not recognize member"
        )