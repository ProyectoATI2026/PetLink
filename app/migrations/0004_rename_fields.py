from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_userprofile_pet'),
    ]

    operations = [
        # AuditLog renames
        migrations.RenameField(
            model_name='auditlog',
            old_name='usuario',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='auditlog',
            old_name='accion',
            new_name='action',
        ),
        migrations.RenameField(
            model_name='auditlog',
            old_name='direccion_ip',
            new_name='ip_address',
        ),
        migrations.RenameField(
            model_name='auditlog',
            old_name='detalles',
            new_name='details',
        ),
        migrations.RenameField(
            model_name='auditlog',
            old_name='fecha_hora',
            new_name='timestamp',
        ),

        # CustomPet renames
        migrations.RenameField(
            model_name='custompet',
            old_name='nombre',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='custompet',
            old_name='especie',
            new_name='species',
        ),
        migrations.RenameField(
            model_name='custompet',
            old_name='raza',
            new_name='breed',
        ),
        migrations.RenameField(
            model_name='custompet',
            old_name='edad',
            new_name='birth_date',
        ),
        migrations.RenameField(
            model_name='custompet',
            old_name='genero',
            new_name='gender',
        ),
        migrations.RenameField(
            model_name='custompet',
            old_name='descripcion',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='custompet',
            old_name='imagen',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='custompet',
            old_name='propietario',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='custompet',
            old_name='fecha_registro',
            new_name='registration_date',
        ),

        # UserProfile renames
        migrations.RenameField(
            model_name='userprofile',
            old_name='cedula',
            new_name='id_number',
        ),
    ]
