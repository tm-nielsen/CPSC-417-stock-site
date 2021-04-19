from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Exchange)
admin.site.register(Stock)
admin.site.register(Put)
admin.site.register(Call)
admin.site.register(Value_History)
admin.site.register(Histogram_Entry)
admin.site.register(User)
admin.site.register(Viewed_History)
admin.site.register(Watchlist_Entry)
admin.site.register(Analyst)
admin.site.register(Analysis)
