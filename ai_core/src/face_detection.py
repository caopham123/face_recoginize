import insightface
from insightface.app import FaceAnalysis

from setting import FACE_MODEL_PATH
class FaceDection():
    def __init__(self):
        self.model = FaceAnalysis(FACE_MODEL_PATH, providers=['CPUExecutionProvider'])
        self.model.prepare(ctx=0)
