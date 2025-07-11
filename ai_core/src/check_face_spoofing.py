import cv2
import torch
from ai_core.lib.cv2_transform import transforms
from ai_core.lib.nets.utils import get_model, load_resume
from ai_core.src.setting import ARCH, RESUME_PATH, INPUT_SIZE_IMAGE

import logging
import albumentations as A
from albumentations.pytorch import ToTensorV2


## Input expected argument is Path of image (image np.array) 
def check_facial_spoofing(image_string):
    
    arch = ARCH
    input_size = INPUT_SIZE_IMAGE
    resume = RESUME_PATH
    global model

    transforms1 = transforms.Compose([
            transforms.Resize(size=(input_size, input_size)),
            transforms.ColorTrans(mode=0), # BGR to RGB
        ])
    transforms2 = A.Compose([
        A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)), # RGB [0,255] input, RGB normalize output
        ToTensorV2(),
    ])

    ## Convert base64 to color image
    image = image_string
    image = transforms1(image)
    image = transforms2(image=image)
    image = image['image']

    logging.info("=> creating model '{}'".format(arch))
    arch = arch
    model = get_model(arch, 2)
    load_resume(resume, model, None)
    # model.cuda()
    # model = torch.nn.DataParallel(model, device_ids=[])


    # images = image.unsqueeze(0).to("cuda")
    images = image.unsqueeze(0).to("cpu")

    model.eval()
    with torch.no_grad():
        _, outputs = model(images)

        scores = torch.softmax(outputs, dim=1).data.cpu().numpy()[:,1]
        print(outputs)
        return scores[0]
