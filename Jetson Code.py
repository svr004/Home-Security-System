import face_recognition
import cv2
import os
import pickle
import time
import numpy as np
import smtplib
import imghdr
import datetime

from datetime import datetime
from email.message import EmailMessage
from telegram.ext import Updater, MessageHandler,Filters,CommandHandler
import os
#api_key = os.getenv('api_key')
y2=0
c=0
y=1
temp=0
BOT_TOKEN = '5073413110:AAHU8nkqTbAWBGOdaZbkxoeuFsAdGHp-218'
u = Updater(BOT_TOKEN,use_context=True)
dp = u.dispatcher 
#pip install python-telegram-bot --upgrade must be done
api_key = os.getenv('api_key')

Unk_Date_Time=[] #list of dates of already seen people to send in mail.

#compare faces to unknown face database and return the count(find number of times already seen for security purposes).
def Cmp_Unk_Face_Ret_Count():
    global y
    #Recent_Frame_Unk_Enc=[]
    #Existing_Frame_Unk_Enc=[]
    Recent_Frame_Unk=face_recognition.load_image_file(f'/home/jetsonnano/Desktop/final_fr/fr1/mailsend/{y}.jpg')
    
    Unk_Count=1  
    Recent_Frame_Unk_Enc=face_recognition.face_encodings(Recent_Frame_Unk)[0]
    image_dir='/home/jetsonnano/Desktop/final_fr/fr1/unknown'

    for root, dirs, files in os.walk(image_dir):
        #Take each file in the unknown folder.
        for file in files:
                
            path=os.path.join(root,file)
            print(path)
            name=os.path.splitext(file)[0]
            Existing_Frame_Unk=face_recognition.load_image_file(path)
            Existing_Frame_Unk_Enc=face_recognition.face_encodings(Existing_Frame_Unk)[0]
            print(Existing_Frame_Unk_Enc)
            Check_For_Match=face_recognition.compare_faces([Existing_Frame_Unk_Enc],Recent_Frame_Unk_Enc) #Check for matches.
            if(Check_For_Match==[True]): #if true,add count and date.
                Unk_Date_Time.append(name)
                Unk_Count+=1
        
    print(Unk_Count)   
    return Unk_Count
#Func Cmp_Unk_Face_Ret_Count() Ends.

#Send mail if unknown
def Send_Email(s2):
    global y
	#variables defined.
    Sender_Email = "jetsonstypv@gmail.com"
    Reciever_Email = "jetsonstypv@gmail.com"
    Password = 'STYPV@jetson'

    #message defined.
    newMessage = EmailMessage()                        
    newMessage['Subject'] = "INTRUDER ALERT!!"
    newMessage['From'] = Sender_Email                  
    newMessage['To'] = Reciever_Email       

    newMessage.set_content(f'UNKNOWN PERSON OUTSIDE. Found {s2} times Before on these dates:{Unk_Date_Time}')

    #Choose image to send.
    with open(f'/home/jetsonnano/Desktop/final_fr/fr1/mailsend/{y}.jpg','rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = str(y)

    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

    #Send mail.
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Sender_Email, Password)              
        smtp.send_message(newMessage)
        print("Mail Sent")
#Func Send_Email Ends.

def Debug_Output(top,right,bottom,left,name,frame,font):

#Debug Starts.(Not needed in Final)
    
    #resize 
    top=top*3
    right=right*3
    bottom=bottom*3
    left=left*3

    #output formatting
    cv2.rectangle(frame,(left,top),(right, bottom),(0,0,255),2)
    cv2.putText(frame,name,(left,top-6),font,.75,(0,0,255),2)

    #Show frame.
    cv2.imshow('Picture',frame)
    cv2.moveWindow('Picture',0,0)
def demo1(bot,update):
    chat_id = bot.message.chat_id
    
    path = 'https://www.meme-arsenal.com/memes/e9b54beadfe37ba414f00f95968a3f38.jpg'
    bot.message.reply_text('I am fine')
    update.bot.sendPhoto(chat_id=chat_id,photo=path)
  
def demo2(bot,update):
    chat_id = bot.message.chat_id
    path = 'https://cdn.technadu.com/wp-content/uploads/2019/06/Nvidia-Logo.png'
    bot.message.reply_text('Im Jetbot!!!!!')
    update.bot.sendPhoto(chat_id=chat_id,photo=path)

def demo3(bot,update): #sending intruder alert with pic
    print('HERE 2')
    global y
    #x=y-1
    chat_id ='1579008460'
    #path = r'/home/jetsonnano/Desktop/final_fr/fr1/mailsend/{y2}.jpg'
    bot.message.reply_text('Intruder Alert!')
    update.bot.send_photo(chat_id, photo=open(f'/home/jetsonnano/Desktop/final_fr/fr1/mailsend/{y}.jpg', 'rb')) #For Image From Jetson!
    #update.bot.sendPhoto(chat_id=chat_id,photo=path)
    
    return
    

def demo4(bot,update): #adding known from user
    chat_id = bot.message.chat_id
    raw = message.photo[2].file_id
    path = raw+".jpg"
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path,'wb') as new_file:
       ew_file.write(downloaded_file)

def bot1(bot,update):
    chat_id ='1579008460'
    global c
    print('HERE')
    a='/start'
    a = bot.message.text.lower()
    print(a)
    x=0
    if c==1:
        print('HERE 2')
        global y
        #x=y-1
        update.bot.send_photo(chat_id, photo=open(f'/home/jetsonnano/Desktop/final_fr/fr1/mailsend/{y+1}.jpg', 'rb')) #For Image From Jetson!
        bot.message.reply_text('Intruder Alert!')
        #demo3(bot,update)
        c=0
       
    elif a == "how are you?":
        demo1(bot,update)
        
    elif a == "/start" and x==0:
        demo2(bot,update)
        x+=1
    elif a =="what is your name?" or a=="name please":
        demo2(bot,update)
    elif a =="add person --i" or a =="add --i": #accepting photo from user
        bot.message.reply_text('Send The Photo ID:')
        demo4(bot,update)
    elif a =="add person --s" or a =="add --s": #accepting photo from user
        bot.message.reply_text('Send The image of the person to be added:')
        demo4(bot,update)
    else:
        bot.message.reply_text('Invalid Text')

    
        
    return 
    
def tcall():
    global c
    if(c==1):
        dp.add_handler(MessageHandler(Filters.text,demo3)) 
        u.start_polling()  
        c=0
    return

def tcall2():
   
    dp.add_handler(MessageHandler(Filters.text,demo3)) 
    u.start_polling()  
    return 
    #Debug ends.

Check_Unkown=1 # 1 if only unknown,0 if known
def main():
    #Define variables  
    Encodings=[] 
    Names=[]
    Check_Unkown=1 # 1 if only unknown,0 if known
    global y
    


    #Open already existing pickle to extract face encodings and names. 


    with open('train1.pkl','rb') as f:
        Encodings=pickle.load(f)
        Names=pickle.load(f)
    font=cv2.FONT_HERSHEY_SIMPLEX

    #Setting csi camera. 
    dispW=320
    dispH=240
    flip=2

    cap0 = cv2.VideoCapture('/dev/video1')
    cap0.set(3,640)
    cap0.set(4,480)

    #cap0 = cv2.VideoCapture('nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink')
    t=time.time()
    #cap0 = cv2.VideoCapture('nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink')  #capture frames

    

    #Define Timers
    Unk_Timer=time.time() #timer for every 'n' seconds
    Cur_Time=0 #dynamic timer
    top=0
    right=0
    bottom=0
    left=0
    name=""
    #Happens each frame 
    
   
    global y2
    while True:

        
        tcall()
        print("here3")
        #dp.add_handler(CommandHandler('bot1',bot1))
        Check_Unkown=1 #unknown by default.
        
        #get frame and resize.
        _,frame=cap0.read()  
        frameSmall=cv2.resize(frame,(0,0),fx=.33,fy=.33)
        frameRGB=cv2.cvtColor(frameSmall,cv2.COLOR_BGR2RGB)

        #Encode the frame.
        facePositions=face_recognition.face_locations(frameRGB,model='cnn')
        allEncodings=face_recognition.face_encodings(frameRGB,facePositions)
        global c
        c=1

        #check frame with known database
        for (top,right,bottom,left),face_encoding in zip(facePositions,allEncodings):
            name='Unknown Person' #By default
            
            #matches = number of matches
            matches=face_recognition.compare_faces(Encodings,face_encoding)

            #if atleast one known, add name 
            if True in matches:
                Check_Unkown=0
                c=0
                first_match_index=matches.index(True)
                name=Names[first_match_index]

            print(name)
            
            #condition for unknown person.
            if(Check_Unkown==1 and (Cur_Time-Unk_Timer)>5 ):
            
                z=datetime.now()
                z=z.replace(second=0, microsecond=0)
                
                print(face_recognition.face_encodings(frame))
     
                if(face_recognition.face_encodings(frame)):

                    cv2.imwrite(f'/home/jetsonnano/Desktop/final_fr/fr1/unknown/{z}.jpg',frame) #add unknown image with name as date 
                    cv2.imwrite(f'/home/jetsonnano/Desktop/final_fr/fr1/mailsend/{y}.jpg',frame) #add unknown image with name as arbitrary number.
                
                    Count=Cmp_Unk_Face_Ret_Count() #Call cmp Function
                    c=1
                    print("inside")
                    Send_Email(Count) 
                    temp=1
                    #dp.add_handler(MessageHandler(Filters.text,demo3))
                
                    Check_Unkown=0 #Shows face is unknown
                    y+=1
                    Unk_Timer=time.time()
            Cur_Time=time.time()
        
        #Debug_Output(top,right,bottom,left,name,frame,font)
        BOT_TOKEN = '5073413110:AAHU8nkqTbAWBGOdaZbkxoeuFsAdGHp-218'
        u = Updater(BOT_TOKEN,use_context=True)
        dp = u.dispatcher
        print('here4')
        
            
        if cv2.waitKey(1)==ord('q'):
            break
    
    cap0.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    
    main()
