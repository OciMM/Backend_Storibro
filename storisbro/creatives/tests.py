from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import AddSingleCreative, TypeButton, StatusCreative
from django.contrib.auth import get_user_model
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class AddSingleCreativeAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse('addsinglecreative')  # Убедитесь, что у вас есть правильный URL
        self.user = User.objects.create_user(
            email='test123@gmail.com', 
            password='testpassword'
        )
        self.button_type = TypeButton.objects.create(name_button="Test Button")
        self.status = StatusCreative.objects.create(status="Test Status")
        
        self.client.login(email='test123@gmail.com', password='testpassword')

    def test_post_add_single_creative(self):
        # Создаем фейковый файл для загрузки
        file_content = b'This is a test file content.'
        fake_file = SimpleUploadedFile("test_file.txt", file_content, content_type="text/plain")
        
        data = {
            'name': 'Test Creative',
            'link': 'https://ru.wikipedia.org/wiki/%D0%A4%D0%BE%D1%80%D0%B4,_%D0%93%D0%B5%D0%BD%D1%80%D0%B8',
            'file': fake_file,
            'button': self.button_type.id,
            'status': self.status.id
        }

        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AddSingleCreative.objects.count(), 1)
        creative = AddSingleCreative.objects.first()
        self.assertEqual(creative.name, 'Test Creative')
        self.assertEqual(creative.link, creative.link)
        self.assertTrue(creative.file)

    def test_post_add_single_creative_without_link(self):
        file_content = b'This is a test file content.'
        fake_file = SimpleUploadedFile("test_file.txt", file_content, content_type="text/plain")
        
        data = {
            'name': 'Test Creative',
            'file': fake_file,
            'button': self.button_type.id,
            'status': self.status.id
        }

        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(AddSingleCreative.objects.count(), 0)
