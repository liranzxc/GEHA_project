from flask import Flask,render_template,request,session,flash,redirect,url_for
from MySqlacademy import FetchType,ConstDic,MySqlHandlerAcademy
from setting import Setting
import time


"""
Queries file :

all queries on db
setting file contain all information to conaction to db

Parser function - get input user from chat, analysis the input and get the currect information from database by keywords in 
our dict
"""

_setting = Setting()

""" Connection information """
db = MySqlHandlerAcademy(_setting.setting["host"],_setting.setting["username"],_setting.setting["password"],_setting.setting["database"])


def SaveScoreToDatabase(How_I_feel:int,How_I_Sleep:int,Do_I_Feel_depressed:int,Do_I_Feel_anxiety:int,
            Do_I_Feel_Fear:int,Have_appetite:int,myscore:int):
        
        """
                Getting points from user quiz and save to database to Personal_Feedback Table 
        """

        UserInformation = session.pop('userdata', None)
        session["userdata"] = list(UserInformation) ## save user information between pages

        _User_ID = UserInformation[0] # User id
        _Date = int(time.time())


        db.Insert("Personal_Feedback",How_I_feel,How_I_Sleep ## insert on cloud 
        ,Do_I_Feel_depressed,Do_I_Feel_anxiety,Do_I_Feel_Fear,Have_appetite,myscore,_Date,_User_ID)
        

def ConvertToDateString(item : "tuple (Date,Score)"):

    """ Get Data and convert to string time  Unix -> String """ 

    unix_date = item[0]
    score = item[1]
    local_time = time.localtime(unix_date)
    local_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time) 

    return (local_time,score)


def GetScoreUserFromDatabase(user_id : "User id for get points"):
        
        """
        input : id_user 
        getting all points from database ,and sort them by date

         """
         
        
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


def valid_login(usernameid:int ,password : int):

        """ Check if user exist , if Yes , return True and all information of user  """

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

        
def GetMediceneFromTable(medicineId : "Medicine_id",selectedList : list):
        
        """
            get medicine information Selected from dataBase by id medicine
         """
        
        
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




def GetIDMedication(UserInformation : tuple):
    
        """
        getting all medication of one user by his id 

        """
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


def GetDiagnosisNameWithDesc(UserInformation:tuple):
        """" 
        getting one diagnosis of user by his id  , with name and description
        
        """
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
        """ Check If Keywords In Sentence"""

        return any(key in sentence for key in keywords)
        

def GetMedicationWithDesc(idMedics : list):

    """ getting Medication with descriptions by ids medication """
    result = []
    for medID in idMedics:
        result.append(GetMediceneFromTable(medID[0],["Medicine_Name","Description","Additional_guidelines"]))
    return result


def GetMedicWithSideEffect(idMeds:list):
    """ getting Medication with Side effects by ids medication """

    result = []
    for medID in idMeds:
        result.append(GetMediceneFromTable(medID[0],["Medicine_Name","Side_Effects"]))
    return result

def GetMedicWithDosage(UserInformation:tuple):

    """getting Medication with dosage by id user"""
    
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


def DepartmentDesc(UserInformation:tuple):

        """  Getting Department of user with Name and type """
    
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
    """ method return a output string of links of rights  to chat """

    return 'For information about your rights click here: <a href="https://hospitals.clalit.co.il/geha/he/patient/Pages/rights.aspx" target="_blank">Right Page </a>'

def DefaultMessage():
    """ When chatbot didnt recongize any keyword in our dict """
    return """ I can not help you in this field. I can help you in the following fields: medication, diagnosis, department, hospitalization type, personal care and rights"""


def Parser(dataComing : "input from user",UserInformation : list):

        """
        input: sentens of user
        parser method have dict of keywords 
        check if word appeard and execute database methods.

        order information for readable data

        
        """
        dataComing = dataComing.lower()

        mykeywordsDic = {

            "med" : {

                "keywords" : ["pill","medication", "medicines","drug","drugs","medicine","cure","remedy","medicament"],
                "sideeffects" : ["side effects","side effect"],
                "dosage" : ["dosage"]
            },
            "diagnosis" : {
                "keywords" : ["diagnosis", "prognosis", "diagnosis"]
            },
            "therapist" : {
                "keywords" : ["therapist", "personal therapist"]
            },
            "department" : {
                "keywords" : ["class", "department"]
            },
            "rights" : {
                "keywords" : ["rights", "privilege","right"]
            }
        }

        if(CheckIfKeywordsInSentence(dataComing,mykeywordsDic["med"]["keywords"])):
            idMeds = GetIDMedication(UserInformation)

            if(CheckIfKeywordsInSentence(dataComing,mykeywordsDic["med"]["sideeffects"])):
                sideEffectData = GetMedicWithSideEffect(idMeds) # (medicName , sideEffect)
                mytext = "" 
                for MedicName_SideEffect in sideEffectData:
                    mytext +=  "<strong> Medication name : </strong>" + MedicName_SideEffect[0] + \
                        "<strong> Side Effects : </strong>" +  MedicName_SideEffect[1]  + " <br/> &#13;&#10;"
                
                return mytext


                # return name + side effect
            elif(CheckIfKeywordsInSentence(dataComing,mykeywordsDic["med"]["dosage"])):
                dosageInformation =  GetMedicWithDosage(UserInformation)
                namesMedic = list(zip(*GetMedicationWithDesc(idMeds)))[0]
                mytext = ""
                for name,information in zip(namesMedic,dosageInformation):
                    mytext += "<strong> Medication name : </strong>" + name + "<strong>  Dosage : </strong> "+ \
                    information[0] + "," + information[1]+". <strong> Type of taking :   </strong> "+ information[2] + " <br/> &#13;&#10;"

                return mytext
                # return name + dosage
            else: # pill only
                listofTuples = GetMedicationWithDesc(idMeds)
                mytext = ""
                for item in listofTuples:
                    mytext +=  "<strong> Medication name : </strong>  " + item[0] + " <br/> &#13;&#10;" +"<strong> Description: </strong> " + item[1] + " <br/> &#13;&#10;"+"<strong> Addication guildline: </strong> " +item[2] + " <br/> &#13;&#10;"
                
                return mytext

        elif(CheckIfKeywordsInSentence(dataComing,mykeywordsDic["diagnosis"]["keywords"])):
            DiagnosisData =  GetDiagnosisNameWithDesc(UserInformation)
        
            mytext =  "<strong> Diagnosis name : </strong>" + DiagnosisData[0] + \
                "<strong> Description : </strong>" +  DiagnosisData[1]  + " <br/> &#13;&#10;"
            
            mytext +=  " <br/> &#13;&#10;" + "<strong> This diagnosis is not final and may change </strong> ."
            return mytext


    # elif(CheckIfKeywordsInSentence(dataComing,mykeywordsDic["hospitalization"]["keywords"])):
        #    pass # To Do after Or created table
        elif(CheckIfKeywordsInSentence(dataComing,mykeywordsDic["therapist"]["keywords"])):
            therapData =  TherapistDesc(UserInformation)
            mytext =  "<strong> Therapist name : </strong>" + therapData[0] + \
                "<strong> Profession : </strong>" +  therapData[1] + " <br/> &#13;&#10;"

            return mytext
            

        elif(CheckIfKeywordsInSentence(dataComing,mykeywordsDic["department"]["keywords"])):
            DepartData = DepartmentDesc(UserInformation)
            mytext =  "<strong> Department name : </strong>" + DepartData[0] + \
                "<strong> Department type : </strong>" +  DepartData[1]  + " <br/> &#13;&#10;"

            return mytext


        elif(CheckIfKeywordsInSentence(dataComing,mykeywordsDic["rights"]["keywords"])):
            return rightsUrl()
        else :
            return DefaultMessage()
            

def TherapistDesc(UserInformation:tuple):
        """
            getting therapist user by id from database (with name and description)
        
        """
    
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