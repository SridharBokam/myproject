import sys  
import os
import base64
import shutil
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from datetime import datetime



fmmsg='' 

def sendmail(fmmsg):#, fromaddr, toaddr):
    fromaddr = "hyperion@deltads.ent"
    toaddr = "sbokam@delta.org;JWoodruff@DELTA.ORG;jwoodruff@delta.org;NVankadari@delta.org"
    #toaddr = toaddr + ";EFSHyperionIT@delta.org"
    #toaddr= toaddr + ";jpidatala@delta.org"
    #toaddr= toaddr + ";#FP&AUsers@delta.org"
  
# File handler code below
    fmfn = 'C:\Sridhar Bokam\Python\FMFileName.txt'
    fo1 = open(fmfn, "ab+")
    fo1.truncate(0)
    fo1.write('\n \n' + fmmsg)
    fo1.close()   
#File handler code above

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "HRMS File pre-check status"
    
    body = "This is HRMS file pre-check status mail"
    
    msg.attach(MIMEText(body, 'plain'))
    print("In the sendmail fun() 1")
    filename = "FMFileName.txt" #'C:\Sridhar Bokam\Python\FMFileName.txt'
    attachment = open("C:\Sridhar Bokam\Python\FMFileName.txt", "rb")
    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    
    msg.attach(part)
    print("In the sendmail Fun() 2 :")
    server = smtplib.SMTP('smtprelay.deltapre.ent')
    server.starttls()
    #server.login(fromaddr, "sender mail password")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    print("In the sendmail Fun() 3 :")
    server.quit()


def main():  
    #filepath = 'C:\Sridhar Bokam\Python\HRMS_Precheck.txt'
    fmmsg=''
########################
    filepath = os.path.isfile('C:\Sridhar Bokam\Python\HRMS_Precheck.txt')
        
    if filepath: # check to see if HRMS file exists or not
        filepath = 'C:\Sridhar Bokam\Python\HRMS_Precheck.txt'
#######################
        #scn_month =''
        #scnVar = ''
        with open(filepath) as fp:
        #line = fp.readline() #This line is not required
            for cnt, line in enumerate(fp):
                if cnt >0:
                    cellcnt = 0 # Column Count
                    while cellcnt < 22:
                        fnret = 'YES'
                        step_cellcnt = line.split('\t')
                        step_nxtcell=step_cellcnt [cellcnt]
                        scnVar=''
    
                        if (cellcnt==0): # This is for Scenario columnn validation
                            scn_month = datetime.now().strftime('%B')# This is for capturing Present month from system date
                            scnVar = ScenMonth_Chk(scn_month, scnVar)
                            if (scnVar.strip() == step_nxtcell.strip()):
                                fnret=Scenario_fun(step_nxtcell,fnret)
                                if (fnret == "NO"):
                                    print ("\n The Scenario column is either empty or invalid value: "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                    fmmsg = fmmsg + "\n The Scenario column is either empty or invalid value: "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1) + "\n"
                                    #break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg
                            else:
                                fmmsg = fmmsg + "\n " + scnVar+ " :is expected for loading at this month. But HRMS file has:"+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1)+ "\n"
                            ##break
                        if (cellcnt==1): # This is for Cost Center columnn validation
                            fnret=CostCenter_fun(step_nxtcell,fnret)
                            if (fnret == "NO"):
                                print ("\n Invalid Costcenter column value :"+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg = fmmsg + "\n"+ " Invalid Costcenter column value :"+ step_nxtcell + " at row: "+ str(cnt+1) + " and column: "+ str(cellcnt+1)
                                #break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg
                        if (cellcnt==10): # This is for Band columnn validation
                            fnret=Band_fun(step_nxtcell,fnret)
                            if (fnret == "NO"):
                                print ("\n Invalid Band column value :"+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg = fmmsg + "\n"+ " Invalid/Lengthy Band column value : "+ step_nxtcell + " at row: "+ str(cnt+1) + " and column: "+ str(cellcnt+1)
                                #break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg
                        if (cellcnt==11): # This is for Grade columnn validation
                            #print("step_nxtcell: "+ step_nxtcell)
                            fnret=Grade_fun(step_nxtcell,fnret)
                            if (fnret == "NO"):
                                print ("\n Invalid Grade column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg = fmmsg + "\n"+ " Invalid Grade column value : "+ step_nxtcell + " at row: "+ str(cnt+1) + " and column: "+ str(cellcnt+1)                            
                                #break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg
                        if (cellcnt==4): # This is for Vacant Since columnn validation
                            #print("step_nxtcell-Previous1: "+ step_cellcnt [cellcnt-1])
                            fnret=VacantSince_fun(step_cellcnt [cellcnt-1],step_nxtcell,fnret)
                            if (fnret == "NO"):
                                print ("\n Invalid VacantSince column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg = fmmsg + "\n"+ " Invalid VacantSince column value : "+ step_nxtcell + " at row: "+ str(cnt+1) + " and column: "+ str(cellcnt+1)                            
    #                            break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg
                        if (cellcnt==21): # This is for AED Since columnn validation
                            #print("clss::" + step_cellcnt [cellcnt-18])
                            fnret=AED_fun(step_cellcnt [cellcnt-18],step_nxtcell,fnret)
                            if (fnret == "NO"):
                                print ("\n Invalid Assignment Effective Date column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg = fmmsg + "\n"+ " Invalid Assignment Effective Date column value :"+ step_nxtcell + " at row: "+ str(cnt+1) + " and column: "+ str(cellcnt+1)                                                        
    #                            break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg
                        if (cellcnt==20): # This is for Latest Hire Date columnn validation
                            #print("clss::" + step_cellcnt [cellcnt-18])
                            fnret=LHD_fun(step_cellcnt [cellcnt-16],step_nxtcell,fnret)
                            if (fnret == "NO"):
                                print ("\n Invalid Latest Hire Date column value : "+ step_nxtcell + " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg = fmmsg + "\n"+ " Invalid Latest Hire Date column value : "+ step_nxtcell + " at row: "+ str(cnt+1) + " and column: "+ str(cellcnt+1)                                                        
    #                            break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg
    
                        if (cellcnt==3): # This is for Classification columnn validation
                            #print("Classification ::" + str(step_cellcnt[cellcnt])) ###print("LN ::" + step_cellcnt [cellcnt+3])
                            FN = step_cellcnt[cellcnt+2]
                            LN = step_cellcnt[cellcnt+3]
                            fnret=classcheck(FN,LN, step_nxtcell, fnret)
                            if (fnret == "NO"):
                                print ("\n Invalid or Blank Classification column value : " + str(step_nxtcell) + " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg = fmmsg + "\n"+ " Invalid or Blank Classification column value : "+ step_nxtcell + " at row: "+ str(cnt+1) + " and column: "+ str(cellcnt+1)                                                        
    #                            break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg
    
                        if (cellcnt==8): # This is for Job Title columnn validation
                            fnret=Job_title(step_nxtcell, fnret) #print("Job Title:" + step_nxtcell)
                            if (fnret == "NO"):
                                print ("\n Invalid Job Title column value : " + str(step_nxtcell) + " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg = fmmsg + "\n"+ " Invalid Job Title column value : "+ step_nxtcell + " at row: "+ str(cnt+1) + " and column: "+ str(cellcnt+1)                                                        
    #                            break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg
                        if (cellcnt==5): # This is for Last Name columnn validation
                            LN = step_cellcnt[cellcnt-2]
                            #print("LN :" + step_cellcnt[cellcnt])
                            fnret=Last_Name(LN, step_nxtcell, fnret) #print("Last Name:" + step_nxtcell)
                            if (fnret == "NO"):
                                print ("\n Invalid Last Name column value :" + str(step_nxtcell) + " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg = fmmsg + "\n"+ " Invalid Last Name column value : "+ step_nxtcell + " at row: "+ str(cnt+1) + " and column: "+ str(cellcnt+1)                                                        
    #                          break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg
                        if (cellcnt==6): # This is for First Name columnn validation
                            FN = step_cellcnt[cellcnt]
                            #print("FN :" + step_cellcnt[cellcnt])
                            fnret=First_Name(LN, step_nxtcell, fnret) #print("First Name:" + step_nxtcell)
                            if (fnret == "NO"):
                                print ("\n Invalid First Name column value :" + str(step_nxtcell) + " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg = fmmsg + "\n"+ " Invalid First Name column value : "+ step_nxtcell + " at row: "+ str(cnt+1) + " and column: "+ str(cellcnt+1)                                                                                   
    #                            break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg
                        if (cellcnt==8): # This is for Job Code Name columnn validation
                            #print("Job Code1 :" + step_cellcnt[cellcnt])
                            fnret=Job_Code(step_nxtcell, fnret) # print("Job Code2:" + step_nxtcell)
                            if (fnret == "NO"):
                                print ("\n Invalid Job Code column value : " + str(step_nxtcell) + " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg = fmmsg + "\n"+ " Invalid Job Code column value : "+ step_nxtcell + " at row: "+ str(cnt+1) + " and column: "+ str(cellcnt+1)                                                                                   
    
    #                            break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg
                        if (cellcnt==2): # This is for Position ID columnn validation
                            fnret=Position_Fun(step_cellcnt[cellcnt+14], step_nxtcell,fnret)
                            if (fnret == "NO"):
                                print ("\n  Invalid Position ID column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg = fmmsg + "\n"+ " Invalid Position ID column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1)
                                #break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg
                        if (cellcnt==13): # This is for Company Code columnn validation
                            fnret=Co_CodeChk(step_nxtcell,fnret)
                            if (fnret == "NO"):
                                print ("\n  Invalid Company Code column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg = fmmsg + "\n" + " Invalid Company Code column value :"+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1)
                                #break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg
                        if (cellcnt==7): # This is for Emp ID columnn validation
                            fnret=EMPID_fun(step_cellcnt[cellcnt-4], step_nxtcell,fnret," ")
                            if ((fnret == "NO") or (fnret =="NO2")):
                                print ("\n Invalid Emp ID Code column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg = fmmsg+ "\n"+ " Invalid Emp ID Code column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1)
                                #break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg
                        if (cellcnt==14): # This is for Loc ID columnn validation
                            fnret=LocID_Chk(step_nxtcell,fnret)
                            if (fnret == "NO"):
                                print ("\n Invalid Loc ID Code column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg = fmmsg +"\n" + " Invalid Loc ID Code column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1)
                                #break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg
                        if (cellcnt==15): # This is for Loc Code columnn validation
                            fnret=LocCode_Chk(step_nxtcell,fnret)
                            if (fnret == "NO"):
                                print ("\n Invalid Location Code column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg= fmmsg +"\n" + " Invalid Location Code or Blank column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1)
                                #break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg
                        if (cellcnt==19): # This is for Loc Code columnn validation
                            fnret=PER_401K(step_cellcnt[cellcnt-16], step_nxtcell,fnret)
                            if (fnret == "NO"):
                                print ("\n Invalid 401k_Percentage column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg= fmmsg +"\n" + " Invalid 401k_Percentage or Blank column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1)
                                #break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg

                        if (cellcnt==12): # This is for Loc Code columnn validation
                            fnret=BiWeeklySal_chk(step_cellcnt[cellcnt-8], step_nxtcell,fnret)
                            if (fnret == "NO"):
                                print ("\n Invalid Bi-WeeklySalary column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg= fmmsg +"\n" + " Invalid Bi-WeeklySalary or Blank column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1)
                                #break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg

                        if (cellcnt==16): # This is for Status columnn validation
                            fnret=Status_Chk(step_cellcnt[cellcnt-13], step_nxtcell,fnret)
                            if (fnret == "NO"):
                                print ("\n Invalid or Blank Status column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg= fmmsg +"\n" + " Invalid or Blank Status column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1)
                                #break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg
                            if (fnret == "BLANK"):
                                print ("\n Blank Status column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg= fmmsg +"\n" + " Blank Status column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1)
                                #break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg                        
                        if (cellcnt==17): # This is for Union Management columnn validation
                            fnret=UMgmnt_fun(step_nxtcell,fnret)
                            if (fnret == "NO"):
                                print ("\n Invalid or Blank Union Management column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1))
                                fmmsg= fmmsg +"\n" + " Invalid or Blank Union Management column value : "+ step_nxtcell+ " at row: "+str(cnt+1) + " and column: "+ str(cellcnt+1)
                                #break# This break to capture all fault fields at once. preceed to 2 tas for one fault field msg
    
    
                        cellcnt += 1
    ## end of While loop                    
    #    sendmail(fmmsg) ## This row is not required
        #print("fmmsg 100 : "+ fmmsg.strip())
        if (fmmsg.strip() != ""):
            fmmsg = fmmsg + "\n \n The HRMS file cannot be moved!!"
        else:
            exists = os.path.isfile('C:\Sridhar Bokam\Python\HRMS_Precheck.txt')
            
            if exists:
                fmmsg = fmmsg + "\n \n The HRMS file is moving..."
                fmmsg = fmmsg + "\n \n and its good to move for ODI load..."
                #shutil.move("D:\HypData\HRMS_Prechk\HRMS_Precheck.txt", "D:\HypData\ODI_Source_Files\HRMS_Precheck.txt")
                shutil.copy("C:\Sridhar Bokam\Python\HRMS_Precheck.txt", "C:\Sridhar Bokam\Python\HRMS_Existing.txt")
            else:
                fmmsg = fmmsg + "\n \n There is no HRMS file to precheck..."
            
        #sendmail(fmmsg) ## This row is not required
    else:#subsequent If is in the line no. 68
        fmmsg = fmmsg + "\n \n There is no HRMS file to precheck..."
    
    sendmail(fmmsg)# To send consolidated email 

## end of While loop
## End of Main () function
## 401(k)- PER_401K  Needs to be rechecked-
def PER_401K(Cls, per401k, fnret):
    #print("401k_per : " + per401k) #per401k='100'
    val="00.0"
    if (Cls.strip().upper() in ('FILLED')):##IF classification is FILLED
        try:
            val = int(per401k)
            fnret ="YES"
        except ValueError:
            if (len(per401k.strip()) == 0):
                fnret= "NO"
            else:
                fnret= "NO"
    elif (Cls.strip().upper() in ('OPEN')): ##IF classification is OPEN
        if per401k.strip() in (''):
            fnret ="NO"
    else:   ##IF classification is  BLANK
        fnret = "YES"
        #print("hi Bi-WeeklySal :")
    return fnret
    

def BiWeeklySal_chk(Cls, Sal, fnret):
    #print("Salary : " + Sal)
    #print("CLass : " + Cls)
    if (Cls.strip().upper() in ('OPEN')):
        val="00.00"
        try:
            val = float(Sal)
        except ValueError:
            if (len(val) != 3):
                fnret= "NO"
            else:
                fnret= "NO"
    else:
        fnret = "YES"
        #print("hi Bi-WeeklySal :")
    return fnret


def ScenMonth_Chk(scn_month, scnVar):
    scn_month = scn_month.upper()
    #print ("Hello in ScenMonth_Chk():" + scnVar)

    if  scn_month in ['AUGUST', 'SEPTEMBER', 'MARCH', 'APRIL', 'JUNE', 'JULY']:
        ##print("YES")
        scnVar = ''
        if ((scn_month == 'AUGUST') or (scn_month == 'SEPTEMBER')):
            scnVar = "\nBUDGET"
        elif ((scn_month == "MARCH") or (scn_month == "APRIL")) :
            scnVar = "\nQ1 Forecast"
            ##print("inner loop2")
        elif ((scn_month == "JUNE") or (scn_month == "JULY")) :
            scnVar = "\nQ2 Forecast"
        else:
            scnVar = "This is not accepted member for Scenario dimension"
    else:
        #print("NO")
        scnVar = "\n This is wrong month to load HRMS File..."
    #print ("End OF ScenMonth_Chk():" + scnVar)
    return scnVar



def Status_Chk(Clss, stats, fnret):
    #print("stats :" + stats)
    #print(" Clss 100 :"+ Clss)
    fnret = ''
    if ((Clss.strip().upper() in ('OPEN')) and (len(stats.strip()) == 0)):
        fnret = "YES"
        #print("hi 1")
    elif ((Clss.strip().upper() in ('FILLED')) and (len(stats.strip()) == 0)) :
        fnret = "BLANK"
        #print("hi 2")
    elif (stats.strip().upper() in ('FULLTIME-REGULAR','FULLTIME-TEMPORARY','PARTTIME-NO BENEFITS','PARTTIME-NO BENEFITS (< 30 HOURS)','PARTTIME-REGULAR','PARTTIME-REGULAR (30 - 39 HOURS)','PARTTIME-REGULAR (GRANDFATHERED)','PARTTIME-NO BENEFITS (< 30 HOURS)','FULLTIME INTERN','PARTTIME INTERN', 'PARTTIME-TEMPORARY')):
        fnret = "YES"
        #print("hi 3")
        ###"Fulltime-Regular","Fulltime-Temporary","Parttime-No Benefits (< 30 hours)","Parttime-Regular (30 - 39 hours)","Parttime-Regular (Grandfathered)","Parttime-No Benefits (< 30 hours)","Fulltime Intern","Parttime Intern"
    else:
        #print("hi 4")
        fnret = "NO"
    return fnret


def LocCode_Chk(LocCD,fnret):
    #print("LocCD-in LocCode_Chk :" + LocCD) #print("fnret :" + fnret)    
    #This cannot be BLANK and whatever is given by HR. 
    #It should be string and within double codes nad cannot be blank.
    if (len(LocCD.strip()) > 80):
        fnret = "NO"
    elif (len(LocCD.strip()) < 0):
        fnret = "NO"
        #print("Hi" + fnret)
    else:
        fnret = "YES"
    return fnret


def Position_Fun(stats, posid, fnret):
    #print("stats:"+ stats) #print("positionid :"+ posid) #print("fnret :"+ fnret)
    #1) it can be blank when emp_status is part-time temporary
    #if (stats.strip().upper() in ('part-time temporary')):
    fnret = ''
    if (len(posid.strip()) == 0):
        #print("in 1st if:::")
        if (stats.strip().upper in ('part-time temporary', 'PART-TIME TEMPORARY')):
            #print("hi, POSID is empty")
            fnret = "YES"
        else:
            fnret = "NO"
            #print("hi, POSID is empty in NO")
            
    if (stats.strip().upper() in ('part-time temporary', 'PART-TIME TEMPORARY')):
        if (len(posid.strip()) > 0):
            fnret = "NO"
    else:
        fnret ="YES"
    
    return fnret;


def LocID_Chk(LocID, fnret):
    #print ("LocID :"+ LocID)
    #print ("fnret :"+ fnret)
    if (len(LocID.strip()) == 5 or len(LocID.strip())==6):
        fnret = "YES"
        #print ("fnret YES :"+ fnret)
    else:
        fnret = "NO"
        #print ("fnret NO :"+ fnret)
    return fnret


def EMPID_fun(Clss,EMPID, fnret,tmmsg):
    #print("\n Clss 1 :"+ Clss.upper()) #print("EMPID100 :"+ EMPID) ##print("tmmsg hello :"+ tmmsg) #fnret="YES"
    if (len(Clss.upper()) > 0):
        if (Clss.upper() in ('OPEN')):
            if (len(EMPID.strip()) == 0):
                fnret = "YES" ##print("EMPID 2 :"+ EMPID)                
            else: ##print("EMPID 3 :"+ EMPID)                
                fnret = "NO"
        elif (Clss.upper() in ('FILLED')):
            ##print("EMPID 4 :"+ EMPID)  ## print("fnret 5 :"+ fnret)
            if (len(EMPID.strip()) == 0):
                fnret = "NO"##print("EMPID 5 :"+ EMPID)
    else:##print("hello :"+ tmmsg)
        fnret ="NO2"
        fmmsg = tmmsg + "Empty/No-Value Classification"
    return fnret


def Co_CodeChk(CoCode, fnret):
    val='0'
    try:
        val = int(CoCode)
    except ValueError:
        if (len(val) != 3):
            fnret= "NO"
        else:
            fnret= "NO"
    else:
        fnret = "YES"
    return fnret

def Job_Code(JC, fnret):
    fnret =''
    #print("JC  :"+ JC)
    if (len((JC).strip()) != 0):
        if len(JC) == 4 :
            JC='0'+str(JC)
        if len(JC) == 3 :
            JC='00'+str(JC)
        if (len(str(JC)) == 5):# or len(JC.strip()) < 5): #This is intermittent for now as HR decides the field length(can be 5 or 6 or more)
            fnret="YES"
        else:
            fnret = "NO" 
    else:
        fnret = "NO"
    return fnret


def Last_Name(Clss, LN, fnret):
    fnret =''
    if (len(LN.strip()) == 0):
        if (Clss.strip().upper() in ('OPEN')):
            fnret="YES"
    else:
        if (Clss.strip().upper()   in ('FILLED')):
            fnret="YES"
                
    return fnret

def First_Name(Clss, FN, fnret):
    fnret =''
    if (len(FN.strip()) == 0):
        if (Clss.strip().upper() in ('OPEN')):
            fnret="YES"
    else:
        if (Clss.strip().upper() in ('FILLED')):
            fnret="YES"
                
    return fnret


def Job_title(JT, fnret):
    fnret =''
    if (len(JT.strip()) > 80):
        fnret="NO"
    return fnret    

def classcheck(FN, LN, Clss, fnret):
    fnret=''
    #print("\n FN:" + FN)
    #print("\n LN:" + LN)
    #print("\n Clss:" + Clss)
    if (Clss.strip().upper() not in ('OPEN','FILLED')):
        fnret = "NO"

    if (len(FN.strip()) == 0  and len(LN.strip()) == 0):
        if (Clss.strip().upper() in ('OPEN')):
            fnret="YES"
    else:
        #print("\n Clss:" + Clss)
        if (Clss.upper() not in ('FILLED')):
            fnret="NO"
            
    return fnret    
    

def UMgmnt_fun(step_nxtcell,fnret):
    if (step_nxtcell.upper() in ('U','M', '')):
        fnret="YES"
    else:
        fnret="NO"
    return fnret


def LHD_fun(clss, LHD, fnret):
    #print("clss::"+clss)
    if (len(LHD.strip()) > 0):
        if (clss.upper().strip() in ('FILLED')):
            try:
                datetime.strptime(LHD.strip(),'%m/%d/%Y')
                fnret = "YES" #   print ("valid date:" + vacSince)
            except ValueError:
                fnret = "NO" #   print ("Invalid date:" + vacSince)
        else:
            fnret = "NO"
    else:
        fnret = "YES"
    return fnret

def AED_fun(clss, AED, fnret):
    #print("clss::"+clss)
    if (len(AED.strip()) > 0):
        if (clss.upper() in ('FILLED')):
            try:
                datetime.strptime(AED.strip(),'%m/%d/%Y')
                fnret = "YES" #   print ("valid date:" + vacSince)
            except ValueError:
                fnret = "NO" #   print ("Invalid date:" + vacSince)
        elif (clss.upper() not in ('FILLED')):
            fnret = "YES"
    else:
        fnret = "YES"
    return fnret


def VacantSince_fun(clss, vacSince, fnret):
    if (len(vacSince.strip()) > 0):
        if (clss.upper().strip() in ('OPEN')):
            try:
                datetime.strptime(vacSince.strip(),'%m/%d/%Y')
                fnret = "YES" #   print ("valid date:" + vacSince)
            except ValueError:
                fnret = "NO" #   print ("Invalid date:" + vacSince)
    else:
        fnret = "YES"
    return fnret


def Scenario_fun(scen, fnret):
    #print("You are in Scenario_fun() :" + scen)
    if scen.upper() in ('BUDGET','Q1 FORECAST', 'Q2 FORECAST'):
        fnret="YES"
    else:
        fnret="NO"
    return fnret


def CostCenter_fun(step_nxtcell,fnret):
    if (len(step_nxtcell.strip()) != 4):
        fnret="NO"
    else:
        fnret="YES"
    return fnret


def Band_fun(step_nxtcell, fnret):
#    print("You are in Band fn()- Length:" + str(len(step_nxtcell)) )
    if ((len(step_nxtcell.strip()) == 1 or len(step_nxtcell.strip()) == 0 )):
        fnret="YES"
    else:
        fnret="NO"
    return fnret


def Grade_fun(step_nxtcell, fnret):
#    print("You are in Band fn()- Length:" + str(len(step_nxtcell)) )

    if (len(step_nxtcell.strip()) <3): # or  len(step_nxtcell.strip())==0):
        fnret="YES"
#    elif (len(step_nxtcell)== 0):
#        fnret="YES"
    else:
        fnret="NO"
    return fnret




if __name__ == '__main__':  
    main()        
