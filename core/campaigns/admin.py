from django.contrib import admin
from .models import Campaign

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'owner')
    search_fields = ('title', 'description', 'owner')
    ordering = ('title',)
    
