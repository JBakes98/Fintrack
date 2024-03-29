from django.contrib import admin
from sector.models import Sector


class SectorAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': (
            'name',
        )}),
    )

    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(Sector, SectorAdmin)
