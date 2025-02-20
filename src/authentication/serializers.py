from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'is_active', 
            'is_staff', 'is_superuser', 'groups', 'permissions'
        ]

    def get_permissions(self, obj):
        request = self.context.get('request')
        
        if request and request.user.is_authenticated:
            if request.user.has_perm('auth.view_permission'):
                return obj.get_all_permissions()
        
        return None