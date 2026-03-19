import psycopg2
from configparser import ConfigParser
from pathlib import Path

class DataManager:
    def __init__(self) -> None:
        """
        Initialize the DataManager and load database credentials from config file.
        
        Reads database connection parameters from a local 'database.ini' file rather than hardcoding them.
        This was done to keep the credentials out of the code by keeping it on a local platform rather than an online repository

        Raises:
            KeyError: If the expected sections or keys are missing from the config file.
            FileNotFoundError: If the database.ini file does not exist.
        """
        
        self.filename = Path(__file__).parent / "database.ini"
        self.config = ConfigParser()
        self.config.read(self.filename)
        self.host = self.config["postgresql"]["host"]
        self.database = self.config["postgresql"]["database"]
        self.user = self.config["postgresql"]["user"]

    def connect_to_db(self) -> None:
        """
        Connect to the PSQL database.
        
        Creates a database connection using the credentials loaded during initialization and stores both the connection and cursor as instance variables.
        
        We create instance variables at this moment and not during initializations because we do not want to connect to the database before it is necessary.
        Adding them here lets us access those only when needed to save some data.        
        """
        
        self.connection = psycopg2.connect(
            host= self.host,
            database=self.database, 
            user=self.user, 
        )
        
        self.cursor = self.connection.cursor()

    def disconnect_from_db(self):
        self.cursor.close()
        self.connection.close()

    def create_tables(self):
        self.connect_to_db()

        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS training(
                            id SERIAL PRIMARY KEY,

                            )
                            ''')
        
        self.connection.commit()
        self.disconnect_from_db()

    def save_training_data(self):
        self.connect_to_db()

        self.cursor.execute("""
                            INSERT INTO training()
                            VALUES (%s) 
                            """,
                            )

        self.connection.commit()

        self.disconnect_from_db()