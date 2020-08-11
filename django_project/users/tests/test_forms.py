from django.test import TestCase
from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User
import pytest

class test_forms(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_user = User.objects.create(username="base_user", password="testing321", email='base@company.com')
        test_cases = ['valid', 'duplicate','bad_email','pass_mismatch']
        fields = ["username","email", "password1", "password2", "valid"]
        data = [
                ("test_valid", "test_bad@company.com", "testing321", "testing321", True),
                ("base_user", "test_bad@company.com", "testing321", "testing321", False), #duplicate
                ("test_bad", "test_bad", "testing321", "testing321", False), #bad email
                ("test_bad", "test_bad@company.com", "testing", "testing321", False),  #mismatched password
            ]

        dict_list = [dict(zip(fields,item)) for item in data]
        test_data_dict = dict(zip(test_cases,dict_list))
        cls.register_form_data = test_data_dict
        cls.register_form_fields = ["username","email", "password1", "password2"]

    @classmethod
    def tearDownClass(cls):
        pass
    
    def test_register_form_valid(self):
        test_data = self.register_form_data['valid']
        form_data = {k: test_data[k] for k in self.register_form_fields}

        form = UserRegisterForm(data=form_data)

        assert form.is_valid() == test_data['valid']

    def test_register_form_duplicate(self):
        test_data = self.register_form_data['duplicate']
        form_data = {k: test_data[k] for k in self.register_form_fields}

        form = UserRegisterForm(data=form_data)
        
        assert form.has_error('username') == True
        assert form.is_valid() == test_data['valid']

    def test_register_form_bad_email(self):
        test_data = self.register_form_data['bad_email']
        form_data = {k: test_data[k] for k in self.register_form_fields}

        form = UserRegisterForm(data=form_data)

        assert form.has_error('email') == True
        assert form.is_valid() == test_data['valid']

    
    def test_register_form_pass_mismatch(self):
        test_data = self.register_form_data['pass_mismatch']
        form_data = {k: test_data[k] for k in self.register_form_fields}

        form = UserRegisterForm(data=form_data)

        assert form.is_valid() == test_data['valid']
        assert form.has_error('password2') == True
        assert "password_mismatch" in form.error_messages

    def test_profile_form_valid_username(self):
        form_data = {'username':'new_username', 'email':self.base_user.email}

        form = UserUpdateForm(instance=self.base_user, data=form_data)

        assert form.is_valid() == True
    
    def test_profile_form_valid_email(self):
        form_data = {'username':self.base_user.username, 'email':'new_email@company.com'}

        form = UserUpdateForm(instance=self.base_user, data=form_data)

        assert form.is_valid() == True

    def test_profile_form_invalid_email(self):
        form_data = {'username':self.base_user.username, 'email':'new_email'}

        form = UserUpdateForm(instance=self.base_user, data=form_data)
        assert form.is_valid() == False
        assert form.has_error('email') == True