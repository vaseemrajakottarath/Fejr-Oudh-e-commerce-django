# Generated by Django 3.2.9 on 2021-11-30 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_ordern'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.ordern'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='status',
            field=models.IntegerField(choices=[(1, 'Order Confirmed'), (2, 'Shipped'), (3, 'Out for delivery'), (4, 'cancelled'), (0, 'cancelled')], default=1),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]