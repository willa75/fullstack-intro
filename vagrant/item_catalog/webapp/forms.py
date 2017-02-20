from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, Field
from wtforms.widgets import TextInput
from wtforms.validators import DataRequired, Length, EqualTo, URL

from .models import User

class TagListField(Field):
    'Creates a field to handle tags in forms'
    widget = TextInput()

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else:
            self.data = []

class OpenIDForm(FlaskForm):
    'Form for OpenID users'
    openid = StringField('OpenID Url', [DataRequired(), URL()])

class LoginForm(FlaskForm):
    'Form to login to the site'
    username = StringField('Username', [
        DataRequired(), Length(max=255)
    ])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField("Remember Me")

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        # if user doesn't exist
        user = User.query.filter_by(
            username=self.username.data
        ).first()
        if not user:
            self.username.errors.append(
                'Invalid username or password'
            )
            return False

        # Do passwords match
        if not user.check_password(self.password.data):
            self.username.errors.append(
                'Invalid username or password'
            )
            return False

        return True

class RegisterForm(FlaskForm):
    'Form to add users to the site'
    username = StringField( 'username', [
        DataRequired(),
        Length(max=255)
    ])
    password = PasswordField('password', [
        DataRequired(),
        Length(min=8)
    ])
    confirm = PasswordField('Confirm Password', [
        DataRequired(),
        EqualTo('password')
    ])
    recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        #if validation fails
        if not check_validate:
            return False

        user = User.query.filter_by(
            username=self.username.data
        ).first()

        # Is the username already in use?
        if user:
            self.username.errors.append(
                "User with that username already exists"
            )
            return False

        return True

class ItemForm(FlaskForm):
    'Form to create or edit items'
    title = StringField('Name', [
        DataRequired(),
        Length(max=255)
    ])
    description = StringField('Description', [Length(max=255)])
    tags = TagListField('Tags')
    price = StringField('Price', [DataRequired()])

    def validate(self):
        check_validate = super(ItemForm, self).validate()

        if not check_validate:
            return False

        return True