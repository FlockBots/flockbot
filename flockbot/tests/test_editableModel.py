import unittest
from flockbot.models import Editable
from flockbot.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestEditableModel(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=True)
        Session = sessionmaker(bind=engine)
        self.database = Session()
        Base.metadata.create_all(engine)

    def tearDown(self):
        self.database.rollback()
        self.database.close()

    def test_insert(self):
        entry = Editable(id='3dnsh1')
        self.database.add(entry)
        db_entry = self.database.query(Editable).first()
        self.assertEqual(db_entry.id, entry.id)

    def test_notContains(self):
        db_entry = self.database.query(Editable).filter(Editable.id == 'non-existent').first()
        self.assertEqual(db_entry, None)

if __name__ == '__main__':
    unittest.main()