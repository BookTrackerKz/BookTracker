from rest_framework import serializers
from .models import Book, BookFollowers
from categories.serializers import CategorySerializer
from categories.models import Category
from publishing_company.serializers import PublisherSerializer
from publishing_company.models import Publisher
import uuid


class BookSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    category = CategorySerializer()
    publisher = PublisherSerializer()

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "description",
            "publish_date",
            "number_pages",
            "language",
            "isbn",
            "category",
            "publisher",
        ]

    def create(self, validated_data):
        category_data = validated_data.pop("category")

        publisher_data = validated_data.pop("publisher")

        category = Category.objects.create(**category_data)
        publisher = Publisher.objects.create(**publisher_data)
        book = Book.objects.create(
            category=category, publisher=publisher, **validated_data
        )
        return book


class BookFollowersSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    followed_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data: dict) -> BookFollowers:
        return BookFollowers.objects.create(**validated_data)
