from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [

        ('publishing_company', '0001_initial'),
        ('books', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0001_initial'),
        ('users', '0001_initial'),

    ]

    operations = [
        migrations.AddField(
            model_name='bookfollowers',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_follower_book', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='categories.category'),
        ),
        migrations.AddField(
            model_name='book',
            name='followers',
            field=models.ManyToManyField(related_name='user_following_books', through='books.BookFollowers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_published', to='publishing_company.publisher'),
        ),
    ]
