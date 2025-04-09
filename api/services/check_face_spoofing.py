import cv2
import torch

import torch.nn.parallel

# Trong abc.py
import sys
from pathlib import Path

# Thêm thư mục gốc (project_root) vào sys.path
project_root = Path(__file__).resolve().parent.parent.parent  # Đi lên 3 cấp từ dic1/sub1/abc.py
sys.path.append(str(project_root))

from ai_core.lib.cv2_transform import transforms

project_root = Path(__file__).resolve().parent.parent.parent.parent  # Đi lên 3 cấp từ dic1/sub1/abc.py
sys.path.append(str(project_root))
from ai_core.lib.nets.utils import get_model

from api.helpers.commons import stringToRGB

import logging
import albumentations as A
from albumentations.pytorch import ToTensorV2

## Input expected argument is Path of image (image np.array) 
def check_facial_spoofing(image_path):
    
    arch = "swin_v2_b"

    input_size = 224
    resume = "models/face_swin_v2_base.pth"
    transforms1 = transforms.Compose([
            transforms.Resize(size=(input_size, input_size)),
            transforms.ColorTrans(mode=0), # BGR to RGB
        ])
    transforms2 = A.Compose([
        A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)), # RGB [0,255] input, RGB normalize output
        # A.Normalize(mean=(0, 0, 0), std=(1, 1, 1)), # RGB [0,255] input, RGB normalize output
        ToTensorV2(),
    ])

    ## Convert base64 to color image
    # image = cv2.imread(image_path)
    image = image_path
    image = transforms1(image)
    image = transforms2(image=image)
    image = image['image']

    logging.info("=> creating model '{}'".format(arch))
    arch = arch
    model = get_model(arch, 2)

    # model.cuda()
    # model = torch.nn.DataParallel(model, device_ids=[])


    # images = image.unsqueeze(0).to("cuda")
    images = image.unsqueeze(0).to("cpu")

    model.eval()
    with torch.no_grad():
        _, outputs = model(images)

        scores = torch.softmax(outputs, dim=1).data.cpu().numpy()[:,1]
        print(outputs)
        # print(f"Reality score: {round(scores[0],3)}")
        return scores[0]
    

# if __name__== "main":

