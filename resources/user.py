from flask_restful import Resource,reqparse
from flask import jsonify

import pymysql
parser = reqparse.RequestParser()
parser.add_argument('name')
parser.add_argument('gender')
parser.add_argument('birth')
parser.add_argument('nate')

class User(Resource): 
    def db_init(self):
        db = pymysql.connect("localhost","root","123456","api")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db,cursor
    def get(self,userid):
        db, cursor = self.db_init()
        sql = "SELECT * FROM api.users  WHERE  `id`={}""".format(userid)
        cursor.execute(sql)
        db.commit()
        user=cursor.fetchone()
        db.close()
        return jsonify({'data':user})
    def delete(self,userid):
        db, cursor = self.db_init()
        sql = """
            UPDATE `api`.`users` SET deleted = 1 WHERE  `id`={}""".format(userid)
        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'Success'
        except:
            response['msg'] = 'Failed'
        db.commit()
        db.close() 
        return jsonify(response)
        
class Users(Resource): 
    def db_init(self):
        db = pymysql.connect("localhost","root","123456","api")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db,cursor
    def get(self):
        db, cursor = self.db_init()
        sql = "SELECT * FROM api.users"
        cursor.execute(sql)
        db.commit()
        users=cursor.fetchall()
        db.close()
        return jsonify({'data':users})
    def delete(self,userid):
        db,cursor = self.db_init()
        sql = "DELETE FROM api.users WHERE id={}",format(userid)
        print(sql)
        response = {}
        try:
            cursor.execute(sql)
            db.commit()
            response['msg'] = "Success"
        except:
            response['msg'] = "Failed"

        return jsonify(response)       


    def post(self):
        db, cursor = self.db_init()
        arg = parser.parse_args()
        user = {
            'name': arg['name'],
            'gender': arg['gender'],
            'birth': arg['birth'],
            'note': arg['note '],
        }
        sql = """
        INSERT INTO `api`.`users` (`name`, `gender`, `birth`, `note`)
        VALUES ('{}', '{}', '{}', '{}');
        """.format(user['name'],user['gender'],user['birth'],user['note'])

        response = {}
        try:
            cursor.execute(sql)
            response['msg'] = 'Success'
        except:
            response['msg'] = 'Failed'
        db.commit()
        db.close() 
        return jsonify(response)