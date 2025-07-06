# main/migrations/0001_initial.py
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bouquet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('image', models.ImageField(upload_to='bouquets/', verbose_name='Изображение')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_address', models.CharField(max_length=255, verbose_name='Адрес доставки')),
                ('delivery_datetime', models.DateTimeField(verbose_name='Дата и время доставки')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('order_datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата оформления заказа')),
                ('bouquet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.bouquet', verbose_name='Букет')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
