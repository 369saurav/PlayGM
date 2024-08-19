import mysql.connector
from mysql.connector import Error

class TiDBCRUD:
    def __init__(self, host, user, password, database):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            print("Successfully connected to TiDB")
        except Error as e:
            print(f"Error connecting to TiDB: {e}")

    def create_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    email VARCHAR(100),
                    department VARCHAR(100)
                )
            """)
            print("Table 'employees' created successfully")
        except Error as e:
            print(f"Error creating table: {e}")

    def create_employee(self, name, email, department):
        try:
            cursor = self.connection.cursor()
            sql = "INSERT INTO employees (name, email, department) VALUES (%s, %s, %s)"
            values = (name, email, department)
            cursor.execute(sql, values)
            self.connection.commit()
            print(f"Employee {name} added successfully")
        except Error as e:
            print(f"Error creating employee: {e}")

    def read_employees(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM employees")
            employees = cursor.fetchall()
            for employee in employees:
                print(f"ID: {employee[0]}, Name: {employee[1]}, Email: {employee[2]}, Department: {employee[3]}")
        except Error as e:
            print(f"Error reading employees: {e}")

    def update_employee(self, id, name, email, department):
        try:
            cursor = self.connection.cursor()
            sql = "UPDATE employees SET name = %s, email = %s, department = %s WHERE id = %s"
            values = (name, email, department, id)
            cursor.execute(sql, values)
            self.connection.commit()
            print(f"Employee with ID {id} updated successfully")
        except Error as e:
            print(f"Error updating employee: {e}")

    def delete_employee(self, id):
        try:
            cursor = self.connection.cursor()
            sql = "DELETE FROM employees WHERE id = %s"
            value = (id,)
            cursor.execute(sql, value)
            self.connection.commit()
            print(f"Employee with ID {id} deleted successfully")
        except Error as e:
            print(f"Error deleting employee: {e}")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("TiDB connection closed")

# Usage example
if __name__ == "__main__":
    # Replace with your TiDB connection details
    tidb = TiDBCRUD("your_host", "your_user", "your_password", "your_database")

    tidb.create_table()

    tidb.create_employee("John Doe", "john@example.com", "IT")
    tidb.create_employee("Jane Smith", "jane@example.com", "HR")

    print("\nAll employees:")
    tidb.read_employees()

    tidb.update_employee(1, "John Doe", "john.doe@example.com", "Engineering")

    print("\nAfter update:")
    tidb.read_employees()

    tidb.delete_employee(2)

    print("\nAfter deletion:")
    tidb.read_employees()

    tidb.close_connection()