import os
import time
import sys
from sqlalchemy import create_engine, text

def wait_for_db():
    uri = os.getenv("DATABASE_URL")
    # Split URI to get the master connection (connecting to 'postgres' db)
    base_uri = uri.rsplit('/', 1)[0] + "/postgres"
    target_db = uri.rsplit('/', 1)[-1]
    
    print(f"Connecting to Postgres at {base_uri.split('@')[-1]}...")
    
    # 1. Connect to master 'postgres' to check/create target database
    master_engine = create_engine(base_uri, isolation_level="AUTOCOMMIT")
    
    for i in range(15):
        try:
            with master_engine.connect() as conn:
                exists = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{target_db}'")).scalar()
                if not exists:
                    print(f"Creating database {target_db}...")
                    conn.execute(text(f"CREATE DATABASE {target_db}"))
                break
        except Exception as e:
            print(f"Waiting for Postgres... {i}/15")
            time.sleep(3)
    else:
        print("Postgres is unreachable.")
        sys.exit(1)

    # 2. Verify we can connect to the target_db
    engine = create_engine(uri)
    try:
        with engine.connect() as conn:
            print(f"Successfully connected to {target_db}")
    except Exception as e:
        print(f"Could not connect to {target_db}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    wait_for_db()