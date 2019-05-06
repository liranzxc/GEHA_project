from flask import Flask,render_template,request,session,flash,redirect,url_for
from MySqlacademy import FetchType,ConstDic,MySqlHandlerAcademy
from setting import Setting
import time
from Queries import *
app = Flask(__name__)
app.secret_key = 'lee'


## Chart
@app.route("/chart")
def chart():
    UserInformation = session.pop('userdata', None)
    session["userdata"] = list(UserInformation) ## save user information between pages

    results = GetScoreUserFromDatabase(UserInformation[0]) ## to do check None
    if(results == None):
        return render_template('chart.html', values=[], labels=[],userdata=UserInformation,MessgeError="יש למלא שאלון מצב אישי על מנת לצפות בגרף")
    else:
        Dates,Scores = zip(*results)

        lastDate,lastScore = Dates[-1],Scores[-1]
        
        if(len(Scores) > 2):
            last2Score = Scores[-2]
            good = -1
            if(lastScore > last2Score):
                good =1
            else:
                good = 0
            return render_template('chart.html', values=Scores, labels=Dates,userdata=UserInformation,LastDate=lastDate,lastScore=lastScore,Message=good)
        else:
            return render_template('chart.html', values=Scores, labels=Dates,userdata=UserInformation,LastDate=lastDate,lastScore=lastScore,Message=None)



@app.route("/chat")
def chat():
    UserInformation = session.pop('userdata', None)
    session["userdata"] = list(UserInformation) ## save user information between pages
	
    return render_template('chatPage.html', userdata=UserInformation)
 

## interview section 
@app.route("/interview",methods=["GET","POST"])
def interview():

    UserInformation = session.pop('userdata', None)
    session["userdata"] = list(UserInformation) ## save user information between pages
        
    if request.method == 'POST':

        try:
            How_I_feel = (request.form["feel"])
            How_I_Sleep = (request.form["sleep"]) 
            Do_I_Feel_depressed = (request.form["depress"]) 
            Do_I_Feel_anxiety = (request.form["anxiety"]) 
            Do_I_Feel_Fear = (request.form["fear"])
            Have_appetite = (request.form["appetite"])
            myscore = eval(How_I_feel) * 0.3 + eval(How_I_Sleep) * 0.05 + eval(Do_I_Feel_depressed)*0.2 + eval(Do_I_Feel_anxiety) * 0.2 + eval(Do_I_Feel_Fear) * 0.2 + eval(Have_appetite) *0.05
            

            SaveScoreToDatabase(How_I_feel,How_I_Sleep,Do_I_Feel_depressed,Do_I_Feel_anxiety,
            Do_I_Feel_Fear,Have_appetite,myscore)

            return redirect(url_for('chart'))
            #return render_template("home.html",userdata=UserInformation)
        except:
                return render_template("contact.html",userdata=UserInformation,ErrorMessage="יש לענות על כל השאלות")

      
    else:
         return render_template("contact.html",userdata=UserInformation)


##  Home page login
@app.route("/home",methods=["GET"])
def home():
    UserInformation = session.pop('userdata', None)
    if(not UserInformation):
        return render_template("index.html")
    else:
        session["userdata"] = list(UserInformation) ## save user information between pages
        return render_template("home.html",userdata=UserInformation)


## login  page    
@app.route("/",methods=["GET","POST"])
def login():
    if request.method == 'POST':
        # login
        usernameid = request.form["inputID"]
        password = request.form["inputPassword"]

        User_exist , UserInformation = valid_login(usernameid,password)

        print(UserInformation)
       

        if User_exist: 
            # user exist 
            session["userdata"] = list(UserInformation) ## save user information between pages
            return render_template("home.html",userdata=UserInformation)
        else:
            return render_template("index.html",unvalid="סיסמא אינה נכונה")
        
    else:
        return render_template("index.html")



@app.route("/chatbot" ,methods =["POST"])
def chatbot():
    dataComing = request.form["data"]
    UserInformation = session.pop('userdata', None)
    session["userdata"] = list(UserInformation) ## save user information between pages
    return Parser(dataComing,UserInformation)


if __name__ == '__main__':
    app.run(debug=True)