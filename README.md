# Face Recognition Intergated Anti-Spoofing System
## Quick Installation
- On Command Line tab of root folder, type command: python -m venv .venv
- Then, type: .venv\Scripts\activate
- Finally, type: pip install -r requirements.txt
## Description
There are 2 main objectives, which include: Face Recognition and Facial Anti-Spoofing.

This project consists of 2 key components: **ai_core** and **api**.
### ai_core Components
The **ai_core/dataset** folder stores faces of users on the system and user’s information after recognition(.json file).

The **ai_core/src** folder is a key component, include:

  1. **setting.py**
This defines all of the settings including database paths, threshold value, model path…

  2. **face_detection.py**
Use RetinaFace backbone to detect and select the biggest face on frame (or image)
Then, normalize this face to a 512D-vector embedding.
Each face has a vector embedding that stores features of each face.

  3. **face_identification**
The mission of this is to record information of users once checked.
First, creating a target vector embedding per user. 
Second, calculating different from the target vector embedding to each vector stored in db
Third, check the value of the return. If it is higher or equal to the threshold, record user’s information (name, id, email, date time)

  4. **face_recognize**
This folder contains Face Detection and Face Identification components

  5. **check_face_spoofing**
Using the pre-trained weights of Swin Transformer V2 that are trained to distinguish between real and spoofing faces.

### api Component
The **api/helpers/commons.py** stores all support functions (convert from image to string and reserve)

The **api/middlewares/global_catch.py** used to catch exceptions (HTTP 500 Internal server err)

The **api/services/face_recognition.py** contains register (or update), remove function. And check_user functions used to check facial spoofing and (if not) recognize face (record check-in)

