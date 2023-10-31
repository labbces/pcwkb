from django.test import SimpleTestCase
from django.urls import reverse, resolve
from pcwkb_core.views.views import species_page

class TestUrls(SimpleTestCase):

    def test_url_species(self):
        self.assertEquals(3, 4, msg='i do basic math')




