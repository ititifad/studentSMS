from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    pass
    list_display = ('user', 'name','phone_number', 'location', 'gender')
    search_fields = ('gender', 'location')
    
    
@admin.register(Classroom)
class ClassroomAdmin(ImportExportModelAdmin):
    pass
    list_display = ('name',)
    search_field = ('name',)


@admin.register(Fee)
class FeeAdmin(ImportExportModelAdmin):
    pass
    list_display = ('student', 'classroom','school_fees', 'paid_fees', 'remaining_fees', 'completed','phase')
    list_filter = ('student', 'classroom','school_fees', 'paid_fees', 'remaining_fees')
    search_fields = ('phase', 'school_fees')
    date_hierarchy = 'publish_date'
    ordering = ('school_fees', 'paid_fees', 'publish_date')

admin.site.register(Phase)