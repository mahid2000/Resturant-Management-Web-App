import unittest
from flaskr.user_account_model import UserAccountModel


class MyTestCase(unittest.TestCase):
    def test_all_blank(self):
        """Test that an exception is raised if invalid data (All None) is provided."""
        self.assertRaises(Exception, UserAccountModel, (None, None, None))

    def test_first_name_blank(self):
        """Test that an exception is raised if a first_name is not provided."""
        self.assertRaises(Exception, UserAccountModel, (None, "Wilson", "Waiter1!"))

    def test_last_name_blank(self):
        """Test that an exception is raised if a first_name is not provided."""
        self.assertRaises(Exception, UserAccountModel, ("Melissa", None, "Waiter1!"))

    def test_password_blank(self):
        """Test that an exception is raised if a first_name is not provided."""
        self.assertRaises(Exception, UserAccountModel, ("Melissa", "Wilson", None))

    def test_hashing(self):
        """Test that the hash function correctly maps the test data passwords to the hashes in the database."""
        self.assertEqual(UserAccountModel.hash_password("Waiter1!"),
                         "15eb3b49fce780facecf0b761712328b0ae12e62a41c573a9629523fa2709dd7")
        self.assertEqual(UserAccountModel.hash_password("Waiter2!"),
                         "52c5f34607e2922524e8a323a0148b72d95919695bb381983858176be05add8e")
        self.assertEqual(UserAccountModel.hash_password("Waiter3!"),
                         "26f569da2d75f45870aa7c0ec11b83dcf9a2f2ae6cc673fedc57e9a49241a71b")
        self.assertEqual(UserAccountModel.hash_password("Kitchen1!"),
                         "1aa5f6f0e0e330b26de90da1968103250d4376f6c877c7539d5eb4781d231f5f")
        self.assertEqual(UserAccountModel.hash_password("Kitchen2!"),
                         "ef8667d2b0a7b4981a81e684765d6532e9b28b3cc79c968cacf73639997d6623")
        self.assertEqual(UserAccountModel.hash_password("Kitchen3!"),
                         "33caf999a6403a65eccee276210f1b6c1802f8bba2b3a4007028aa26c1569f8c")
        self.assertEqual(UserAccountModel.hash_password("Manager1!"),
                         "c4ffc94910796e8633061539e3815c10cada0d4092a596c150c0812f32a31a15")
        self.assertEqual(UserAccountModel.hash_password("Manager2!"),
                         "3e3b916b101b24d3ebf206254acd53a81ed4163d42e0c1aa42d7ebd09c87a643")
        self.assertEqual(UserAccountModel.hash_password("Owner10!"),
                         "7507c2b6bf438cd0137632eb1734dc42b14e724bf604554410091f5bfd4baae0")

    def test_correct_data(self):
        """Test that an exception is not thrown, and values are correctly assigned for valid data."""
        user_account = UserAccountModel("Melissa", "Wilson", "Waiter1!")
        self.assertEqual(user_account.first_name, "Melissa")
        self.assertEqual(user_account.last_name, "Wilson")
        self.assertEqual(user_account.password, "15eb3b49fce780facecf0b761712328b0ae12e62a41c573a9629523fa2709dd7")


if __name__ == '__main__':
    unittest.main()
