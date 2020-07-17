# Generated by Django 3.0.5 on 2020-07-16 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rex_app', '0010_userattribute_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='userattribute',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userattribute',
            name='timezone',
            field=models.CharField(choices=[('1', 'Asia/Taipei')], default='Asia/Taipei', max_length=99999),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userattribute',
            name='avatar',
            field=models.CharField(choices=[('1', 'fab fa-500px'), ('2', 'far fa-angry'), ('3', 'fas fa-backspace'), ('4', 'fas fa-atom'), ('5', 'fab fa-battle-net'), ('6', 'fas fa-biohazard'), ('7', 'fas fa-braille'), ('8', 'fas fa-burn'), ('9', 'fab fa-canadian-maple-leaf'), ('10', 'fas fa-car-crash')], max_length=99999),
        ),
    ]