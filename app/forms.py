from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from app.models.user import User


class RegistrationForm(FlaskForm):
    """User registration form with validation."""
    
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ])
    
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address')
    ])
    
    phone = StringField('Phone Number', validators=[
        Optional(),
        Length(max=20, message='Phone number too long')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    
    password_confirm = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """Check if username already exists."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        """Check if email already exists."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')


class LoginForm(FlaskForm):
    """User login form."""
    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class BotForm(FlaskForm):
    """Bot creation and editing form."""
    
    name = StringField('Bot Name', validators=[
        DataRequired(),
        Length(min=3, max=100, message='Bot name must be between 3 and 100 characters')
    ])
    
    description = TextAreaField('Description', validators=[
        Optional(),
        Length(max=500, message='Description cannot exceed 500 characters')
    ])
    
    language = SelectField('Language', choices=[
        ('uz', 'Uzbek'),
        ('ru', 'Russian'),
        ('en', 'English'),
        ('es', 'Spanish')
    ], validators=[DataRequired()])
    
    platform = SelectField('Platform', choices=[
        ('telegram', 'Telegram')
    ], validators=[DataRequired()], default='telegram')
    
    system_prompt = TextAreaField('System Prompt', validators=[
        Optional(),
        Length(max=2000, message='System prompt cannot exceed 2000 characters')
    ], description='Instructions for the AI assistant')
    
    # Multiple Telegram tokens support
    telegram_token_1 = StringField('Primary Telegram Token', validators=[
        DataRequired(),
        Length(max=100, message='Token too long')
    ], description='Primary token from @BotFather')
    
    telegram_token_2 = StringField('Secondary Telegram Token', validators=[
        Optional(),
        Length(max=100, message='Token too long')
    ], description='Secondary token for backup (optional)')
    
    telegram_token_3 = StringField('Tertiary Telegram Token', validators=[
        Optional(),
        Length(max=100, message='Token too long')
    ], description='Tertiary token for reliability (optional)')
    
    submit = SubmitField('Create Bot')
