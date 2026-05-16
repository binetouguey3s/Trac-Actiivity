# Generated manually because Python is unavailable in the current sandbox.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def creer_profils_existants(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('core', 'Profile')

    for utilisateur in User.objects.all():
        Profile.objects.get_or_create(utilisateur=utilisateur)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='photo_profil_auteur',
            field=models.ImageField(blank=True, null=True, upload_to='photos_profil/'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos_profil/')),
                ('utilisateur', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profil',
                'verbose_name_plural': 'Profils',
            },
        ),
        migrations.RunPython(creer_profils_existants, migrations.RunPython.noop),
    ]
