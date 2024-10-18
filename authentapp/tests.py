from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from authentapp.models import Employee, Degree, EmployeeDegree, Company

User = get_user_model()
class SignupUsuTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('signup_usu')
        self.degree = Degree.objects.create(name="Bachelor")

    def test_signup_usu_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('degrees', response.context)

    def test_signup_usu_post_success(self):
        data = {
            "doc_id": "123456789",
            "your_email": "testuser@example.com",
            "password": "testpassword123",
            "repassword": "testpassword123",
            "first_name": "Test",
            "last_name": "User",
            "code": "US",
            "phone": "1234567890",
            "titles[]": [self.degree.name],
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirección a la página de login
        self.assertTrue(User.objects.filter(username="testuser@example.com").exists())
        self.assertTrue(Employee.objects.filter(doc="123456789").exists())
        self.assertTrue(EmployeeDegree.objects.filter(employee__doc="123456789", degree=self.degree).exists())

    def test_signup_usu_post_password_mismatch(self):
        data = {
            "doc_id": "123456789",
            "your_email": "testuser@example.com",
            "password": "testpassword123",
            "repassword": "differentpassword",
            "first_name": "Test",
            "last_name": "User",
            "code": "US",
            "phone": "1234567890",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Las contraseñas no coinciden.", response.context['error'])

    def test_signup_usu_post_existing_employee(self):
        user = User.objects.create_user(
            username="existinguser@example.com",
            password="testpassword123",
            email="existinguser@example.com",
            first_name="Existing",
            last_name="User",
            phone="1234567890",
            country_code="US",
            is_employee=True,
        )
        Employee.objects.create(user=user, doc="123456789")
        data = {
            "doc_id": "123456789",
            "your_email": "newuser@example.com",
            "password": "testpassword123",
            "repassword": "testpassword123",
            "first_name": "New",
            "last_name": "User",
            "code": "US",
            "phone": "0987654321",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ya existe un empleado con ese documento.", response.context['error'])

class SigninTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('signin')
        self.user = User.objects.create_user(
            username='testuser@example.com',
            password='testpassword123'
        )
    
    def test_signin_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    
    """def test_signin_post_success(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('signin'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)"""

    def test_signin_post_invalid_credentials(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIn('Credenciales invalidas', response.context['error'])
        self.assertFalse(response.wsgi_request.user.is_authenticated)

class TestSignupCon(TestCase):
    def setUp(self):
        self.url = reverse('signup_con')

    def test_signup_con_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup-con.html')

    def test_signup_con_post_password_mismatch(self):
        data = {
            "password": "testpassword123",
            "repassword": "differentpassword",
            "your_email": "testuser@example.com",
            "first_name": "Test",
            "code": "US",
            "phone": "1234567890",
            "nit_id": "123456789",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Las contraseñas no coinciden.", response.context['error'])

    def test_signup_con_post_existing_nit(self):
        user = User.objects.create_user(
            username="existinguser",
            password="testpassword123",
            email="existinguser@example.com"
        )
        Company.objects.create(user=user, nit="123456789")
        data = {
            "password": "testpassword123",
            "repassword": "testpassword123",
            "your_email": "testuser@example.com",
            "first_name": "Test",
            "code": "US",
            "phone": "1234567890",
            "nit_id": "123456789",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ya existe una compañía con ese NIT.", response.context['error'])

    def test_signup_con_post_success(self):
        data = {
            "password": "testpassword123",
            "repassword": "testpassword123",
            "your_email": "testuser@example.com",
            "first_name": "Test",
            "code": "US",
            "phone": "1234567890",
            "nit_id": "123456789",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirección a la página de login
        self.assertTrue(User.objects.filter(username="testuser@example.com").exists())
        self.assertTrue(Company.objects.filter(nit="123456789").exists())