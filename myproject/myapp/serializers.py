from rest_framework import serializers
from .models import User, Organization, Member, Role

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'profile', 'status', 'settings', 'created_at', 'updated_at']
        
    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['name', 'status', 'personal', 'settings', 'created_at', 'updated_at']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name', 'description', 'org']

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['org', 'user', 'role', 'status', 'settings', 'created_at', 'updated_at']
