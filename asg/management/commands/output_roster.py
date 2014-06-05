import csv
import sys
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from asg.models import *
from command_utils import get_ldap_info

class Command(BaseCommand):
    args = 'none'
    help = 'Outputs CSV data for all people in ASG'

    def handle(self, *args, **options):
        # Write results to stdout
        writer = csv.writer(sys.stdout)

        # Query: retrieve all people who are Senators/Exec members,
        # or who serve on a committee
        people = Person.objects.filter(Q(positions__isnull=False) |\
                                    Q(committee__isnull=False))\
                                    .order_by('last_name', 'first_name')

        # Write header row
        writer.writerow(('Name', 'Email', 'School', 'Position', 'Committee 1', 'Committee 2', 'Committee 3'))

        for person in people:
            if person.user:
                info = get_ldap_info(netid=person.user.username)
            else:
                # Some people haven't ever logged in
                info = get_ldap_info(email=person.email)
            school = info['nuCurriculumOnly'][0]
            committees = person.committee_set.all()
            committee_1 = committees[0] if len(committees) > 0 else ''
            committee_2 = committees[1] if len(committees) > 1 else ''
            committee_3 = committees[2] if len(committees) > 2 else ''
            writer.writerow((person.full_name(), person.email, school, person.main_position(), committee_1, committee_2, committee_3))

