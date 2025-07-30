from django.contrib import admin
from .models import GreenPost, ContactMessage, Feedback, VolunteerApplication, Suggestion, ReportIssue, \
    VolunteerRequest, Event

admin.site.register(GreenPost)
admin.site.register(ContactMessage)
admin.site.register(Feedback)
admin.site.register(VolunteerApplication)
admin.site.register(Suggestion)
admin.site.register(ReportIssue)
admin.site.register(Event)


@admin.register(VolunteerRequest)
class VolunteerRequestAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'phone_number', 'area_of_interest', 'availability', 'created_at')
    list_filter   = ('area_of_interest', 'created_at')
    search_fields = ('name', 'email', 'area_of_interest')