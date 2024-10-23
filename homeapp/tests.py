from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from authentapp.models import Company
from homeapp.models import Project, Task, Role, StatusTask, ProjectEmployee
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Project, StatusTask, Task

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

class NuevaTareaTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        self.company = Company.objects.create(user=self.user, nit="123456789")
        self.project = Project.objects.create(
            name='Test Project',
            description='This is a test project.',
            start_date='2023-01-01',
            end_date='2023-01-10',
            budget='1000',
            company=self.company
        )
        self.status = StatusTask.objects.create(status='Pendiente')
        self.client.login(username='testuser', password='testpassword123')
        self.url = reverse('nueva-tarea', args=[self.project.id])

    def test_nueva_tarea_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nueva-tarea.html')
        self.assertIn('status_list', response.context)

    def test_nueva_tarea_post_success(self):
        data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'start-date': '2023-01-01',
            'end-date': '2023-01-10',
            'presupuesto': '1000',
            'status': self.status.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('proyectos'))
        self.assertTrue(Task.objects.filter(name='Test Task').exists())

    def test_nueva_tarea_post_invalid_data(self):
        data = {
            'title': '',
            'description': 'Test Description',
            'start-date': '2023-01-01',
            'end-date': '2023-01-10',
            'presupuesto': '1000',
            'status': ''
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nueva-tarea.html')
        self.assertIn('error', response.context)
        self.assertEqual(response.context['error'], 'Ingresa datos válidos.')
        self.assertFalse(Task.objects.filter(description='Test Description').exists())

class EliminarTareaTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        self.company = Company.objects.create(user=self.user, nit="123456789")
        self.project = Project.objects.create(
            name='Test Project',
            description='This is a test project.',
            start_date='2023-01-01',
            end_date='2023-01-10',
            budget='1000',
            company=self.company
        )
        self.status = StatusTask.objects.create(status='Pendiente')
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            start_date='2023-01-01',
            end_date='2023-01-10',
            budget='1000',
            project=self.project,
            status=self.status
        )
        self.client.login(username='testuser', password='testpassword123')
        self.url = reverse('eliminar_tarea', args=[self.task.id])

    def test_eliminar_tarea_success(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('proyectos'))
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    """def test_eliminar_tarea_not_exist(self):
        non_existent_url = reverse('eliminar_tarea', args=[999])
        response = self.client.post(non_existent_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('proyectos'))"""

class EditarTareaTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )
        self.company = Company.objects.create(user=self.user, nit="123456789")
        self.project = Project.objects.create(
            name='Test Project',
            description='This is a test project.',
            start_date='2023-01-01',
            end_date='2023-01-10',
            budget='1000',
            company=self.company
        )
        self.status = StatusTask.objects.create(status='Pendiente')
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            start_date='2023-01-01',
            end_date='2023-01-10',
            budget='1000',
            project=self.project,
            status=self.status
        )
        self.client.login(username='testuser', password='testpassword123')
        self.url = reverse('editar_tarea', args=[self.task.id])

    def test_editar_tarea_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('proyectos'))

    def test_editar_tarea_post_success(self):
        new_status = StatusTask.objects.create(status='Completada')
        data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'start-date': '2023-02-01',
            'end-date': '2023-02-10',
            'presupuesto': '2000',
            'status': new_status.id
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('proyectos'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')
        self.assertEqual(self.task.description, 'Updated Description')
        self.assertEqual(self.task.start_date.strftime('%Y-%m-%d'), '2023-02-01')
        self.assertEqual(self.task.end_date.strftime('%Y-%m-%d'), '2023-02-10')
        self.assertEqual(self.task.budget, 2000)
        self.assertEqual(self.task.status, new_status)

    def test_editar_tarea_post_invalid_data(self):
        data = {
            'title': '',
            'description': '',
            'start-date': '',
            'end-date': '',
            'presupuesto': '',
            'status': ''
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('proyectos'))
        self.task.refresh_from_db()
        self.assertNotEqual(self.task.name, '')
        self.assertNotEqual(self.task.description, '')
        self.assertNotEqual(self.task.start_date.strftime('%Y-%m-%d'), '')
        self.assertNotEqual(self.task.end_date.strftime('%Y-%m-%d'), '')
        self.assertNotEqual(self.task.budget, 0)