from django.contrib import admin

# Register your models here.

from .models import WatchList,StreamPlatform,Review

admin.site.register(WatchList)
admin.site.register(StreamPlatform)
admin.site.register(Review)





#models for initial lectures
# from .models import Movie

# admin.site.register(Movie)