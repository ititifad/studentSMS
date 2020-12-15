from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import F
from phonenumber_field.modelfields import PhoneNumberField

class Student(models.Model):
    GENDER =(
        (None, 'Choose gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        )
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    classroom = models.ForeignKey('Classroom', on_delete=models.DO_NOTHING,null=True)
    phone_number = PhoneNumberField(null=True)
    gender = models.CharField(max_length=50, null=True, choices=GENDER)
    location = models.CharField(max_length=50, blank=True)
    profile_pic = models.ImageField(default='default.png',upload_to='profile_pics', null=True, blank=True)
    reports = models.FileField(upload_to='reports', null=True)
    results = models.FileField(upload_to='results', blank=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.name)


    def get_total_fee(self):
        return sum(student.school_fees for student in self.fee_set.all())
    def get_total_paid_fee(self):
        return sum(student.paid_fees for student in self.fee_set.all())

    def get_remaining_fee(self):
        total_fee = self.get_total_fee()
        total_paid = self.get_total_paid_fee()
        return float(total_fee - total_paid)

class Classroom(models.Model):
    CLASSES = (
        (None, 'Select Class'),
        ('Baby class', 'Baby class'),
        ('Class 1', 'class 1'),
        ('Class 2', 'class 2'),
        ('Class 3', 'class 3'),
        ('Class 4', 'class 4'),
        ('Class 5', 'class 5'),
        ('Class 6', 'class 6'),
        ('Class 7', 'class 7'),
    )
    name = models.CharField(max_length=40, choices=CLASSES, blank=True, null=True)
    

    def __str__(self):
        return str(self.name)

#class Subject(models.Model):
    #subject_name = models.CharField(max_length=100)
    #subject_code = models.IntegerField()
    #subject_creation_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    ##subject_update_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    #def __str__(self):
        #return self.subject_name


#class SubjectCombination(models.Model):
    #select_class = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    #select_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
    #def __str__(self):
        #return '%s Section-%s'%(self.select_class.name, self.select_class.section)

class Result(models.Model):
    STATUS =(
        (None, 'Select status'),
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
        )
    SUBJECT=(
        (None, 'Select subjects'),
        ('English', 'English'),
        ('Mathematics', 'Mathematics'),
        ('Swahili', 'Swahili'),
        ('Science', 'Science'),
        ('Sports', 'Sports'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True,)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True)
    #subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, null=True)
    subject = models.CharField(max_length=50, blank=True, choices=SUBJECT, null=True)
    score = models.IntegerField(null=True, blank=True, default=0)
    language = models.CharField(max_length=50, blank=True)
    type = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True, blank=True, choices=STATUS)
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.student.name)

        
class Teacher(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.DO_NOTHING, null=True)
    phone_number = PhoneNumberField(null=True)
    image = models.ImageField(default="/profile_pics/glogo.png", null=True, blank=True)
    
    def __str__(self):
        return str(self.name)
    
class Phase(models.Model):
    PHASE = (
        ('Phase 1', 'Phase 1'),
        ('Phase 2', 'Phase 2'),
        ('Phase 3', 'Phase 3'),
        ('Phase 4', 'Phase 4')
    )
    name = models.CharField(max_length=40, choices=PHASE, blank=True, null=True)
    
    def __str__(self):
        return str(self.name)
    
class Fee(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True,)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, null=True)
    school_fees = models.FloatField(default=1000000)
    paid_fees = models.FloatField(null=False)
    remaining_fees = models.FloatField(blank=True)
    completed = models.BooleanField(null=False, default=False)
    publish_date = models.DateTimeField(auto_now_add=True)
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.remaining_fees = self.school_fees - self.paid_fees
        super().save( *args, **kwargs)
        
    def save(self, *args, **kwargs):
        self.remaining_fees = self.school_fees - self.paid_fees
        if self.remaining_fees == 0:
            self.completed = True
        else:
            self.completed = False
            
        super().save(*args, **kwargs)

    
    def __str__(self):
        return str(self.student.name)

