import csv
from django.core.management.base import BaseCommand, CommandError
from asg.models import *
from command_utils import get_ldap_info

class Command(BaseCommand):
    args = 'file.csv - a csv file (without headers) with two columns: Groups represented and personal Northwestern email address'
    help = 'Update current senators based on a CSV file'

    def handle(self, *args, **options):
        if len(args) < 1:
            print 'Missing name of csv file'
            return

        position = Position.objects.get(name='Senator')

        # Remove old senators
        people = Person.objects.filter(positions=position)
        for p in people:
            p.positions.remove(position)
        approvals = ApprovedUser.objects.filter(position=position).delete()

        # Add new senators
        with open(args[0], 'r') as f:
            reader = csv.DictReader(f, fieldnames=('groups', 'email'))
            people_added = 0

            for i, row in enumerate(reader):
                # Skip vacant positions
                if len(row['email']) == 0:
                    continue

                # Fetch info from the directory
                ldap_info = get_ldap_info(email=row['email'])

                # Create a Person object -- if they haven't yet logged in,
                # the corresponding user object will be created when they do
                person, created = Person.objects.get_or_create(netid=ldap_info['uid'][0],
                                    defaults={'first_name': ldap_info['givenName'][0],
                                              'last_name': ldap_info['sn'][0],
                                              'email': ldap_info['mail'][0],
                                              'groups_represented': row['groups']})
                person.positions.add(position)

                if created:
                    people_added += 1

                if len(person.groups_represented) == 0:
                    person.groups_represented = row['groups']
                    person.save()

                # Create an ApprovedUser object so this person can log in later
                au, _ = ApprovedUser.objects.get_or_create(netid=ldap_info['uid'][0],
                                                position=position)

            print 'Added %d senators' % people_added
