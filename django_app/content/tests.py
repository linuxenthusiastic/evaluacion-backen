import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from content.models import Conference, Track, Session, Speaker, SessionSpeaker, Registration
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class ConferenceModelTest(TestCase):

    def setUp(self):
        self.conference = Conference.objects.create(
            name='PyCon Bolivia 2025',
            description='La mejor conferencia de Python',
            starts_at=timezone.now(),
            ends_at=timezone.now() + timedelta(days=3),
        )

    def test_conference_creation(self):
        self.assertEqual(self.conference.name, 'PyCon Bolivia 2025')
        self.assertIsNotNone(self.conference.id)
        self.assertIsNotNone(self.conference.created)

    def test_conference_str(self):
        self.assertEqual(str(self.conference), 'PyCon Bolivia 2025')

    def test_track_belongs_to_conference(self):
        track = Track.objects.create(
            name='Backend',
            conference=self.conference,
        )
        self.assertEqual(track.conference, self.conference)

        self.assertIn(track, self.conference.tracks.all())

    def test_session_capacity(self):
        track = Track.objects.create(name='Backend', conference=self.conference)
        session = Session.objects.create(
            title='Intro a FastAPI',
            starts_at=timezone.now(),
            capacity=50,
            track=track,
        )
        self.assertEqual(session.capacity, 50)

    def test_unique_registration(self):
        track = Track.objects.create(name='Backend', conference=self.conference)
        session = Session.objects.create(
            title='Intro a FastAPI',
            starts_at=timezone.now(),
            capacity=50,
            track=track,
        )
        user = User.objects.create_user(username='testuser', password='test1234')

        Registration.objects.create(user=user, session=session)

        with self.assertRaises(Exception):
            Registration.objects.create(user=user, session=session)

    def test_many_to_many_speakers(self):
        track = Track.objects.create(name='Backend', conference=self.conference)
        session = Session.objects.create(
            title='Intro a FastAPI',
            starts_at=timezone.now(),
            capacity=50,
            track=track,
        )
        speaker = Speaker.objects.create(name='Ana López', bio='Dev senior')
        SessionSpeaker.objects.create(session=session, speaker=speaker)

        self.assertIn(speaker, session.speakers.all())
