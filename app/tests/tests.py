from django.test import TestCase, Client
from django.urls import reverse
from app.models import CustomUser, CustomPet, AuditLog
from app.forms import CustomPetForm

class PetLinkUnitTests(TestCase):

    def setUp(self):
        """
        Configuración inicial que se ejecuta antes de cada prueba.
        Crea un usuario estándar, un superusuario y una mascota adaptados a models_3.py.
        """

        self.user_estandar = CustomUser.objects.create_user(
            username='usuario_prueba',
            email='usuario@test.com',
            password='Password123!'
        )

        self.user_admin = CustomUser.objects.create_superuser(
            username='admin_prueba',
            email='admin@test.com',
            password='AdminPassword123!'
        )

        self.mascota = CustomPet.objects.create(
            name='Firulais',
            species='Perro',
            breed='Mestizo',
            owner=self.user_estandar,
            description='Un perro muy juguetón'
        )

        self.client = Client()

    def test_creacion_mascota(self):
        """Prueba que la mascota se cree correctamente en la BD y responda a __str__."""

        self.assertEqual(self.mascota.name, 'Firulais')
        self.assertEqual(self.mascota.species, 'Perro')
        self.assertEqual(self.mascota.owner, self.user_estandar)
        
        self.assertEqual(str(self.mascota), 'Firulais (Perro)')

    def test_login_redireccion_segun_rol(self):
        """Prueba la lógica de redirección post-login diferenciada por rol de usuario."""

        response_user = self.client.post(reverse('login'), {
            'username': 'usuario_prueba',
            'password': 'Password123!'
        })
        self.assertRedirects(response_user, reverse('home'))

        self.client.logout()

        response_admin = self.client.post(reverse('login'), {
            'username': 'admin_prueba',
            'password': 'AdminPassword123!'
        })
        self.assertRedirects(response_admin, reverse('reports'))

    def test_validacion_formulario_mascota(self):
        """Prueba que el formulario rechace entradas sin los campos requeridos (name/species)."""
        
        datos_invalidos = {
            'species': 'Gato',
            'description': 'Falta el nombre de la mascota'
        }
        form = CustomPetForm(data=datos_invalidos)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

        datos_validos = {
            'name': 'Michi',
            'species': 'Gato',
            'breed': 'Siamés',
            'description': 'Gato tranquilo'
        }
        form_valido = CustomPetForm(data=datos_validos)
        self.assertTrue(form_valido.is_valid())

    def test_registro_log_auditoria_login_fallido(self):
        """Prueba que un intento de login incorrecto cree un registro en AuditLog (usando campos de models_3.py)."""
        conteo_inicial_logs = AuditLog.objects.count()

        self.client.post(reverse('login'), {
            'username': 'usuario_prueba',
            'password': 'ClaveErronea999!'
        })

        self.assertEqual(AuditLog.objects.count(), conteo_inicial_logs + 1)
        
        ultimo_log = AuditLog.objects.latest('timestamp')
        self.assertEqual(ultimo_log.action, 'LOGIN_FAILED')
        self.assertIn('usuario_prueba', ultimo_log.details)