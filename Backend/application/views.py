from application import app
from flask_pymongo import PyMongo
from flask import request,jsonify,session
from twilio.rest import Client
import random


mongo_reg=PyMongo(app,uri='mongodb://localhost:27017/car')
db= mongo_reg.db

@app.route('/register',methods=['POST','GET'])
def reg():
      if request.method=='POST':
        data = request.get_json()
        print(data)
        name = data["Name"]
        email = data["Email"]
        pno = data["PhoneNo"]
        user={"Name":name,"email":email,"PhoneNo":pno}
        # print(user)
        db.user_reg.insert_one(user)
        response = jsonify({'message': 'Login successful'})
        # response.headers['Authorization'] = f'Bearer {token}'
        response.headers.add('Access-Control-Allow-Origin', '  *')
        response.headers.add('Access-Control-Allow-Headers', 'Authorization')
        print(response)
        return response
        # return {"message": "User registered successfully"}
@app.route('/login',methods=['POST','GET'])
def getOTP():
  data = request.get_json()
#   print(data)
  number=data['number']
  getOTPApi(number)

  # s=generateOTP()
  # print(s,"kkkkkkkkkkk")
  # session['response']=str(s)
  # print(session['response'],'yyyyyyyy')
  return number
   # pass
def generateOTP():
   val=random.randrange(10000,999999)
   return val

@app.route('/ValidateOtp',methods=['POST','GET'])

def validateOTP():
   data = request.get_json()
   print(data)
   otp = data['otp']
   print ( 'response' in session,otp)
   if ('response' in session):
      s= session['response']
      session.pop('response',None)
      if s==otp:
         return 'authorized'
      else:
         return 'unauthorized'
   else:
      return "jjjj"   
 

def getOTPApi(number):
   account_sid='ACb1c12049f0012b4490a1bed4de92bd5e'
   auth_tok='070b576790180f1204c47a9c5bbf3bb3'
   client=Client(account_sid,auth_tok)
   otp=generateOTP()
   session['response']=str(otp)
   print( session['response'])
   body='Your OTP is '+str(otp)
   message=client.messages.create(
      from_='+16506839641',
      body=body,
      to=number
   )
   if message.sid:
      return True
   else:
      False