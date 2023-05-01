# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import HttpResponse,HttpResponseRedirect
from .models import CustomUser
from django.views import View
from .models import *
from allauth import *
from django.contrib.auth import logout
import allauth
from allauth.account.views import get_adapter
from allauth.account.views import LogoutFunctionalityMixin
# from .signals import employee_activity_signal
from django.utils import timezone
from datetime import datetime,date
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import calendar
from datetime import datetime, timedelta
from django.shortcuts import render
from .models import Attendance
import calendar
from calendar import HTMLCalendar
from .forms import *
import openpyxl
# from allauth import socialaccount
from django.contrib import admin
from allauth.socialaccount.models import SocialAccount
from.models import EmailValidation
from django.contrib.auth.decorators import permission_required
from.models import EmployeeAttendancePermission
# from allauth import 




# from .models import Status
# Create your views here.   



# def loginpage(request):
#     return render(request,'loginpage.html')
# def login(request):
#     if request.method=='POST':
#         # email = user.email
#         username = request.POST['username']
#         password = request.POST['password']
#         # email = request.POST['email']
        # user = auth.authenticate(username=username,password=password)
        # if user is not None:
        #     auth.login(request,user)
        #     return render(request,'Homepage/home.html',{'name':request.user.username})
#         else:
#             return HttpResponse("Invalid User!")
#     elif request.method=='GET':
#         return render(request, 'loginpage.html')

# def logout(request):
#     auth.logout(request)
#     return HttpResponse("Log out Successfull!")


# def registeruser(request):
#     return render(request,'registeruser/register.html')

# any_view = LogoutFunctionalityMixin()
# log_out = any_view.logout()


# def googlogout(request):
#     view = LogoutFunctionalityMixin.as_view()
#     return view(request)

@login_required
def signin(request):
    # try:
        if EmailValidation.objects.filter(email=request.user.email, is_active = True).exists():
            userr = EmailValidation.objects.get(email = request.user.email)
            username = userr.username
            idus = userr.id
            data = Regularization.objects.all()
            if data:
                for d in data:
                    man = d.emp.manager
            queryreg = "select * from app_Regularization where %s == %s and is_approved IS NULL"
            try:
                regdata = Regularization.objects.raw(queryreg,[man,idus])
            except:
                regdata = Regularization.objects.all()
            tdate = date.today()
            reg = userr.region.id   
            print(reg)
            query = "select * from app_AllHolidays WHERE date > %s and region_id = %s ORDER BY date limit 3"
            holidays = AllHolidays.objects.raw(query,[tdate,reg])
            null= 'null'
            if Attendance.objects.filter(username = request.user.email, signout__isnull = True).last() and (Attendance.objects.filter(username = request.user.email, signout__isnull = True).last()).date == (timezone.localtime(timezone.now()).date()):
                null = '1'
            leaves=Leaves.objects.all().filter(Is_approved=None)

            #For Permissions
            key=EmailValidation.objects.filter(email=request.user.email).values_list('permissions')
            perm=[t[0] for t in key]
            permuser = CustomUser.objects.get(email=request.user.email)
            
            for i in perm:
                print(i)
                permuser.user_permissions.add(i)
            
            
            for i in range(1,100):
                if i not in perm:
                    print(i)
                    permuser.user_permissions.remove(i)

            #For Groups
            keys=EmailValidation.objects.filter(email=request.user.email).values_list('groups')
            gr=[t[0] for t in keys]
            user34 = CustomUser.objects.get(email=request.user.email)
             
            for x in gr:
                user34.groups.add(x)
            
            for i in range(1,70):
                if i not in gr:
                    user34.groups.remove(i)

            le=leaves.count()
            EmailValidations = EmailValidation.objects.all()

            context = {
                'regdata':regdata,
                'holidays': holidays,
                'signin' : null,
                'count':le,
                'leaves':list(leaves),
                'EmailValidations' : EmailValidations,
                'username':username,
            }
            return render(request,'Homepage/home.html',context) 
        else:
            logout(request)
            return HttpResponse("Email is not valid")
        

def registeruser(request):
    if request.method=='POST':
        firstname = request.POST['firstname']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        cnfpassword = request.POST['cnfpassword']

        if password == cnfpassword:
            if CustomUser.objects.filter(username=username).exists():
                return HttpResponse('Username Taken!')
            else:
                user = CustomUser.objects.create_user(first_name=firstname,last_name=last_name,username=username,password=password,email=email)
                user.save()
                return HttpResponse("User Created Successfully!")
        else:
            return HttpResponse("Password Not Matching!")   
    return render(request,'registeruser/register.html')
    #New One


def updation(request):
    alluser = CustomUser.objects.all()
    context = {
        'alluser':alluser,
    }
    return render(request,'recent/updation.html',context)

# def updateempp(request,id):
#     data = CustomUser.objects.get(id=id)
#     data.first_name == 'don1'
#     data.save()
#     return HttpResponse("Jamla bhau!")

# @permission_required("app.add_customuser", login_url='/accounts/google/login/')
# @permission_required("app.delete_customuser", login_url='/accounts/google/login/')

@permission_required("app.view_customuser", login_url='/accounts/google/login/')
def alteremp(request):
    data = EmailValidation.objects.all()
    context = {
        'data': data,
    }
    return render(request,"Admin/altemp.html",context)


def newupdate(request,id):
    empid = CustomUser.objects.get(id=id)
    alluser = CustomUser.objects.all()
    roles = Role.objects.all()
    context = {
        'alluser' : alluser,
        'empid' : empid,
        'roles' : roles,
    }
    # messages.info(request, "Holiday Added!")
    return render(request, 'recent/newupdate.html',context)

def createstatus(request,id):
    data = CustomUser.objects.get(id=id)
    x = request.POST['newstatus']
    data.roles_id = x
    data.save()
    messages.info(request, "Updated!")
    return render(request,'recent/newupdate.html')

def updateppl(request,id):
    data = EmailValidation.objects.get(id=id)
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        contact = request.POST['contact']
        gender = request.POST['gender']
        jdate = request.POST['jdate']
        region = request.POST['region']
        manager = request.POST['manager']
        econtact = request.POST['econtact']
        bloodgroup = request.POST['bloodgroup']
        username = request.POST['username']
        dob = request.POST["dob"]
        address = request.POST["address"]
        designation = request.POST["designation"]
        hr = request.POST["hr"]
        eemail = request.POST["eemail"]
        role = request.POST["role"]
        active = request.POST.get('active')
        permission = request.POST.getlist('permission')

        data.first_name = firstname
        data.last_name = lastname
        data.email = email
        data.contact = contact
        data.gender = gender
        data.date_joined = jdate
        data.username = username
        data.date_of_birth = dob
        data.address = address
        data.designation = designation
        data.hr = hr
        data.emergency_contact = econtact
        data.date_joined = jdate
        data.region_id = region
        data.blood_group = bloodgroup
        data.emergency_email = email
        data.is_active = active
        data.manager = manager
        data.eemail = eemail
        data.roles_id = role
        

        if active == "on":
            data.is_active = True
        else:
            data.is_active = False
        data.save()


        theperm = Role.objects.filter(id = role).values_list('permissions')

        print(theperm)

        perm=[t[0] for t in theperm]
    
        permuser = EmailValidation.objects.get(email=email)
        
        for i in perm:
            permuser.permissions.clear()
            permuser.permissions.add(i)
        
        for i in range(1,50):
            if i not in perm:
                permuser.permissions.remove(i)

        # if permission:
        #     ppp = []
        #     for per in permission:
        #         pr = Permission.objects.get(codename=per)
        #         ppp.append(pr)
        #         print(ppp)
        #     data.permissions.set(ppp)
        # else:
        #     data.permissions.clear()
        
        
        # if role == "1":
        #     g = Group.objects.get(name="Admin")
        #     data.groups.clear()
        #     data.groups.add(g)
        # elif role == "2":
        #     g = Group.objects.get(name="HR")
        #     data.groups.clear()
        #     data.groups.add(g)
        # elif role == "3":
        #     g = Group.objects.get(name="Manager")
        #     data.groups.clear()
        #     data.groups.add(g)
        # elif role == "4":
        #     g = Group.objects.get(name="Employee")
        #     data.groups.clear()
        #     data.groups.add(g)

        messages.success(request, "Employee Updated Successfully")
        return redirect(alteremp)
        # return HttpResponse("Employee Updated Successfully!")
    regiondata = Region.objects.all()
    print(regiondata)
    user = EmailValidation.objects.all()
    roless = Role.objects.all()
    Manager = EmailValidation.objects.filter(roles__role='Manager')
    HR = EmailValidation.objects.filter(roles__role='HR')
    groups = Group.objects.all()
    g = data.groups.all()
    p = data.permissions.all()

    context = {
        'regiondata':regiondata,
        'user':user,
        'roless':roless,
        'Manager':Manager,
        'HR':HR,
        'data':data,
        'groups':groups,
        'g':g,
        'p':p,
        'is_checked':True,
    }
    return render(request,"Admin/updateemp.html",context)

            
    


def addnewstatus(request):
    if request.method == "POST":
        x = request.POST['nstatus']
        news = Role(role = x)
        permission = request.POST.getlist('permission')
        news.save()
        ppp = []
        for per in permission:
            pr = Permission.objects.get(codename=per)
            print(pr)
            ppp.append(pr)
            print(ppp)
            news.permissions.set(ppp)
        return HttpResponse('Status Created Successfully')
    groups = Group.objects.all()
    context = {
        'groups':groups,
    }
    return render(request, 'Admin/addnewstatus.html',context)


# Alter Employee



def addemp(request):
    user = request.user
    if request.method == "POST":
        # id = 23454
        updatedby = EmailValidation.objects.filter(email = request.user.email).values_list('email')
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        contact = request.POST['contact']
        gender = request.POST['gender']
        jdate = request.POST['jdate']
        region = request.POST['region']
        manager = request.POST['manager']
        econtact = request.POST['econtact']
        bloodgroup = request.POST['bloodgroup']
        username = request.POST['username']
        dob = request.POST["dob"]
        address = request.POST["address"]
        designation = request.POST["designation"]
        hr = request.POST["hr"]
        eemail = request.POST["eemail"]
        role = request.POST["role"]
        activ = request.POST["active"]
        permission = request.POST.getlist('permission')
        updatedon = datetime.now()
        print(permission)
        if activ == "on":
            active = True
        else:
            activ = False
        if EmailValidation.objects.filter(username=username,email=email).exists():
            messages.info(request, "Username/Email Taken.")
            return redirect(addemp)
        else:
            data = EmailValidation(first_name = firstname, last_name=lastname, email = email, contact = contact,updated_on = updatedon,region_id=region,manager = manager, updated_by = updatedby,blood_group = bloodgroup, emergency_contact = econtact, date_joined = jdate, username = username , date_of_birth = dob, address = address, designation = designation,hr=hr,emergency_email = eemail, is_active = active, roles_id = role)
            data.save()

            theperm = Role.objects.filter(id = role).values_list('permissions')

            print(theperm)
            print("Above is codename")

            perm=[t[0] for t in theperm]
        
            permuser = EmailValidation.objects.get(email=email)
            
            for i in perm:
                permuser.permissions.add(i)
            
            for i in range(1,50):
                if i not in perm:
                    permuser.permissions.remove(i)

            # ppp = []
            # print("above is permission")
            # for per in permission:
            #     pr = Permission.objects.get(codename=per)
            #     ppp.append(pr)
            #     print(ppp)
            #     data.permissions.set(ppp)
            # if role == "1":
            #     g = Group.objects.get(name="Admin")
            #     data.groups.add(g)
            # elif role == "2":
            #     g = Group.objects.get(name="HR")
            #     data.groups.add(g)
            # elif role == "3":
            #     g = Group.objects.get(name="Manager")
            #     data.groups.add(g)
            # elif role == "4":
            #     g = Group.objects.get(name="Employee")
            #     data.groups.add(g)
            messages.success(request, "Employee Created Successfully")
            return redirect(addemp)
        

    regiondata = Region.objects.all()
    print(regiondata)
    # user = CustomUser.objects.all()
    roless = Role.objects.all()
    Manager = EmailValidation.objects.filter(roles__role='Manager')
    HR = EmailValidation.objects.filter(roles__role='HR')
    groups = Group.objects.all()
    context = {
        'regiondata':regiondata,
        'user':user,
        'roless':roless,
        'Manager':Manager,
        'HR':HR,
        'groups':groups,
        'is_checked':True,
        # 'groups_permissions':groups_permissions,
    }
    return render(request,"Admin/addemp.html",context)

def inactive(request,id):
    data = CustomUser.objects.get(id=id)
    if data.is_active:
        data.is_active = False
    elif data.is_active == False:
        data.is_active = True
    data.save()
    messages.info(request, "Employee Status Changed!")
    return redirect(alteremp)
    # return HttpResponse("Employee Activation Status is Changed.")


# Add Holiday

@permission_required("app.add_holidaypermission", login_url='/accounts/google/login/')
@permission_required("app.delete_holidaypermission", login_url='/accounts/google/login/')
def addholiday(request):
    if request.method == "POST":
        region = request.POST["region"]
        date = request.POST["date"]
        year = request.POST["year"]
        occasion = request.POST["occasion"]
        updated_by = request.user.id
        updated_on = timezone.localtime(timezone.now())
        data = AllHolidays(region_id = region, date = date, year = year, occasion=occasion,updated_by = updated_by,updated_on = updated_on) 
        data.save()
        messages.info(request, "Holiday Added!")
        # return HttpResponse("Holiday Added")
    regiondata = Region.objects.all()
    context = {
        'regiondata' : regiondata,
    }   
    return render(request, 'Admin/addholiday.html',context)

def holidayview(request):
    data = AllHolidays.objects.all()
    context = {
        'data':data,
    }
    return render(request,'Admin/holidayview.html',context)

def regularization(request):
    if request.method == "POST":
        em = EmailValidation.objects.get(email = request.user.email)
        print(em)
        emp = em.id
        date = request.POST['date']
        todate = request.POST['todate']
        reason = request.POST['reason']
        updated_by = request.user.id
        updated_on = timezone.localtime(timezone.now())
        applied_on = timezone.localtime(timezone.now())
        data = Regularization(emp_id = emp, date = date,todate = todate, reason = reason,updated_by=updated_by,updated_on=updated_on,applied_on = applied_on)
        data.save()
        messages.info(request, "Regularization Applied!")
        return redirect(regularization)
    data = Regularization.objects.all()
    context = {
        'data': data,
    }
    return render(request, 'Attendance_Regularization/regularization.html',context)


# Employee Request

@permission_required("app.view_employeerequestpermission", login_url='/accounts/google/login/') 
def employeerequest(request):
    us = EmailValidation.objects.get(email = request.user.email)
    user = us.id
    print(user)
    data = Regularization.objects.all()
    if data:
        for d in data:
            man = d.emp.manager
    queryreg = "select * from app_Regularization where %s == %s and is_approved IS NULL"
    leaves = Leaves.objects.all()
    specificleaves=Leaves.objects.all().filter(Is_approved=None)
    le=specificleaves.count()
    try:
        regdata = Regularization.objects.raw(queryreg,[man,user])
    except:
        regdata = Regularization.objects.all()
    context = {
        'regdata':regdata,
        'leaves':leaves,
        'specific':le,
    }
    return render(request, 'Manager/emprequest.html',context)

def approverequest(request,id):
    data = Regularization.objects.get(id=id)
    data.is_approved = True
    data.approved_by = request.user.id
    data.approved_on = timezone.localtime(timezone.now())
    data.updated_on = timezone.localtime(timezone.now())
    data.updated_by = request.user.id
    data.save()
    messages.info(request, "Approved")
    # send_mail(
    #     'Regularization Status',
    #     'Regualarization Request Approved',
    #     'csea539samyakbendre@gmail.com',
    #     ['samyak.bendre@amnetdigital.com'],
    #     fail_silently=False,
    # )
    return redirect(employeerequest)
    
def rejectrequest(request,id):
    data = Regularization.objects.get(id=id)
    data.is_approved = False
    data.updated_on = timezone.localtime(timezone.now())
    data.updated_by = request.user.id
    data.save()
    messages.info(request, 'Rejected')
    return redirect(employeerequest)

def requests(request):
    data = EmailValidation.objects.get(email = request.user.email)
    user = data.id
    print(user)
    data = Regularization.objects.all()
    if data:
        for d in data:
            emp = d.emp.id
            print(emp)
    queryreg = "select * from app_Regularization where %s == %s order by date"
    try:
        regdata = Regularization.objects.raw(queryreg,[emp,user])
        regdata = Regularization.objects.filter()
        print(regdata)
    except:
        regdata = Regularization.objects.all()
    context = {
        'regdata':regdata,
    }
    return render(request, 'Attendance_Regularization/requests.html',context)

# Emp Holiday View


def empholidayview(request):
    tdate = date.today()
    data = EmailValidation.objects.get(email = request.user.email)
    reg = data.region.id
    query = "select * from app_AllHolidays WHERE date > %s and region_id = %s ORDER BY date"
    holidays = AllHolidays.objects.raw(query,[tdate,reg])
    context = {
        'holidays':holidays,
    }
    return render(request,'Holidays/holidays.html',context)


#Logout

def logout_view(request):
    logout(request)
    return redirect('/accounts/google/login/')



@permission_required('app.view_employeeattendancepermission', login_url='/accounts/google/login/') 
def hrempattendance(request):
    import calendar
    if request.method == "POST":
        email=request.POST['email']
        month=request.POST['month']
        year=request.POST['year']


        cal = calendar.monthcalendar(int(year), int(month))  # Get calendar object for specified month and year 
        # Create list of weekend dates
        weekend_dates = []
        for week in cal:
            sat = week[calendar.SATURDAY]
            sun = week[calendar.SUNDAY]
            if sat != 0:
                weekend_dates.append(int(sat))
            if sun != 0:
                weekend_dates.append(int(sun))

        attend_dates = Attendance.objects.filter(username = email,date__year=year,date__month=month).values_list('date').distinct()
        holiday_list = AllHolidays.objects.filter(date__year=year,date__month=month).values_list('date')
        casual_leave= Leaves.objects.filter(Emp__email = email, Leave_date__year=year,Is_approved=True,Leave_date__month=month,Leave_type="Casual").values_list('Leave_date').distinct()
        print(casual_leave)
        paternity_leave= Leaves.objects.filter(Emp__email = email, Leave_date__year=year,Is_approved=True,Leave_date__month=month,Leave_type="Paternity").values_list('Leave_date').distinct()
        regularize = Regularization.objects.filter(emp__email = email, date__year=year,date__month=month,is_approved=True).values_list('date').distinct()
        attend_list = [t[0].day for t in attend_dates]
        holiday_list = [t[0].day for t in holiday_list]
        c_list= [t[0].day for t in casual_leave]
        print(c_list)
        p_list= [t[0].day for t in paternity_leave]
        regularise_list= [t[0].day for t in regularize ]
        present=0
        count=0
        p=0
        for i in attend_list:
            if i != None :
                if int(i) not in holiday_list  and int(i) not in c_list and int(i) not in p_list and  int(i) not in weekend_dates:
                    present=present+1
        for i in regularise_list:
            if i != None :
                if int(i) not in holiday_list  and int(i) not in c_list and int(i) not in p_list and  int(i) not in weekend_dates:
                    present=present+1

        for i in c_list:
            count=count+1
        for i in p_list:
            p=p+1
        data = EmailValidation.objects.all()
        context={"present":present,"ccount":count,"pcount":p,"month":month,"year":year,"email":email,"c_list":c_list,"p_list":p_list,"data":data}
        return render(request,"HR/attendanceinfo.html",context)
    else:
        data = EmailValidation.objects.all()
        context = {
            'data':data,
        }
        return render(request,"HR/attendanceinfo2.html",context)
    



from django.utils.html import conditional_escape as escape
now=datetime.now()

def attendance(request,year=now.year,month=now.month):
    now=datetime.now()
    startmonth=2
    startyear=2023
    total=2025
    email=request.user.email
    regions = EmailValidation.objects.get(email = request.user.email)
    region = regions.region.id

    if request.method == "POST":
        year=int(request.POST['year'])
        month=int(request.POST['month'])
    # current_year=now.year
    # current_month=now.month
    if(int(year) >= int(startyear) and int(year)+int(month)>=int(total)):
        holiday_list = AllHolidays.objects.filter(region = region,date__year=year,date__month=month).values_list('date')
        usertime = Attendance.objects.filter(username = email,date__year=year,date__month=month).values_list('date').distinct()
        leave = Leaves.objects.filter(Emp__email = email, Leave_date__year=year, Leave_date__month=month,Is_approved=True).values_list('Leave_date').distinct()
        regularize = Regularization.objects.filter(emp__email = email, date__year=year,date__month=month,is_approved=True).values_list('date').distinct()

        my_new_list = [t[0].day for t in usertime]
        my_holiday_list = [t[0].day for t in holiday_list]
        leave_list = [t[0].day for t in leave]
        regularize=[t[0].day for t in regularize]

        calendar = CustomHTMLCalendar(my_new_list,my_holiday_list,month,year,leave_list,regularize) #passing values to customehtmlcalender class
        calendar_html = calendar.formatmonth(year,month)   # displaying the data that we got from above line
        return render(request,'Attendance_Regularization/attendance.html',{"cal":calendar_html , "user":my_new_list })
    else:
        return HttpResponse("<h>data of the month you enetered is not present in our database ...you can check attendance from March-2023")

class CustomHTMLCalendar(HTMLCalendar):
    def __init__(self, my_new_list,my_holiday_list,month,year,leave_list,regularize):
        super().__init__(firstweekday=0)
        self.attendance_list =my_new_list
        self.holiday_list =my_holiday_list
        self.month=int(month)
        self.year=int(year)
        self.leave=leave_list
        self.regularize=regularize

    def formatday(self, day, weekday):
            now=datetime.now()
            
            if day != 0:
                cssclass = self.cssclasses[weekday]
                 
                if day in self.attendance_list or day in self.regularize: 
                    cssclass += ' special-day'  # add custom CSS class to highlight the day
                elif now.month == self.month and now.year==self.year:
                    if day < now.day:
                        cssclass += ' absent'
                elif now.year> self.year:
                    cssclass += ' absent'
                elif now.year==self.year and now.month >self.month:
                    cssclass += ' absent'
                if day in self.leave: 
                    cssclass += ' leave'

                if day in self.holiday_list : 
                    cssclass += ' holiday'
                
                return f'<td class="{cssclass}">{escape(str(day))}</td>'
            return '<td class="noday">&nbsp;</td>'
    

def signinn(request):
    # try:
        user = request.user.email
        today = date.today()
        attend = Attendance.objects.all()
        attend = Attendance(username=user, date=today, signin=timezone.localtime(timezone.now()),day=today.day)
        attend.save()
        messages.success(request,"Signed in")
        # return render(request,'Homepage/home.html',{"signin":1})
        return redirect(signin)
    # except:
    #     return render(request,"logout_sessoin_out.html")

def signoutt(request):
    try:
        username = request.user.email
        today = date.today()
        attend = Attendance.objects.filter(username=username).last()
        attend.signout = timezone.localtime(timezone.now())
        attend.save()
        messages.success(request, "Signed out" )
        # return render(request,'Homepage/home.html',{"signin":null})
        return redirect(signin)
    except:
        return render(request,"logout_sessoin_out.html")
    
def someleave(request):
    form = leaveform()
    if request.method == "POST":
        form = leaveform(request.POST)
        if form.is_valid():
            form.save()
            data = Leaves.objects.last()
            data.Emp_id = request.user.id
            data.save()
            messages.success(request, "Leave is applied")
            return redirect(someleave)
    context = {"forms": form}
    return render(request, "practise/form.html", context)


def someleaverequest(request, pk):
    data = Leaves.objects.get(id=pk)
    forms = leaveform1(instance=data)
    if request.method == "POST":
        forms = leaveform1(request.POST, instance=data)
        if forms.is_valid():
            if data.Leave_type == "Casual":
                data.casual_leaves_left = data.casual_leaves_left - 1
                # messages.success(request,"Leave is approved")
            else:
                data.paternity_leaves_left = data.paternity_leaves_left - 1
                # messages.success(request,"Leave is rejected")
            forms.save()

            return redirect(employeerequest)
    context = {"forms": forms}
    return render(request, "practise/form1.html", context)


def allleavereq(request):
    datas = Leaves.objects.all()
    context = {"datas": datas}
    return render(request, "practise/form2.html", context)

# @permission_required("app.add_leavepermission", login_url='/accounts/google/login/')
@permission_required("app.change_leavepermission", login_url='/accounts/google/login/')
def admin_leave_access(request):
    search1 = EmailValidation.objects.all()
    search = {"search": search1}
    return render(request, "Admin/modifyleave.html", search)


def addleave_emp(request):
    if request.method == "POST":
        email = request.POST["email"]
        num = request.POST["number"]
        data = EmailValidation.objects.get(email=email)
        data.Leaves = data.Leaves + int(num)
        data.save()
        messages.success(request, "Leaves are added")
        return render(request, "Admin/modifyleave.html")
        # return HttpResponse("<h1>leave of an employee updated sucessfuly</h1>")
    else:
        return render(request, "Admin/modifyleave.html")


def addleave_org(request):
    if request.method == "POST":
        num = request.POST["number"]
        data = EmailValidation.objects.all()
        for r in data:
            r.Leaves = r.Leaves + int(num)
            r.save()
        # data.Leaves=data.Leaves+int(num)
        # data.save()
        messages.success(request, "Leaves are added for whole oraganization")
        return render(request, "Admin/modifyleave.html")
        # return HttpResponse("<h1>leave of organisaiton updated sucessfuly</h1>")
    else:
        return render(request, "Admin/modifyleave.html")


# DELETING LEAVES
def deleteleave_emp(request):
    if request.method == "POST":
        email = request.POST["email"]
        num = request.POST["number"]
        data = EmailValidation.objects.get(email=email)
        data.Leaves = data.Leaves - int(num)
        data.save()
        messages.success(request, "Leaves are deleted")
        return render(request, "Admin/modifyleave.html")
        # return HttpResponse("<h1>leave of an employee updated sucessfuly</h1>")
    else:
        return render(request, "Admin/modifyleave.html")


def deleteleave_org(request):
    if request.method == "POST":
        num = request.POST["number"]
        data = EmailValidation.objects.all()
        for r in data:
            r.Leaves = r.Leaves - int(num)
            r.save()
        # data.Leaves=data.Leaves+int(num)
        # data.save()
        messages.success(request, "Leaves are deleted for whole organization")
        return render(request, "Admin/modifyleave.html")
        # return HttpResponse("<h1>leave of organisaiton updated sucessfuly</h1>")
    else:
        return render(request, "Admin/modifyleave.html")


def approveleave(request,pk):
    leave=Leaves.objects.get(id=pk)
    leave.Is_approved=True
    leave.save()
    return redirect(employeerequest)

def rejectleave(request,pk):
    leave=Leaves.objects.get(id=pk)
    leave.Is_approved=False
    leave.save()
    return redirect(employeerequest)
    

def downloadfile(request):
    content1 = request.POST.get('content1')
    content2 = request.POST.get('content2')
    content3 = request.POST.get('content3')
    content4 = request.POST.get('content4')
    content5 = request.POST.get('content5')
    content6 = request.POST.get('content6')
    content7 = request.POST.get('content7')
    # Create a new Excel workbook
    workbook = openpyxl.Workbook()
    # Get the active worksheet
    worksheet = workbook.active

    worksheet['A1'] = content1
    worksheet['A2'] = content2
    worksheet['A3'] = content3
    worksheet['A4'] = content4
    worksheet['A5'] = content5
    worksheet['A6'] = content6
    worksheet['A7'] = content7

    # Setting the content type and filename of the response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="content.xlsx"'
    # Save the workbook to the response
    workbook.save(response)
    return response


def addregion(request):
    if request.method == "POST":
        x = request.POST['region']
        data  = Region(country = x)
        data.save()
        messages.success(request, "Region Added Successfully.")
        return redirect(addregion)
    return render(request,'Admin/addregion.html')


def updateemp(request):
    if request.method == "POST":
        x = request.POST['email']
        data = EmailValidation.objects.get(email = x)
        data
    email = CustomUser.objects.all()
    context = {
        'email':email,
    }
    return render(request, 'Admin/updateemp.html',context)


def deleteholiday(request):
    holidays = AllHolidays.objects.all()
    context = {
        'holidays': holidays,
    }
    return render(request, 'Admin/deleteholiday.html',context)


def dlt(request,id):
    hol = AllHolidays.objects.get(id=id)
    hol.delete()
    messages.success(request, "Holiday Deleted Successfully.")
    return redirect(deleteholiday)