from flask import Flask,render_template,request

app = Flask(__name__)



def valid_login(usernameid,password):
    if usernameid == "liran":
        return True,"לירן"
    else:
        return False,None


@app.route("/chat")
def chat():
    return "chat page"

    
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