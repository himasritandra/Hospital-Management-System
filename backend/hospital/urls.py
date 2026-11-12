from django.urls import path
from .views import CsrfView, RegisterView, LoginView, LogoutView, MeView,DepartmentListView,DoctorListView,DoctorDetailView

urlpatterns = [
    path('csrf/', CsrfView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('me/', MeView.as_view()),
     path('departments/', DepartmentListView.as_view()),
    path('doctors/', DoctorListView.as_view()),
    path('doctors/<int:pk>/', DoctorDetailView.as_view())
]