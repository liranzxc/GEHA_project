from flask import Flask,render_template,request,session,flash,redirect,url_for
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
    

def ConvertToDateString(item : "tuple (Date,Score)"):
    unix_date = item[0]
    score = item[1]
    local_time = time.localtime(unix_date)
    local_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time) 

    return (local_time,score)


def GetScoreUserFromDatabase(user_id : "User id for get points"):
    PointQuery = {

    ConstDic.TABLENAME : "Personal_Feedback",

    ConstDic.SELECTED : ["Date","Score"],

    ConstDic.FILTER : {

            "User_ID" :user_id
    },

    ConstDic.TYPEFETCH : FetchType.FETCH_ALL

    }

    result = db.Select(PointQuery)


    if(result):
       sorted(result, key = lambda x: x[0]) 

       result = list(map(ConvertToDateString ,result)) # map list >> each item do func
       return result
       #result = [ (1554643647, 100) , (1554643704, 40)   ]
    else:
        return None


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


##  Home page login
@app.route("/",methods=["GET","POST"])
def login():
    if request.method == 'POST':
        # login
        usernameid = request.form["inputID"]
        password = request.form["inputPassword"]

        User_exist , UserInformation = valid_login(usernameid,password)

        print(UserInformation)
       
        session["userdata"] = list(UserInformation) ## save user information between pages

        if User_exist: 
            # user exist 
            return render_template("home.html",userdata=UserInformation)
        else:
            return render_template("index.html")
        
    else:
        return render_template("index.html")

def GetMediceneFromTable(medicineId : "Medicine_id",selectedList : list):
    MedicQuery = {
    ConstDic.TABLENAME : "Medicine",

    ConstDic.SELECTED : selectedList,

    ConstDic.FILTER : {

            "Medicine_ID" :medicineId
    },

    ConstDic.TYPEFETCH : FetchType.FETCH_ONE

    }

    result = db.Select(MedicQuery)

    return result




def GetIDMedication(UserInformation):
   
    User_id = UserInformation[0]

    MedicUseQuery = {

    ConstDic.TABLENAME : "Medicine_Use",

    ConstDic.SELECTED : ["Medicine_ID"],

    ConstDic.FILTER : {

            "User_ID" :User_id
    },

    ConstDic.TYPEFETCH : FetchType.FETCH_ALL

    }

    result_FromMedicine_User = db.Select(MedicUseQuery)

    return result_FromMedicine_User


def GetDiagnosisNameWithDesc(UserInformation):
    
    User_id = UserInformation[0]
    ## get user id from cookies

    ## step 1 , get diagnosis id from patient table
    DiagnosisQuery = {

    ConstDic.TABLENAME : "Patient",

    ConstDic.SELECTED : ["Diagnosis_ID"],

    ConstDic.FILTER : {

            "User_ID" :User_id
    },

    ConstDic.TYPEFETCH : FetchType.FETCH_ONE

    }

    idDiagnosis = db.Select(DiagnosisQuery)


    ## step two , get name and description from diagnosis by id diagnosis

    DiagnosisTableQuery = {

    ConstDic.TABLENAME : "Diagnosis",

    ConstDic.SELECTED : ["Diagnosis_Name","Description"],

    ConstDic.FILTER : {

            "Diagnosis_ID" : idDiagnosis[0]
    },

    ConstDic.TYPEFETCH : FetchType.FETCH_ONE

    }

    result = db.Select(DiagnosisTableQuery)

    return result




def CheckIfKeywordsInSentence(sentence : "data user input",keywords : list):
    return any(key in sentence for key in keywords)
    

def GetMedicationWithDesc(idMedics : list):
    result = []
    for medID in idMedics:
        result.append(GetMediceneFromTable(medID[0],["Medicine_Name","Description","Additional_guidelines"]))
    return result


def GetMedicWithSideEffect(idMeds:list):
    result = []
    for medID in idMeds:
        result.append(GetMediceneFromTable(medID[0],["Medicine_Name","Side_Effects"]))
    return result

def GetMedicWithDosage(UserInformation):
   
    User_id = UserInformation[0]

    MedicUseQuery = {

    ConstDic.TABLENAME : "Medicine_Use",

    ConstDic.SELECTED : ["Dosage","Number_of_dose","Type of taking"],

    ConstDic.FILTER : {

            "User_ID" :User_id
    },

    ConstDic.TYPEFETCH : FetchType.FETCH_ALL

    }

    dosageInformationFromDB = db.Select(MedicUseQuery)

    return dosageInformationFromDB


def DepartmentDesc(UserInformation):
   
    User_id = UserInformation[0]
    ## get user id from cookies

    ## step 1 , 
    DepartmentDescQuery = {

    ConstDic.TABLENAME : "Patient",

    ConstDic.SELECTED : ["Department_Name"],

    ConstDic.FILTER : {

            "User_ID" :User_id
    },

    ConstDic.TYPEFETCH : FetchType.FETCH_ONE

    }

    id_department = db.Select(DepartmentDescQuery)


    ## step two , get name department 

    departmentNameAndTypeQuery = {

    ConstDic.TABLENAME : "Department",

    ConstDic.SELECTED : ["Department_Name","Department_Type"],

    ConstDic.FILTER : {

            "Department_Name" : id_department[0]
    },

    ConstDic.TYPEFETCH : FetchType.FETCH_ONE

    }

    result = db.Select(departmentNameAndTypeQuery)

    return result

def rightsUrl():
    return '<a href="https://hospitals.clalit.co.il/geha/he/patient/Pages/rights.aspx">Right Page </a>'

def DefaultMessage():
    return """ I can not help you in this field. I can help you in the following fields: medication, diagnosis, department, hospitalization type, personal care and rights"""


def Parser(dataComing : "input from user",UserInformation : list):
    dataComing = dataComing.lower()

    mykeywordsDic = {

        "med" : {

            "keywords" : ["pill","medication", "medicines","drug","drugs","תרופה"],
            "sideeffects" : ["side effects","side effect"],
            "dosage" : ["dosage"]
        },
        "diagnosis" : {
            "keywords" : ["diagnosis", "prognosis", "diagnosis"]
        },
        "hospitalization" : {
                "keywords" : ["hospitalization"]

        },
        "therapist" : {
             "keywords" : ["therapist", "personal therapist"]
        },
        "department" : {
            "keywords" : ["class", "department"]
        },
        "rights" : {
            "keywords" : ["rights", "privilege"]
        }
    }

    if(CheckIfKeywordsInSentence(dataComing,mykeywordsDic["med"]["keywords"])):
        idMeds = GetIDMedication(UserInformation)

        if(CheckIfKeywordsInSentence(dataComing,mykeywordsDic["med"]["sideeffects"])):
            return GetMedicWithSideEffect(idMeds)
            # return name + side effect
        elif(CheckIfKeywordsInSentence(dataComing,mykeywordsDic["med"]["dosage"])):
            dosageInformation =  GetMedicWithDosage(UserInformation)
            namesMedic = list(zip(*GetMedicationWithDesc(idMeds)))[0]
            mytext = ""
            for name,information in zip(namesMedic,dosageInformation):
                mytext += "<strong> Medication name : </strong>" + name + "<strong>  Dosage : </strong> "+ \
                information[0] + "," + information[1]+" <strong> Type of taking :   </strong> "+ information[2]


            return mytext
            # return name + dosage
        else:
            listofTuples = GetMedicationWithDesc(idMeds)
            mytextparser = str(list(map(lambda item : "<strong> Medication name : </strong>  " + item[0] + "<strong> Description: </strong> " + item[1] +" <strong> Addication guildline: </strong> " +item[2] ,listofTuples)))
            mytextparser = mytextparser[2:-2]
            mytextparser = mytextparser.replace("\r","")
            mytextparser = mytextparser.replace("\n","")
            mytextparser = mytextparser.replace("\r\n","")

            print(mytextparser)
            return mytextparser

    elif(CheckIfKeywordsInSentence(dataComing,mykeywordsDic["diagnosis"]["keywords"])):
        return GetDiagnosisNameWithDesc(UserInformation)

    elif(CheckIfKeywordsInSentence(dataComing,mykeywordsDic["hospitalization"]["keywords"])):
        pass # To Do after Or created table
    elif(CheckIfKeywordsInSentence(dataComing,mykeywordsDic["therapist"]["keywords"])):
        return TherapistDesc(UserInformation)

    elif(CheckIfKeywordsInSentence(dataComing,mykeywordsDic["department"]["keywords"])):
        return DepartmentDesc(UserInformation)

    elif(CheckIfKeywordsInSentence(dataComing,mykeywordsDic["rights"]["keywords"])):
        return rightsUrl()
    else :
        return DefaultMessage()
        
    

    

def TherapistDesc(UserInformation):
  
    User_id = UserInformation[0]
    ## get user id from cookies

    ## step 1 , get personal thrapist id from patient table
    DiagnosisQuery = {

    ConstDic.TABLENAME : "Patient",

    ConstDic.SELECTED : ["Personal_therapist"],

    ConstDic.FILTER : {

            "User_ID" :User_id
    },

    ConstDic.TYPEFETCH : FetchType.FETCH_ONE

    }

    idthrapist = db.Select(DiagnosisQuery)


    ## step two , get name and description from diagnosis by id diagnosis

    StaffMemberTableQuery = {

    ConstDic.TABLENAME : "Staff_Member",

    ConstDic.SELECTED : ["Staff_Member_Name","Profession"],

    ConstDic.FILTER : {

            "Staff_Member_ID" : idthrapist[0]
    },

    ConstDic.TYPEFETCH : FetchType.FETCH_ONE

    }

    result = db.Select(StaffMemberTableQuery)

    return result





@app.route("/chatbot" ,methods =["POST"])
def chatbot():
    dataComing = request.form["data"]
    UserInformation = session.pop('userdata', None)
    session["userdata"] = list(UserInformation) ## save user information between pages
    return Parser(dataComing,UserInformation)


if __name__ == '__main__':
    app.run(debug=True)