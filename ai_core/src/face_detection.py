import insightface
from insightface.app import FaceAnalysis
import numpy as np
from .setting import FACE_MODEL_PATH


class FaceDetection():
    def __init__(self):
        self.model = FaceAnalysis(FACE_MODEL_PATH, providers=['CPUExecutionProvider'])
        self.model.prepare(ctx_id=0)

    def dectect_face(self, image: np.ndarray):
        ## Detect and retrive faces
        faces = self.model.get(image)

        if faces is not None:
            face = faces[0] ## Get the biggest face
            x1, y1, x2, y2 = face.bbox.astype(np.int32)
            crop_image = image[y1:y2, x1:x2]
            vecto_embedding = face.normed_embedding
            return crop_image, vecto_embedding
        return None, None
    
if __name__ == "__main__":
    import cv2
    face_detection = FaceDetection()
    image = cv2.imread("ai_core/pic/noo_phuoc_thinh_1.jpg")
    crop_img, embedding = face_detection.dectect_face(image)
    print(f"Embedding (512D): {len(embedding)}")

