from jsonschema import validate, Draft3Validator



def validate_input(input, schema):

    try:
        validation_errors = Draft3Validator(schema).validate(input)
        return True
    except Exception as e:
        print str(e)
        return False
