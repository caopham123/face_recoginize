# Face Recognition Intergated Anti-Spoofing System
## Quick Installation
1. Set up the enviroment
- On Command Line tab of root folder, type command: **python -m venv .venv**
- Then, type: **.venv\Scripts\activate**
- Finally, type: **pip install -r requirements.txt**
2. Download the pre-trained model for Facial Anti-spoofing:
- At the **ai_core** folder, make a new **model** folder
- Download the **face_swin_v2_face** [(Get here)](https://drive.google.com/file/d/1E4UD8UK_KzjhpAvR6hYInlteOEaxDZbZ/view)
3. Upload images for running:
- At the **ai_core** folder, make a new **pic** folder to contain images
4. Check facial spoofing (without GPU)
- Usually, this task need GPU to execute. But I don't have GPU, following the below way:
- On **ai_core/src/check_face_spoofing.py** file, replace 3 comment lines (line 54-58) to line 59
 ![image](https://github.com/user-attachments/assets/30b6944e-365b-4aa2-8e7f-4ed0e520fbea)
5. Run uvicorn
- By default, we type this command: **uvicorn main:app**
- If you customize port or host:
![image](https://github.com/user-attachments/assets/91f2a499-c4f4-4faf-aa1c-72fb7a09dd99)
- After that, run: **uvicorn main:app --host 0.0.0.0 --port 5050**

## Work flow:
![image](https://github.com/user-attachments/assets/2fb4067e-6af2-4060-b3d8-1cc6a9731d81)

## Architecture:
![image](https://github.com/user-attachments/assets/a41fd3f7-f94f-4910-a1f5-10a8ebbbbdfe)

## Use Case:
### Register new users 
The server takes information from a new user which consists of username, email, user id, and an image (converted to string base64).
In case of registering or updating an image of an existing user, the server will check whether the input image is valid. 
After, the face detection process begins by the pre-trained model. This process takes a string image, and returns the bounding box of the face (if it exists) and a 512D vector embedding that stores features of each face. If not, return None. 
If the field is valid, the server verifies whether information of an assigned user is available on the database. In case of unavailable information, the server will store it. If it not, update and store it 

### Delete information of assigned users
This function takes the user id. Then, checking this value whether it is available on the database. In case of existing, it will delete all of the user's information.

### Detect the valid input image
This function takes the image (converted to string). First, the pre-trained model locates faces on the image,  selects the biggest face and 5 landmarks on one. This model returns a bounding box and a 512D vector embedding.
If the return either a bounding box is None or a vector embedding is None, this function alerts the image is invalid.

### Check-in users
First, the server checks whether input is **facial spoofing**.
Second, when the input is valid (real face images), the model will begin detecting (**Detect the valid input image**)
Third, when the model returns a vector embedding, the server will take this return vector, and compare it with each saved vector stored on the database by using cosine_similarity algorithm. If the return cosine is higher than the threshold value (equal is 0.5) and it is the highest value, the server will record information of the user (whose saved vector equals the return vector) and current time.

### Check facial spoofing
This function takes an input image (converted to string) and loads the  pre-trained model (architecture is swin_v2_b). 
Then, an input image is resized to a 224x224 image, and converted from BGR to RGB color. After that, normalize the image by using Swin Transformer V2. The output of this process is an array format.
Finally, apply softmax to get probabilities and return the result.

