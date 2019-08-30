from django.contrib import admin

from .models import Program, ProgramSlot, ProgramSlotRecord


class ProgramSlotRecordInlineModel(admin.TabularInline):
    model = ProgramSlotRecord


class ProgramSlotAdminModel(admin.ModelAdmin):
    inlines = [ProgramSlotRecordInlineModel, ]
    list_display = ['id', 'program_id', 'program_name', 'starts_at', 'ends_at', 'capacity']

    def program_name(self, obj):
        return obj.program.name


class ProgramSlotInlineModel(admin.TabularInline):
    model = ProgramSlot


class ProgramAdminModel(admin.ModelAdmin):
    inlines = [ProgramSlotInlineModel, ]
    list_display = ['id', 'name', 'starts_at', 'ends_at']


admin.site.register(Program, ProgramAdminModel)
admin.site.register(ProgramSlot, ProgramSlotAdminModel)
# admin.site.register(ProgramSlotRecord)
