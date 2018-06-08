
import pymongo
import bottle

emp_coll = pymongo.MongoClient("localhost", 27017).Employee.emp

@bottle.route("/")
def home():

    employees_in_db_temp = ""

    i = 0
    for emp in emp_coll.find():

        i += 1

        employees_in_db_temp += """
        <tr>
        <td style="padding: 5px; border: 1px solid white;">{}</td>
        <td style="padding: 5px; border: 1px solid white;">{}</td>
        <td style="padding: 5px; border: 1px solid white;">{}</td>
        <td style="padding: 5px; border: 1px solid white;">{}</td>
        </tr>
        """.format(i, emp["EmpNo"], emp["FirstName"], emp["Age"])

    html = open("./views/index.html", "r").read().format(employees_in_db_temp)
    return html

@bottle.route("/emp/<name>")
def empInfo(name=None):
    for emp in emp_coll.find({"FirstName": name}):
        return open("./views/info.html").read().format(emp["FirstName"], emp["Age"], emp["EmpNo"], """
        <form action="/emp/{}" method="POST">
        <input type="submit" value="Delete Employee" />
        </form>
        """.format(name))
    return "<h1>Enter Valid Employee Name</h1>"

@bottle.route("/emp/<name>", method="POST")
def deleteEmp(name=None):
    emp_coll.delete_one({"FirstName": name})
    bottle.redirect("/")

@bottle.route("/emp")
def empError():
    return "<h1>Please Specify Employee Name in Route</h1><p><b>For Example:</b> `<code>/emp/ABC</code>`</p>"

@bottle.route("/new")
def registerPage():
    return open("./views/new.html", "r").read().format("""
    <form action="/new" method="POST">
        <table>
            <tr>
                <td>Name:</td>
                <td><input type="text" name="empName" /></td>
            </tr>
            <tr>
                <td>Age:</td>
                <td><input type="text" name="empAge" /></td>
            </tr>
            <tr>
                <td>Employee Number:</td>
                <td><input type="text" name="empNo" /></td>
            </tr>
        </table>
        <br>
        <input type="submit" value="Register" />
    </form>
    """)

@bottle.route("/new", method="POST")
def registerEmp():
    name = bottle.request.forms.empName
    age = bottle.request.forms.empAge
    empNo = bottle.request.forms.empNo
    emp_coll.insert_one({"FirstName": name, "Age": age, "EmpNo": empNo})
    bottle.redirect("/")

if __name__ == "__main__":
    bottle.run(host="localhost", port="8080")