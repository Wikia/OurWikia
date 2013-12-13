from django.contrib import admin
import models

admin.site.register(models.Wiki)
admin.site.register(models.Story)
admin.site.register(models.WikiaUser)
admin.site.register(models.Comment)
admin.site.register(models.UpVote)
admin.site.register(models.DownVote)

