import psycopg2

# Database connection
connection = psycopg2.connect('postgresql://neondb_owner:npg_jokt5EV8KDBa@ep-shiny-math-a1gy8dtc-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require')
cursor = connection.cursor()

# List of columns to alter to TEXT
columns_to_change = [
    'ip_add', 'host_name', 'dev_user', 'os_name_ver', 'latlong',
    'city', 'state', 'country', 'act_name', 'act_mail', 'act_mob', 'pdf_name'
]

print("Starting schema migration...")

for col in columns_to_change:
    try:
        # Check if column exists first or just try to alter
        print(f"Altering column {col} to TEXT...")
        cursor.execute(f"ALTER TABLE user_data ALTER COLUMN {col} TYPE TEXT;")
        connection.commit()
        print(f"Successfully altered {col}.")
    except Exception as e:
        print(f"Failed to alter {col}: {e}")
        connection.rollback()

print("Schema migration completed.")
connection.close()
