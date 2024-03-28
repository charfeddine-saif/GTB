from django.contrib import admin
from .models import Noeud, Lampe, Planification

class LampeInline(admin.TabularInline):
    model = Lampe

class NoeudAdmin(admin.ModelAdmin):
    inlines = [
        LampeInline,
    ]

admin.site.register(Noeud, NoeudAdmin)
admin.site.register(Lampe)
admin.site.register(Planification)
