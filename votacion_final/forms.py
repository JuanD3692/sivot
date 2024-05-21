
from wtforms import Form
from wtforms import StringField,TextAreaField
from wtforms  import  validators
from wtforms.validators import InputRequired, Email


def length_honeypot(form,field):
    if len(field.data)>0:
        raise validators.ValidationError('El campo debe de estar vacio.')
    
    
class RegisterForm(Form):
    username = StringField('Nombre:',
                           [
                               validators.DataRequired(message='El nombre es exigido'),
                               validators.length(min=1, max=25, message='Ingrese un username valido!.')
                           ])
    
    apellido = StringField('Apellido:',  [
        validators.DataRequired(message='El nombre es exigido'),
        validators.length(min=1, max=25, message='Ingrese un username valido!.')
    ])
    
    cedula = StringField('Cedula:',
                         [
                             validators.DataRequired(message='La cedula es requerida'),
                             validators.length(
                                 min=7, max=10, message='Ingrese una cedula valida!.'),
                         ])
    expedicion = StringField('Expedicion:',  [
        validators.DataRequired(message='la expedicion'),
        validators.length(min=10, max=10, message='Ingrese un username valido!.')
    ])



class LoginForm(Form):
    cedula = StringField('cedula',
                         [
                             validators.DataRequired(message='La cedula es requerida'),
                             validators.length(min=7, max=10, message='Ingrese una cedula valida!.'),
                         ])

class ContactForm(Form):
    nombre = StringField('Nombre:',
                           [
                               validators.DataRequired(message='El nombre es exigido'),
                               validators.length(min=1, max=25, message='Ingrese un username valido!.')
                           ])
    email = StringField("Email",  [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])      
        
    message = TextAreaField("Message",[
                               validators.DataRequired(message='El nombre es exigido'),
                               validators.length(min=10, max=250, message='Ingrese un username valido!.')
                           ])
    