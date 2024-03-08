import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError
from models import db, User, Message, Follow, Like, DEFAULT_IMAGE_URL

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

from app import app

db.drop_all()
db.create_all()

Msg1 = dict(text='testing1', user_id=1)
Msg2 = dict(text='testing2', user_id=2)

class MessageModelTestCase(TestCase):
    ''' Tests message model '''

    def setUp(self):
        Message.query.delete()
        User.query.delete()

        db.session.commit()
        m1 = Message(**Msg1)
        m2 = Message(**Msg2)

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        # must append here, the rest, including the db relationships,
        # is abstracted away
        u1.messages.append(m1)
        u2.messages.append(m2)

        db.session.commit()

        self.u1_id = u1.id
        self.u2_id = u2.id

        self.m1_id = m1.id
        self.m2_id = m2.id


    def tearDown(self):
        db.session.rollback()


    def test_message_model(self):
        '''Tests message model'''

        m1 = Message.query.get(self.m1_id)

        self.assertEqual(m1.text, 'testing1')
        self.assertIsInstance(m1, Message)


    def test_users_messages(self):
        '''Tests message model'''
        u1 = User.query.get(self.u1_id)
        m1 = Message.query.get(self.m1_id)

        self.assertEqual(len(u1.messages), 1)

        self.assertIs(u1.messages[0], m1)

    def test_add_message(self):
        u1 = User.query.get(self.u1_id)

        u1.messages.append(Message(**Msg1))
        db.session.commit()
        self.assertEqual(len(u1.messages), 2)

    def test_like_message(self):
        pass

    def test_unlike_message(self):
        pass

    def test_delete_message(self):
        pass

    def test_empty_message(self):
        pass