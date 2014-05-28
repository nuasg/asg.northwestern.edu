from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit
from asg.models import Person

class PersonForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '/edit_profile/'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'Save changes'))

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'email', 'bio', 'photo', 'thumbnail_size')


class ASGAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(ASGAuthForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = '/login/'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-10'
        self.helper.add_input(Submit('login', 'Log in'))

        self.helper.layout = Layout(
            Field('username', placeholder='NetID'),
            Field('password', placeholder='Password'),
            Field('login'),
        )
