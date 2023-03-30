from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Problems)
admin.site.register(Events)
admin.site.register(EventComments)
admin.site.register(ProblemComments)
admin.site.register(Orgs)

