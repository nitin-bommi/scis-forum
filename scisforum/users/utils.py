import os, secrets
import cv2
import numpy as np
import face_recognition
import base64
from io import BytesIO
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from scisforum import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='imtech2k18@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


def image_to_encoding(image, username):
    file_path = username + '.npy'
    encoding_path = os.path.join(current_app.root_path, 'static/encodings', file_path)

    sbuf = BytesIO()
    sbuf.write(base64.b64decode(image[22:]))
    img = Image.open(sbuf)
    
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
    img_enc = face_recognition.face_encodings(img)[0]
    if img_enc.size == 0:
        return False
    np.save(encoding_path, img_enc)
    
    return file_path


def verify_face(encoding_file, image):
    encoding_path = os.path.join(current_app.root_path, 'static/encodings', encoding_file)
    face_encodings_for_id = np.load(encoding_path, allow_pickle=True)
    
    sbuf = BytesIO()
    sbuf.write(base64.b64decode(image[22:]))
    img = Image.open(sbuf)

    img = cv2.resize(np.array(img), (0, 0), fx=0.6, fy=0.6)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    harcascadePath = os.path.join(current_app.root_path, 'models/haarcascade_frontalface_default.xml')
    face_detector = cv2.CascadeClassifier(harcascadePath)
    
    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(50, 50),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    result = [None]*len(faces)

    for idx, (x,y,w,h) in enumerate(faces):
        encoding = face_recognition.face_encodings(rgb, [(y, x+w, y+h, x)])[0]
        if encoding.size == 0:
            print("No face detected...")
            return False
        result[idx] = face_recognition.compare_faces([face_encodings_for_id], encoding, 0.3)[0]

    if any(result):
        return True
    return False