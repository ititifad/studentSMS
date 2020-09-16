from django.urls import path
from.import views
from .views import GeneratePdf, PdfDetail, FeeDetailView

urlpatterns = [
    path('', views.home, name='home'),
    path('classrooms/', views.classrooms, name='classroom'),
    path('create_classroom/', views.createClassroom, name='create_classroom'),
    path('student/<str:pk>/', views.student, name="student"),
    path('students/',views.students, name="students"),
    path('create_fee/<str:pk>/', views.createFee, name="create_fee"),
    path('create_student/', views.createStudent, name="create_student"),
    path('update_fee/<str:pk>/', views.UpdateFee, name="update_fee"),
    path('delete_fee/<str:pk>/', views.deleteFee, name="delete_fee"),
    path('pdf/', GeneratePdf.as_view(), name="pdf"),
    path('mypdf/<int:pk>/', PdfDetail.as_view(), name='pdf-detail'),
    path('fee/<int:pk>/', FeeDetailView.as_view(), name='fee-detail'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('student_detail/<str:pk>/', views.Student_detail, name="student_detail"),
    path('update/<str:pk>/', views.UpdateStudent, name="update-student")
    
]

