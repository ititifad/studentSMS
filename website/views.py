from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import (
    FeeForm, StudentForm, 
    StudentSearchForm, 
    StudentFeeSearchForm,
    ClassroomForm, 
    ClassroomSearchForm,
    CreateUserForm,
    StudentsForm, 
    StaffForm,
    ResultsForm
)
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.db.models import Sum, Count
from django.db.models import Q, F, FloatField, ExpressionWrapper
from django.views.generic import View, DetailView, ListView
from easy_pdf.views import PDFTemplateResponseMixin
from django.template.loader import get_template
from .utils import render_to_pdf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from .decorators import allowed_users, admin_only
from django.urls import reverse_lazy
from django.forms import inlineformset_factory

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        qs = Fee.objects.all().order_by('-publish_date')
        template = get_template('website/fee_pdf.html')
        context = {
            'queryset':qs,
        }
        html = template.render(context)
        pdf = render_to_pdf('website/fee_pdf.html', context)
        return HttpResponse(pdf, content_type='application/pdf')
    
def is_valid_queryparam(param):
    return param != '' and param is not None

@login_required(login_url='login')
@admin_only
def home(request):
    form = StudentFeeSearchForm(request.POST or None)
    qs = Fee.objects.all().order_by('-publish_date')
    student_contains_query = request.GET.get('student_contains')
    students = Student.objects.all()
    classrooms = Classroom.objects.all()
    phases = Phase.objects.all()
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    classroom = request.GET.get('classroom')
    phase = request.GET.get('phase')
    student = request.GET.get('student')
    completed = request.GET.get('completed')
    not_completed = request.GET.get('notCompleted')
    
    if is_valid_queryparam(student_contains_query):
        qs = qs.filter(student__name__icontains=student_contains_query)
        
    if is_valid_queryparam(date_min):
        qs = qs.filter(publish_date__gte=date_min)
        
        
    if is_valid_queryparam(date_max):
        qs = qs.filter(publish_date__lt=date_max)
        
    if is_valid_queryparam(classroom) and classroom != 'Choose...':
        qs= qs.filter(classroom__name=classroom)
        
    if is_valid_queryparam(student) and student != 'Choose...':
        qs= qs.filter(student__name=student)
        
    if is_valid_queryparam(phase) and phase != 'Choose...':
        qs= qs.filter(phase__name=phase)
        
    if completed == 'on':
        qs = qs.filter(completed=True)

    elif not_completed == 'on':
        qs = qs.filter(completed=False)
        
        
    total_students = students.count()
    baby_class = Student.objects.filter(classroom__name="Baby class").count()
    class1 = Student.objects.filter(classroom__name="Class 1").count()
    class2 = Student.objects.filter(classroom__name="Class 2").count()
    class3 = Student.objects.filter(classroom__name="Class 3").count()
    class4 = Student.objects.filter(classroom__name="Class 4").count()
    class5 = Student.objects.filter(classroom__name="Class 5").count()
    class6 = Student.objects.filter(classroom__name="Class 6").count()
    class7 = Student.objects.filter(classroom__name="Class 7").count()
    fees_completed = qs.filter(completed='True').count()
    total_fees_paid = qs.aggregate(sum=Sum('paid_fees'))['sum']
    fees_not_completed = qs.filter(completed='False').count()
    
    context ={
        'queryset':qs,
        'baby_class':baby_class,
        'class1': class1,
        'class2': class2,
        'class3': class3,
        'class4': class4,
        'class5': class5,
        'class6': class6,
        'class7': class7,
        'students' : students,
        'total_fees_paid': total_fees_paid,
        'classrooms' : classrooms,
        'phases' : phases,
        'total_students' : total_students,
        'fees_completed':  fees_completed,
        'fees_not_completed': fees_not_completed,
        'form': form
    }
    
    if request.method == 'POST':
        qs = Fee.objects.all().filter(student=form['student'].value())
        
        context = {
        'queryset':qs,
        'students' : students,
        'classrooms' : classrooms,
        'total_students' : total_students,
        'fees_completed':  fees_completed,
        'fees_not_completed': fees_not_completed,
        'form': form
        }
    return render(request, 'website/home.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def UserPage(request):
    fees = request.user.student.fee_set.all()
    results = request.user.student.result_set.all()
    labels = []
    data = []
    result = Result.objects.all()
    
    
    first_record = request.user.student.fee_set.first()
    school_fees = first_record.school_fees
    
    classroom = request.user.student.classroom
    phone_number = request.user.student.phone_number
    
    paid_fees = request.user.student.fee_set.all().aggregate(total_paid_fees=Sum('paid_fees'))
    
    balance_fees =  school_fees - paid_fees["total_paid_fees"]
    
    if balance_fees == 0:
        messages.info(request, 'Student School fees is Completed')
    
    #total_fees =  student.fee_set.all().filter(student__id=pk).aggregate(sum=Sum('paid_fees', flat=True))['sum']
    total_score = results.aggregate(sum=Sum('score'))['sum']
    for result in results:
        labels.append(result.subject)
        data.append(result.score)
    
    if total_score > 100:
        messages.info(request, 'Student has passed the examination')
    else:
        messages.info(request, 'Student has failed')
        
    status = ''
    if total_score > 100:
        status= 'YES'
    else:
        status = 'NO'
        
    context={'fees': fees,
            "paid_fees": paid_fees,
            "school_fees": school_fees,
            "balance_fees": balance_fees,
            "classroom": classroom,
            "phone_number": phone_number,
            'results': results,
            'total_score': total_score,
            'status': status,
            'labels': labels,
            'data': data
            }
    
    return render(request, 'website/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def AccountSettings(request):
    student = request.user.student
    student_results = request.user.student.results
    student_reports = request.user.student.reports
    form = StudentsForm(instance=student)
    
    if request.method == 'POST':
        form = StudentsForm(request.POST ,request.FILES, instance=student)
        if form.is_valid():
            form.save()
            
    context={'form': form, 'student_results': student_results, 'student_reports': student_reports}
    return render(request, 'website/account_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def student(request, pk):
    qs = Fee.objects.all()
    student = Student.objects.get(id=pk)
    result = Result.objects.all()
    
    fees = student.fee_set.all().order_by('-publish_date')
    #total_fees =  student.fee_set.all().filter(student__id=pk).aggregate(sum=Sum('paid_fees', flat=True))['sum']
    first_record = student.fee_set.first()
    school_fees = first_record.school_fees
    
    paid_fees = student.fee_set.all().aggregate(total_paid_fees=Sum('paid_fees'))
    
    balance_fees =  school_fees - paid_fees["total_paid_fees"]
    
    if balance_fees == 0:
        messages.info(request, 'Student School fees is Completed')
   
    results = student.result_set.all()
    #total_fees =  student.fee_set.all().filter(student__id=pk).aggregate(sum=Sum('paid_fees', flat=True))['sum']
    
    total_score = student.result_set.all().aggregate(sum=Sum('score'))['sum']
    
    #if total_score > 100:
        #messages.info(request, 'Student has passed the examination')
    #else:
        #messages.info(request, 'Student has failed')
        
    #status = ''
    #if total_score > 100:
        #status= 'YES'
    #else:
        #status = 'NO'
    
    context = {"student": student,
               'fees': fees,
               "paid_fees": paid_fees,
               "school_fees": school_fees,
               "balance_fees": balance_fees,
               'results': results,
               'total_score': total_score,
               #'status': status
               }

    #context = {
        #'student' : student,
        #'fees' : fees,
        #'total_fees' : total_fees,
    return render(request, 'website/students.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def students(request):
    form = StudentSearchForm(request.POST or None)
    students = Student.objects.all()
    classrooms = Classroom.objects.all()
    
    context = {
        'form':form,
        'students':students
    }
    
    if request.method == 'POST':
        students = Student.objects.all().filter(name__icontains = form['name'].value())
        context = {
            'form':form,
            'students':students,
            'classrooms':classrooms
        }
    return render(request, 'website/student.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createFee(request, pk):
    student = Student.objects.get(id=pk)
    form = FeeForm(initial={'student':student})
    if request.method == 'POST':
        form = FeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'website/fee_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def UpdateFee(request, pk):
	fee = Fee.objects.get(id=pk)
	form = FeeForm(instance=fee)
	#print('FEE:', fee)
	if request.method == 'POST':

		form = FeeForm(request.POST, instance=fee)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'website/fee_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteFee(request, pk):
	fee = Fee.objects.get(id=pk)
	if request.method == "POST":
		fee.delete()
		return redirect('/')

	context = {'fee':fee}
	return render(request, 'website/delete.html', context)

def createStudent(request):
    form = StudentForm()
    if request.method=='POST':
        form=StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context={
        'form': form
    }
    return render(request, 'website/student_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def UpdateStudent(request, pk):
    student = Student.objects.get(id=pk)
    form = StudentForm(instance=student)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            form = StudentForm()
        context = {'form':form}
        return render(request, 'website/student_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def classrooms(request):
    qs = Fee.objects.all()
    form = ClassroomSearchForm(request.POST or None)
    classrooms = Classroom.objects.all()
    
    context = {
        'form':form,
        'classrooms':classrooms,
    }
    
    if request.method == 'POST':
        classrooms = Classroom.objects.all().filter(name=form['name'].value())
        context = {
            'form':form,
            'classrooms':classrooms
        }
    return render(request, 'website/classroom.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createClassroom(request):
    qs = Fee.objects.all()
    students = Student.objects.all()
    total_students = students.count()
    baby_class = qs.filter(classroom__name="Baby class").annotate(Count("id"))
    form = ClassroomForm()
    if request.method=='POST':
        form=ClassroomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context={
        'form': form,
        'queryset':qs,
        'baby_class':baby_class,
        'total_students':total_students
    }
    return render(request, 'website/classroom_form.html', context)


class PdfDetail(PDFTemplateResponseMixin, DetailView):
    model = Fee
    template_name = 'website/fee_detail.html'

class FeeDetailView(DetailView):
    model = Fee

#user Register

def Register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form =  CreateUserForm()
        if request.method == 'POST':
            form =  CreateUserForm(request.POST)
            if form.is_valid():
                user=form.save()
                username = form.cleaned_data.get('username')
                
                group = Group.objects.get(name='student')
                user.groups.add(group)
                Student.objects.create(
                    user=user
                )
                
                messages.success(request, 'Account was created for ' + username)
                
                return redirect('login')
            
    context = {
        'form': form
    }
    return render(request, 'website/register.html', context)
    
# LOGIN FORM SECTION
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username Or Password is incorrect')
            
        context={}
        return render(request, 'website/login.html', context)

def Logout(request):
    logout(request)
    return redirect('login')

def Student_detail(request, pk):
    student = Student.objects.get(id=pk)
    
    first_record = student.fee_set.first()
    school_fees = first_record.school_fees
    
    paid_fees = student.fee_set.all().aggregate(total_paid_fees=Sum('paid_fees'))
    
    balance_fees =  school_fees - paid_fees["total_paid_fees"]
    
    context = {"student": student,
               "paid_fees": paid_fees,
               "school_fees": school_fees,
               "balance_fees": balance_fees, }

    
    return render(request, 'website/students_detail.html', context)

class TeacherListView(ListView):
    model = Teacher
    template_name = 'website/teachers.html'
    context_object_name = 'teachers'
    
def addStaff(request):
    form = StaffForm()
    if request.method=='POST':
        form=StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teachers')

    context={
        'form': form
    }
    return render(request, 'website/staff_form.html', context)

def pie_chart(request):
    labels = []
    data = []
    
    queryset = Result.objects.order_by('-score')[:5]
    for result in queryset:
        labels.append(result.subject)
        data.append(result.score)
        
    return render(request, 'website/pie_chart.html', 
                  {'labels': labels,
                   'data': data
                   })
    
    
def createResult(request, pk):
    ResultFormSet = inlineformset_factory(Student, Result, fields=('subject', 'score', 'language', 'type', 'status'), extra=8)
    student = Student.objects.get(id=pk)
    formset = ResultFormSet(queryset=Result.objects.none(), instance=student)
    #form = ResultsForm(initial={'student':student})
    if request.method == 'POST':
        form = ResultsForm(request.POST)
        formset = ResultFormSet(request.POST, instance=student)
        if formset.is_valid():
            formset.save()
            return redirect('student')
    context = {'form':formset}
    return render(request, 'website/results_form.html', context)

def StudentClass(request, pk):
    student = Student.objects.get(id=pk)
    classroom = Classroom.objects.all()
    
    studentsperclass = classroom._student_set.all()
    
    context = {
        'student': student,
        'studentsperclass': studentsperclass,
        'classroom': classroom
    }
    
    return render(request, 'website/studentperclass.html', context)