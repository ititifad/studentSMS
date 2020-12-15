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
    
@admin.register(Teacher)
class TeacherAdmin(ImportExportModelAdmin):
    pass
    list_display = ('name','title', 'classroom','phone_number')
    list_filter = ('name', 'title', 'classroom','phone_number')
    search_fields = ('name','title','classroom')

#@admin.register(Subject)
#class SubjectAdmin(ImportExportModelAdmin):
    #pass
    #list_display = ('subject_name','subject_code', 'subject_creation_date','subject_update_date')
    #list_filter = ('subject_name', 'subject_code')
    #search_fields = ('subject_name', 'subject_code')
    
@admin.register(Result)
class ResultAdmin(ImportExportModelAdmin):
    pass
    list_display = ('student','classroom', 'subject','score', 'language', 'type', 'status')
    list_filter = ('student','classroom', 'subject','score', 'language', 'type', 'status')
    search_fields = ('student','classroom', 'subject','score')

admin.site.register(Phase)