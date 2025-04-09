from ai_core.src.face_recognize import FaceRecognition
from ai_core.src.face_recognize import FaceDetection
from ai_core.src.make_train_data import Trainer
from ai_core.src.checking_member import CheckingMember
from fastapi.responses import JSONResponse
from fastapi import status
from .check_face_spoofing import check_facial_spoofing


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
    score_face_spoofing = check_facial_spoofing(image)
    print(f"\n=========>score {score_face_spoofing}\n\n")
    if score_face_spoofing < 0.5 or score_face_spoofing is None:
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content= "Detected facial spoofing"
            )
    result = face_recognition.recognize_face(image)

    if result is None: 
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content= "Not found member"
        )
    
    target_email = result['email']
    target_name = result['name']
    target_time = result['time_checking']
    ## Trainer
    print(f"service check user: {target_email, target_name, target_time}")
    rs_checking = checking_Member.check_member(target_email=target_email, target_name=target_name, target_time=target_time)
    if rs_checking is False:
        rs_checking = "Not found member"
    else: 
        rs_checking = {
            "email": target_email, 
            "name": target_name,
            "time_checking": target_time
        }
    return JSONResponse(
        status_code=status.HTTP_200_OK,
            content= rs_checking
        )