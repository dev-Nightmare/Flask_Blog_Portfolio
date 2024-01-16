import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


def update_picture(form_picture, old_filename):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    print(f'print1 {form_picture.filename}')
    print(f'print2 {old_filename}')
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static//profile_pics', picture_filename)

    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    if old_filename != 'default.jpg':
        picture_path = os.path.join(current_app.root_path, 'static//profile_pics', old_filename)
        if os.path.exists(picture_path):
            os.remove(picture_path)

    return picture_filename


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@test.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
