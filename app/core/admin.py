from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'message')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'email', 'message')

