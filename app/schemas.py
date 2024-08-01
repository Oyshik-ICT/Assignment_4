from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Str()
    role = fields.Str()  # UserRole Enum as string
    create_date = fields.DateTime()
    update_date = fields.DateTime()
    active = fields.Bool()

user_schema = UserSchema()  # Single user schema instance
users_schema = UserSchema(many=True)  # Multiple users schema instance
