from flask import Flask, jsonify, request, abort
app = Flask(__name__)

empDB=[
 {
 'id':'1',
 'name':'amin',
 'title':'Technical Leader'
 },
 {
 'id':'2',
 'name':'Elyess',
 'title':'Sr Software Engineer'
 },
  {
 'id': '3',
 'name':'abbes',
 'title':'jaune'
 }
 ]

@app.route("/")
def hello():
    return  "Hello world !"

@app.route('/empdb/employee',methods=['GET'])
def getAllEmp():
    return jsonify({'emps':empDB})

@app.route("/empdb/employee/<empId>", methods=["GET"])
def getEmp(empId):
    usr = [ emp for emp in empDB if (emp['id'] == empId) ]
    if not len(usr):
        abort(404)
    return jsonify({'emp':usr})

@app.route('/empdb/employee/<int:empId>',methods=['PUT'])
def updateEmp(empId): 
    em = [ emp for emp in empDB if (emp['id'] == empId) ]
    if "name" in request.json: 
        em[0]['name'] = request.json['name'] 
    if 'title' in request.json:
        em[0]['title'] = request.json['title']
    return jsonify({'emp':em[0]})

@app.route('/empdb/employee',methods=['POST'])
def createEmp(): 
    data = {
        'id':request.json['id'],
        'name':request.json['name'],
        'title':request.json['title']
    }
    empDB.append(data)
    return jsonify(data)

@app.route('/empdb/employee/<string:empId>',methods=['DELETE'])
def deleteEmp(empId): 
    em = [ emp for emp in empDB if (emp['id'] == empId) ] 
    if len(em) == 0:
        abort(404)
    empDB.remove(em[0])
    return jsonify({'response':'Success'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
