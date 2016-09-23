import csv
from django.core.management.base import BaseCommand, CommandError
from asg.models import *
from command_utils import get_ldap_info

class Command(BaseCommand):
    args = 'file.csv - a csv file (without headers) with two columns: committee and personal Northwestern email address'
    help = 'Update current committee members based on a CSV file'

    def handle(self, *args, **options):
        if len(args) < 1:
            print 'Missing name of csv file'
            return

        # Remove all old committee members
        Committee.members.through.objects.all().delete()

        with open(args[0], 'r') as f:
            reader = csv.DictReader(f, fieldnames=('committee', 'email'))
            people_added = 0
            for i, row in enumerate(reader):
                # Fetch info from the directory
                ldap_info = get_ldap_info(email=row['email'])

                # Get the relevant committee
                committee, _ = Committee.objects.get_or_create(name=row['committee'])

                # Create a Person object -- if they haven't yet logged in,
                # the corresponding user object will be created when they do
                # Note: there's not a position for committee members
                person, created = Person.objects.get_or_create(netid=ldap_info['uid'][0],
                                    defaults={'first_name': ldap_info['givenName'][0],
                                              'last_name': ldap_info['sn'][0],
                                              'email': ldap_info['mail'][0]})
                committee.members.add(person)

                if created:
                    people_added += 1

                # Create an ApprovedUser object so this person can log in later
                au, _ = ApprovedUser.objects.get_or_create(netid=ldap_info['uid'][0])

            print 'Added %d new committee members' % people_added

