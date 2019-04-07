from flask import Flask,render_template,request

app = Flask(__name__)

# class User:
#     def __init__(self):
#         self.name = "לירן"
#         self.age = 13
    


def valid_login(usernameid,password):
    if usernameid == "liran":
        return True,"לירן"
    else:
        return False,None


## Chart
@app.route("/chart")
def chart():
    #values , labels = zip(*generateChart())
    labels = ["January","test1","test2","March","April","May","June","July","August"]
    values = [1,2,3,4,5,6,7,8,9,10,11]
    #labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun" ]
    #values = ['Day off', 'Day off', 'Work day', 'Day off', 'Work day', 'Day off', 'Work day']
        
    return render_template('chart.html', values=values, labels=labels)





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
        print(type(Have_appetite))
        myscore = eval(How_I_feel) * 0.3 + eval(How_I_Sleep) * 0.05 + eval(Do_I_Feel_depressed)*0.2 + eval(Do_I_Feel_anxiety) * 0.2 + eval(Do_I_Feel_Fear) * 0.2 + eval(Have_appetite) *0.05
        
        print(myscore)
        return "Good"
    else:
        return render_template("contact.html")



##  Home page login
@app.route("/",methods=["GET","POST"])
def login():
    if request.method == 'POST':
        # login
        usernameid = request.form["inputID"]
        password = request.form["inputPassword"]

        User_exist,UserInformation = valid_login(usernameid,password)

        if User_exist: 
            # user exist 
            return render_template("home.html",userdata=UserInformation)
        else:
            return render_template("index.html")
        
    else:
        return render_template("index.html")







if __name__ == '__main__':
    app.run(debug=True)