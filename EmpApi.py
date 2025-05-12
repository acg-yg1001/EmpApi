from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId


# Initialize Flask app
app = Flask(__name__)
# MongoDB connection
client = MongoClient("mongodb+srv://Yashwanth:Yashwanth2002@cluster0.f1w0d4e.mongodb.net/")
db = client["0ffice_collection"]  # Database name
# Collections
Edetials_col = db["employee_details"]
Esalary_col = db["employee_salary"]
# To check if the collections are empty and insert initial data and to create collections
if Edetials_col.count_documents({}) == 0:
    Emp_data = [
        {"Eid": 111 , "Name": "Saiprashanth",  "Age": 25 , "Role":"Frontend Developer"},
        {"Eid": 222 , "Name":"Yashwanth" ,     "Age": 26 , "Role":"Fullstack Developer"},
        {"Eid": 333 , "Name":"Madhu" ,         "Age": 24 , "Role":"Backend Developer"},
        {"Eid": 444 ,  "Name":"Chandu" ,       "Age": 28 , "Role":"Frontend Developer"},
        {"Eid": 555 ,  "Name":"Tharun" ,       "Age": 30 , "Role":"Fullstack Developer"},
        {"Eid": 666 , "Name":"Ganesh" ,        "Age": 29 , "Role":"Tester"},
        {"Eid": 777 , "Name":"Srujan" ,        "Age": 27 , "Role":"Backend Developer"},
        {"Eid": 888 , "Name":"Mani" ,          "Age": 24 , "Role":"Frontend Developer"},
        {"Eid": 999 , "Name":"ramu " ,         "Age": 30 , "Role":"Backend Developer"},
        {"Eid": 1000, "Name":"charan" ,        "Age": 23 , "Role":"Tester"},
    ]
    Edetials_col.insert_many(Emp_data)
# To check if the collection is empty and insert initial data and to create collections
if Esalary_col.count_documents({}) == 0:
    Emps_data = [
        {"Eid": 111,"Salary":20000 }, {"Eid": 222,"Salary":25000 }, {"Eid": 333,"Salary":23000 },
        {"Eid": 444,"Salary":2000}, {"Eid": 555,"Salary": 25000}, {"Eid": 666,"Salary":18000 },
        {"Eid":777,"Salary":23000 }, {"Eid": 888,"Salary":2000}, {"Eid": 999,"Salary":23000},{"Eid": 1000,"Salary":18000}
    ]
    Esalary_col.insert_many(Emps_data)

# ------------------- Employee Detials API -----------------------
@app.route('/employee_details/read', methods=['GET'])
def get_all_Employees():
    Employee= list(Edetials_col.find())
    return dumps(Employee), 200
#----------------------------------------------------------------------------------------------------------------
@app.route('/employee_details/read/<int:Employee_Eid>', methods=['GET'])
def get_Employees_by_Eid(Employee_Eid):
    Employee = Edetials_col.find_one({"Eid":Employee_Eid })
    return (dumps(Employee), 200) if Employee else (jsonify({"error": "Employee not found"}), 404)
#------------------------------------------------------------------------------------------------------------------
@app.route('/employee_details/create', methods=['POST'])
def create_employee():
    data = request.get_json()
    if not data or not all(key in data for key in ["Eid", "Name", "Age", "Role"]):
        return jsonify({"error": "Invalid data format"}), 400

    if Edetials_col.find_one({"Eid": data["Eid"]}):
        return jsonify({"error": "Employee ID already exists"}), 400

    Edetials_col.insert_one(data)
    return jsonify({"message": "Employee added successfully"}), 201

#--------------------------------------------------------------------------------------------------

@app.route('/employee_details/update/<int:Employee_Eid>', methods=['PUT'])
def update_employee(Employee_Eid):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data format"}), 400

    updated_data = {"$set": data}
    result = Edetials_col.update_one({"Eid": Employee_Eid}, updated_data)

    if result.modified_count == 0:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify({"message": "Employee updated successfully"}), 200
#--------------------------------------------------------------------------------------------------
@app.route('/employee_details/delete/<int:Employee_Eid>', methods=['DELETE'])
def delete_employee(Employee_Eid):
    result = Edetials_col.delete_one({"Eid": Employee_Eid})

    if result.deleted_count == 0:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify({"message": "Employee deleted successfully"}), 200

#-------------------------Employee Salary Api---------------------------------------------

@app.route('/employee_salary/read', methods=['GET'])
def get_all_salaries():
    salaries = list(Esalary_col.find())
    return dumps(salaries), 200
#--------------------------------------------------------------------------------------------------------------------

@app.route('/employee_salary/read/<int:Employee_Eid>', methods=['GET'])
def get_salary_by_eid(Employee_Eid):
    salary = Esalary_col.find_one({"Eid": Employee_Eid})
    return (dumps(salary), 200) if salary else (jsonify({"error": "Salary record not found"}), 404)
#----------------------------------------------------------------------------------------------------------------------

@app.route('/employee_salary/update/<int:Employee_Eid>', methods=['PUT'])
def update_salary(Employee_Eid):
    data = request.get_json()
    if not data or "Salary" not in data:
        return jsonify({"error": "Invalid data format"}), 400

    result = Esalary_col.update_one({"Eid": Employee_Eid}, {"$set": {"Salary": data["Salary"]}})

    if result.modified_count == 0:
        return jsonify({"error": "Salary record not found"}), 404
    return jsonify({"message": "Salary updated successfully"}), 200
#---------------------------------------------------------------------------------------------------------------------
@app.route('/employee_salary/create', methods=['POST'])
def create_salary():
    data = request.get_json()
    if not data or not all(key in data for key in ["Eid", "Salary"]):
        return jsonify({"error": "Invalid data format"}), 400

    if Esalary_col.find_one({"Eid": data["Eid"]}):
        return jsonify({"error": "Salary record for this Employee ID already exists"}), 400

    Esalary_col.insert_one(data)
    return jsonify({"message": "Salary record added successfully"}), 201
#-------------------------------------------------------------------------------------------------------------------
@app.route('/employee_salary/delete/<int:Employee_Eid>', methods=['DELETE'])
def delete_salary(Employee_Eid):
    result = Esalary_col.delete_one({"Eid": Employee_Eid})

    if result.deleted_count == 0:
        return jsonify({"error": "Salary record not found"}), 404

    return jsonify({"message": "Salary record deleted successfully"}), 200

#-------------------------Employee Details and Emplyee Salary full Api------------------------------------------

@app.route('/employee/full_details/<int:Employee_Eid>', methods=['GET'])
def get_full_employee_details(Employee_Eid):
    employee = Edetials_col.find_one({"Eid": Employee_Eid})
    salary = Esalary_col.find_one({"Eid": Employee_Eid})

    if not employee:
        return jsonify({"error": "Employee not found"}), 404
    if not salary:
        return jsonify({"error": "Salary record not found"}), 404

    full_details = {
        "Eid": employee["Eid"],
        "Name": employee["Name"],
        "Age": employee["Age"],
        "Role": employee["Role"],
        "Salary": salary["Salary"]
    }

    return jsonify(full_details), 200
#------------------------------------------------------------------------------------------------------------------------
@app.route('/employee/full_details', methods=['GET'])
def get_all_full_employees():
    employees = list(Edetials_col.find())
    salaries = list(Esalary_col.find())

    # Convert salaries to a dictionary for easy lookup
    salary_dict = {entry["Eid"]: entry["Salary"] for entry in salaries}

    full_employee_list = []
    for emp in employees:
        emp_details = {
            "Eid": emp["Eid"],
            "Name": emp["Name"],
            "Age": emp["Age"],
            "Role": emp["Role"],
            "Salary": salary_dict.get(emp["Eid"], "Salary not found")
        }
        full_employee_list.append(emp_details)

    return jsonify(full_employee_list), 200
#---------------------------------------------------------------------------------------------------------------------
@app.route('/employee/full_details/name/<string:Employee_Name>', methods=['GET'])
def get_full_employee_details_by_name(Employee_Name):
    employee = Edetials_col.find_one({"Name": Employee_Name})
    salary = Esalary_col.find_one({"Eid": employee["Eid"]}) if employee else None

    if not employee:
        return jsonify({"error": "Employee not found"}), 404
    if not salary:
        return jsonify({"error": "Salary record not found"}), 404

    full_details = {
        "Eid": employee["Eid"],
        "Name": employee["Name"],
        "Age": employee["Age"],
        "Role": employee["Role"],
        "Salary": salary["Salary"]
    }

    return jsonify(full_details), 200
#----------------------------------------------------------------------------------------------------------------------
@app.route('/employee/full_details/names', methods=['GET'])
def get_full_employee_details_by_names():
    names = request.args.getlist("name")  # Get a list of names from query parameters
    employees = list(Edetials_col.find({"Name": {"$in": names}}))

    if not employees:
        return jsonify({"error": "No matching employees found"}), 404

    salaries = list(Esalary_col.find({"Eid": {"$in": [emp["Eid"] for emp in employees]}}))
    salary_dict = {entry["Eid"]: entry["Salary"] for entry in salaries}

    full_employee_list = []
    for emp in employees:
        emp_details = {
            "Eid": emp["Eid"],
            "Name": emp["Name"],
            "Age": emp["Age"],
            "Role": emp["Role"],
            "Salary": salary_dict.get(emp["Eid"], "Salary not found")
        }
        full_employee_list.append(emp_details)

    return jsonify(full_employee_list), 200
#---------------------------------------------------------------------------------------------------------------------
@app.route('/employee/delete/<int:Employee_Eid>', methods=['DELETE'])
def delete_employee_and_salary(Employee_Eid):
    employee_result = Edetials_col.delete_one({"Eid": Employee_Eid})
    salary_result = Esalary_col.delete_one({"Eid": Employee_Eid})

    if employee_result.deleted_count == 0 and salary_result.deleted_count == 0:
        return jsonify({"error": "Employee and salary record not found"}), 404
    elif employee_result.deleted_count == 0:
        return jsonify({"error": "Employee details not found, but salary deleted"}), 404
    elif salary_result.deleted_count == 0:
        return jsonify({"error": "Salary record not found, but employee details deleted"}), 404

    return jsonify({"message": "Employee details and salary deleted successfully"}), 200
#---------------------------------------------------------------------------------------------------------------------
@app.route('/employee/search', methods=['GET'])
def search_employee():
    query = {}
    
    # Extract query parameters (if provided)
    if 'Eid' in request.args:
        query["Eid"] = int(request.args["Eid"])
    if 'Name' in request.args:
        query["Name"] = request.args["Name"]
    if 'Age' in request.args:
        query["Age"] = int(request.args["Age"])
    if 'Role' in request.args:
        query["Role"] = request.args["Role"]
    if 'Salary' in request.args:
        salary_query = list(Esalary_col.find({"Salary": int(request.args["Salary"])}))
        salary_eids = [entry["Eid"] for entry in salary_query]
        query["Eid"] = {"$in": salary_eids}  # Find employees matching the given salary

    employees = list(Edetials_col.find(query))
    
    if not employees:
        return jsonify({"error": "No matching employees found"}), 404

    salaries = list(Esalary_col.find({"Eid": {"$in": [emp["Eid"] for emp in employees]}}))
    salary_dict = {entry["Eid"]: entry["Salary"] for entry in salaries}

    full_employee_list = []
    for emp in employees:
        emp_details = {
            "Eid": emp["Eid"],
            "Name": emp["Name"],
            "Age": emp["Age"],
            "Role": emp["Role"],
            "Salary": salary_dict.get(emp["Eid"], "Salary not found")
        }
        full_employee_list.append(emp_details)

    return jsonify(full_employee_list), 200
#----------------------------------------------------------------------------------------------------------------
@app.route('/employee/list_by_salary/<int:Salary>', methods=['GET'])
def list_employees_by_salary(Salary):
    employees = list(Edetials_col.find({"Eid": {"$in": [entry["Eid"] for entry in Esalary_col.find({"Salary": Salary})]}}))

    if not employees:
        return jsonify({"error": "No employees found with this salary"}), 404

    employee_list = [{"Eid": emp["Eid"], "Name": emp["Name"], "Role": emp["Role"]} for emp in employees]

    return jsonify({"Salary": Salary, "Employee Count": len(employees), "Employees": employee_list}), 200

#----------------------------------------------------------------------------------------------------------------------
#Run Flask
if __name__ == '__main__':
    app.run(debug=True, port=5000)




