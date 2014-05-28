import csv
from django.core.management.base import BaseCommand, CommandError
from asg.models import *
from command_utils import get_ldap_info

class Command(BaseCommand):
    args = 'file.csv - a csv file (without headers) with two columns: Position and Email Address (the person\'s individual one)'
    help = 'Update the senate leadership based on a CSV file'

    def handle(self, *args, **options):
        if len(args) < 1:
            print 'Missing name of csv file'
            return

        with open(args[0], 'r') as f:
            reader = csv.DictReader(f, fieldnames=('position', 'email'))
            positions_created = 0
            people_added = 0
            for i, row in enumerate(reader):
                position, created = Position.objects.get_or_create(name=row['position'],
                                                        defaults={'senate_leadership': True})
                if created:
                    positions_created += 1
                position.order = i
                position.save()

                # Fetch info from the directory
                ldap_info = get_ldap_info(email=row['email'])

                # Remove old exec members with this position
                people = Person.objects.filter(positions=position)
                for p in people:
                    p.positions.remove(position)
                ApprovedUser.objects.filter(position=position).delete()

                # Create a Person object -- if they haven't yet logged in,
                # the corresponding user object will be created when they do
                person, created = Person.objects.get_or_create(netid=ldap_info['uid'][0],
                                    defaults={'first_name': ldap_info['givenName'][0],
                                              'last_name': ldap_info['sn'][0],
                                              'email': ldap_info['mail'][0]})
                if created:
                    people_added += 1
                person.positions.add(position)

                # Create an ApprovedUser object so this person can log in later
                au, _ = ApprovedUser.objects.get_or_create(netid=ldap_info['uid'][0],
                                                position=position)

            print 'Added %d people' % people_added
            print 'Created %d positions' % positions_created

