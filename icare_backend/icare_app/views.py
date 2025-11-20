# icare_app/views.py
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from .models import Registration, Showcase, LoginHistory, Demonstration
from .serializers import RegistrationSerializer, ShowcaseSerializer, LoginHistorySerializer, DemonstrationSerializer
import requests

# Helper function to get client IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# ---------------- Visitor Registration ----------------
# WhatsApp API Credentials
WHATSAPP_API_URL = "https://app.dxing.in/api/send/whatsapp"
SECRET = "7b8ae820ecb39f8d173d57b51e1fce4c023e359e"
ACCOUNT = "1761365422812b4ba287f5ee0bc9d43bbf5bbe87fb68fc4daea92d8"

# Admin WhatsApp Number (CHANGE THIS TO YOUR ACTUAL ADMIN NUMBER)
ADMIN_PHONE = "919072791379"   # Example: "918281592544"


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register_visitor(request):
    data = request.data
    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    email = data.get("email", "").strip()

    if not name or not phone:
        return Response({"error": "Name and phone number are required"}, status=400)

    # Save visitor data
    Registration.objects.create(name=name, phone=phone, email=email)

    # Count total users (visitors)
    total_users = Registration.objects.count()

    # WhatsApp message to admin
    message_text = (
        f"🔔 *New User Logged In - icare 🧡!*\n\n"
        f"👤 *Name:* {name}\n"
        f"📞 *Phone:* {phone}\n"
        f"📧 *Email:* {email if email else 'Not provided'}\n"
        f"📊 *Total Users:* {total_users}"
    )

    params = {
        "secret": SECRET,
        "account": ACCOUNT,
        "recipient": ADMIN_PHONE,
        "type": "text",
        "message": message_text,
        "priority": 1
    }

    try:
        response = requests.post(WHATSAPP_API_URL, params=params, timeout=10)
        if response.status_code != 200:
            print(f"WhatsApp API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"WhatsApp Error: {e}")

    return Response({"message": "Registration successful"}, status=201)


# ---------------- Admin Login ----------------
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    ip_address = get_client_ip(request)

    if username == "imcbs" and password == "1234":
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'is_staff': True, 'is_superuser': True}
        )
        LoginHistory.objects.create(
            user=user,
            username=username,
            ip_address=ip_address,
            user_agent=user_agent,
            status='success'
        )
        request.session['user_id'] = user.id
        request.session['username'] = user.username

        return Response({
            "message": "Login successful",
            "user": {"id": user.id, "username": user.username, "email": user.email}
        }, status=200)
    else:
        LoginHistory.objects.create(
            user=None,
            username=username or "unknown",
            ip_address=ip_address,
            user_agent=user_agent,
            status='failed'
        )
        return Response({"error": "Invalid credentials"}, status=401)


# ---------------- Dashboard ----------------
@api_view(['GET'])
@permission_classes([AllowAny])
def dashboard_data(request):
    visitors = Registration.objects.all().order_by('-created_at').values("id", "name", "phone", "email", "created_at")
    total_visitors = Registration.objects.count()
    login_history = LoginHistory.objects.all()[:20]
    login_serializer = LoginHistorySerializer(login_history, many=True)
    user_id = request.session.get('user_id')
    user_data = None
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            user_data = {"id": user.id, "username": user.username, "email": user.email}
        except User.DoesNotExist:
            pass

    return Response({
        "total_visitors": total_visitors,
        "visitors": list(visitors),
        "login_history": login_serializer.data,
        "user": user_data
    }, status=200)


# ---------------- Showcase List + Create ----------------
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def showcase_list_create(request):
    if request.method == 'GET':
        showcases = Showcase.objects.all().order_by('-created_at')
        serializer = ShowcaseSerializer(showcases, many=True, context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ShowcaseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# ---------------- Showcase Update + Delete ----------------
@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def showcase_detail(request, pk):
    try:
        showcase = Showcase.objects.get(pk=pk)
    except Showcase.DoesNotExist:
        return Response({"error": "Showcase item not found"}, status=404)

    if request.method == 'GET':
        serializer = ShowcaseSerializer(showcase, context={'request': request})
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = ShowcaseSerializer(showcase, data=request.data, partial=partial, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        showcase.delete()
        return Response({"message": "Showcase item deleted successfully"}, status=204)


# ---------------- Demonstration List + Create ----------------
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def demonstration_list_create(request):
    if request.method == 'GET':
        demonstrations = Demonstration.objects.all().order_by('-created_at')
        serializer = DemonstrationSerializer(demonstrations, many=True, context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = DemonstrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# ---------------- Demonstration Update + Delete ----------------
@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def demonstration_detail(request, pk):
    try:
        demonstration = Demonstration.objects.get(pk=pk)
    except Demonstration.DoesNotExist:
        return Response({"error": "Demonstration item not found"}, status=404)

    if request.method == 'GET':
        serializer = DemonstrationSerializer(demonstration, context={'request': request})
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:
        partial = request.method == 'PATCH'
        serializer = DemonstrationSerializer(demonstration, data=request.data, partial=partial, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        demonstration.delete()
        return Response({"message": "Demonstration item deleted successfully"}, status=204)