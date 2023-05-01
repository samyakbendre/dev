from django.contrib import admin
from .models import CustomUser,EmailValidation,AllHolidays,Region,Regularization,UserActivity,Attendance,Leaves,Role,AuthenticationLog,LeaveTypemodel
# Register your models here.


# admin.site.register(Leaves,LeavesAdmin)
admin.site.register(CustomUser)
admin.site.register(EmailValidation)
admin.site.register(AllHolidays)
admin.site.register(Region)
admin.site.register(Regularization)
admin.site.register(UserActivity)
admin.site.register(Attendance)
admin.site.register(Leaves)
admin.site.register(Role)
admin.site.register(AuthenticationLog)
admin.site.register(LeaveTypemodel)


