from django.contrib import admin
from .models import Song, UserInterest, Review
# Register your models here.

class SongAdmin(admin.ModelAdmin):
    list_display = ['name','tag']
    search_fields = ('name', 'tag')
    # prepopulated_fields = {'slug':('name',)}
admin.site.register(Song,SongAdmin)

class UserInterestAdmin(admin.ModelAdmin):
    list_display = ['user','tag','song']
    list_filter = ['user','song']
    # prepopulated_fields = {'slug':('name',)}
admin.site.register(UserInterest,UserInterestAdmin)
    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user','song','rating','review']    
admin.site.register(Review,ReviewAdmin)
