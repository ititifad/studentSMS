from django.shortcuts import render, redirect
from .forms import (
    FeeForm, StudentForm, 
    StudentSearchForm, 
    StudentFeeSearchForm,
    ClassroomForm, 
    ClassroomSearchForm,
    LoginForm
)
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.db.models import Sum, Count
from django.db.models import Q, F, FloatField, ExpressionWrapper
from django.views.generic import View, DetailView
from easy_pdf.views import PDFTemplateResponseMixin
from django.template.loader import get_template
from .utils import render_to_pdf
from django.contrib.auth import authenticate, login, logout

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
#@login_required(login_url='login')
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

def student(request, pk):
    qs = Fee.objects.all()
    student = Student.objects.get(id=pk)
    
    fees = student.fee_set.all().order_by('-publish_date')
    #total_fees =  student.fee_set.all().filter(student__id=pk).aggregate(sum=Sum('paid_fees', flat=True))['sum']
    first_record = student.fee_set.first()
    school_fees = first_record.school_fees
    
    paid_fees = student.fee_set.all().aggregate(total_paid_fees=Sum('paid_fees'))
    
    balance_fees =  school_fees - paid_fees["total_paid_fees"]
    
    if balance_fees == 0:
        messages.info(request, 'Student School fees is Completed')
   
        
    
    context = {"student": student,
               'fees': fees,
               "paid_fees": paid_fees,
               "school_fees": school_fees,
               "balance_fees": balance_fees, }

    #context = {
        #'student' : student,
        #'fees' : fees,
        #'total_fees' : total_fees,
    return render(request, 'website/students.html', context)


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

def UpdateStudent(request, pk):
    student = Student.objects.get(id=pk)
    form = StudentForm(instance=student)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('/')
        context = {'form':form}
        return render(request, 'website/student_form.html', context)

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
    
# LOGIN FORM SECTION
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    return HttpResponse('Disabled Account')
            else:
                 return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'website/login.html', {'form':form})


def Logout(request):
    logout(request)
    return redirect('login')

def student_detail(request, pk):
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