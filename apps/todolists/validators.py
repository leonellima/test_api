from cerberus import Validator


class TaskValidator:
    schema = {
        'id': {
            'type': 'integer',
            'empty': True,
            'nullable': False
        },
        'description': {
            'type': 'string',
            'empty': False,
            'nullable': False,
            'maxlength': 128
        },
        'finished_at': {
            'type': 'datetime',
            'empty': False,
            'nullable': True
        },
        'is_finished': {
            'type': 'boolean',
            'empty': False,
            'nullable': False
        }
    }

    def __init__(self, data):
        self.validator = Validator()
        self.data = data
        self.schema = self.__class__.schema

    def validate(self):
        return self.validator.validate(self.data, self.schema)

    def errors(self):
        return self.validator.errors
