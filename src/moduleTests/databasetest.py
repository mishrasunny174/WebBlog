from src.database.database import Database

Database.initialize()

Database.insert('testing_phase', {'_id': '12345', 'hello': 'world'})

results = Database.find('testing_phase', {})

for result in results:
    print(result)