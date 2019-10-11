import numpy as np
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Resource, reqparse, Api
from flask_jwt_extended import  jwt_required, JWTManager, create_access_token

import datetime

db = SQLAlchemy()
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:vivekm@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

jwt = JWTManager(app)

db.init_app(app)

app.app_context().push()

db.Model.metadata.reflect(db.engine)



class Banks(db.Model):
    __table__ = db.Model.metadata.tables['MyData']
    
    @classmethod    
    def branch_details(cls, bank, city, offset_value, limit_value):
        return cls.query.filter_by(bank_name=bank).filter_by(city=city).offset(offset_value).limit(limit_value).all()
    
    @classmethod
    def find_by_ifsc(cls, ifsc):
        return cls.query.filter_by(ifsc=ifsc).all()
    
    def json(self):
        return {'district': self.district, 'address': self.address, 'bank_id': self.bank_id, 'state': self.state, 
                'city': self.city, 'branch': self.branch, 'ifsc': self.ifsc, 'bank_name': self.bank_name}
    
        
        
class IFSC(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('ifsc', type=str, required=True, help='Ifsc of the bank')
    parser.add_argument('offset', type=int, required=False, help='Offset value')
    parser.add_argument('limit', type=int, required=False, help='Limit value')
    @jwt_required
    def get(self):
        ifsc_code = IFSC.parser.parse_args()['ifsc']
        bank_details = Banks.find_by_ifsc(ifsc_code)[0].json()
        return bank_details
    
    
class BRANCH(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('bank_name', type=str, required=True, help='Bank name')
    parser.add_argument('city', type=str, required=True, help='City name')
    parser.add_argument('offset', type=int, required=False, help='Offset value')
    parser.add_argument('limit', type = int, required=False, help='Limit value')
    @jwt_required
    def get(self):
        args = BRANCH.parser.parse_args()
        bank_name = args['bank_name']
        city = args['city']
        offset_value = args['offset']
        limit_value = args['limit']
        branch_list = list(map(lambda x: x.json(), Banks.branch_details(bank_name, city, offset_value, limit_value)))
        return {'Branch_Details': branch_list}
    

class LOGIN(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username is required')
    parser.add_argument('password', type=str, required=True, help='Password is required')
    def post(self):
        args = LOGIN.parser.parse_args()
        username = args['username']
        password = args['password']
        if username != 'test' or password != 'test':
            return {"msg": "Bad username or password"}

        ret = {'access_token': create_access_token(username)}
        return ret



api.add_resource(IFSC, '/branch_ifsc')
api.add_resource(BRANCH, '/branch')
api.add_resource(LOGIN, '/login')

if __name__ == '__main__':
    app.run(debug=True)