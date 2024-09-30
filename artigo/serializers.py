from rest_framework import serializers
from artigo.models import Artigo

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artigo
        fields = '__all__'