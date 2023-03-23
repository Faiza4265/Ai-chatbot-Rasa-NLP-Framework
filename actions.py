# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import EventType
from database_connectivity import getDataDep
from prediction_side import vomitting
#from database_connectivity import getData
#import mysql.connector
import mysql.connector 
import pandas as pd 
import re
from validate_email import validate_email
import datetime
import phonenumbers
#import dnspython3  
from rasa_sdk.forms import FormValidationAction, FormAction
from socket import gaierror
import csv 
import sys
import logging
import time
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from pandas.io.stata import precision_loss_doc
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
#from sklearn.externals import joblib
import joblib
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine



class StoreSympthom(Action):
    def name(self):
        return "action_db_status_update"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username= tracker.get_slot("username_chk")
        user_name=str(username[0])

        mydb3 = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="",
                    database="rasa"
                    )
        mycursor3 = mydb3.cursor()	


        sql3="SELECT user_full_name FROM user_tb where user_name='%s'"% (user_name)
        mycursor3.execute(sql3) 
        name = mycursor3.fetchone()
        #name=str(name_1[0]) 

        mydb1 = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="",
                    database="rasa"
                    )
        mycursor1 = mydb1.cursor()	


        sql1="SELECT Id FROM user_tb where user_full_name='%s'"% (name)
        mycursor1.execute(sql1) 
        id = mycursor1.fetchone()
        #id=str(id1[0])
        

        mydb2 = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="rasa"
                )
        mycursor2 = mydb2.cursor()


        #sql="INSERT INTO intent_collection (intent_name) VALUES ('%s') " % (intent)
        sql2= "UPDATE user_history SET is_better=true WHERE user_id='%s'" %(id)

        mycursor2.execute(sql2) 
        mydb2.commit()
        msg="so "+ str(name[0]) + " what other problem are you facing with your health this time?"
        dispatcher.utter_message(text="Thats good, am glad i helped you with your health")
        dispatcher.utter_message(msg)
        return[]    


class StoreSympthom(Action):
    def name(self):
        return "action_selectdb_chk"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        username= tracker.get_slot("username_chk")
        user_name=str(username[0])

        mydb3 = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="",
                    database="rasa"
                    )
        mycursor3 = mydb3.cursor()	


        sql3="SELECT user_full_name FROM user_tb where user_name='%s'"% (user_name)
        mycursor3.execute(sql3) 
        name = mycursor3.fetchone()
        #name=str(name_1[0]) 

        mydb1 = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="",
                    database="rasa"
                    )
        mycursor1 = mydb1.cursor()	


        sql1="SELECT Id FROM user_tb where user_full_name='%s'"% (name)
        mycursor1.execute(sql1) 
        id = mycursor1.fetchone()
        #id=str(id1[0])
        

      


        mydb2 = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="rasa"
                )
        mycursor2 = mydb2.cursor()


        #sql="INSERT INTO intent_collection (intent_name) VALUES ('%s') " % (intent)
        sql2= "SELECT dieases FROM user_history WHERE user_id='%s'" %(id)

        mycursor2.execute(sql2) 
        dieases = mycursor2.fetchone()
        #dieases=str(dieases_gt[0]) 
        mess="hello " + str(name[0])+ " how are you " + " from your last check up you have a dieases called " + str(dieases[0]) + " did my suggestion helped you?"
        dispatcher.utter_message(mess)

        #mydb.commit() 

        return[]



class StroreIntent(Action):
    def name(self):
        return "check_intent_no"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent= tracker.latest_message['intent'].get('name')
        #intent=tracker.get_intent_of_latest_message
        print(intent)

        # first storing the intent name to the db
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="rasa"
                )
        mycursor = mydb.cursor()

        sql="INSERT INTO intent_collection (intent_name) VALUES ('%s') " % (intent)

        mycursor.execute(sql)   
        mydb.commit() 
        #dispatcher.utter_message("intent has been stored")

        # check how many times the current stored intent tooken from a user appear in the database
        mydb2 = mysql.connector.connect( host="localhost", user="root", passwd="", database="rasa")
        sql2="SELECT * FROM  intent_collection"
        df= pd.read_sql_query(sql2, con=mydb2)
        intent_count= (df['intent_name']=='vomitting_initial').sum()
        intent_count
        if intent_count in range(1,4):
            dispatcher.utter_message(template="utter_confirm")
        else:
            dispatcher.utter_message(template="utter_register")

        return[]

class ValidateloginForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_login_form"
#
    def validate_username(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate username."""

        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="rasa"
                )
        mycursor = mydb.cursor()
        
        get_username= tracker.get_slot("username_chk")

        sql = "SELECT FROM user_tb where user_name='%s'"% (get_username)

        mycursor.execute(sql) 
        res = mycursor.fetchone()
        if res != 0:
            # validation succeeded, set the value of the "phone" slot to value
            return {"username": value}
        else:
            dispatcher.utter_message(template="utter_invalid_usernm")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"username": None} 

    def validate_password(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate password."""
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="rasa"
                )
        mycursor = mydb.cursor()
        get_password= tracker.get_slot("password_chk")

        sql = "SELECT FROM user_tb where password='%s'"% (get_password)

        mycursor.execute(sql) 
        res = mycursor.fetchone()
        if res !=0:
            # validation succeeded, set the value of the "phone" slot to value
            return {"password": value}
        else:
            dispatcher.utter_message(template="utter_invalid_passwd")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"password": None}         

        return[]        





class ValidateAppointmentForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_userdata_form"
    
    def validate_phone_no(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate phone number."""

        res = re.search(r'(\+\d{12})', str(value))
        if res:
            # validation succeeded, set the value of the "phone" slot to value
            return {"phone_no": value}
        else:
            dispatcher.utter_message(template="utter_invalid_phone_num")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"phone_no": None} 

    def validate_email(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate email."""

        #email_validate=re.match(r'[\w-]{1,20}@\w{2,20}\.\w{2,3}$',email)
        #email_validate='^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        #re.match(r'[\w-]{1,20}@\w{2,20}\.\w{2,3}$',value)
        #re.search(r'(((\d{4})-\d{2})-\d{2})', '2018-09-01')

        if validate_email(value):
            # validation succeeded, set the value of the "email" slot to value
            return {"email": value}
        else:
            dispatcher.utter_message(template="utter_invalid_email")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"email": None}  

    def validate_name(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate name."""


        regex_name = re.compile(r'^(Dr\.|Mrs\.|Ms\.) ([a-z]+)( [a-z]+)*( [a-z]+)*$',  
              re.IGNORECASE)
        res = regex_name.search(value) 

        if res:
            # validation succeeded, set the value of the "name" slot to value
            return {"name": value}
        else:
            dispatcher.utter_message(template="utter_invalid_namm")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"name": None}  

    def validate_username(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate username."""

        res = re.search(r'(\b[A-Z]{4}-\d{3}\b)', str(value))

        if res:
            # validation succeeded, set the value of the "name" slot to value
            return {"username": value}
        else:
            dispatcher.utter_message(template="utter_invalid_u_nm")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"username": None} 


    def validate_password(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate password."""

        res = re.search(r'(\b[A-Z]{2}#\d{5}\b)', str(value))
        if res:
            # validation succeeded, set the value of the "name" slot to value
            return {"password": value}
        else:
            dispatcher.utter_message(template="utter_invalid_passwd")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"password": None}         


    def validate_birthdate(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate birthdate."""
 

        #res=datetime.datetime.strptime(str(value), format)
        res = re.search(r'(\d{4})-(\d{2})-(\d{2})', str(value))
    
        if res:
            # validation succeeded, set the value of the "name" slot to value
            return {"birthdate": value}
        else:
            dispatcher.utter_message(template="utter_invalid_b_dt")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"birthdate": None}   


        return [] 
        

class AskForDepartment(Action):
    def name(self):
        return "action_insert_userinfo"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name= tracker.get_slot("name")
        email= tracker.get_slot("email")
        username= tracker.get_slot("username")
        password= tracker.get_slot("password")

        mydb = mysql.connector.connect(
               host="localhost",
               user="root",
               password="",
               database="rasa"
            ) 

        mycursor = mydb.cursor()
    
        sql="INSERT INTO user_tb (user_full_name, user_email ,user_name, password) VALUES ( '%s', '%s', '%s', '%s') " % (name,email,username[0],password[0])
        mycursor.execute(sql)
        mydb.commit()    
        mess="so "+ name + " how can i help you"  
        dispatcher.utter_message("thank you, i have stored you as one of my patient")
        dispatcher.utter_message(mess) 
        return[]



class AskForDepartment(Action):
    def name(self):
        return "j"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name= tracker.get_slot("name")
        email= tracker.get_slot("email")
        username= tracker.get_slot("username")
        password= tracker.get_slot("password")
        gender= tracker.get_slot("gender")
        blood_group= tracker.get_slot("blood_group")

        mydb = mysql.connector.connect(
               host="localhost",
               user="root",
               password="",
               database="rasa"
            ) 

        mycursor = mydb.cursor()
    
        sql="INSERT INTO useraccount_tb (username, password) VALUES ( '%s', '%s') " % (username,password)
        mycursor.execute(sql)
        mydb.commit()    
 
        return[]





class PredictionItch(Action):
    def name(self):
        return "action_predictitching"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            df= pd.read_csv("Training.csv")
            df.head()
            recommend= {
                     'Fungal infection':'medication1', 
                     'Allergy':'medication2', 
                     'GERD':'medication3',
                     'Chronic cholestasis':'medication4',
                     'Drug Reaction':'medication5',
                     'Peptic ulcer diseae':'medication6',
                     'AIDS':'medication6', 
                     'Diabetes ':'medication7',
                     'Gastroenteritis':'medication8',
                     'Bronchial Asthma':'medication9', 
                     'Hypertension ':'medication10',
                     'Migraine':'medication11',
                     'Cervical spondylosis':'medication12',
                     'Paralysis (brain hemorrhage)':'medication13', 
                     'Jaundice':'medication14',
                     'Malaria':'medication15', 
                     'Chicken pox':'medication16', 
                     'Dengue':'medication17',
                     'Typhoid':'medication18', 
                     'hepatitis A':'medication19',
                     'Hepatitis B':'medication20',
                     'Hepatitis C':'medication21', 
                     'Hepatitis D':'medication22', 
                     'Hepatitis E':'medication23',
                     'Alcoholic hepatitis':'medication24',
                     'Tuberculosis':'medication25',
                     'Common Cold':'medication26', 
                     'Pneumonia':'medication27',
                     'Dimorphic hemmorhoids(piles)':'medication28',
                     'Heart attack':'medication29', 
                     'Varicose veins':'medication30',
                     'Hypothyroidism':'medication31',
                     'Hyperthyroidism':'medication32',
                     'Hypoglycemia':'medication33',
                     'Osteoarthristis':'medication34',
                     'Arthritis':'medication35',
                     '(vertigo) Paroymsal  Positional Vertigo':'medication36', 
                     'Acne':'medication37',
                     'Urinary tract infection':'medication39', 
                     'Psoriasis':'medication40',
                     'Impetigo':'medication41',
                     
                 }
            df['recommendation']= df['prognosis'].apply(lambda x : recommend[x])     
            X= df[[ 'skin_rash', 'nodal_skin_eruptions', 'dischromic_patches']]
            Y= df['prognosis']
            X.head()
            model= DecisionTreeClassifier()
            model.fit(X,Y)
            text= "i will ask you four different sympthoms you might think you will have follow me and say yes if you have or no if you dont have"
            print(text)
            input_x1=tracker.get_slot("skin_rash")
            input_x2=tracker.get_slot("nodal_skin_eruptions")
            input_x3=tracker.get_slot("dischromic_patches")

           
            
            if input_x1=='skin_rash':
                input_x1=1
            elif input_x1=='not_skin_rash':
                input_x1=0
            else:
                print("invalid")
                
            if input_x2=='nodal_skin_eruptions':
                input_x2=1
            elif input_x2=='not_nodal_skin_eruptions':
                input_x2=0
            else:
                print("invalid")
                
            
            if input_x3=='dischromic_patches':
                input_x3=1
            elif input_x3=='not_dischromic_patches':
                input_x3=0
            else:
                print("invalid")    

    
            prediction1= model.predict([[input_x1, input_x2, input_x3]])
            print(prediction1) 
            pred=   "based on your sympthoms you have a likely dieases to be a : " + str(prediction1[0])
            dispatcher.utter_message(pred)  

        
            
            return[]


class PredictionVomm(Action):
    def name(self):
        return "action_predictvomiting"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            df= pd.read_csv("Training.csv")    
            X= df[[ 'indigestion', 'loss_of_appetite', 'abdominal_pain' , 'passage_of_gases', 'internal_itching','chest_pain','high_fever','dehydration']]
            Y= df['prognosis']
            X.head()
            model= MultinomialNB()
            model.fit(X,Y)
            input_x1=tracker.get_slot("indigestion")
            input_x2=tracker.get_slot("loss_of_appetite")
            input_x3=tracker.get_slot("abdominal_pain")
            input_x4=tracker.get_slot("passage_of_gases")
            input_x5=tracker.get_slot("internal_itching")
            input_x6=tracker.get_slot("chest_pain")
            input_x7=tracker.get_slot("high_fever")
            input_x8=tracker.get_slot("dehydration")

            if input_x1=='indigestion':
                a=1
            else:
                a=0
            if input_x2=='loss_of_appetite':
                b=1
            else:
                b=0
            if input_x3=='abdominal_pain':
                c=1
            else:
                c=0
            if input_x4=='passage_of_gases':
                d=1
            else:
                d=0
            if input_x5=='internal_itching':
                e=1
            else:
                 e=0 
            if input_x6=='chest_pain':
                f=1
            else:
                 f=0 
            if input_x7=='high_fever':
                g=1
            else:
                 g=0 
            if input_x8=='dehydration':
                h=1
            else:
                 h=0           

            prediction1= model.predict([[a, b, c, d, e,f,g,h]])
            print(prediction1) 
            pred=   "based on your sympthoms you have a likely dieases to be a : " + str(prediction1[0])
            dispatcher.utter_message(pred)  

            id_name = tracker.get_slot("name")
            mydb2 = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="",
                    database="rasa"
                    )
            mycursor2 = mydb2.cursor()	


            sql2="SELECT Id FROM user_tb where user_full_name='%s'"% (id_name)
    
            mycursor2.execute(sql2) 

            id1 = mycursor2.fetchone()
            id=id1[0] 
            dieases	=str(prediction1[0])
    
            mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="",
                    database="rasa"
                    )
            mycursor = mydb.cursor()

            if input_x1=='indigestion':
                a="indigestion"
            else:
                a="no_sympthom"
            if input_x2=='loss_of_appetite':
                b="loss_of_appetite"
            else:
                b="no_sympthom"
            if input_x3=='abdominal_pain':
                c="abdominal_pain"
            else:
                c="no_sympthom"
            if input_x4=='passage_of_gases':
                d="passage_of_gases"
            else:
                d="no_sympthom"
            if input_x5=='internal_itching':
                e="internal_itching"
            else:
                 e="no_sympthom"
            if input_x6=='chest_pain':
                f="chest_pain"
            else:
                 f="no_sympthom"
            if input_x7=='high_fever':
                g="high_fever"
            else:
                 g="no_sympthom"
            if input_x8=='dehydration':
                h="dehydration"
            else:
                 h="no_sympthom"         


            sql="INSERT INTO user_history (user_id, sympthom_1,sympthom_2,sympthom_3,sympthom_4,sympthom_5,sympthom_6,sympthom_7,sympthom_8 ,dieases) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % ( id,a,b,c,d,e,f,g,h ,dieases )
    
            mycursor.execute(sql)   
            mydb.commit()  

           
            if dieases=="Fungal infection":
                dispatcher.utter_message(template="")
            elif dieases=="Allergy":
                dispatcher.utter_message(template="")
            elif dieases=="GERD":
                dispatcher.utter_message(template="")
            elif dieases=="Chronic cholestasis":
                dispatcher.utter_message(template="")
            elif dieases=="Drug Reaction":
                dispatcher.utter_message(template="")
            elif dieases=="Peptic ulcer diseae":
                dispatcher.utter_message(template="") 
            elif dieases=="AIDS":
                dispatcher.utter_message(template="")
            elif dieases=="Diabetes":
                dispatcher.utter_message(template="") 
            elif dieases=="Gastroenteritis":
                dispatcher.utter_message(template="")
            elif dieases=="Bronchial Asthma":
                dispatcher.utter_message(template="") 
            elif dieases=="Hypertension":
                dispatcher.utter_message(template="") 
            elif dieases=="Migraine":
                dispatcher.utter_message(template="")
            elif dieases=="Cervical spondylosis":
                dispatcher.utter_message(template="")
            elif dieases=="Paralysis (brain hemorrhage)":
                dispatcher.utter_message(template="")
            elif dieases=="Jaundice":
                dispatcher.utter_message(template="")
            elif dieases=="Malaria":
                dispatcher.utter_message(template="")
            elif dieases=="Chicken pox":
                dispatcher.utter_message(template="")
            elif dieases=="Dengue":
                dispatcher.utter_message(template="")
            elif dieases=="Typhoid":
                dispatcher.utter_message(template="")
            elif dieases=="hepatitis A":
                dispatcher.utter_message(template="")
            elif dieases=="Hepatitis B":
                dispatcher.utter_message(template="")
            elif dieases=="Hepatitis C":
                dispatcher.utter_message(template="") 
            elif dieases=="Hepatitis D":
                dispatcher.utter_message(template="") 
            elif dieases=="Hepatitis E":
                dispatcher.utter_message(template="")
            elif dieases=="Alcoholic hepatitis":
                dispatcher.utter_message(template="")
            elif dieases=="Tuberculosis":
                dispatcher.utter_message(template="")
            elif dieases=="Common Cold":
                dispatcher.utter_message(template="") 
            elif dieases=="Pneumonia":
                dispatcher.utter_message(template="")
            elif dieases=="Dimorphic hemmorhoids(piles)":
                dispatcher.utter_message(template="")
            elif dieases=="Heart attack":
                dispatcher.utter_message(template="")
            elif dieases=="Varicose veins":
                dispatcher.utter_message(template="")
            elif dieases=="Hypothyroidism":
                dispatcher.utter_message(template="") 
            elif dieases=="Hyperthyroidism":
                dispatcher.utter_message(template="")
            elif dieases=="Hypoglycemia":
                dispatcher.utter_message(template="")
            elif dieases=="Osteoarthristis":
                dispatcher.utter_message(template="")
            elif dieases=="Arthritis":
                dispatcher.utter_message(template="")
            elif dieases=="(vertigo) Paroymsal  Positional Vertigo":
                dispatcher.utter_message(template="")
            elif dieases=="Acne":
                dispatcher.utter_message(template="")
            elif dieases=="Urinary tract infection":
                dispatcher.utter_message(template="")
            elif dieases=="Psoriasis":
                dispatcher.utter_message(template="")
            elif dieases=="Imdieases":
                dispatcher.utter_message(template="")
            else:
                dispatcher.utter_message(text="no advice sorry...")    

            return[]


class PredictionRest(Action):
    def name(self):
        return "action_predictrestlness"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            df= pd.read_csv("Training.csv")    
            X= df[[ 'fatigue', 'weight_loss', 'irregular_sugar_level', 'obesity', 'excessive_hunger', 'increased_appetite', 'blurred_and_distorted_vision', 'lethargy']]
            Y= df['prognosis']
            X.head()
            model= MultinomialNB()
            model.fit(X,Y)
            text= "i will ask you four different sympthoms you might think you will have follow me and say yes if you have or no if you dont have"
            print(text)
            input_x1=tracker.get_slot("fatigue")
            input_x2=tracker.get_slot("weight_loss")
            input_x3=tracker.get_slot("irregular_sugar_level")
            input_x4=tracker.get_slot("obesity")
            input_x5=tracker.get_slot("excessive_hunger")
            input_x6=tracker.get_slot("increased_appetite")
            input_x7=tracker.get_slot("blurred_and_distorted_vision")
            input_x8=tracker.get_slot("lethargy")


            if input_x1=='fatigue':
                a=1
            else:
                a=0
            if input_x2=='weight_loss':
                b=1
            else:
                b=0
            if input_x3=='irregular_sugar_level':
                c=1
            else:
                c=0
            if input_x4=='obesity':
                d=1
            else:
                d=0
            if input_x5=='excessive_hunger':
                e=1
            else:
                e=0
            if input_x6=='increased_appetite':
                f=1
            else:
                f=0   
            if input_x6=='blurred_and_distorted_vision':
                g=1
            else:
                g=0 
            if input_x6=='lethargy':
                h=1
            else:
                h=0     
    
            prediction1= model.predict([[a, b, c, d, e, f, g, h]])
            print(prediction1) 
            pred=   "based on your sympthoms you have a likely dieases to be a : " + str(prediction1[0])
            dispatcher.utter_message(pred)  

            id_name1 = tracker.get_slot("username_chk")
            id_name=str(id_name1[0])
            mydb2 = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="",
                    database="rasa"
                    )
            mycursor2 = mydb2.cursor()	


            sql2="SELECT Id FROM user_tb where user_name='%s'"% (id_name)
    
            mycursor2.execute(sql2) 

            id1 = mycursor2.fetchone()
            id=id1[0] 
            dieases	=str(prediction1[0])
    
            mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="",
                    database="rasa"
                    )
            mycursor = mydb.cursor()

           
            if input_x1=='fatigue':
                a="fatigue"
            else:
                a="no_sympthom"
            if input_x2=='weight_loss':
                b="weight_loss"
            else:
                b="no_sympthom"
            if input_x3=='irregular_sugar_level':
                c="irregular_sugar_level"
            else:
                c="no_sympthom"
            if input_x4=='obesity':
                d="obesity"
            else:
                d="no_sympthom"
            if input_x5=='excessive_hunger':
                e="excessive_hunger"
            else:
                e="no_sympthom"
            if input_x6=='increased_appetite':
                f="increased_appetite"
            else:
                f="no_sympthom"   
            if input_x6=='blurred_and_distorted_vision':
                g="blurred_and_distorted_vision"
            else:
                g="no_sympthom" 
            if input_x6=='lethargy':
                h="lethargy"
            else:
                h="no_sympthom"


            sql="INSERT INTO user_history (user_id, sympthom_1,sympthom_2,sympthom_3,sympthom_4,sympthom_5,sympthom_6,sympthom_7,sympthom_8 ,dieases) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') " % ( id,a,b,c,d,e,f,g,h ,dieases )
    
            mycursor.execute(sql)   
            mydb.commit()  

            #dispatcher.utter_message(template="utter_what_to_do")

            return[]
 


class AskForDepartment(Action):
    def name(self):
        return "action_predictyelloweye"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            df= pd.read_csv("Training.csv")



            #df['recommendation']= df['prognosis'].apply(lambda x : recommend[x])     
            X= df[[ 'abdominal_pain', 'loss_of_appetite', 'yellowish_skin', 'vomiting']]
            Y= df['prognosis']
            X.head()
            model= DecisionTreeClassifier()
            model.fit(X,Y)
            text= "i will ask you four different sympthoms you might think you will have follow me and say yes if you have or no if you dont have"
            print(text)
            input_x1=tracker.get_slot("abdominal_pain")
            input_x2=tracker.get_slot("loss_of_appetite")
            input_x3=tracker.get_slot("yellowish_skin")
            input_x4=tracker.get_slot("vomiting")

            if input_x1=='abdominal_pain':
                input_x1=1
            elif input_x1=='not_abdominal_pain':
                input_x1=0
            else:
                print("invalid")
            
            if input_x2=='loss_of_appetite':
                input_x2=1
            elif input_x2=='not_loss_of_appetite':
                input_x2=0
            else:
                print("invalid")
                
            if input_x3=='yellowish_skin':
                input_x3=1
            elif input_x3=='not_yellowish_skin':
                input_x3=0
            else:
                print("invalid")
                
            if input_x4=='vomiting':
                input_x4=1
            elif input_x4=='not_vomiting':
                input_x4=0
            else:
                print("invalid")

            prediction1= model.predict([[input_x1, input_x2, input_x3, input_x4]])
            print(prediction1) 
            pred=   "based on your sympthoms you have a likely dieases to be a : " + str(prediction1[0])
            dispatcher.utter_message(pred)  

            return[]
 












class ActionEmail(Action):
    def name(self):
        return "action_sympthomslotcheck"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

     
        itching = tracker.get_slot("itching")
        restlessness = tracker.get_slot("restlessness")
        vomiting = tracker.get_slot("vomiting")
        yellowing_of_eyes = tracker.get_slot("yellowing_of_eyes")
       
             
        #if itching:
        #     dispatcher.utter_message(Action="utter_itchingask")
        #
        #elif restlessness:
        #     dispatcher.utter_message(Action="utter_restlessnessask") 
#
        #elif vomiting:
        #     dispatcher.utter_message(Action="utter_vomitingask")      
#
        #elif yellowing_of_eyes:
        #     dispatcher.utter_message(Action="utter_yellowing_of_eyesask")     
#
        #else:
            # dispatcher.utter_message(template="utter_notfound") 


     
        #dispatcher.utter_message(Action="")         
   
        return[] 
 


class ActionEmail(Action):
    def name(self):
        return "action_sympthon_description"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        csvfile = open("symptom_Description.csv")
        reader = csv.reader(csvfile)

        # Get from user input drug name: 
        syphtom_name= tracker.get_slot("sympthom")
        nodescription = False

        for row in reader:
            # Check for the user input
            if syphtom_name in row[0] or row[2]:
                print(row[0]+"\t"+row[1])
                symptom_Description= row[0]+":- "+row[1] 
                dispatcher.utter_message(text=str(symptom_Description)) 
                nodescription = False
                break 
            else:
               nodescription = True

            # elif nodescription:
            #     dispatcher.utter_message(template="utter_notfound")
        if nodescription:
           dispatcher.utter_message(template="utter_notfound")         
   
        return[]




class ActionEmail(Action):
    def name(self):
        return "action_email_patient"

    def run(self, dispatcher, tracker, domain):
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="rasa"
                )
        mycursor = mydb.cursor()
        getname=tracker.get_slot("name")

        sql = "SELECT patient_email FROM patient_tb where patient_full_name='%s'"% (getname)

   # sql='INSERT INTO user_info(name, email, phone) VALUES (?, ?, ?)', (travel_date, travel_period, trip_type, adults, child, budget, email, phno)'
   
        mycursor.execute(sql)   
        email = mycursor.fetchone() 

        sender_email="chatbot721@gmail.com"
        reciver_email=email
        password="imaxgirl@721"
        TEXT="welcome "+ getname+", your appointment has been scheduled and you will soon hear back from our team"
        #TEXT="hey " + getname  +" you have an appointment scheduled from a user named patril....and the email was fetched from the database..thank you"
        SUBJECT="Appointment"
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
        try: 

            server=smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email,password)
            print("login success")
            server.sendmail(sender_email,reciver_email,message)
            print("email has been sent")

        except (gaierror, ConnectionRefusedError):

            print('Failed to connect to the server. Bad connection settings?')
        except smtplib.SMTPServerDisconnected:

            print('Failed to connect to the server. Wrong user/password?')
        except smtplib.SMTPException as e:
            print('SMTP error occurred: ' + str(e))
          
        dispatcher.utter_message("we have sent you an email to confirm your email,thank you for your time.")
        return[]        



class ActionAdvice(Action):
    def name(self):
        return "action_advice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        mydb2 = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="rasa"
                )
        mycursor2 = mydb2.cursor()
        getname=tracker.get_slot("name") 
        #using getname select the user id then store it in id

        sql2 = "SELECT Id FROM user_tb where user_full_name='%s'"% (getname)
        mycursor2.execute(sql2)   
        id = mycursor2.fetchone()

        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="rasa"
                )
        mycursor = mydb.cursor()
        #getname=tracker.get_slot("name") 
        #using getname select the user id then store it in id
        user_id= str(id[0])
        sql = "SELECT dieases FROM user_history where user_id='%s'"% (user_id)
        mycursor.execute(sql)   
        di = mycursor.fetchone() 
        dieases= di[0]
        #print(dieases[0])
        csvfile= open("symptom_precaution.csv")
        reader= csv.reader(csvfile)
        node= False
        for row in reader:
            if dieases in row[0]:
                steps= "1:- " + row[1] + "\n" + "2:- " + row[2]+ "\n"+ "3:- " + row[3]
                print(str(steps))
                dispatcher.utter_message(text=str(steps))
                node = False
                break
            else:
                node= True
        if node:
            print("not found , but please dont say that")
        

        return[]