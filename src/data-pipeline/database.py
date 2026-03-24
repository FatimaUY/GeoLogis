import psycopg2
from psycopg2.extras import execute_values
from configparser import ConfigParser
from pathlib import Path
import logging
import io
from datetime import datetime
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
                            annee INT,
                            code_commune INT,
                            prix_m2 REAL,
                            nom_commune TEXT,
                            dep_code TEXT,
                            dep_nom TEXT,
                            reg_code TEXT,
                            reg_nom TEXT,
                            code_postal VARCHAR,
                            population INT,
                            densite REAL,
                            superficie_km2 REAL,
                            zone_emploi REAL,
                            taux_global_tfb REAL,
                            taux_global_tfnb REAL,
                            taux_plein_teom REAL,
                            taux_global_th REAL,
                            y VARCHAR,
                            )
                            ''')
        
        self.connection.commit()
        self.disconnect_from_db()
        logger.info("Training table created or already exists")

    def save_training_data(self, df: pd.DataFrame) -> dict:
        """
        Save training data from a pandas DataFrame into PostgreSQL using COPY for bulk loading
        and UPSERT for handling duplicate records.
        
        This method:
        1. Validates the DataFrame has all required columns
        2. Converts DataFrame to CSV format (in-memory buffer)
        3. Uses PostgreSQL COPY command for high-performance bulk loading
        4. Implements UPSERT logic to handle duplicates (identified by annee + code_commune)
        5. Returns statistics on the operation
        
        Args:
            df (pd.DataFrame): DataFrame with columns matching the training table schema.
                              Required columns: annee, code_commune, prix_m2, nom_commune,
                              dep_code, dep_nom, reg_code, reg_nom, code_postal, population,
                              densite, superficie_km2, zone_emploi, taux_global_tfb,
                              taux_global_tfnb, taux_plein_teom, taux_global_th, y
        
        Returns:
            dict: Operation statistics with keys:
                - rows_processed: Total rows in input DataFrame
                - rows_inserted: New rows inserted
                - rows_updated: Existing rows updated (duplicates)
                - success: Boolean indicating if operation completed successfully
                - timestamp: When the operation occurred
                - message: Summary message
        
        Raises:
            ValueError: If DataFrame is missing required columns or is empty
            psycopg2.Error: If database operation fails
        """
        try:
            # Step 1: Validate DataFrame
            self._validate_dataframe(df)
            
            if df.empty:
                logger.warning("DataFrame is empty, nothing to insert")
                return {
                    'rows_processed': 0,
                    'rows_inserted': 0,
                    'rows_updated': 0,
                    'success': False,
                    'timestamp': datetime.now().isoformat(),
                    'message': 'DataFrame is empty'
                }
            
            logger.info(f"Starting save_training_data operation with {len(df)} rows")
            
            # Step 2: Connect to database
            self.connect_to_db()
            
            # Step 3: Convert DataFrame to CSV buffer
            csv_buffer = self._df_to_csv_buffer(df)
            
            # Step 4: Create temp table for COPY
            temp_table = "training_temp"
            self._create_temp_table(temp_table)
            
            # Step 5: Load data into temp table using COPY
            copy_sql = f"COPY {temp_table} (annee, code_commune, prix_m2, nom_commune, dep_code, " \
                       f"dep_nom, reg_code, reg_nom, code_postal, population, densite, " \
                       f"superficie_km2, zone_emploi, taux_global_tfb, taux_global_tfnb, " \
                       f"taux_plein_teom, taux_global_th, y) FROM STDIN WITH CSV HEADER"
            
            self.cursor.copy_expert(copy_sql, csv_buffer)
            logger.info(f"Successfully loaded {len(df)} rows into temporary table")
            
            # Step 6: UPSERT from temp table to main training table
            # Composite key: (annee, code_commune) - if these match, update other fields
            upsert_sql = f"""
                INSERT INTO training (annee, code_commune, prix_m2, nom_commune, dep_code, 
                                    dep_nom, reg_code, reg_nom, code_postal, population, 
                                    densite, superficie_km2, zone_emploi, taux_global_tfb, 
                                    taux_global_tfnb, taux_plein_teom, taux_global_th, y)
                SELECT annee, code_commune, prix_m2, nom_commune, dep_code, 
                       dep_nom, reg_code, reg_nom, code_postal, population, 
                       densite, superficie_km2, zone_emploi, taux_global_tfb, 
                       taux_global_tfnb, taux_plein_teom, taux_global_th, y
                FROM {temp_table}
                ON CONFLICT (annee, code_commune) 
                DO UPDATE SET
                    prix_m2 = EXCLUDED.prix_m2,
                    nom_commune = EXCLUDED.nom_commune,
                    dep_code = EXCLUDED.dep_code,
                    dep_nom = EXCLUDED.dep_nom,
                    reg_code = EXCLUDED.reg_code,
                    reg_nom = EXCLUDED.reg_nom,
                    code_postal = EXCLUDED.code_postal,
                    population = EXCLUDED.population,
                    densite = EXCLUDED.densite,
                    superficie_km2 = EXCLUDED.superficie_km2,
                    zone_emploi = EXCLUDED.zone_emploi,
                    taux_global_tfb = EXCLUDED.taux_global_tfb,
                    taux_global_tfnb = EXCLUDED.taux_global_tfnb,
                    taux_plein_teom = EXCLUDED.taux_plein_teom,
                    taux_global_th = EXCLUDED.taux_global_th,
                    y = EXCLUDED.y
            """
            self.cursor.execute(upsert_sql)
            
            # Step 7: Get statistics
            rows_affected = self.cursor.rowcount
            logger.info(f"UPSERT operation affected {rows_affected} rows")
            
            # Step 8: Clean up temp table
            self.cursor.execute(f"DROP TABLE IF EXISTS {temp_table}")
            
            # Step 9: Commit transaction
            self.connection.commit()
            logger.info("Transaction committed successfully")
            
            # Step 10: Prepare result
            result = {
                'rows_processed': len(df),
                'rows_inserted': rows_affected,  # This includes both inserts and updates
                'rows_updated': rows_affected,
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'message': f'Successfully processed {len(df)} rows. Affected {rows_affected} rows in training table.'
            }
            
            logger.info(result['message'])
            return result
            
        except ValueError as ve:
            logger.error(f"Validation error: {str(ve)}")
            if hasattr(self, 'connection'):
                self.connection.rollback()
            return {
                'rows_processed': len(df) if 'df' in locals() else 0,
                'rows_inserted': 0,
                'rows_updated': 0,
                'success': False,
                'timestamp': datetime.now().isoformat(),
                'message': f'Validation error: {str(ve)}'
            }
            
        except psycopg2.Error as e:
            logger.error(f"Database error: {str(e)}")
            if hasattr(self, 'connection'):
                self.connection.rollback()
            return {
                'rows_processed': len(df) if 'df' in locals() else 0,
                'rows_inserted': 0,
                'rows_updated': 0,
                'success': False,
                'timestamp': datetime.now().isoformat(),
                'message': f'Database error: {str(e)}'
            }
            
        finally:
            if hasattr(self, 'connection'):
                self.disconnect_from_db()
    
    def _validate_dataframe(self, df: pd.DataFrame) -> None:
        """
        Validate that the DataFrame has all required columns.
        
        Args:
            df (pd.DataFrame): DataFrame to validate
            
        Raises:
            ValueError: If required columns are missing
        """
        required_columns = {
            'annee', 'code_commune', 'prix_m2', 'nom_commune', 'dep_code',
            'dep_nom', 'reg_code', 'reg_nom', 'code_postal', 'population',
            'densite', 'superficie_km2', 'zone_emploi', 'taux_global_tfb',
            'taux_global_tfnb', 'taux_plein_teom', 'taux_global_th', 'y'
        }
        
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        logger.info(f"DataFrame validation passed. Schema is valid.")
    
    def _df_to_csv_buffer(self, df: pd.DataFrame) -> io.StringIO:
        """
        Convert a pandas DataFrame to a CSV format in memory using StringIO.
        This format is compatible with PostgreSQL's COPY command.
        
        Args:
            df (pd.DataFrame): DataFrame to convert
            
        Returns:
            io.StringIO: CSV buffer ready for COPY command
        """
        # Select only the columns we need in the correct order
        columns_order = [
            'annee', 'code_commune', 'prix_m2', 'nom_commune', 'dep_code',
            'dep_nom', 'reg_code', 'reg_nom', 'code_postal', 'population',
            'densite', 'superficie_km2', 'zone_emploi', 'taux_global_tfb',
            'taux_global_tfnb', 'taux_plein_teom', 'taux_global_th', 'y'
        ]
        
        df_subset = df[columns_order]
        
        # Convert to CSV format with header
        csv_buffer = io.StringIO()
        df_subset.to_csv(csv_buffer, index=False, header=True)
        csv_buffer.seek(0)  # Reset buffer position to beginning
        
        logger.info(f"DataFrame converted to CSV buffer ({csv_buffer.tell()} bytes)")
        return csv_buffer
    
    def _create_temp_table(self, table_name: str) -> None:
        """
        Create a temporary table with the same schema as the training table.
        
        Args:
            table_name (str): Name of the temporary table to create
        """
        self.cursor.execute(f'''
            CREATE TEMP TABLE IF NOT EXISTS {table_name} (
                annee INT,
                code_commune INT,
                prix_m2 REAL,
                nom_commune TEXT,
                dep_code TEXT,
                dep_nom TEXT,
                reg_code TEXT,
                reg_nom TEXT,
                code_postal VARCHAR,
                population INT,
                densite REAL,
                superficie_km2 REAL,
                zone_emploi REAL,
                taux_global_tfb REAL,
                taux_global_tfnb REAL,
                taux_plein_teom REAL,
                taux_global_th REAL,
                y VARCHAR
            )
        ''')