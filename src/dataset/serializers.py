from rest_framework.serializers import ModelSerializer
from .models import DataSet

class DataSetSerializer(ModelSerializer):
    class Meta:
        model = DataSet
        fields = '__all__'