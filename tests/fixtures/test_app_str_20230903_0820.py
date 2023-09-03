
class TestCaseServer(TestCase):

    def test_create(self):
        """
        Test the creation of a Server model using a factory
        """
        server = ServerFactory.create()
        self.assertEqual(Server.objects.count(), 1)

    def test_create_batch(self):
        """
        Test the creation of 5 Server models using a factory
        """
        servers = ServerFactory.create_batch(5)
        self.assertEqual(Server.objects.count(), 5)
        self.assertEqual(len(servers), 5)


    def test_attribute_count(self):
        """
        Test that all attributes of Server server are counted. It will count the primary key and
        all editable attributes. This test should break if a new attribute is added.
        """
        server = ServerFactory.create()
        server_dict = model_to_dict(server)
        self.assertEqual(len(server_dict.keys()), 11)


    def test_attribute_content(self):
        """
        Test that all attributes of Server server have content. This test will break if an attributes name
        is changed.
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
            self.assertEqual(str(e), '') #FIXME This test is incomplete
