from rest_framework import serializers
from .models import AIAnalysis, AIModel, AILearningData

class AIAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIAnalysis
        fields = '__all__'

class AIModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIModel
        fields = '__all__'

class AILearningDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AILearningData
        fields = '__all__'
