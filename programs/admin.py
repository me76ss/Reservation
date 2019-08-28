from django.contrib import admin

# Register your models here.
from .models import Program, ProgramSlot, ProgramSlotRecord


class ProgramSlotInlineModel(admin.TabularInline):
    model = ProgramSlot


class ProgramAdminModel(admin.ModelAdmin):
    inlines = [ProgramSlotInlineModel]


admin.site.register(Program, ProgramAdminModel)
# admin.site.register(ProgramSlot)
admin.site.register(ProgramSlotRecord)
