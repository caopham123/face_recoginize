from ai_core.src.face_detection import FaceDetection
from ai_core.src.face_identification import FaceIdentification
import pandas as pd

class FaceRecognition:
    def __init__(self):
        self.detection = FaceDetection()
        self.identification = FaceIdentification()

    ## Pass a image to compare this image with image existed in dataset
    def recognize_face(self, image):
        _, embedding = self.detection.dectect_face(image)
        if embedding is None:
            return None
        rs = self.identification.get_result(target_embedding= embedding)
        return rs
        
