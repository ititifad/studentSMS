from django.urls import path
from.import views
from .views import GeneratePdf, PdfDetail, FeeDetailView, TeacherListView

urlpatterns = [
    path('', views.home, name='home'),
    path('classrooms/', views.classrooms, name='classroom'),
    path('create_classroom/', views.createClassroom, name='create_classroom'),
    path('student/<str:pk>/', views.student, name="student"),
    path('students/',views.students, name="students"),
    path('staffs/',views.addStaff, name="staff"),
    path('create_fee/<str:pk>/', views.createFee, name="create_fee"),
    path('add_result/<str:pk>/', views.createResult, name="add_result"),
    path('create_student/', views.createStudent, name="create_student"),
    path('update_fee/<str:pk>/', views.UpdateFee, name="update_fee"),
    path('delete_fee/<str:pk>/', views.deleteFee, name="delete_fee"),
    path('pdf/', GeneratePdf.as_view(), name="pdf"),
    path('mypdf/<int:pk>/', PdfDetail.as_view(), name='pdf-detail'),
    path('fee/<int:pk>/', FeeDetailView.as_view(), name='fee-detail'),
    path('teachers/', TeacherListView.as_view(), name='teachers'),
    path('register/', views.Register, name='register'),
    path('user-page/', views.UserPage, name='user-page'),
    path('account/', views.AccountSettings, name='account'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('student_detail/<str:pk>/', views.Student_detail, name="student_detail"),
    path('student_class/<str:pk>/', views.StudentClass, name="student_class"),
    path('update_student/<str:pk>/', views.UpdateStudent, name="update_student"),
    path('pie-chart/', views.pie_chart, name='pie-chart')
    
]

