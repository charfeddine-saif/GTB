from django.contrib import admin

# Register your models here.
from .models import Noeud, Lampe 


class LampeInline(admin.TabularInline):
    model = Lampe

class NoeudAdmin(admin.ModelAdmin):
    inlines = [
        LampeInline,
    ]

admin.site.register(Noeud, NoeudAdmin)
admin.site.register(Lampe)