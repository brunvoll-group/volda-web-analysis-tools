from flask import Flask
from flask.views import MethodView
from flask_smorest import Api, Blueprint, abort
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['API_TITLE'] = 'My API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.2'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

api = Api(app)

# Define Marshmallow schemas (reusable!)
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)

class UserQueryArgsSchema(Schema):
    limit = fields.Int()
    offset = fields.Int()

# Create a blueprint
blp = Blueprint(
    'users',
    __name__,
    url_prefix='/users',
    description='User operations'
)

@blp.route('/')
class UserList(MethodView):
    @blp.arguments(UserQueryArgsSchema, location='query')
    @blp.response(200, UserSchema(many=True))
    def get(self, args):
        """List users"""
        # Set defaults manually if not provided
        limit = args.get('limit', 10)
        offset = args.get('offset', 0)
        return [{'id': 1, 'name': 'John', 'email': 'john@example.com'}]
    
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        """Create a user"""
        # user_data is validated and deserialized
        user_data['id'] = 1
        return user_data

@blp.route('/<int:user_id>')
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        """Get user by ID"""
        return {'id': user_id, 'name': 'John', 'email': 'john@example.com'}
    
    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def put(self, user_data, user_id):
        """Update a user"""
        user_data['id'] = user_id
        return user_data
    
    @blp.response(204)
    def delete(self, user_id):
        """Delete a user"""
        return ''

api.register_blueprint(blp)

if __name__ == '__main__':
    app.run(debug=True)