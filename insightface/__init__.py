from insightface.process import face_model
import numpy as np
import cv2
import os


class FaceArgs:
    def __init__(self, **args):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.det = 0
        self.flip = 0
        self.ga_model = ''
        self.gpu = 0
        self.image_size = '112,112'
        self.model = os.path.join(current_dir, 'models/model-r100-ii') + ',0'
        self.threshold = 1.24
        self.__dict__.update(args)


def compare_two_faces(face1, face2, args=None) -> (float, float):
    if args is None:
        args = {}
    # model config
    args = FaceArgs(**args)
    model = face_model.FaceModel(args)
    # get f1 features
    f1_input = model.get_input(face1)
    f1 = model.get_feature(f1_input)
    # get f2 features
    f2_input = model.get_input(face2)
    f2 = model.get_feature(f2_input)
    # calc & return
    dist = np.sum(np.square(f1 - f2))
    sim = np.dot(f1, f2.T)
    return sim, dist
