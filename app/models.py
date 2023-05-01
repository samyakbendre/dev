from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.auth.models import AbstractUser,Group,Permission
# Create your models here.


# class Status(models.Model):
#     status = models.CharField(max_length=100,null=True, blank=True)

#     def __str__(self):
#         return self.status

class Role(models.Model):
    role = models.CharField(max_length=100,default=0)
    groups = models.ManyToManyField(Group,blank=True)
    permissions = models.ManyToManyField(Permission,blank=True)
    def __str__(self):
        return self.role

class Region(models.Model):
    # id = models.PositiveIntegerField(primary_key=True)
    worklocation = models.CharField(max_length=100)

    def __str__(self):
        return self.worklocation


class CustomUser(AbstractUser):
    # email = models.EmailField(unique=True)
    roles = models.ForeignKey(Role, on_delete=models.CASCADE,null=True,blank=True)
    contact = models.IntegerField(default=0,null=True,blank=True)    
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True,blank=True)
    manager = models.PositiveIntegerField(null=True,blank=True,default=0)
    emergency_contact = models.IntegerField(default=0,null=True,blank=True)
    blood_group = models.CharField(max_length=50,null=True,blank=True)
    Leaves=models.IntegerField(default=21)
    emergency_email = models.EmailField(null=True,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    address = models.CharField(max_length=400,null=True,blank=True)
    updated_on = models.DateTimeField(null=True,blank=True)
    updated_by = models.EmailField(null=True,blank=True)
    designation = models.CharField(max_length=100,null=True,blank=True)
    hr = models.PositiveIntegerField(null=True,blank=True,default=0)
    gender = models.CharField(max_length=10,null=True,blank=True)
    
    def __str__(self):
        return self.email
    

class UserActivity(models.Model):
    employee_id = models.PositiveIntegerField()
    path = models.CharField(max_length=255)
    date = models.DateField(default=None)
    time = models.TimeField(default=None)
    duration = models.CharField(max_length=100,default=None)

    def __str__(self):
        return self.path



class EmailValidation(models.Model):
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,default=None,null=True,blank=True)
    first_name = models.CharField(max_length=50, null=True,blank=True)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(Group, blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)
    roles = models.ForeignKey(Role, on_delete=models.CASCADE,null=True,blank=True)
    contact = models.IntegerField(default=0,null=True,blank=True)    
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True,blank=True)
    manager = models.PositiveIntegerField(null=True,blank=True,default=0)
    emergency_contact = models.IntegerField(default=0,null=True,blank=True)
    blood_group = models.CharField(max_length=50,null=True,blank=True)
    Leaves=models.IntegerField(default=21)
    emergency_email = models.EmailField(null=True,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    address = models.CharField(max_length=400,null=True,blank=True)
    updated_on = models.DateTimeField(null=True,blank=True)
    updated_by = models.EmailField(null=True,blank=True)
    designation = models.CharField(max_length=100,null=True,blank=True)
    hr = models.PositiveIntegerField(null=True,blank=True,default=0)
    gender = models.CharField(max_length=10,null=True,blank=True)
    first_name = models.CharField(max_length=30, null=True,blank=True)
    last_name = models.CharField(max_length=30,null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.username
        
    
class AllHolidays(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE,default=1)
    year = models.IntegerField()
    date = models.DateField()
    day=models.IntegerField(null=True,blank=True)
    occasion = models.CharField(max_length=100)
    updated_by = models.PositiveIntegerField(null=True,blank=True)
    updated_on = models.DateTimeField(null=True,blank=True)


    # def __str__(self):
    #     return self.date

    # def __str__(self):
    #     return self.updated_by



class LeaveTypemodel(models.Model):
    # emp = models.ForeignKey(EmailValidation, on_delete = models.CASCADE,null= True,blank=True)
    leave_type = models.CharField(max_length=100, null=True,blank=True)
    no_of_days = models.DecimalField(max_digits=3, decimal_places=1)
    balance = models.DecimalField(max_digits=3, decimal_places=1)

    
class Leaves(models.Model):
    leave_choices = (
        ('Casual','Casual'),
        ('Paternity','Paternity'),
    )
    Emp = models.ForeignKey(EmailValidation,on_delete=models.CASCADE,blank=True,null=True)
    leave_type = models.ForeignKey(LeaveTypemodel, on_delete=models.CASCADE,null=True,blank=True)
    Leave_date=models.DateField()
    Reason=models.CharField(max_length=300)
    Leave_type = models.CharField(max_length=100,choices=leave_choices)
    Is_approved=models.BooleanField(default=None,null=True,blank=True)
    day=models.IntegerField(null=True,blank=True)
    casual_leaves_left=models.IntegerField(default=10,null=True,blank=True)
    paternity_leaves_left=models.IntegerField(default=10,null=True,blank=True)
    # email = models.EmailField(null=True,blank=True)

    def __str__(self):
        return self.Reason

class Regularization(models.Model):
    emp = models.ForeignKey(EmailValidation, on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(null=True,blank=False)
    todate = models.DateField(null=True,blank=True)
    reason = models.CharField(max_length=255)
    applied_on = models.DateTimeField(null=True,blank=True)
    is_approved = models.BooleanField(default=None,null=True,blank=True)
    updated_by = models.PositiveIntegerField(null=True,blank=True)
    updated_on = models.DateTimeField(null=True,blank=True)
    approved_by = models.PositiveIntegerField(null=True,blank=True)
    approved_on = models.DateTimeField(null=True,blank=True)

class Attendance(models.Model):
    emp = models.ForeignKey(EmailValidation, on_delete=models.CASCADE,null=True,blank=True)
    date=models.DateField(max_length=100)
    signin= models.TimeField(max_length=100,default='null')
    signout= models.TimeField(max_length=100,null=True,blank=True)
    username=models.CharField(max_length=50)
    day = models.IntegerField(null=True,blank=True)
    email = models.EmailField(null=True,blank=True)

class AuthenticationLog(models.Model):
    user = models.CharField(max_length = 50,null=True,blank=True)
    timestamp = models.DateTimeField(null=True,blank=True)
    action = models.CharField(max_length=20,null=True,blank=True)
    ip_address = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user} - {self.timestamp} - {self.action} - {self.ip_address}'
    

class EmployeeAttendancePermission(models.Model):
    class Meta:
        permissions = [("Attendance","Attendance")]


class EmployeeRequestPermission(models.Model):
    class Meta:
        permissions = [("employee_request","Employee Request")]


class HolidayPermission(models.Model):
    class Meta:
        permissions = [("holiday","Holiday")]
        
class LeavePermission(models.Model):
    class Meta:
        permissions = [("leave","Leave")]

class RolePermission(models.Model):
    class Meta:
        permissions = [("role","Role")]

# class UserPermission(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('user','permission')

