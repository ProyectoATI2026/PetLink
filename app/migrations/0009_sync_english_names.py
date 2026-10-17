from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_report'),
    ]

    operations = [

        # -------------------------------------------------
        # AUDIT LOG
        # -------------------------------------------------

        migrations.RenameField(
            model_name='auditlog',
            old_name='accion',
            new_name='action',
        ),

        migrations.RenameField(
            model_name='auditlog',
            old_name='detalles',
            new_name='details',
        ),

        migrations.RenameField(
            model_name='auditlog',
            old_name='direccion_ip',
            new_name='ip_address',
        ),

        migrations.RenameField(
            model_name='auditlog',
            old_name='fecha_hora',
            new_name='timestamp',
        ),

        migrations.RenameField(
            model_name='auditlog',
            old_name='usuario',
            new_name='user',
        ),

        migrations.AlterModelOptions(
            name='auditlog',
            options={
                'ordering': ['-timestamp'],
                'verbose_name': 'Log de Auditoría',
                'verbose_name_plural': 'Logs de Auditoría',
            },
        ),

        # -------------------------------------------------
        # CUSTOM PET
        # -------------------------------------------------

        migrations.RenameField(
            model_name='custompet',
            old_name='edad',
            new_name='birth_date',
        ),

        migrations.RenameField(
            model_name='custompet',
            old_name='raza',
            new_name='breed',
        ),

        migrations.RenameField(
            model_name='custompet',
            old_name='descripcion',
            new_name='description',
        ),

        migrations.RenameField(
            model_name='custompet',
            old_name='genero',
            new_name='gender',
        ),

        migrations.RenameField(
            model_name='custompet',
            old_name='imagen',
            new_name='image',
        ),

        migrations.RenameField(
            model_name='custompet',
            old_name='nombre',
            new_name='name',
        ),

        migrations.RenameField(
            model_name='custompet',
            old_name='fecha_registro',
            new_name='registration_date',
        ),

        migrations.RenameField(
            model_name='custompet',
            old_name='especie',
            new_name='species',
        ),

        migrations.RenameField(
            model_name='custompet',
            old_name='propietario',
            new_name='owner',
        ),

        migrations.AlterField(
            model_name='custompet',
            name='owner',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='pets',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Propietario',
            ),
        ),

        migrations.AlterModelOptions(
            name='custompet',
            options={
                'ordering': ['name'],
                'verbose_name': 'Mascota',
                'verbose_name_plural': 'Mascotas',
            },
        ),

        # -------------------------------------------------
        # USER PROFILE
        # -------------------------------------------------

        migrations.RenameModel(
            old_name='ProfileInfo',
            new_name='UserProfile',
        ),

        migrations.RenameField(
            model_name='userprofile',
            old_name='cedula',
            new_name='id_number',
        ),

        migrations.RenameField(
            model_name='userprofile',
            old_name='nacimiento',
            new_name='birth_date',
        ),

        migrations.RenameField(
            model_name='userprofile',
            old_name='genero',
            new_name='gender',
        ),

        migrations.RenameField(
            model_name='userprofile',
            old_name='ubicacion',
            new_name='location',
        ),

        migrations.RenameField(
            model_name='userprofile',
            old_name='gustos',
            new_name='interests',
        ),

        migrations.AlterField(
            model_name='userprofile',
            name='id_number',
            field=models.CharField(
                blank=True,
                max_length=20,
                null=True,
                unique=True,
                verbose_name='Cédula de identidad',
            ),
        ),

        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(
                blank=True,
                choices=[
                    ('Masculino', 'Masculino'),
                    ('Femenino', 'Femenino'),
                ],
                max_length=20,
                null=True,
                verbose_name='Género',
            ),
        ),

        migrations.AlterField(
            model_name='userprofile',
            name='location',
            field=models.CharField(
                blank=True,
                max_length=100,
                null=True,
                verbose_name='Ubicación',
            ),
        ),

        migrations.AlterField(
            model_name='userprofile',
            name='interests',
            field=models.TextField(
                blank=True,
                help_text='Separados por comas o en formato adecuado',
                null=True,
                verbose_name='Gustos / Preferencias',
            ),
        ),

        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='profile',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Usuario',
            ),
        ),

        migrations.AddField(
            model_name='userprofile',
            name='is_verified',
            field=models.BooleanField(
                default=False,
                verbose_name='Verificado',
            ),
        ),
    ]
