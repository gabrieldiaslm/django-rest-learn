from django.test import TestCase
from api.models import Patient
from api.views import patient_list_view


class PatientTestCase (TestCase):

    def test_patient_exists_name_birthdate_mothername_gender_view(self):
        self.assertIsNotNone (Patient.name)
        self.assertIsNotNone (Patient.birth_date)
        self.assertIsNotNone (Patient.mother_name)
        self.assertIsNotNone (Patient.gender)