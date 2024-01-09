from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from . models import train,passengers,wallet,info,user1,journeys
from datetime import date, timedelta
import os
import xlsxwriter
from django.http import FileResponse
der=0

def custsign(request):
        if request.method=='POST':
            uname=request.POST.get('username')
            email=request.POST.get('email')
            pass1=request.POST.get('password1')
            pass2=request.POST.get('password2')
           

            if pass1!=pass2:
                return HttpResponse("Your password and confrom password are not Same!!")
            else:

                my_user=User.objects.create_user(uname,email,pass1)
                
                my_user.save()
                return redirect('custlogin')
        



        return render (request,'train/custsign.html')
def custlogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('custview')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'train/loginc.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')
def home(request):
    global der
    if der == 0:
         return render(request,"train/redirect_staff.html")    
    return render(request,'train/admin_page.html')
b=0
def add(request):
    global der
    if der == 0:
        return render(request,"train/redirect_staff.html")    
    if request.method=="POST":
        name=request.POST.get('name','')
        s1=request.POST.get('s1','')
   
        seatss=request.POST.get('seatss','')
        seatsg=request.POST.get('seatsg','')
        seats1=request.POST.get('seats1','')
        seats2=request.POST.get('seats2','')
        seats3=request.POST.get('seats3','')
        time=request.POST.get('time','')
        days=request.POST.get('days','')
        fareg=request.POST.get('fareg','')
        fareg=int(fareg)
        fares=request.POST.get('fares','')
        fares=int(fares)
        fare1=request.POST.get('fare1','')
        fare1=int(fare1)
        fare2=request.POST.get('fare2','')
        fare2=int(fare2)
        fare3=request.POST.get('fare3','')
        fare3=int(fare3)

        
        
        
        id=int(request.POST.get('id',''))
        
        request.session['adding_train_id']=id
        y=train(name=name,s1=s1,seatss=int(seatss),seatsg=int(seatsg),seats1=int(seats1),seats2=int(seats2),seats3=int(seats3),time=time,days=days,fares=fares,fareg=fareg,fare1=fare1,fare2=fare2,fare3=fare3,train_id=id)
        y.save()
        return redirect("addinng")
        

    return render(request,"train/add.html")
import datetime
import datetime

def all_weekdays(weekday):
 

   today = datetime.date.today()  # Get the current date
   end_date = datetime.date(2025, 12, 31)  # Set the end date as December 31, 2025

   weekday_index = {
       "M": 0,
       "T": 1,
       "W": 2,
       "Th": 3,
       "F": 4,
       "Sat": 5,
       "S": 6
   }



   # Get the index of the specified weekday
   weekday_index_num = weekday_index[weekday.title()]
   a=train.objects.get(train_id=b)
   c=a.name
   seatss=a.seatss


  

   # Calculate the number of days to advance to reach the next instance of the weekday
   days_to_advance = (weekday_index_num - today.weekday()) % 7

   current_date = today + datetime.timedelta(days=days_to_advance)  # Start from the next upcoming weekday

   while current_date <= end_date:
        
        u=info(name=c,id_1=b,date=current_date.strftime("%Y-%m-%d"),seatss=seatss,seatsg=a.seatsg,seats1=a.seats1,seats2=a.seats2,seats3=a.seats3,s_1=a.s1,fare1=a.fare1,fare2=a.fare2,fare3=a.fare3,fares=a.fares,fareg=a.fareg,time=a.time)
        u.save()
        current_date += datetime.timedelta(days=7)  # Advance to the next week's same weekday

# Get user input for the weekday




def adding(request):
    global b
    u=train.objects.get(train_id=request.session.get('adding_train_id'))
    y=u.days
    for i in y:
        all_weekdays(i)




 
 
    return redirect("home")
def cancel(request):
    global der
    if der == 0:
         return render(request,"train/redirect_staff.html")    
    if request.method=="POST":
        a=request.POST.get("train_id","")
        b=request.POST.get("Date","")
        w=passengers.objects.all()
        tyui=info.objects.get(id_1=int(a),date=b)
   
        for i in w:
            if i.train_id == a and i.date == b :
                unique=i.unique_id


                amount1=journeys.objects.get(id1=unique).price
                ty=user1.objects.all()
                name1=""
                for j in ty:
                    if unique in j.unique_id :
                        name1=j.user
                


                

                o=wallet.objects.get(name=name1)
                o.amount=o.amount+amount1
                o.save()
                ayu=journeys.objects.get(id1=unique)
                ayu.price=0
                ayu.save()


                t=user1.objects.get(user=name1)
                string = t.unique_id
                word_to_remove =unique
                new_string = string.replace(word_to_remove, "")
                t.unique_id=new_string
                t.save()


                i.delete()

        return HttpResponse("done")

       

    return render(request,"train/cancel.html")
h=[]
o=""
w=[]
y=[]


def search(request):
        
        
        if request.method=="POST":
            global h
            global o
            global w
            w.clear()
            h.clear()

            global y
            y.clear()
            clas=request.POST.get("class1","r")
   


            
            a=request.POST.get("journey_date","")
            b=request.POST.get("from_station","")
            c=request.POST.get("to_station","")
            request.session['to_station'] =c
            request.session['from_station'] =b
            request.session['journey_date'] =a
            w.append(request.session.get('journey_date'))
            w.append(request.session.get('from_station'))
            w.append(request.session.get('to_station'))
            
           
            request.session['w'] =w

            o=a
            t=info.objects.all()
            l=[]
            uiop=[]
            uidates=[]
            for i in t:
                opq=(i.s_1).split()
                if i.date == request.session.get('journey_date') and request.session.get('from_station') in i.s_1 and c in i.s_1 and b!=c and opq.index(c) > opq.index(b) :
                    if i.id_1 !="":
                        l.append(i.id_1)
                        uiop.append(i.id_1)
                        uidates.append(i.date)

                        y.append(i)
            request.session['uiop']=uiop
            request.session['uidates']=uidates

          
         
            h=l[:]

   
            request.session['h']=h
            request.session['l']=l
            return redirect("search_results")
    

        
           

           
            
   
        return render(request,"train/search.html")
ui=0

def search_result(request):
    global ui
    ui=0


    if request.method=="POST":
        
        a=request.POST.get("train_id","152")
        request.session['train_id']=a
      
        ui=a
        
    
        return redirect("customer")


        
      

    

    warn=""
    if len(request.session.get('h')) == 0:
        warn="NO TRAINS TO SHOW"
    io=request.session.get('l')
    dater=request.session.get('uidates')
    

    ya=[]
    for i in range(len(io)):
        

        ya.append(info.objects.get(id_1=int(io[i]),date=dater[i]))
    

        

   

   

    

 
    return render(request,"train/search_result.html",{"search":ya,"extra":request.session.get('w'),"WARNING":warn})
import random

def unique_refrence_number(num_references):


 generated_numbers = set()


 while len(generated_numbers) < num_references:
 
   random_number = random.randint(10000, 99999)


   if random_number not in generated_numbers:
  
     generated_numbers.add(random_number)


 return list(generated_numbers)
from django.core.mail import send_mail
def booking(request):
   
    if request.method=="POST":
        a=request.POST.get("name","12")
        b=request.POST.get("email","12")
        c=request.POST.get("number","")
        d=request.POST.get("age","12")
        e=request.POST.get("gender","12")
        f=request.POST.get("meal","12")
        global ui
        g=ui
        h=o
      
      

        t=info.objects.get(id_1=g,date=h)

        if t.seats>=int(c):
            e=wallet.objects.get(name=request.user.username)
            if e.amount>=int(c)*(t.fareg):
                e.amount=e.amount-(int(c)*(t.fareg))

                t.seats=t.seats-int(c)
                y=passengers(name=a,train_id=g,mobile=c,date=h,age=d,gender=e,email=b,meal=f)
                y.save()
                send_mail(
        subject="Ticket confirmation",
        message="Your journey details are"+a+'\n'+b+str(g)+str(t.seats)+str(c),
        from_email=None, # use DEFAULT_FROM_EMAIL if None
        recipient_list=["kalravyoma10@gmail.com"],)
            else:
                return HttpResponse("YOU DONT HAVE MONEY TO BOOK TICKET")
        else:
            
            send_mail(
        subject="Ticket confirmation",
        message="Your ticket cant be booked",
        from_email=None, # use DEFAULT_FROM_EMAIL if None
        recipient_list=["kalravyoma10@gmail.com"],
)


            
        

        

    return render(request,"train/booking.html")
@login_required
def wallet1(request):
    opi=0
    if request.method=="POST":
        a=request.POST.get("vyoma","")
        name=request.user.username
        y=wallet.objects.all()
        c=0

        for i in y:
            if i.name == name:
                c=c+1
        print(c)
        if c==0:
                
                
                 
            u=wallet(name=name,amount=a)
            u.save()
        else:
            u=wallet.objects.get(name=name)
            u.amount=u.amount+int(a)
            u.save()
        return redirect("custview")
    try:
        opi=wallet.objects.get(name=request.user.username).amount# This will raise a ZeroDivisionError
    except wallet.DoesNotExist:
        opi=0
    

     

   
   


        


    return render(request,"train/wallet.html",{"amount":opi})

from django.shortcuts import render
q=0
n=0
p=[]


@login_required
def process_data(request):
    if request.method == 'POST':
        # Access form data dynamically using a loop
        customer_data = []
        
        global ui
        train_id=ui
        global o
        global user
        global q
        global n
      
        g=0
        s=0
        c1=0
        c2=0
        c3=0
        amt=0
      
        
     
        t=info.objects.get(id_1=int(request.session.get('train_id')),date=request.session.get('journey_date'))
        c=int(request.POST.get('customerCount'))
        request.session['customer_count']=c
        data=[]
        
     
      
      

        if t.seatsg>=int(c):
      
            
            e=wallet.objects.get(name=request.user.username)
            
            n=int(c)*(t.fareg)
            #if e.amount>=int(c)*(t.fareg):
                #e.amount=e.amount-(int(c)*(t.fareg))
                #e.save()

            t.seatsg=t.seatsg-int(c)
            y=unique_refrence_number(1)[0]
           


            request.session['refrence_number']=y
            global p
            p.clear()
            we=[]
     

            for i in range(1, int(request.POST.get('customerCount')) + 1):
                b=[]
                customer = {
                'name': request.POST.get(f'name{i}',""),
                'email': request.POST.get(f'email{i}',""),
                'age': request.POST.get(f'age{i}',""),
                'meal': request.POST.get(f'meal{i}',""),
                'gender': request.POST.get(f'gender{i}',""),
                'class': request.POST.get(f'class{i}',""),
                # Add more fields as needed
            }
                amount=0
                if customer["class"] == "3rdAC":
                    amount=t.fare3
                    c3=c3+1
                if customer["class"] == "2ndAC":
                    amount=t.fare2
                    c2=c2+1
                if customer["class"] == "1stAC":
                    amount=t.fare1
                    c1=c1+1
                if customer["class"] == "Sleeper":
                    amount=t.fares
                    s=s+1
                if customer["class"] == "General":
                    amount=t.fareg
                    g=g+1
                amt=amount+amt
                request.session['amount']=amt
                request.session['g']=g
                request.session['s']=s
                request.session['c1']=c1
                request.session['c2']=c2
                request.session['c3']=c3
                

                
                b.append((customer["name"],customer["gender"],customer["email"],customer["meal"],customer["age"],ui,o,y,customer["class"],amount))
                we.append(b[0])
            request.session['data']=we
                
                #u=passengers(name=customer["name"],gender=customer["gender"],email=customer["email"],meal=customer["meal"],age=customer["age"],train_id="2322",date="2024-12-26",unique_id=y)
                #u.save()
                #p=user1(user="rahul",ticket_id=y)
                #p.save()
              
            return redirect("payment")
           
        else:
            return HttpResponse("not enough seats")
                

    


        


        

    else:
   
        return render(request, 'train/customer.html')

a=""
b=0
def view1(request):
            global der
            if der == 0:
                 return render(request,"train/redirect_staff.html")            
            if request.method=="POST":
                global a
                global b
                a=request.POST.get("train_id","")
                b=request.POST.get("Date","")
                return redirect("view")
            return render(request,"train/view1.html")
ta=""
qw=""
def download(request):
    global ta
    global qw
    global der
    if der == 0:
         return render(request,"train/redirect_staff.html")    
    if request.method=="POST":
        ta,qw="",""
        a=request.POST.get("train_id","")
        b=request.POST.get("Date","")
        ta=a
        qw=b
        return redirect("export")
       

    return render(request,"train/download.html")
 
       

def view(request):
        global der
        if der == 0:
             return render(request,"train/redirect_staff.html")        
        l=[]
        v=passengers.objects.all()

        
      
        

       
        for i in v:
            if i.date==b and i.train_id==a:
                l.append(i.name)
            
            
        
        

            
        return render(request,"train/view.html",{"bookings":l})
@login_required
def viewc(request):
    k=[]
    global user
    q=user1.objects.get(user=request.user.username).ticket_id
    t=q.split()
    for i in t:
        u=[]
        r=passengers.objects.all()
        for j in r:
            if j.unique_id==i:
                u.append(i)
                u.append(j.name)
        k.append(u)

    return render(request,"train/viewc.html",{"data":k})
from django.conf import settings
import openpyxl
def export(request):
    global der
    if der == 0:
         return render(request,"train/redirect_staff.html")    
    workbook = openpyxl.load_workbook("train\static\Expenditure.xlsx")
    worksheet = workbook.active
    worksheet.delete_rows(1, worksheet.max_row)
    worksheet.append(["name", "age", "gender", "class", "mobile_number"])
    global ta,qw
    da=passengers.objects.all()

    p=[]
    for i in da:
        l=[]

        if i.train_id == ta and i.date == qw :
         
            l.append((i.name,i.age,i.gender,i.clas,i.mobile))
        p.append(l[0])

    
    data = [["John", 25, "M", "10", "1234567890"],
        ["Jane", 30, "F", "12", "9876543210"]]
    for row in p:
        worksheet.append(row)
    workbook.save("train\static\Expenditure.xlsx")

    

    file=os.path.join(settings.BASE_DIR,'train\static\Expenditure.xlsx')
    fileopened=open(file,'rb')
    return FileResponse(fileopened)
@login_required
def payment(request):
            global q
            
            global n
            global w,g,s,c1,c2,c3
            global amt
            t=request.session.get('amount')

          

            
            if request.method=="POST":
                        p=request.session.get('data')
                        e=wallet.objects.get(name=request.user.username)
                
                        
                        if e.amount>=t:
                            e.amount=e.amount-t
                            e.save()
                           
                            rt=info.objects.get(id_1=int(request.session.get('train_id')),date=request.session.get('journey_date'))
                            rt.seatsg=rt.seatsg-int(request.session.get('g'))
                            rt.seatss=rt.seatss-int(request.session.get('s'))
                            rt.seats1=rt.seats1-int(request.session.get('c1'))
                            rt.seats2=rt.seats2-int(request.session.get('c2'))
                            rt.seats3=rt.seats3-int(request.session.get('c3'))
                            rt.save()
                            d=user1.objects.all()
                            n=0
                            for i in d:
                                if i.user == request.user.username:
                                    n=n+1
                            if n == 0:

                                s=user1(user=request.user.username,unique_id=request.session.get('refrence_number'))
                                s.save()
                            elif n == 1 :
                                s=user1.objects.get(user=request.user.username)
                                s.unique_id=s.unique_id+" "+str(request.session.get('refrence_number'))
                                s.save()
                           
                            
                            for i in p:
                                u=passengers(name=i[0],gender=i[1],email=i[2],meal=i[3],age=i[4],train_id=i[5],date=i[6],unique_id=i[7],clas=i[8],fare=i[9],s1=w[0],s2=w[1])
                                u.save()
                                send_mail(
        subject="Ticket confirmation",
        message="Your journey tickets have been booked",
        from_email=None, # use DEFAULT_FROM_EMAIL if None
        recipient_list=[i[2]],)
                            h=journeys(id1=p[0][7],journey=request.session.get('to_station'),price=t,date=request.session.get('journey_date'),time="15:00:00",user=request.user.username)
                            h.save()

                            return redirect("custview")
                        
                        
                        



                        else:

                                            
                            o=passengers.objects.all()
                            for i in o:

                                
                                if i.unique_id == str(q):
                                    print(i.unique_id)
                                    i.delete()
                            
                            r=user1.objects.get(user=request.user.username)
                            r.delete()
                        
                            return HttpResponse("not enough funds")
            my_list=[1,2,47]
            json_string = json.dumps(my_list)
            
                        
      

                        
                            
            


            
            
     
            return render(request,"train/payment.html",{"bill":t,"infos":json_string,"number":1})

import datetime
import random
import json
def login1(request):
    return render(request,'train/google_login.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login1')




    return render (request,'train/sign.html')
def LoginPage(request):

    if request.method=='POST':
        global der
        der=0
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)

        if user is not None:

            login(request,user)
            der=1

        

            return redirect("home")





        else:
            return HttpResponse ("Username or Password is incorrect!!!")
    return render (request,'train/login.html')
@login_required
def custview(request):
    return render(request,"train/custview.html")
def random_time(start_time):

    start_time = datetime.datetime.strptime(start_time, "%H:%M:%S")

    seconds = random.randint(0, 2700)
  
    end_time = start_time + datetime.timedelta(seconds=seconds)

    end_time = end_time.strftime("%H:%M:%S")
   
    return end_time
def h1(request):
    return render(request,'train/basic.html')
id=""
date=""

@login_required
def track1(request):
    global id
    global date
    id=""
    date=""

    if request.method=="POST":
        a=request.POST.get("train_id","")
        b=request.POST.get("date","")
        id=a
        request.session['tracking_id']=a
        request.session['tracking_date']=b
        date=b
        return redirect("tracking")
    return render(request,"train/track1.html")
def add_two_hours(time_str):
  
    time_obj = datetime.datetime.strptime(time_str, "%H:%M:%S")

    new_time_obj = time_obj + datetime.timedelta(hours=2)

    new_time_str = new_time_obj.strftime("%H:%M:%S")
 
    return new_time_str
@login_required
def tracking(request):
    global date
    global id
    l=info.objects.get(date=request.session.get('tracking_date'),id_1=int(request.session.get('tracking_id'))).s_1.split()
    o=[info.objects.get(date=request.session.get('tracking_date'),id_1=int(request.session.get('tracking_id'))).time]
    for i in range(1,len(l)):
        o.append(add_two_hours(o[-1]))
    current_time = datetime.datetime.now().time()
    new_time_list = []
    stations=[]
    for time_str in range(len(o)):

        time_obj = datetime.datetime.strptime(o[time_str], "%H:%M:%S").time()
    
        if time_obj > current_time:
      
            new_time_list.append(o[time_str])
            stations.append(l[time_str])


    

    
    ex_arrival=new_time_list[:]
    fina_arrival=[]
    for i in ex_arrival:
        fina_arrival.append(random_time(i))
    return render(request,"train/tracking.html",{"stations":stations,"extra":new_time_list,"final":fina_arrival})

from django.http import HttpResponse
journey=""

@login_required

def journeys1(request):
  up=[]
  pa=[]
  upj=[]
  paj=[]
  u=[]
  try:
     ticket_ids=(user1.objects.get(user=request.user.username).unique_id).split()

  except user1.DoesNotExist:
   
    return HttpResponse("no bookings have been made")
 

  ticket_ids=(user1.objects.get(user=request.user.username).unique_id).split()
  
  for i in ticket_ids:
        iop=journeys.objects.get(id1=i).date
        
        
        date_obj = datetime.datetime.strptime(iop, "%Y-%m-%d")
       
        
        today_obj = datetime.datetime.today()
        if date_obj > today_obj:
 
            up.append(i)
        elif date_obj < today_obj:
     
            pa.append(i)

   
  for i in up:
    
    upj.append(journeys.objects.get(id1=i).journey)
  for i in pa:
    
    paj.append(journeys.objects.get(id1=i).journey)


  
  small=[]
  big=[]
  if (len(paj) > len(upj)):
      small=upj[:]
      big=paj[:]
  else:
      small=paj[:]
      big=upj[:]
  while len(small) < len(big):
    small.append("")





  for x, y in zip(small, big):

    u.append([x, y])


         



  

  if request.method == "POST":

    global journey
    journey=""
   
  





      

    upcoming_journey = request.POST.get("name")
    request.session['cancel_journey']=upcoming_journey
    if upcoming_journey == "":
        return HttpResponse("cant cancel this")
    journey=upcoming_journey

    return redirect("cancel_passenger")

  
    return HttpResponse(upcoming_journey)
  return render(request,"train/journeys.html",{"pa":pa,"up":up,"paj":paj,"upj":upj,"u":u})
@login_required
def cancelp(request):
    global journey
    global user
    u=journeys.objects.get(journey=request.session.get('cancel_journey'),user=request.user.username).id1
    t=journeys.objects.get(journey=request.session.get('cancel_journey'),user=request.user.username).time
    y=journeys.objects.get(journey=request.session.get('cancel_journey'),user=request.user.username).date

    date_obj = (datetime.datetime.strptime(y, "%Y-%m-%d")).date()

    time_obj = (datetime.datetime.strptime(t, "%H:%M:%S")).time()
  
    datetime_str = datetime.datetime.combine(date_obj, time_obj)
    datetime_obj = datetime.datetime.strptime(str(datetime_str), "%Y-%m-%d %H:%M:%S")
    current_datetime = datetime.datetime.now()
    six_hours_ago = datetime_obj - datetime.timedelta(hours=6)
    time_obj = datetime.datetime.strptime(t, "%H:%M:%S")
    current_time = datetime.datetime.now()
 
 
    
    if (current_datetime.strftime("%Y-%m-%d %H:%M:%S") < six_hours_ago.strftime("%Y-%m-%d %H:%M:%S")) == False:
       

    
        return HttpResponse("Your ticket cant be cancelled")
    elif (current_datetime.strftime("%Y-%m-%d %H:%M:%S") < six_hours_ago.strftime("%Y-%m-%d %H:%M:%S")) == True:
        amount1=journeys.objects.get(journey=request.session.get('cancel_journey'),user=request.user.username).price
        o=wallet.objects.get(name=request.user.username)
        o.amount=o.amount+amount1
        o.save()


        t=user1.objects.get(user=request.user.username)
        string = t.unique_id
        word_to_remove = u
        new_string = string.replace(word_to_remove, "")
        t.unique_id=new_string
        t.save()
        r=passengers.objects.all()

        for i in r:
            if i.unique_id == u :
                i.delete()

        return HttpResponse("done")
import datetime
from datetime import datetime

uiq=""
def find_nearest_upcoming_date(current_date_string, date_list, date_format="%Y-%m-%d"):
    current_date =datetime.datetime.strptime(current_date_string, date_format)
    future_dates = [datetime.datetime.strptime(date, date_format) for date in date_list if datetime.datetime.strptime(date, date_format) > current_date]
    if not future_dates:
        return "No upcoming dates found"
    nearest_upcoming_date = min(future_dates)
    return nearest_upcoming_date.strftime(date_format)

def update(request):
    global der
    if der == 0:
        return render(request,"train/redirect_staff.html")    
    global uiq
    uiq=""
    if request.method=="POST":
        a=request.POST.get("train_id","")
        b=request.POST.get("time","")
        c=request.POST.get("schedule","")
        d=request.POST.get("fare","")
        request.session['update_id']=a
       
        s=train.objects.get(train_id=a)
        if b!="":
            s.time=b
        if c!="":
            s.days=c
        if d!="":
            s.fareg=s.fareg+int(d)
            s.fares=s.fares+int(d)
            s.fare1=s.fare1+int(d)
            s.fare2=s.fare2+int(d)
            s.fare3=s.fare3+int(d)
        s.save()
        u=train.objects.get(train_id=a)
        yu=info.objects.all()
        for i in yu:
            if i.id_1 == int(a):

                i.delete()
        dates=[]
        
        
        
        y=u.days
        for i in y:
            weekdays(i)
        ui=info.objects.all()
        for j in ui:
            dates.append(j.date)

        
        op=passengers.objects.all()
        for i in op:
            if i.train_id == a and (i.date in dates) == False :
                i.date=find_nearest_upcoming_date(i.date,dates)
                i.save()
                send_mail(
        subject="Journey update",
        message="Your journey date have changed of ticket id"+a+"to"+i.date,
        from_email=None, 
        recipient_list=["kalravyoma10@gmail.com"],)

        
        
            



        

            
  
       

    return render(request,"train/update.html")
import datetime
def weekdays(weekday,request):
   """Prints dates of all specified weekdays until the end of 2025.

   Args:
       weekday: The weekday name (e.g., "Monday", "Tuesday", etc.)
   """

   today = datetime.date.today()  
   end_date = datetime.date(2025, 12, 31)  

   weekday_index = {
       "M": 0,
       "T": 1,
       "W": 2,
       "Th": 3,
       "F": 4,
       "Sat": 5,
       "S": 6
   }




   weekday_index_num = weekday_index[weekday.title()]
   a=train.objects.get(train_id=request.session.get('update_id'))
   c=a.name
   seatss=a.seatss


  


   days_to_advance = (weekday_index_num - today.weekday()) % 7

   current_date = today + datetime.timedelta(days=days_to_advance)  

   while current_date <= end_date:
        
        u=info(name=c,id_1=uiq,date=current_date.strftime("%Y-%m-%d"),seatss=seatss,seatsg=a.seatsg,seats1=a.seats1,seats2=a.seats2,seats3=a.seats3,s_1=a.s1,fare1=a.fare1,fare2=a.fare2,fare3=a.fare3,fares=a.fares,fareg=a.fareg,time=a.time)
        u.save()
        current_date += datetime.timedelta(days=7) 
@login_required
def passeng(request,id):
    pa=[]
    
    ticket_id=str(id)
    u=passengers.objects.all()
            
    for i in u:
        if i.unique_id == ticket_id :
            pa.append(i)


    return render(request,"train/passenger_info.html",{"passengers":pa,"id":id})
@login_required
def edit_passenger(request,passenger_id):
    passenger = passengers.objects.get(id=passenger_id)

    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email') 

    
        if not name:
          
            return render(request, 'train/edit_passenger.html', {'passenger': passenger, 'error': 'Please enter a name.'})

    
        passenger.name = name
        passenger.email = email 
        passenger.save()

        return redirect('custview') 

    else:
 
        return render(request, 'train/edit_passenger.html', {'passenger': passenger})
@login_required
def show(request):
    up=[]
    pa=[]
    upj=[]
    paj=[]
    u=[]
    try:
     
     ticket_ids=(user1.objects.get(user=request.user.username).unique_id).split()
 
    except user1.DoesNotExist:
   
        return HttpResponse("no bookings have been made")
    
   
  
    for i in ticket_ids:
        
        date_obj = datetime.datetime.strptime(journeys.objects.get(id1=i).date, "%Y-%m-%d")
        today_obj = datetime.datetime.today()
        if date_obj > today_obj:
 
            up.append(i)
        elif date_obj < today_obj:
   
            pa.append(i)
   
    for i in up:
    
        upj.append(journeys.objects.get(id1=i).journey)
    small=[]
    big=[]
    if (len(upj) > len(u)):
      small=upj[:]
      big=up[:]
    else:
      small=up[:]
      big=upj[:]
    while len(small) < len(big):
        small.append("")
    
    for x, y in zip(small, big):
  
        u.append([x, y])
    return render(request,"train/pre_show.html",{"ids":up,"upj":upj,"u":u})
def H5(request):
    return redirect("search")




    

   





   

 






            
                
            


    









            




    

    




# Create your views here.