# Generated by Django 3.1.7 on 2021-03-09 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_user_agents_per_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='client_tree_sort',
            field=models.CharField(choices=[('alphafail', 'Move failing clients to the top'), ('alpha', 'Sort alphabetically')], default='alphafail', max_length=50),
        ),
    ]
