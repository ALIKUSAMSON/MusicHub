
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import Required, Email, Length, EqualTo, AnyOf
from flask_wtf.file import FileField, FileAllowed, FileRequired




class RegistrationForm(Form):
    username = StringField('Username',validators=[Required(), Length(min=6,max=18)])
    email = StringField('Email',validators=[Required(),Email(message='Invalid address')])
    password = PasswordField('Password',validators=[Required(),Length(min=8, message="Password must be 6 characters as and more"),EqualTo('confirm',message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Register')

class LoginForm(Form):
    username = StringField('Username',validators=[Required(),Length(min=6,max=18)])
    password = PasswordField('Password',validators=[Required(), Length(min=8, message="Password must be 6 characters as and more")])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class ContactForm(Form):
    email = StringField('Email',validators=[Required(),Email(message='Invalid address')])
    subject = StringField('Subject',validators=[ Length(min=5,max=50)])
    message = TextAreaField('Message',validators=[Length(min=10)])
    submit = SubmitField('Send')    

class UploadSongForm(Form):
    artist_name = StringField('Artist Name', validators=[Required()])
    song_title = StringField('Song Title',validators=[Required()])
    upload = FileField('Upload')
    submit = SubmitField('Upload')

class UploadNewsForm(Form):
    story_title = StringField('Story Title',validators=[Required()])
    upload = FileField('Upload Images' )
    body =TextAreaField('Body',validators=[Length(min=10)])
    submit = SubmitField('Upload')

#validators=[Required(), AnyOf(['mp3'], 'Only mp3 audios allowed!')]
#validators=[Required(), AnyOf(['jpg','jpeg','png','gif'], 'Images only with jpg,jpeg,png,gif extensions')]


