import unittest
from database import setup_database, add_pir, update_pir, delete_pir, add_source, update_source, delete_source, add_mapping, delete_mapping
import os
import sqlite3

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the database before any tests run
        setup_database()

    @classmethod
    def tearDownClass(cls):
        # Remove the test database file after all tests complete
        if os.path.exists('intelligence.db'):
            os.remove('intelligence.db')

    def setUp(self):
        # Establish a connection to the database for each test
        self.connection = sqlite3.connect('intelligence.db')
        self.cursor = self.connection.cursor()

    def tearDown(self):
        # Close the connection after each test
        self.connection.close()

    def test_add_pir(self):
        add_pir("Test PIR", "High", "2024-11-10", "Open", "None")
        self.cursor.execute("SELECT * FROM PIRs WHERE description = ?", ("Test PIR",))
        pir = self.cursor.fetchone()
        self.assertIsNotNone(pir)
        self.assertEqual(pir[1], "Test PIR")

    def test_update_pir(self):
        add_pir("Test PIR", "High", "2024-11-10", "Open", "None")
        self.cursor.execute("SELECT id FROM PIRs WHERE description = ?", ("Test PIR",))
        pir_id = self.cursor.fetchone()[0]
        update_pir(pir_id, description="Updated PIR")
        self.cursor.execute("SELECT description FROM PIRs WHERE id = ?", (pir_id,))
        updated_description = self.cursor.fetchone()[0]
        self.assertEqual(updated_description, "Updated PIR")

    def test_delete_pir(self):
        add_pir("Test PIR", "High", "2024-11-10", "Open", "None")
        self.cursor.execute("SELECT id FROM PIRs WHERE description = ?", ("Test PIR",))
        pir_id = self.cursor.fetchone()[0]
        delete_pir(pir_id)
        self.cursor.execute("SELECT * FROM PIRs WHERE id = ?", (pir_id,))
        pir = self.cursor.fetchone()
        self.assertIsNone(pir)

    def test_add_source(self):
        add_source("Test Source", "Open", "High")
        self.cursor.execute("SELECT * FROM Sources WHERE name = ?", ("Test Source",))
        source = self.cursor.fetchone()
        self.assertIsNotNone(source)
        self.assertEqual(source[1], "Test Source")

    def test_update_source(self):
        add_source("Test Source", "Open", "High")
        self.cursor.execute("SELECT source_id FROM Sources WHERE name = ?", ("Test Source",))
        source_id = self.cursor.fetchone()[0]
        update_source(source_id, name="Updated Source")
        self.cursor.execute("SELECT name FROM Sources WHERE source_id = ?", (source_id,))
        updated_name = self.cursor.fetchone()[0]
        self.assertEqual(updated_name, "Updated Source")

    def test_delete_source(self):
        add_source("Test Source", "Open", "High")
        self.cursor.execute("SELECT source_id FROM Sources WHERE name = ?", ("Test Source",))
        source_id = self.cursor.fetchone()[0]
        delete_source(source_id)
        self.cursor.execute("SELECT * FROM Sources WHERE source_id = ?", (source_id,))
        source = self.cursor.fetchone()
        self.assertIsNone(source)

    def test_add_mapping(self):
        add_pir("Test PIR", "High", "2024-11-10", "Open", "None")
        add_source("Test Source", "Open", "High")
        self.cursor.execute("SELECT id FROM PIRs WHERE description = ?", ("Test PIR",))
        pir_id = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT source_id FROM Sources WHERE name = ?", ("Test Source",))
        source_id = self.cursor.fetchone()[0]
        add_mapping(pir_id, source_id)
        self.cursor.execute("SELECT * FROM Mappings WHERE pir_id = ? AND source_id = ?", (pir_id, source_id))
        mapping = self.cursor.fetchone()
        self.assertIsNotNone(mapping)

    def test_delete_mapping(self):
        add_pir("Test PIR", "High", "2024-11-10", "Open", "None")
        add_source("Test Source", "Open", "High")
        self.cursor.execute("SELECT id FROM PIRs WHERE description = ?", ("Test PIR",))
        pir_id = self.cursor.fetchone()[0]
        self.cursor.execute("SELECT source_id FROM Sources WHERE name = ?", ("Test Source",))
        source_id = self.cursor.fetchone()[0]
        add_mapping(pir_id, source_id)
        self.cursor.execute("SELECT mapping_id FROM Mappings WHERE pir_id = ? AND source_id = ?", (pir_id, source_id))
        mapping_id = self.cursor.fetchone()[0]
        delete_mapping(mapping_id)
        self.cursor.execute("SELECT * FROM Mappings WHERE mapping_id = ?", (mapping_id,))
        mapping = self.cursor.fetchone()
        self.assertIsNone(mapping)

if __name__ == '__main__':
    unittest.main()
