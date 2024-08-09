from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import User, Organization, Member, Role
import bcrypt

class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_data = request.data.get('user')
        org_data = request.data.get('organization')

        if not user_data or not org_data:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        # Hash password
        hashed_password = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())

        # Create user
        user = User(email=user_data['email'], password=hashed_password)
        user.save()

        # Create organization
        organization = Organization.objects.create(
            name=org_data['name'],
            status=org_data.get('status', 0),
            personal=org_data.get('personal', False),
            settings=org_data.get('settings', {})
        )

        # Create or get 'owner' role
        owner_role, created = Role.objects.get_or_create(
            name='owner',
            org=organization,
            defaults={'description': 'Owner of the organization'}
        )

        # Add member
        Member.objects.create(
            org=organization,
            user=user,
            role=owner_role,
            status=0
        )

        return Response({"msg": "User created successfully"}, status=status.HTTP_201_CREATED)

class SignInView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('password')

        user = User.objects.filter(email=email).first()
        print("user",user)
        if user:
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user.password = hashed_password
            user.save()
            return Response({"msg": "Password updated successfully"}, status=status.HTTP_200_OK)

        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class InviteMemberView(APIView):
    def post(self, request):
        org_id = request.data.get('org_id')
        email = request.data.get('email')
        role_id = request.data.get('role_id')

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        Member.objects.create(
            org_id=org_id,
            user=user,
            role_id=role_id,
            status=0
        )

        return Response({"msg": "Member invited successfully"}, status=status.HTTP_201_CREATED)

class DeleteMemberView(APIView):
    def delete(self, request):
        org_id = request.data.get('org_id')
        user_id = request.data.get('user_id')

        member = Member.objects.filter(org_id=org_id, user_id=user_id).first()
        if not member:
            return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)

        member.delete()
        return Response({"msg": "Member deleted successfully"}, status=status.HTTP_200_OK)

class UpdateMemberRoleView(APIView):
    def put(self, request):
        org_id = request.data.get('org_id')
        user_id = request.data.get('user_id')
        role_id = request.data.get('role_id')

        member = Member.objects.filter(org_id=org_id, user_id=user_id).first()
        if not member:
            return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)

        member.role_id = role_id
        member.save()
        return Response({"msg": "Member role updated successfully"}, status=status.HTTP_200_OK)

