from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client=MongoClient("mongodb://db:27017")

#db=client.navidb

#UserNum=db["UserNum"]

#UserNum.insert({
#    'num_of_users':0
#    })



db=client.SentencesDatabase
users=db["Users"]


class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        hashed_pw = bcrypt.hashpw(password,bcryt.gensalt())

        users.insert({
            "Username":username,
            "Password":hashed_pw,
            "Sentence":"",
            "Tokens":6
        })

        retJson = {
            "status":200,
            "msg":"Successfully signed up for the API"
        }

        return jsonify(retJson)

class Sentence(Resource):
    def post(self):
        #step1: get the posted data
        postedData=request.get_json()
        #step2: read the data

        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        #step3 verify the username pw match
        correct_pw = verifyPw(username,password)

        if not correct_pw:
            retJson={
                "status":302
            }
            return jsonify(retJson)

        #step4 verify user has enough tokens

        num_tokens = countTokens(username)
        if num_tokens <= 0:
            return jsonify({"status":301})
        #step5 store the sentence and return 200

        users.update({
            "Username":username
        },{
            "$set":{"Sentence":sentence,
                    "Tokens": num_tokens -1}
        })

        return jsonify({
            "status":200,
            "msg":"sentence saved successfully"
        })




class Visit(Resource):
    def get(self):
        user_num  = UserNum.find({})[0]['num_of_users']
        user_num+=1
        UserNum.update({},{"$set":{"num_of_users":user_num}})
        return str("Hello user" + str(user_num))



def checkPostedData(postedData, functionName):
    if (functionName == "add" or functionName == "subtract" or functionName == "multiply"):
        if "x" not in postedData or "y" not in postedData:
            return 301 #Missing parameter
        else:
            return 200
    elif (functionName == "division"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif int(postedData["y"])==0:
            return 302
        else:
            return 200

class Add(Resource):
    def post(self):
        #If I am here, then the resouce Add was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "add")
        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        #If i am here, then status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Add the posted data
        ret = x+y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

class Subtract(Resource):
    def post(self):
        #If I am here, then the resouce Subtract was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "subtract")


        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        #If i am here, then status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Subtract the posted data
        ret = x-y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)


class Multiply(Resource):
    def post(self):
        #If I am here, then the resouce Multiply was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "multiply")


        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        #If i am here, then status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Multiply the posted data
        ret = x*y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

class Divide(Resource):
    def post(self):
        #If I am here, then the resouce Divide was requested using the method POST

        #Step 1: Get posted data:
        postedData = request.get_json()

        #Steb 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, "division")


        if (status_code!=200):
            retJson = {
                "Message": "An error happened",
                "Status Code":status_code
            }
            return jsonify(retJson)

        #If i am here, then status_code == 200
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)

        #Step 2: Multiply the posted data
        ret = (x*1.0)/y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)



api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/division")
api.add_resource(Visit,"/hello")
api.add_resource(Register,"/register")

@app.route('/')
def hello_world():
    return "Hello World!"


if __name__=="__main__":
    app.run(host='0.0.0.0',port='5000',debug=True)
