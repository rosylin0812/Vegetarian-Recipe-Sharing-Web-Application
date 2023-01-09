import os, secrets
from PIL import Image
from flask import url_for, current_app
from veggyblog import mail
from flask_login import current_user
from flask_mail import Message 
       

def save_picture(form_picture):
    # randomlized the image name
    random_hex = secrets.token_hex(8)
    # split file name and extension( jpg  or png)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn) # replace app with current_app
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    if current_user.image_file != 'default.jpg':
        os.remove(os.path.join(current_app.root_path, 'static/profile_pics', current_user.image_file))
    i.save(picture_path)
    
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Resent Request', 
                  sender='noreply.veggyteam@gmail.com', 
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token =token, _external=True)}
   
If you did not make this request, please simply ignore this email and no changes will be made.

Sincerely,
Veggy Team    
'''
    mail.send(msg)
