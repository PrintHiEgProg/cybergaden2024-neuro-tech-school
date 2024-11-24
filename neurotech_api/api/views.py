from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Calibri
from .serializers import CalibriSerializer
from .models import UserProfile

class CalibriListView(APIView):
    def get(self, request):
        calibri_objects = Calibri.objects.all()
        serializer = CalibriSerializer(calibri_objects, many=True)
        return Response(serializer.data)

    def post(self, request):
        name = request.data.get('name')
        if Calibri.objects.filter(name=name).exists():
            return Response(
                {"error": f"Calibri with name '{name}' already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = CalibriSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CalibriDetailView(APIView):
    def get(self, request, name):
        try:
            calibri = Calibri.objects.get(name=name)
            serializer = CalibriSerializer(calibri)
            return Response(serializer.data)
        except Calibri.DoesNotExist:
            return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, name):
        try:
            calibri = Calibri.objects.get(name=name)
            calibri.delete()
            return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Calibri.DoesNotExist:
            return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, name):
        try:
            calibri = Calibri.objects.get(name=name)
            serializer = CalibriSerializer(calibri, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Calibri.DoesNotExist:
            return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)


from django.contrib.auth import authenticate

class CheckAuthView(APIView):
    """
    API endpoint for checking Django User authentication.
    """
    def post(self, request):
        username = request.data.get('username')  # Получение имени пользователя из запроса
        password = request.data.get('password')  # Получение пароля из запроса

        # Проверка на отсутствие данных
        if not username or not password:
            return Response(
                {"error": "Both 'username' and 'password' fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Попытка аутентификации пользователя
        user = authenticate(username=username, password=password)

        if user is not None:
            # Аутентификация успешна
            return Response(
                {"message": "Authentication successful", "username": user.username},
                status=status.HTTP_200_OK
            )
        else:
            # Неверные учетные данные
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )
