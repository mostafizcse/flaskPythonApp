
from flask import Flask, render_template,session, request, flash, url_for, redirect
from flask_mysqldb import MySQL
import base64

#from wtforms import Form
from mysqlx import Session

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'testuser'
app.config['MYSQL_PASSWORD'] = 'test123'
app.config['MYSQL_DB'] = 'TESTDB'
mysql = MySQL(app)


#session['username'] = 0

#login
@app.route('/login', methods=['POST'])
def login():
     loginemail = request.form['Loginemail']
     loginpassword = request.form['Loginpassword']

     ###Encoding###
     # string to bytes

     encoding = bytes(loginpassword, encoding='utf-8')
     byte = base64.b64encode(encoding)
     #byte to string
     loginpassword = byte.decode()
     print('encodaed',loginpassword)

     new = (loginemail,loginpassword)
     print('form data',new)
     cur = mysql.connection.cursor()
     cur.execute("SELECT EMAIL,PASSWORD1 FROM user_list")
     data = cur.fetchall()

     for p in data:
         print(p)
         if(p == new):
             print('found',new)
             global session
             session['username'] = p[0]
             session['logged_in'] = True
             print(p[0])
             return redirect('/')
             break
     else:
         message = 'Email and password do not match'
         return render_template('login.html',nmessage=message)


#loginfrom
@app.route('/login_from')
def login_from():
    return render_template('login.html')

#logout
@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('login_from'))

#data show
@app.route('/')
def home():
    user = mysql.connection.cursor()
    user.execute("SELECT EMAIL FROM user_list")
    useremail = user.fetchall()

    curretUser = session.get('username')
    print("curretUser",curretUser)
    print(type(curretUser))

    for users in useremail:
        strUsers = ''.join(users)
        if(curretUser == strUsers):
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM employee")
            rv = cur.fetchall()
            mysql.connection.commit()
            return render_template('list.html', employees=rv)
            break
    else:
        return redirect(url_for('login_from'))


#signup from
@app.route('/signup_form')
def signup_form():
    return render_template('signup.html')


#signup operation
@app.route('/signup',methods=["POST"])
def signup():
    username = request.form['UserName']
    email = request.form['Email1']
    password1 = request.form['PasswordOne']
    password2 = request.form['PasswordTwo']

    #string to bytes using bytes()
    b1 = bytes(password1, encoding='utf-8')
    password1 = base64.b64encode(b1)

    b2 = bytes(password2, encoding='utf-8')
    password2 = base64.b64encode(b2)

    print(password1)
    print(password2)




    if(password1 == password2):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user_list(USER_NAME,EMAIL,PASSWORD1,PASSWORD2)VALUES (%s,%s,%s,%s)",
                    (username, email, password1, password2))
        mysql.connection.commit()
        return redirect(url_for('login_from'))
    else:
        print("Not Match")
        massage = 'first and secound password are not matched'
        return render_template('signup.html',massage=massage)






#add_employ
@app.route('/add_employee')
def add_employee():

    user = mysql.connection.cursor()
    user.execute("SELECT EMAIL FROM user_list")
    useremail = user.fetchall()

    curretUser = session.get('username')
    print("curretUser", curretUser)
    print(type(curretUser))

    for users in useremail:
        strig = ''.join(users)
        if (curretUser == strig):
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM employee")
            rv = cur.fetchall()
            cur.close()
            return render_template('index.html', employees=rv)
            break
    else:
        return redirect(url_for('login_from'))





#data insert
@app.route('/insert',methods=["POST"])
def insert():
    user = mysql.connection.cursor()
    user.execute("SELECT EMAIL FROM user_list")
    useremail = user.fetchall()

    curretUser = session.get('username')
    print("curretUser", curretUser)
    print(type(curretUser))

    for users in useremail:
        strig = ''.join(users)
        if (curretUser == strig):
            first = request.form['FirstName']
            last = request.form['LastName']
            father = request.form['FatherName']
            mother = request.form['MotherName']
            age = request.form['Age']  # int
            sex = request.form['Sex']
            position = request.form['Position']
            email = request.form['EmailAddress']
            phone = request.form['PhoneNumber']
            emr_phn = request.form['emergencyPhoneNumber']
            address1 = request.form['PresentAddress']
            address2 = request.form['PermanentAddress']
            joindate = request.form['joiningDate']
            bank_acc = request.form['BankAccountNumber']
            nid_number = request.form['NIDNumber']
            bank_name = request.form['BankName']
            print(nid_number, bank_name)
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO employee(FIRST_NAME,LAST_NAME,FATHER_NAME,MOTHER_NAME,SEX,POSITION,EMAILL_ADDRESS,PRESENT_ADDRESS,PERMANENT_ADDRESS,AGE,EMERGANCY_PHOONE,PHONE_NUMBER,	JOINING_DATE,ACCOUNT_NUMBER,NID,BANK_NAME)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (first, last, father, mother, sex, position, email, address1, address2, age, phone, emr_phn, joindate,
                 bank_acc, nid_number, bank_name))
            mysql.connection.commit()
            return redirect('/')
            break
    else:
        return redirect(url_for('login_from'))





#update_form
@app.route('/update_form/<string:id_data>',methods=["GET"])
def update_form(id_data):

    #sessinon and login stuff requermant code
    user = mysql.connection.cursor()
    user.execute("SELECT EMAIL FROM user_list")
    useremail = user.fetchall()

    curretUser = session.get('username')
    print("curretUser", curretUser)
    print(type(curretUser))

    for users in useremail:
        strig = ''.join(users)
        if (curretUser == strig):

            #main code
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM employee WHERE ID=%s", (int(id_data),))
            rv = cur.fetchall()
            print(rv)
            cur.close()
            id = int(rv[0][0])
            first = rv[0][1]
            last = rv[0][2]
            father = rv[0][3]
            mother = rv[0][4]
            sex = rv[0][5]
            position = rv[0][6]
            emaill = rv[0][7]
            present = rv[0][8]
            permanent = rv[0][9]
            age = rv[0][10]
            phone = rv[0][11]
            emergancy = rv[0][12]
            date = rv[0][13]
            account = rv[0][14]
            nid = rv[0][15]
            bank = rv[0][16]
            return render_template('update_from.html', nfirst=first, nlast=last, nfather=father, nmother=mother, nposition=position, nemaill=emaill, nphone=phone, nemergancy=emergancy, nage=age, nsex=sex, npresent=present, npermanent=permanent, nid=id, ndate=date,naccount=account, nnid=nid, nbank=bank)
            # //End main code

            break
    else:
        return redirect(url_for('login_from'))




#update
@app.route('/update/',methods=["POST"])
def update():

    #main code start
    id_data = request.form['EmployeeID']
    first = request.form['FirstName']
    last = request.form['LastName']
    father = request.form['FatherName']
    mother = request.form['MotherName']
    age = request.form['Age']  # int
    sex = request.form['Sex']
    position = request.form['Position']
    email = request.form['EmailAddress']
    phone = request.form['PhoneNumber']
    emr_phn = request.form['emergencyPhoneNumber']
    address1 = request.form['PresentAddress']
    address2 = request.form['PermanentAddress']
    joindate = request.form['joiningDate']
    bank_acc = request.form['BankAccountNumber']
    nid_number = request.form['NIDNumber']
    bank_name = request.form['BankName']
    print(nid_number,bank_name)
    cur = mysql.connection.cursor()
    cur.execute("UPDATE employee SET FIRST_NAME=%s, LAST_NAME=%s, FATHER_NAME=%s, MOTHER_NAME=%s, SEX=%s,POSITION=%s, EMAILL_ADDRESS=%s, PRESENT_ADDRESS=%s, PERMANENT_ADDRESS=%s, AGE=%s, EMERGANCY_PHOONE=%s, PHONE_NUMBER=%s, JOINING_DATE=%s, ACCOUNT_NUMBER=%s,NID=%s,BANK_NAME=%s WHERE ID=%s",(first, last, father, mother, sex, position, email, address1, address2, age, phone, emr_phn, joindate, bank_acc,nid_number,bank_name, id_data))
    mysql.connection.commit()
    return redirect('/')
    #End main code



#Delete

@app.route('/delete/<string:id_data>', methods=["GET"])
def delete(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM employee WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect('/')

#host='0.0.0.0', port=80
#debug = True
if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(debug = True)

