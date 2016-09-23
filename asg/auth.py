from django.contrib.auth.models import User, Group
from django_auth_ldap.backend import LDAPBackend
from asg.models import *

class ASGLDAPBackend(LDAPBackend):
    # Override this method -- given a valid NetID entry,
    # check if the user is an ApprovedUser. If so,
    # get (or create) the user object, populating the fields,
    # creating the Person object, and adding the User to the
    # correct group.
    def get_or_create_user(self, username, ldap_user):
        # Check if this student should be able to log in
        # TODO this should be replaced by checking/modifying
        # the is_active flag on the User model
        try:
            approval = ApprovedUser.objects.get(netid=username)
        except ApprovedUser.DoesNotExist:
            return (None, False)

        # Check if the user object exists
        try:
            user = User.objects.get(username=username)
            return (user, False)
        except User.DoesNotExist:
            pass

        # If not, call the parent method
        user, _ = super(ASGLDAPBackend, self)\
                    .get_or_create_user(username, ldap_user)

        # Put user in the right group
        user.is_staff = True
        if approval.position:
            if approval.position.name == 'Senator':
                user.groups.add(Group.objects.get(name='Senators'))
            elif approval.position.on_exec_board or\
                    approval.position.senate_leadership:
                user.groups.add(Group.objects.get(name='Exec Board Members'))
        else:
            user.groups.add(Group.objects.get(name='Committee Members'))

        # Copy name and email to Person object
        person, created = Person.objects.get_or_create(netid=user.username,
                    defaults={'user': user,
                              'first_name': ldap_user.attrs['givenname'][0],
                              'last_name': ldap_user.attrs['sn'][0],
                              'email': ldap_user.attrs['mail'][0]})

        # If the person created a profile previously, update it
        if not created:
            person.user = user
            person.save()

        # Add position to Person object
        if approval.position:
            person.positions.add(approval.position)

        return (user, True)

