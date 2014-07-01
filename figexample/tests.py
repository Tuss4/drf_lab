from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from fig_codelab.models import Employee
from pprint import pprint
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import json
from pprint import pprint


class APITestCase(TestCase):
    """
    Setup class, so I can take care of
    Users, Employees, and the APIClient.
    """

    root_user = dict(user='root',
                     email='root@example.com',
                     passw='root',
                     super=True,
                     staff=True)

    reg_user = dict(user='rick_james',
                    email='im@rick.james',
                    passw='superfreaky')

    post_employee_json = json.dumps(dict(first_name='Glenn',
                                         last_name='Quagmire',
                                         salary=500.00))
    def setUp(self):
        self.client = APIClient()
        User.objects.create(username=self.root_user['user'],
                            password=self.root_user['passw'],
                            email=self.root_user['email'],
                            is_superuser=self.root_user['super'],
                            is_staff=self.root_user['staff'])
        User.objects.create(username=self.reg_user['user'],
                            password=self.reg_user['passw'],
                            email=self.reg_user['email'])
        Employee.objects.create(first_name='Randy',
                                last_name='Marsh',
                                salary=1000.00)
        Employee.objects.create(first_name='Gerald',
                                last_name='Broflovski',
                                salary=90000)
        #Get or create Tokens
        for user in User.objects.all():
            Token.objects.get_or_create(user=user)


class GetTest(APITestCase):
    def test_list_all(self):
        response = self.client.get('/api/v1/employees/')
        self.assertEqual(response.status_code, 200)

    def test_get_obj(self):
        employee_one = Employee.objects.get(first_name='Randy', last_name='Marsh')
        url = '/api/v1/employees/' + str(employee_one.pk) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class PostTest(APITestCase):
    def test_post_success(self):
        """
        User is staff/admin and Token is set.
        """
        self.client.login(username='root', password='root')
        token = Token.objects.get(user__username='root')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = '/api/v1/employees/'
        data = self.post_employee_json
        request = self.client.post(url, data, content_type='application/json')
        self.assertEqual(request.status_code, 201)

    def test_post_failure(self):
        """
        Regular user attempts to post.
        """
        self.client.login(username='rick_james', password='superfreaky')
        token = Token.objects.get(user__username='rick_james')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        url = '/api/v1/employees/'
        data = self.post_employee_json
        request = self.client.post(url, data, content_type='application/json')
        self.assertEqual(request.status_code, 403)


class PutTest(APITestCase):
    def test_put_success(self):
        """
        User is staff and token is set.
        """
        self.client.login(username='root', password='root')
        token = Token.objects.get(user__username='root')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        employee = Employee.objects.get(first_name='Randy')
        emp_data = json.dumps(dict(first_name=employee.first_name,
                                   last_name=employee.last_name,
                                   salary=3000))
        url = '/api/v1/employees/' + str(employee.id) + '/'
        request = self.client.put(url, emp_data, content_type='application/json')
        self.assertEqual(request.status_code, 200)

    def test_put_failure(self):
        """
        Regular user attempts to put.
        """
        self.client.login(username='rick_james', password='superfreaky')
        token = Token.objects.get(user__username='rick_james')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        employee = Employee.objects.get(first_name='Randy')
        emp_data = json.dumps(dict(first_name=employee.first_name,
                                   last_name=employee.last_name,
                                   salary=3000))
        url = '/api/v1/employees/' + str(employee.id) + '/'
        request = self.client.put(url, emp_data, content_type='application/json')
        self.assertEqual(request.status_code, 403)


class PatchTest(APITestCase):
    def test_patch_success(self):
        """
        User is staff and token is set.
        Update salary.
        """
        self.client.login(username='root', password='root')
        token = Token.objects.get(user__username='root')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        employee = Employee.objects.get(first_name='Gerald')
        emp_data = json.dumps(dict(salary=60000))
        url = '/api/v1/employees/' + str(employee.id) + '/'
        request = self.client.patch(url, emp_data, content_type='application/json')
        self.assertEqual(request.status_code, 200)

    def test_patch_failure(self):
        """
        Regular user.
        Update salary.
        """
        self.client.login(username='rick_james', password='superfreaky')
        token = Token.objects.get(user__username='rick_james')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        employee = Employee.objects.get(first_name='Gerald')
        emp_data = json.dumps(dict(salary=60000))
        url = '/api/v1/employees/' + str(employee.id) + '/'
        request = self.client.patch(url, emp_data, content_type='application/json')
        self.assertEqual(request.status_code, 403)


class DeleteTest(APITestCase):
    def test_delete_success(self):
        """
        User is staff and token is set.
        Delete Randy Marsh.
        """
        self.client.login(username='root', password='root')
        token = Token.objects.get(user__username='root')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        employee = Employee.objects.get(first_name='Randy')
        url = '/api/v1/employees/' + str(employee.id) + '/'
        request = self.client.delete(url)
        self.assertEqual(request.status_code, 204)

    def test_delete_failure(self):
        """
        Regular user.
        Delete Randy Marsh.
        """
        self.client.login(username='rick_james', password='superfreaky')
        token = Token.objects.get(user__username='rick_james')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        employee = Employee.objects.get(first_name='Randy')
        url = '/api/v1/employees/' + str(employee.id) + '/'
        request = self.client.delete(url)
        self.assertEqual(request.status_code, 403)
