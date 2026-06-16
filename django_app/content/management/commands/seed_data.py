import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from content.models import Conference, Track, Session, Speaker, SessionSpeaker, Registration
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

TRACK_NAMES = ["Backend", "Frontend", "DevOps", "IA", "Blockchain", "Seguridad", "Mobile"]
SPEAKER_NAMES = ["Ana López", "Carlos Mamani", "María Quispe", "Juan Flores", "Lucía Torrez"]

class Command(BaseCommand):
    help = 'Seed de datos iniciales — 300 sessions, speakers, registrations'

    def handle(self, *args, **kwargs):
        if Session.objects.count() >= 300:
            self.stdout.write('Seed ya ejecutado, saltando')
            return

        self.stdout.write('Creando datos...')

        speakers = []
        for name in SPEAKER_NAMES:
            s, _ = Speaker.objects.get_or_create(
                name=name,
                defaults={'bio': f'Bio de {name}'}
            )
            speakers.append(s)

        users = []
        for i in range(20):
            u, _ = User.objects.get_or_create(
                username=f'user{i}',
                defaults={'email': f'user{i}@test.com'}
            )
            u.set_password('test1234')
            u.save()
            users.append(u)

        for c in range(5):
            conference = Conference.objects.create(
                name=f'Conferencia Tech Bolivia {c+1}',
                description=f'Descripción de la conferencia {c+1}',
                starts_at=timezone.now() + timedelta(days=c*30),
                ends_at=timezone.now() + timedelta(days=c*30+3),
            )

            for t in range(len(TRACK_NAMES)):
                track = Track.objects.create(
                    name=TRACK_NAMES[t],
                    conference=conference,
                )

                for s in range(12):
                    session = Session.objects.create(
                        title=f'Sesión {s+1} — {TRACK_NAMES[t]}',
                        description=f'Descripción de la sesión {s+1}',
                        starts_at=timezone.now() + timedelta(days=c*30, hours=s),
                        capacity=random.randint(20, 100),
                        track=track,
                    )

                    for speaker in random.sample(speakers, k=random.randint(1, 2)):
                        SessionSpeaker.objects.get_or_create(
                            session=session,
                            speaker=speaker
                        )

                    for user in random.sample(users, k=random.randint(3, 10)):
                        Registration.objects.get_or_create(
                            user=user,
                            session=session
                        )

        count = Session.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Seed completo — {count} sessions creadas'))
