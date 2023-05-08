from rest_framework import serializers
from .models import Book, BookFollowers
from copies.models import Copy
from categories.serializers import CategorySerializer
from categories.models import Category
from publishing_company.serializers import PublisherSerializer
from copies.serializers import CopySerializer
from users.serializers import UserSerializer

from publishing_company.models import Publisher


class BookFollowersSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    followed_at = serializers.DateTimeField(read_only=True)
    followed_by = serializers.CharField(source="user.email", read_only=True)
    user = UserSerializer(read_only=True)

    def create(self, validated_data: dict) -> BookFollowers:
        return BookFollowers.objects.create(**validated_data)

    class Meta:
        model = BookFollowers
        fields = ["id", "book_id", "user_id", "followed_at", "followed_by", "user"]


class BookSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    category = CategorySerializer()
    publisher = PublisherSerializer()
    copies = CopySerializer(many=True)
    num_copies = serializers.SerializerMethodField()
    followers = BookFollowersSerializer(many=True, read_only=True)
    num_followers = serializers.SerializerMethodField()

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
            "copies",
            "num_copies",
            "followers",
            "num_followers",
        ]

    def get_num_copies(self, obj):
        return obj.copies.count()

    def get_num_followers(self, obj):
        return obj.followers.count()

    def create(self, validated_data):
        category_data = validated_data.pop("category")

        publisher_data = validated_data.pop("publisher")

        category = Category.objects.filter(name=category_data["name"])
        if category.exists():
            category = category.first()
        else:
            category = Category.objects.create(**category_data)

        publisher = Publisher.objects.filter(name=publisher_data["name"])
        if publisher.exists():
            publisher = publisher.first()
        else:
            publisher = Publisher.objects.create(**publisher_data)

        copies_data = validated_data.pop("copies")

        book = Book.objects.create(
            category=category, publisher=publisher, **validated_data
        )

        copies = [Copy(book=book, **copy_data) for copy_data in copies_data]
        Copy.objects.bulk_create(copies)
        return book


class BookSerializerUpdate(serializers.ModelSerializer):
    category = CategorySerializer()
    publisher = PublisherSerializer()
    copies = CopySerializer(many=True)

    def update(self, instance, validated_data):
        category_data = validated_data.pop("category", None)
        publisher_data = validated_data.pop("publisher", None)
        copies_data = validated_data.pop("copies", None)
        if category_data:
            category, _ = Category.objects.get_or_create(name=category_data["name"])
            validated_data["category"] = category
        if publisher_data:
            publisher, _ = Publisher.objects.get_or_create(name=publisher_data["name"])
            validated_data["publisher"] = publisher
        return super().update(instance, validated_data)

    class Meta(BookSerializer.Meta):
        fields = ["title", "author", "category", "publisher", "copies"]
        partial = True


class BookFollowersSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    followed_at = serializers.DateTimeField(read_only=True)
    followed_by = serializers.CharField(source="user.email", read_only=True)

    def create(self, validated_data: dict) -> BookFollowers:
        return BookFollowers.objects.create(**validated_data)

    class Meta:
        model = BookFollowers
        fields = ["id", "followed_at", "followed_by"]
