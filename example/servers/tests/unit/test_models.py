from example.servers.models import Server
from ..factories import ServerFactory
from django.forms.models import model_to_dict
from django.test import TestCase
from django.conf import settings
from example.servers.models import OperatingSystem
from ..factories import OperatingSystemFactory
from django.db import IntegrityError

class TestCaseOperatingSystem(TestCase):

    def test_create(self):
        """
        Test the creation of a OperatingSystem model using a factory
        """
        operatingsystem = OperatingSystemFactory.create()
        self.assertEqual(1, OperatingSystem.objects.count())

    def test_create_batch(self):
        """
        Test the creation of 5 OperatingSystem models using a factory
        """
        operatingsystems = OperatingSystemFactory.create_batch(5)
        self.assertEqual(5, OperatingSystem.objects.count())
        self.assertEqual(5, len(operatingsystems))

    def test_attribute_count(self):
        """
        Test that all attributes of OperatingSystem server are counted. It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """
        operatingsystem = OperatingSystemFactory.create()
        operatingsystem_dict = model_to_dict(operatingsystem)
        self.assertEqual(5, len(operatingsystem_dict.keys()))

    def test_attribute_content(self):
        """
        Test that all attributes of OperatingSystem server have content. This test will break if an attributes name is changed.
        """
        operatingsystem = OperatingSystemFactory.create()
        self.assertIsNotNone(operatingsystem.id)
        self.assertIsNotNone(operatingsystem.name)
        self.assertIsNotNone(operatingsystem.version)
        self.assertIsNotNone(operatingsystem.licenses_available)
        self.assertIsNotNone(operatingsystem.cost)

    # def test_(self):
    #     operatingsystem = OperatingSystemFactory.create()
    #     servers = ServerFactory.create_batch(5, operating_system=operatingsystem)
    #     from django.conf import settings
    #     from django.db import connection, reset_queries
    #
    #     try:
    #         settings.DEBUG = True
    #         #servers = operatingsystem.servers.all()
    #         for s in servers:
    #             k = s.operating_system.name
    #         self.assertEquals(len(connection.queries), 1000000)
    #     finally:
    #         settings.DEBUG = False
    #         reset_queries()






class TestCaseServer(TestCase):

    def test_create(self):
        """
        Test the creation of a Server model using a factory
        """
        server = ServerFactory.create()
        self.assertEqual(1, Server.objects.count())

    def test_create_batch(self):
        """
        Test the creation of 5 Server models using a factory
        """
        servers = ServerFactory.create_batch(5)
        self.assertEqual(5, Server.objects.count())
        self.assertEqual(5, len(servers))


    def test_attribute_count(self):
        """
        Test that all attributes of Server server are counted. It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """
        server = ServerFactory.create()
        server_dict = model_to_dict(server)
        self.assertEqual(11, len(server_dict.keys()))


    def test_attribute_content(self):
        """
        Test that all attributes of Server server have content. This test will break if an attributes name is changed.
        """
        server = ServerFactory.create()
        self.assertIsNotNone(server.id)
        self.assertIsNotNone(server.name)
        self.assertIsNotNone(server.notes)
        self.assertIsNotNone(server.virtual)
        self.assertIsNotNone(server.ip_address)
        self.assertIsNotNone(server.created)
        self.assertIsNotNone(server.online_date)
        self.assertIsNotNone(server.operating_system)
        self.assertIsNotNone(server.server_id)
        self.assertIsNotNone(server.use)
        self.assertIsNotNone(server.comments)

    def test_name_is_unique(self):
        """
        Tests attribute name of model Server to see if the unique constraint works.
        This test should break if the unique attribute is changed.
        """
        server = ServerFactory.create()
        server_02 = ServerFactory.create()
        server_02.name = server.name
        try:
            server_02.save()
            self.fail('Test should have raised and integrity error')
        except IntegrityError as e:
            self.assertEqual('UNIQUE constraint failed: my_app_server.name', str(e))
