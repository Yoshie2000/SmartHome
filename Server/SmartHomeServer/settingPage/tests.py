# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import resolve
from django.core.urlresolvers import reverse

from django.test import TestCase

from .views import home, edit_profile
from .models import Profile

class HomeTests(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(name='Rainbow', description='The default rainbow profile')
        url = reverse('home')
        self.response = self.client.get(url)
    
    def testStatusCode(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        
    def testURL(self):
        view = resolve('/')
        self.assertEquals(view.func, home)
        
    def testLinkExistance(self):
        profile_url = reverse('edit_profile', kwargs={'pk': self.profile.pk})
        self.assertContains(self.response, 'href="{0}"'.format(profile_url))

class EditProfileTest(TestCase):
    def setUp(self):
        profile = Profile.objects.create(name='Rainbow', description='The default rainbow profile')

    def testStatusCode(self):
        url = reverse('edit_profile', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def testNotFoundStatusCode(self):
        url = reverse('edit_profile', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def testURL(self):
        view = resolve('/profiles/1/')
        self.assertEquals(view.func, edit_profile)
        
    def testLinkExistance(self):
        profiles_url = reverse('edit_profile', kwargs={'pk': 1})
        response = self.client.get(profiles_url)
        homepage_url = reverse('home')
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
