from flask import Flask, jsonify, request, abort
import pymongo

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["mydatabase"]
mycol = mydb["employees"]



# empDB=[
#  {
#  'id':'1',
#  'name':'amin',
#  'title':'Technical Leader'
#  },
#  {
#  'id':'2',
#  'name':'Elyess',
#  'title':'Sr Software Engineer'
#  },
#   {
#  'id': '3',
#  'name':'abbes',
#  'title':'jaune'
#  }
#  ]
#####################################################
@app.route("/")
def hello():
    return  "Hello world !"
#######################################################
@app.route('/mydatabase/employee',methods=['GET'])
def getAllEmp():
    usr = [ emp for emp in mycol.find({}, {"_id":False})]
    return jsonify({'emps': usr })
############################################################
@app.route("/mydatabase/employee/<int:empId>", methods=["GET"])
def getEmp(empId):
    get_query = {"id": empId}
    usr = [ emp for emp in mycol.find(get_query, {"_id":False})]
    if not len(usr):
        abort(404)
    return jsonify({'emp':usr})
#################################################################
@app.route('/mydatabase/employee/<int:empId>',methods=['PUT'])
def updateEmp(empId): 
    myquery = { "id": empId }
    x = mycol.update_many(myquery, {"$set": request.json})
    # em = [ emp for emp in mycol.find({}, {"_id":False}) if (emp['id'] == empId) ]
    # if "name" in request.json: 
    #     em[0]['name'] = request.json['name'] 
    # if 'title' in request.json:
    #     em[0]['title'] = request.json['title']
    # return jsonify({'emp':em[0]})
    return jsonify({"modified_count": x.modified_count})
##########################################################

@app.route('/mydatabase/employee',methods=['POST'])
def createEmp(): 
    data = {
        'id':request.json['id'],
        'name':request.json['name'],
        'title':request.json['title']
    }

    mycol.insert_one(data)
    del data["_id"]
    return jsonify(data)
#################################################################""""
@app.route('/mydatabase/employee/<int:empId>',methods=['DELETE'])
def deleteEmp(empId): 
    get_query = {"id": empId}
    response = mycol.delete_many(get_query)
    # em = [ emp for emp in empDB if (emp['id'] == empId) ] 
    # if len(em) == 0:
    #     abort(404)
    # empDB.remove(em[0])
    return jsonify({'response': response.deleted_count})


######################################################""
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
