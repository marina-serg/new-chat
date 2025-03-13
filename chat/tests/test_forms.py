from django.test import TestCase

from chat.forms import GroupForm, InviteUserForm


class GroupFormTests(TestCase):

    def setUp(self):
        self.valid_data = {
            'name': 'Test Group',
            'chat_avatar': None}
        self.invalid_data = {
            'name': '',
            'chat_avatar': None}

    def test_group_form_valid(self):
        form = GroupForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_group_form_invalid(self):
        form = GroupForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_group_form_saves_correctly(self):
        form = GroupForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
        group = form.save()
        self.assertEqual(group.name, self.valid_data['name'])


class InviteUserFormTests(TestCase):

    def setUp(self):
        self.valid_data = {
            'email': 'testuser1@yandex.ru'
        }
        self.invalid_data = {
            'email': 'invalid-email'}

    def test_invite_user_form_valid(self):
        form = InviteUserForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invite_user_form_invalid(self):
        form = InviteUserForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
