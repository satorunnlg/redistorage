import unittest
from redistorage.model import RedisStorageModel

class TestRedisStorageModel(unittest.TestCase):

    class SampleConfig(RedisStorageModel):
        system_name = "Test System"
        debug = True

        class Meta:
            redis_key = "test_config"

    def test_initial_values(self):
        config = self.SampleConfig()
        self.assertEqual(config.system_name, "Test System")
        self.assertTrue(config.debug)

    def test_save_and_reload(self):
        config = self.SampleConfig()
        config.system_name = "Updated System"
        config.save()

        new_config = self.SampleConfig()
        self.assertEqual(new_config.system_name, "Updated System")

if __name__ == "__main__":
    unittest.main()
