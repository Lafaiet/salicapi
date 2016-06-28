from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
from wtforms import ValidationError

from jsonschema import validate, Draft3Validator


schema = {

    'type': 'object',
    'properties': {
        'PRONAC' : {'type' : 'number'},
    }

}

def testPRONAC(form, field):
    print field.data.keys()
    try:
        int(field.data)
    except:
        raise ValidationError('PRONAC must be integer')

class InputValidation():

    def __init__(self, fields):
       self.fields = fields

    def validate(self):
        Draft3Validator(schema).validate(self.fields)
