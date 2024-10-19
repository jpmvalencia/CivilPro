from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from authentapp.models import Company
from homeapp.models import Project, Task, Role, StatusTask, ProjectEmployee

User = get_user_model()

class NuevoProyectoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        self.company = Company.objects.create(user=self.user, nit="123456789")
        self.client.login(username='testuser', password='testpassword123')
        self.url = reverse('nuevo-proyecto')

    def test_nuevo_proyecto_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nuevo-proyecto.html')

    def test_nuevo_proyecto_post_success(self):
        data = {
            'title': 'Test Project',
            'description': 'This is a test project.',
            'start-date': '2023-01-01',
            'end-date': '2023-01-10',
            'presupuesto': '1000'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('proyectos'))
        self.assertTrue(Project.objects.filter(name='Test Project').exists())

    def test_nuevo_proyecto_post_invalid_data(self):
        data = {
            'title': '',
            'description': 'This is a test project.',
            'start-date': '2023-01-01',
            'end-date': '2023-01-10',
            'presupuesto': '1000'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nuevo-proyecto.html')
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Ingresa datos válidos.')
        self.assertFalse(Project.objects.filter(description='This is a test project.').exists())

class EliminarProyectoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        self.company = Company.objects.create(user=self.user, nit="123456789")
        self.client.login(username='testuser', password='testpassword123')
        self.proyecto = Project.objects.create(
            name='Test Project',
            description='This is a test project.',
            start_date='2023-01-01',
            end_date='2023-01-10',
            budget='1000',
            company=self.company
        )
        self.url = reverse('eliminar_proyecto', args=[self.proyecto.id])

    def test_eliminar_proyecto_success(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('proyectos'))
        self.assertFalse(Project.objects.filter(id=self.proyecto.id).exists())

    def test_eliminar_proyecto_not_exist(self):
        non_existent_url = reverse('eliminar_proyecto', args=[999])
        response = self.client.post(non_existent_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('proyectos'))

