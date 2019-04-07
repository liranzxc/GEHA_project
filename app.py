from flask import Flask,render_template,request,session
from MySqlacademy import FetchType,ConstDic,MySqlHandlerAcademy
from setting import Setting
import time

app = Flask(__name__)
app.secret_key = 'lee'


_setting = Setting()
db = MySqlHandlerAcademy(_setting.setting["host"],_setting.setting["username"],_setting.setting["password"],_setting.setting["database"])


def SaveScoreToDatabase(How_I_feel,How_I_Sleep,Do_I_Feel_depressed,Do_I_Feel_anxiety,
        Do_I_Feel_Fear,Have_appetite,myscore):

    UserInformation = session.pop('userdata', None)
    session["userdata"] = list(UserInformation) ## save user information between pages

    _User_ID = UserInformation[0] # User id
    _Date = int(time.time())


    db.Insert("Personal_Feedback",How_I_feel,How_I_Sleep ## insert on cloud 
    ,Do_I_Feel_depressed,Do_I_Feel_anxiety,Do_I_Feel_Fear,Have_appetite,myscore,_Date,_User_ID)








    


def valid_login(usernameid,password):

    MyQueryDic = {
    ConstDic.TABLENAME : "Patient",
    ConstDic.SELECTED : [],
    ConstDic.FILTER : {

            "User_ID" :usernameid ,
            "Password" : password
            
    },
    ConstDic.TYPEFETCH : FetchType.FETCH_ONE
    }

    result = db.Select(MyQueryDic)

    if(result == None):
        return False,None
    else:
        return True,result

## Chart
@app.route("/chart")
def chart():
    UserInformation = session.pop('userdata', None)
    session["userdata"] = list(UserInformation) ## save user information between pages

    #values , labels = zip(*generateChart())
    labels = ["January","test1","test2","March","April","May","June","July","August"]
    values = [1,2,3,4,5,6,100,8,9,10,11]
    #labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun" ]
    #values = ['Day off', 'Day off', 'Work day', 'Day off', 'Work day', 'Day off', 'Work day']
        
    return render_template('chart.html', values=values, labels=labels,userdata=UserInformation)





@app.route("/chat")
def chat():
    return "chat page"



## interview section 
@app.route("/interview",methods=["GET","POST"])
def interview():
    if request.method == 'POST':
        How_I_feel = (request.form["feel"])
        How_I_Sleep = (request.form["sleep"]) 
        Do_I_Feel_depressed = (request.form["depress"]) 
        Do_I_Feel_anxiety = (request.form["anxiety"]) 
        Do_I_Feel_Fear = (request.form["fear"])
        Have_appetite = (request.form["appetite"])
        myscore = eval(How_I_feel) * 0.3 + eval(How_I_Sleep) * 0.05 + eval(Do_I_Feel_depressed)*0.2 + eval(Do_I_Feel_anxiety) * 0.2 + eval(Do_I_Feel_Fear) * 0.2 + eval(Have_appetite) *0.05
        

        SaveScoreToDatabase(How_I_feel,How_I_Sleep,Do_I_Feel_depressed,Do_I_Feel_anxiety,
        Do_I_Feel_Fear,Have_appetite,myscore)

        return "Good"
        
      
    else:
        UserInformation = session.pop('userdata', None)
        session["userdata"] = list(UserInformation) ## save user information between pages
        return render_template("contact.html",userdata=UserInformation)


##  Home page login
@app.route("/home",methods=["GET"])
def home():
    UserInformation = session.pop('userdata', None)
    session["userdata"] = list(UserInformation) ## save user information between pages
    return render_template("home.html",userdata=UserInformation)


##  Home page login
@app.route("/",methods=["GET","POST"])
def login():
    if request.method == 'POST':
        # login
        usernameid = request.form["inputID"]
        password = request.form["inputPassword"]

        User_exist , UserInformation = valid_login(usernameid,password)

       
        session["userdata"] = list(UserInformation) ## save user information between pages

        if User_exist: 
            # user exist 
            return render_template("home.html",userdata=UserInformation)
        else:
            return render_template("index.html")
        
    else:
        return render_template("index.html")



if __name__ == '__main__':
    app.run(debug=True)