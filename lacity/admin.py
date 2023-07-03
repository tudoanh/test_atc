from django.contrib import admin
from .models import Council, Document, Voter, Vote, Activity


class CouncilAdmin(admin.ModelAdmin):
    list_display = ("id", "council_id", "title", "url", "data")
    search_fields = ("id", "council_id", "title", "url", "data")


class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "council", "date", "title", "url", "data")
    search_fields = ("id", "council", "date", "title", "url", "data")

class ActivityAdmin(admin.ModelAdmin):
    list_display = ("id", "council", "date", "activity")
    search_fields = ("id", "council", "date", "activity")

class VoterAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

class VoteAdmin(admin.ModelAdmin):
    list_display = ("council", "voter",)
    search_fields = ("council", "voter",)


admin.site.register(Council, CouncilAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Voter, VoterAdmin)
admin.site.register(Vote, VoteAdmin)