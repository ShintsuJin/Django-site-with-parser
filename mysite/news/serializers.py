from rest_framework import serializers
from .models import News, Category


class CategorySerializer(serializers.ModelSerializer):
    title = serializers.CharField()

    class Meta:
        model = Category
        fields = ['id', 'title']


class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    content = serializers.CharField()
    #Todo: change type to file
    #photo = serializers.ImageField()
    photo = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(default=True)
    category = CategorySerializer()
    views = serializers.IntegerField(default=0)

    class Meta:
        model = News
        fields = ['title', 'content', 'photo', 'created_at', 'updated_at', 'is_published', 'category', 'views']

    def create(self, validated_data):
        category = validated_data.pop('category')
        i = Category.objects.get(title=category['title'])
        validated_data['category'] = i
        return News.objects.create(**validated_data)
