from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Department,Doctor
from .serializers import (
    DepartmentSerializer,
    DoctorSerializer,
    RegisterSerializer,
)


def user_data(user):
    if hasattr(user, 'profile'):
        role = user.profile.role
    elif user.is_superuser:
        role = 'admin'
    else:
        role = 'patient'
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'role': role,
    }


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CsrfView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request):
        return Response({'detail': 'CSRF cookie set'})


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return Response(user_data(user), status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {'error': 'Invalid username or password'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        login(request, user)
        return Response(user_data(user))


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'detail': 'Logged out'})


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(user_data(request.user))
class DepartmentListView(ListAPIView):
    queryset = Department.objects.all().order_by('name')
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class DoctorListView(ListAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Doctor.objects.select_related('user', 'department')
        search = self.request.query_params.get('search')
        department = self.request.query_params.get('department')
        if search:
            qs = qs.filter(
                Q(user__first_name__icontains=search)
                | Q(user__last_name__icontains=search)
                | Q(user__username__icontains=search)
            )
        if department:
            qs = qs.filter(department_id=department)
        return qs.order_by('user__first_name')


class DoctorDetailView(RetrieveAPIView):
    queryset = Doctor.objects.select_related('user', 'department')
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]