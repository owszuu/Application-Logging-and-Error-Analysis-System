from pymongo import MongoClient

# Wklej tutaj swój connection string z MongoDB Atlas
CONNECTION_STRING = "mongodb+srv://zuzswo_db_user:zbazowane@cluster0.vlex7cc.mongodb.net/?appName=Cluster0"

# Nazwa bazy danych
DB_NAME = "log_system"

def get_db():
    """Zwraca połączenie z bazą danych."""
    client = MongoClient(CONNECTION_STRING)
    return client[DB_NAME]