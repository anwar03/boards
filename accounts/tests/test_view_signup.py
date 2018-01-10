from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.test import TestCase
from django.contrib.auth.forms import UserCreationForm
from ..views import signup
from ..forms import signUpForm

class SignUpForm(TestCase):

    def test_form_has_field(self):
        form = signUpForm()
        expected = ['username', 'email', 'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

class signUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)

    def test_csrftoken(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    
    def test_contain_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, signUpForm)

    def test_form_inputs(self):
        '''
        The view must contain five inputs: csrf, username, email,
        password1, password2
        '''
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class successfulSignupTests(TestCase):

    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'john',
            'email': 'test@test.com',
            'password1': 'asdf1234',
            'password2': 'asdf1234'
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')
    
    def test_redirect_home(self):
        '''
        A user submitted valid data user redirect to home page.
        '''
        self.assertRedirects(self.response, self.home_url)
    
    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)



class invalidSignUP(TestCase):

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})

    def test_signup_status_code(self):
        ''' An invalid form submission should return to be same page.'''
        self.assertEquals(self.response.status_code, 200)
    
    def test_invalid_user(self):
        self.assertFalse(User.objects.exists())

    def test_error_form(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)