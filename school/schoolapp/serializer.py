from rest_framework import serializers
from .models import CustomUser, Student, LibraryHistory, FeesHistory

# Serializer for CustomUser
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'address', 'is_active', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True},  # Make password write-only
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save()
        return instance

# Serializer for Student
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'age', 'grade']

# Serializer for LibraryHistory
class LibraryHistorySerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = LibraryHistory
        fields = ['id', 'student', 'book_title', 'issue_date', 'return_date']

# Serializer for FeesHistory
class FeesHistorySerializer(serializers.ModelSerializer):
    student = StudentSerializer()

    class Meta:
        model = FeesHistory
        fields = ['id', 'student', 'amount', 'payment_date']