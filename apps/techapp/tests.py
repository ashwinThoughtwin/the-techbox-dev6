from django.contrib.auth.models import User
from django.test import TestCase
from .models import Employee, TechItem, AllottedItem
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import tempfile


class TechitemAPITestCase(APITestCase):

    def setUp(self):
        self.username = "rishi"
        self.email = "rishi@gmail.com"
        self.password = "some_strong_pass"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        TechItem.objects.create(item_name="Mouse",
                                item_description="This is mouse",
                                )
        TechItem.objects.create(item_name="Mouse2",
                                item_description="This is mouse2",
                                )

    def test_1_get_method(self):
        url = 'http://127.0.0.1:8000/api/api-techitem/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        qs = TechItem.objects.filter(item_name='Mouse')
        self.assertEqual(qs.count(), 1)

    def test_2_get_method_fail(self):
        url = 'http://127.0.0.1:8000/api/api-techitem'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 301)

    def test_3_post_method_success(self):
        url = 'http://127.0.0.1:8000/api/api-techitem/'
        data = {'item_name': "Mouse",
                # 'item_image': SimpleUploadedFile('small.gif',content=small_gif, content_type='image/png'),
                'item_description': "This is mouse",
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_4_post_method_fail(self):
        url = 'http://127.0.0.1:8000/api/api-techitem/'
        data = {'item_name': "Mouse",
                'item_image': "someimage",
                'item_description': "This is mouse",
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_5_update_method_success(self):
        url = 'http://127.0.0.1:8000/api/api-techitem/2/'
        data = {'item_name': "Mouseupdated",
                'item_description': "This is updated mouse",
                }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_6_update_method_fail(self):
        url = 'http://127.0.0.1:8000/api/api-techitem/3/'
        data = {'item_name': "Mouseupdated",
                'item_description': "This is updated mouse",
                }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 404)

    def test_7_delete_method_success(self):
        url = 'http://127.0.0.1:8000/api/api-techitem/2/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_8_delete_method_fail(self):
        url = 'http://127.0.0.1:8000/api/api-techitem/200/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)


class AssigntemAPITestCase(APITestCase):

    def setUp(self):
        self.username = "rishi"
        self.email = "rishi@gmail.com"
        self.password = "some_strong_pass"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        self.techitem = TechItem.objects.create(item_name='pendrive', item_description='This is pendrive')
        self.employee = Employee.objects.create(name="rishi", email="rishi@gmail.com", address="indore",
                                                mobile='1234567890',
                                                team="python")

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_9_post_method_success(self):
        url = 'http://127.0.0.1:8000/api/assign-techitem/'
        data = {
            "tech_item": self.techitem.id,
            "employee_name": self.employee.id,
            "issue_date": "2021-04-27T17:14:00Z",
            "end_date": "2021-04-27T17:15:00Z"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_10_post_method_fail(self):
        url = 'http://127.0.0.1:8000/api/assign-techitem/'
        data = {
            "employee_name": self.employee.id,
            "issue_date": "2021-04-27T17:14:00Z",
            "end_date": "2021-04-27T17:15:00Z"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)


class EmployeeAPITestCase(APITestCase):

    def setUp(self):
        self.username = "rishi"
        self.email = "rishi@gmail.com"
        self.password = "some_strong_pass"
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        Employee.objects.create(name="Mouse",
                                email="mouse@gmail.com",
                                address="This is mouse",
                                mobile="This is mouse",
                                team="This is mouse",
                                )

    def test_11_post_method(self):
        url = 'http://127.0.0.1:8000/api/add-employee/'
        data = {'name': "Mouse",
                'email': "this@gmail.com",
                'address': "This is mouse",
                'mobile': "This is mouse",
                'team': "This is mouse",
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)


# small_gif = Image.open('https://lh3.googleusercontent.com/proxy/Mbls8zS0MVjV_zyYPduW8Z33yCb6LHbliRlS0emK9YmVT1reksWZWGxbV0tY5SjhAtsOG7uHykfSJMUi2AKkWSnySQGoizMlhodm')
# Create your tests here.
# class RemoteAuthenticatedTest(APITestCase):
#     client_class = APIClient
#
#     def setUp(self):
#         self.username = 'rishi'
#         self.user = User.objects.create_user(username='rishi',
#                                              email='',
#                                              password='1234')
#         Token.objects.create(user=self.user)
#         super(RemoteAuthenticatedTest, self).setUp()


class EmployeeTestCase(TestCase):
    def setUp(self):
        Employee.objects.create(name='Rishiraj Singh',
                                email='rishi@gmail.com',
                                address='indore',
                                mobile='1234567890',
                                team='Python',
                                )
        Employee.objects.create(name='Rishiraj Singh2',
                                email='rishi@gmail.com',
                                address='indore2',
                                mobile='1234567890',
                                team='Python2',
                                )

    def test_12_employee_test(self):
        obj1 = Employee.objects.get(name='Rishiraj Singh')
        obj2 = Employee.objects.get(name='Rishiraj Singh2')
        obj3 = Employee.objects.get(address='indore')
        self.assertEqual(obj1.name, 'Rishiraj Singh')
        self.assertEqual(obj2.name, 'Rishiraj Singh2')
        self.assertEqual(obj3.address, 'indore')


class TechitemTestCase(TestCase):
    def setUp(self):
        TechItem.objects.create(item_name='mouse',
                                item_description='rishcom',

                                )

    def test_13_techitem_test(self):
        obj1 = TechItem.objects.get(item_name='mouse')
        self.assertEqual(obj1.item_name, 'mouse')
