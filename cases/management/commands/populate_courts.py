from django.core.management.base import BaseCommand
from cases.models import Court

class Command(BaseCommand):
    help = 'Populate initial court data'

    def handle(self, *args, **options):
        courts_data = [
            {
                'name': 'Delhi High Court',
                'base_url': 'https://delhihighcourt.nic.in',
                'court_type': 'HIGH',
                'is_active': True
            },
            {
                'name': 'Faridabad District Court',
                'base_url': 'https://districts.ecourts.gov.in/faridabad',
                'court_type': 'DISTRICT',
                'is_active': True
            },
            {
                'name': 'Gurgaon District Court',
                'base_url': 'https://districts.ecourts.gov.in/gurgaon',
                'court_type': 'DISTRICT',
                'is_active': True
            }
        ]

        for court_data in courts_data:
            court, created = Court.objects.get_or_create(
                name=court_data['name'],
                defaults=court_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created court: {court.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Court already exists: {court.name}')
                )
