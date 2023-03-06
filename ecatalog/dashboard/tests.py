from django.test import TestCase
from django.contrib.auth.models import User
from item.models import Category, Item

class ItemModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )

        cls.category = Category.objects.create(
            name='Test Category'
        )

        cls.item = Item.objects.create(
            category=cls.category,
            name='Test Item',
            description='This is a test item.',
            price=10.0,
            created_by=cls.user
        )

    def test_item_name(self):
        category = Category.objects.create(
            name='Test Category'
        )
        item = Item.objects.create(
            category=category, 
            name='Test Item',
            description='Test Item Description', 
            price=10.0, 
            created_by=self.user
        )
        expected_name = 'Test Item'
        self.assertEquals(item.name, expected_name)
