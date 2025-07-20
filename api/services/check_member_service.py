from ai_core.src.face_recognition import FaceRecognition
from ai_core.src.make_train_data import Trainer
from ai_core.src.check_face_spoofing import check_facial_spoofing
from ai_core.src.setting import FACIAL_SPOOFING_THRESHOLD
from fastapi.responses import JSONResponse
from fastapi import status
from api.helpers.db_connection import QueryMember


face_recognition = FaceRecognition()
trainer = Trainer()
query_member = QueryMember()

def register_member(email = None, name = None, image = None):
    if not query_member.validate_email(email):  # Found email
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST
                            ,content={"message": "Email is exists!"} )
    if image is not None:
        _, embedding = face_recognition.detection.dectect_face(image)
        # Not found faces on image
        if embedding is None:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST
                            ,content={"message": "Image doesn't contain face!"} )

        if trainer.register_member(name, email, embedding):
            return JSONResponse(status_code=status.HTTP_200_OK
                                ,content={"message": "Register Successfully"} )
    
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST
                            ,content={"message": "Invalid image base64"} )

def modify_member(id: int, email = None, name = None, image = None):
    if not query_member.validate_id(id): 
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": "Id doesn't exists!"})
    embedding = None
    if image is not None:
        _, embedding = face_recognition.detection.dectect_face(image)
    if trainer.update_member(id, email, name, embedding):
        return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"message": "Modify Successfully!"})
def search_member_by_name(name: str=None):
    if name is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": "Invalid input name!"})
    result= trainer.search_member_by_name(name)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": result})

def search_member_by_email(email: str=None):
    if email is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": "Invalid input email!"})
    result= trainer.search_member_by_email(email)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": result})
    
def del_user(id):
    if not query_member.validate_id(id): 
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": "Id doesn't exists!"})
    if trainer.delete_member(id):
        return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"message": "Remove Successfully!"})

def check_user(image):
    # ======== CHECK FICAL-SPOOFING ============
    score_face_spoofing = check_facial_spoofing(image)
    print(f"=========>score {score_face_spoofing}\n")
    if score_face_spoofing is None or score_face_spoofing < FACIAL_SPOOFING_THRESHOLD:
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content= {"message":"Detected facial spoofing"}
            )
    # ========= FACE RECOGNITION =============
    result = face_recognition.recognize_face(image)
    if result is None: 
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content= {"message":"Not found member"}
        )
    id = result['id']
    email = result['email']
    name = result['full_name']

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content= {"id":id, "email": email, "name":name}
    )

def check_image(image):
        crop_face, embedding = face_recognition.detection.dectect_face(image)
        if crop_face is not None and embedding is not None:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content= "Found faces on the image"
            )
        return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content= "Not found any faces on the image"
            )

