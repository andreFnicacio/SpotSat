# init_db.py
import time
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Tentativas de conexão
attempts = 5
for attempt in range(attempts):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST')
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        break
    except psycopg2.OperationalError as e:
        print(f"Attempt {attempt + 1} of {attempts} failed: {e}")
        time.sleep(5)  # Espera 5 segundos antes da próxima tentativa
else:
    raise Exception("Could not connect to the database after several attempts.")
cur = conn.cursor()

# Criar o banco de dados se não existir
cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'spot_sat_db'")
exists = cur.fetchone()
if not exists:
    cur.execute('CREATE DATABASE spot_sat_db')

# Fechar a conexão com o banco padrão
cur.close()
conn.close()

# Conectar ao novo banco de dados para criar as extensões e tabelas
conn = psycopg2.connect(
    dbname="spot_sat_db",
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST')
)
cur = conn.cursor()

# Criar as extensões PostGIS
cur.execute('CREATE EXTENSION IF NOT EXISTS postgis')
cur.execute('CREATE EXTENSION IF NOT EXISTS postgis_topology')

# Criar as tabelas, se necessário (simplificação; a migração Django geralmente cuidaria disso)
cur.execute('''
CREATE TABLE IF NOT EXISTS api_image (
    id SERIAL PRIMARY KEY,
    file_path VARCHAR(255),
    cloud_coverage FLOAT,
    processing_date DATE DEFAULT CURRENT_DATE,
    geom GEOMETRY,
    classification_result JSONB
);
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS api_classification (
    idRaster UUID PRIMARY KEY,
    class_name VARCHAR(50),
    area FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')

# Fechar a conexão
conn.commit()
cur.close()
conn.close()
