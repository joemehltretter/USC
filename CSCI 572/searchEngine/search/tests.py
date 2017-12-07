# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from search.models import Item

class ItemModelTest(TestCase):

  def test_save_and_retrieve_items(self):
    first_item = Item()
    first_item.query = "Test1"
    first_item.save()

    second_item = Item()
    second_item.query = "Test2"
    second_item.save()

    saved_items = Item.objects.all()
    self.assertEqual(saved_items.count(), 2)

    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    self.assertEqual(first_saved_item.query, 'Test1')
    self.assertEqual(second_saved_item.query, 'Test2')


  def test_save_POST_request(self):
    response = self.client.post('/', data={'item_text': 'A query made'})

    self.assertEqual(Item.objects.count(), 1)
    new_item = Item.objects.first()
    self.assertEqual(new_item.query, 'A query made')

    self.assertEqual(response.status_code, 302)
    self.assertEqual(response['location'], '/')

  def test_redirects_after_POST(self):
    response = self.client.post('/', data = {'item_text': 'A query made'})
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response['location'], '/')

def test_uses_home_template(self):
  response = self.client.get('/')
  self.assertTemplateUsed(response, 'search/home.html')

def test_can_save_a_POST_request(self):
  response = self.client.post('/', data={'item_text': 'A new query'})
  self.assertIn('A new query', response.content.decode())
  self.assertTemplateUsed(response, 'search/home.html')
