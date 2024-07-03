from models import storage
from models.club import Club

def test_db():
    # Drop all tables if necessary
    storage.drop_all_tables()
    
    # Create all tables
    storage.create_tables()

    # Add a new club
    new_club = Club(name="Test Club")
    storage.new(new_club)
    storage.save()

    # Query the database
    clubs = storage.all(Club)
    for club in clubs.values():
        print(club)

if __name__ == "__main__":
    test_db()

