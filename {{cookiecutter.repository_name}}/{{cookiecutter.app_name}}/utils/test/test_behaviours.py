# import datetime
# import uuid

# from django.db import connection
# from django.db.models import CharField
# from django.test import TestCase

# from ..behaviours import IDable, Ownable, Timeframable, Timestampable
# from ..users.test.factories import UserFactory


# class IDableTestModel(IDable):
#     class Meta:
#         app_label = "cvalki.users"


# class OwnableTestModel(Ownable):
#     class Meta:
#         app_label = "cvaliki.users"


# class TimeframableTestModel(Timeframable):
#     class Meta:
#         app_label = "cvalki.users"


# class TimestampableTestModel(Timestampable):
#     data_point = CharField(max_length=50, blank=True, null=True)

#     class Meta:
#         app_label = "cvalki.users"


# class TestIDableBehaviour(TestCase):
#     model = IDableTestModel

#     def setUp(self):
#         with connection.schema_editor() as schema_editor:
#             schema_editor.create_model(self.model)

#     def test_idable_behaviour_adds_uuid4_primary_key(self):
#         test_model = self.model.objects.create()
#         self.assertTrue(isinstance(test_model.id, uuid.UUID))


# class TestOwnableBehaviour(TestCase):
#     model = OwnableTestModel

#     def setUp(self):
#         self.user = UserFactory.create()
#         with connection.schema_editor() as schema_editor:
#             schema_editor.create_model(self.model)

#     def test_ownable_model_relates_to_user(self):
#         instance = self.model.objects.create(owner=self.user)
#         instance.save()
#         self.assertEqual(instance.owner, self.user)
#         self.assertEqual(self.user.ownabletestmodel_set.first(), instance)


# class TestTimeframableBehaviour(TestCase):
#     model = TimeframableTestModel

#     def setUp(self):
#         self.user = UserFactory.create()
#         with connection.schema_editor() as schema_editor:
#             schema_editor.create_model(self.model)

#     def test_timeframable_model_raises_an_error_when_end_date_is_before_start_date(
#             self
#     ):
#         with self.assertRaises(ValueError):
#             instance = self.model.objects.create(
#                 start_date=datetime.date(2005, 5, 5), end_date=datetime.date(2005, 5, 4)
#             )

#     def test_timeframable_model_raises_an_error_when_start_date_is_in_the_future(self):
#         with self.assertRaises(ValueError):
#             future_date = datetime.date.today() + datetime.timedelta(days=1)
#             instance = self.model.objects.create(start_date=future_date)

#     def test_setting_timeframable_model_to_active_sets_end_date_to_none(self):
#         instance = self.model.objects.create(
#             start_date=datetime.date(2005, 5, 5), active=True
#         )
#         self.assertIsNone(instance.end_date)


# class TestTimestampableBehaviour(TestCase):
#     model = TimestampableTestModel

#     def setUp(self):
#         with connection.schema_editor() as schema_editor:
#             schema_editor.create_model(self.model)

#     def test_timestampable_model_automatically_sets_created_date_and_updated_date(self):
#         instance = self.model.objects.create()
#         self.assertIsNotNone(instance.created_date)
#         self.assertIsNotNone(instance.modified_date)

#     def test_timestampable_model_updates_modified_date(self):
#         instance = self.model.objects.create()
#         created = instance.created_date
#         initial_modified_date = instance.modified_date
#         instance.data_point = "Test"
#         instance.save()
#         self.assertNotEqual(instance.modified_date, initial_modified_date)
