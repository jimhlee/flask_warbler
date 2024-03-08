"""User model tests."""
# Before anything else, we must create the test database.
# Here we're calling it warbler_test which you can see in the os.environ assignment
# below

# run these tests(outside of ipython) like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError
from models import db, User, Message, Follow, Like, DEFAULT_IMAGE_URL

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    '''Tests user model.'''

    def setUp(self):
        '''Sets up two users.'''
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

    def tearDown(self):
        db.session.rollback()

    def test_user_model(self):
        '''Tests user model itself'''
        u1 = User.query.get(self.u1_id)

        # User should have no messages/followers/liked msgs and default image url
        self.assertEqual(len(u1.messages), 0)
        self.assertEqual(len(u1.followers), 0)
        self.assertEqual(len(u1.liked_messages), 0)
        self.assertEqual(u1.image_url, DEFAULT_IMAGE_URL)


    def test_follows(self):
        '''Tests user.follows and user.following'''
        u1 = User.query.get(self.u1_id)
        u2 = User.query.get(self.u2_id)

        u1.following.append(u2)

        self.assertEqual(len(u1.following), 1)
        self.assertEqual(len(u2.followers), 1)
        self.assertIs(u1.is_following(u2), True)
        self.assertIs(u1.is_followed_by(u2), False)
        self.assertIs(u2.is_followed_by(u1), True)
        self.assertIs(u2.is_following(u1), False)


    def test_update_user(self):
        '''Test user update'''
        u1 = User.query.get(self.u1_id)

        u1.username = 'test_1'
        u1.email = 'test_1@email.com'
        u1.image_url = 'test_1.com'
        u1.bio = 'test_1 bio'
        u1.location = 'testing, USA'
        u1.header_image_url = 'test_header_1.com'

        self.assertIs(u1.username, 'test_1')
        self.assertIs(u1.email, 'test_1@email.com')
        self.assertIs(u1.image_url, 'test_1.com')
        self.assertIs(u1.bio, 'test_1 bio')
        self.assertIs(u1.location, 'testing, USA')
        self.assertIs(u1.header_image_url, 'test_header_1.com')


    def test_authenticate_user_success(self):
        '''Test user authentication success'''
        u1 = User.query.get(self.u1_id)

        self.assertIs(User.authenticate(u1.username, 'password'), u1)


    def test_authenticate_user_failure_password(self):
        '''Test user authentication failure'''
        u1 = User.query.get(self.u1_id)

        self.assertFalse(User.authenticate(u1.username, 'test_password'))


    def test_authenticate_user_failure_username(self):
        '''Test user authentication failure'''
        u1 = User.query.get(self.u1_id)

        self.assertFalse(User.authenticate('test_username', 'password'))


    def test_signup_user_success(self):
        '''Test user authentication'''
        u3 = User.signup("u3", "u3@email.com", "password", None)
        db.session.commit()

        self.assertIsInstance(u3, User)
        self.assertIs(User.query.get(u3.id), u3)


    def test_signup_user_failure_invalid_password(self):
        with self.assertRaises(ValueError):
            User.signup("u4", "u3@email.com", '', None)


    def test_signup_failre_invalid_username(self):
        with self.assertRaises(IntegrityError):
            User.signup(None, "u4@email.com", "password", None)
            db.session.commit()

