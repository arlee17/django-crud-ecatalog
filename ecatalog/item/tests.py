from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from item.models import Item, Category
from django.core.files.uploadedfile import SimpleUploadedFile

class ItemActionsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass'
        )
        self.category = Category.objects.create(
            name='Test Category'
        )
        image_data = b'binary_data_for_testing'
        self.image = SimpleUploadedFile("test_image.jpg", image_data, content_type="image/jpeg")
        self.item_data = {
            'category': self.category,
            'name': 'Test Item',
            'description': 'This is a test item',
            'price': 100.0,
            'image': self.image,
        }
        self.item = Item.objects.create(**self.item_data, created_by=self.user)

    def test_create_item(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('item:new'), data=self.item_data)
        self.assertEqual(response.status_code, 200)
        item = Item.objects.last()
        self.assertEqual(item.category, self.category)
        self.assertEqual(item.name, 'Test Item')
        self.assertEqual(item.description, 'This is a test item')
        self.assertEqual(item.price, 100.0)
        self.assertEqual(item.created_by, self.user)

    def test_read_item(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('item:detail', args=[self.item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Item')
        self.assertContains(response, 'This is a test item')
        self.assertContains(response, '100.0')
        
    def test_update_item(self):
        self.client.login(username='testuser', password='testpass')
        item = Item.objects.get(id=self.item.id)
        updated_data = {
            'category': self.category.id,
            'name': 'Updated Test Item',
            'description': 'This is an updated test item',
            'price': 200.0,
        }
        response = self.client.post(reverse('item:edit', args=[self.item.id]), data=updated_data)
        self.assertEqual(response.status_code, 302)
        item.refresh_from_db()
        self.assertEqual(item.name, 'Updated Test Item')
        self.assertEqual(item.description, 'This is an updated test item')
        self.assertEqual(item.price, 200.0)

    def test_delete_item(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('item:delete', args=[self.item.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Item.objects.filter(id=self.item.id).exists())
