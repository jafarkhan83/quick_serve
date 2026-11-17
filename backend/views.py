from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.exceptions import ParseError
from .models import User
from .errors import api_400
import json

# Create your views here.

@api_view(["POST"])
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return api_400(None, None)

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        if not (first_name and last_name and email and password): return api_400(None, None)
        
        try:
            User.objects.create(first_name=first_name, last_name=last_name, email=email, password=password)

        # need to catch specific exception for database constraints don't match
        except Exception as e:
            return JsonResponse({'exception': str(e)})
            

        return JsonResponse({'message': f'User {first_name} {last_name} ({email}) registered successfully'})

@api_view(["POST"])
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError | ParseError:
            return api_400(None, None)

        email = data.get('email')
        password = data.get('password')
        if not (email and password): return api_400(None, None)

        try:
            User.objects.get(email=email, password=password)

        # need to catch specific exception for invalid credentials
        except Exception as e:
            return JsonResponse({"exception": str(e)})
        return JsonResponse({'bearer_token': 'hello_world'})

@api_view(['GET'])
def hello(request):
    return JsonResponse({'message': 'hello_world'})