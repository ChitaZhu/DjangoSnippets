from rest_framework import serializers
from news.models import Reporter, Article

class ReporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporter
        fields = ['id', 'full_name', 'keyword']

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'pub_date', 'headline', 'content', 'reporter']