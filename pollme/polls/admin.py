from django.contrib import admin
from polls.models import Choice, Poll, Vote


admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Vote)
