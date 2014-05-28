from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Fieldset, HTML, Layout, Submit
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

        person = kwargs.get('instance')

        layout = [
            Field('first_name'), 
            Field('last_name'),
            HTML('<div id="div_id_position" class="form-group"><label for="id_position" class="control-label col-md-3">Main position</label><div class="controls col-md-9"><input class="form-control" id="id_position" disabled value="{{ person.main_position }}"></div></div>'),
            Field('email'),
            Field('bio', placeholder='Spill your heart out, but keep it kinda short.'),
            Field('photo'),
            Field('thumbnail_size'),
        ]

        if person.is_senator():
            layout.append(HTML('<div id="div_id_groups_represented" class="form-group"><label for="id_groups_represented" class="control-label col-md-3">Groups represented</label><div class="controls col-md-9"><input class="form-control" id="id_groups_represented" disabled value="{{ person.groups_represented }}"></div></div>'))
            layout.append(Field('full_groups', rows=4))
        else:
            layout.append(Field('full_groups', type='hidden', disabled=True))

        self.helper.layout = Layout(*layout)

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'bio', 'photo', 'thumbnail_size', 'full_groups']


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
