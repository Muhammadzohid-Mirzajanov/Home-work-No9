import psycopg2

connection = psycopg2.connect(
    host="localhost",  # Host (odatda localhost)
    user="postgres",     # Foydalanuvchi nomi
    password="123456",   # Parol
)



cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS products;")
cursor.execute("DROP TABLE IF EXISTS categories;")

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE SET NULL
);
""")

cursor.executemany("""
INSERT INTO categories (category_name)
VALUES (%s);
""", [
    ('Electronics',),
    ('Books',),
    ('Clothing',),
    ('Toys',),
    ('Furniture',)
])

cursor.executemany("""
INSERT INTO products (product_name, category_id)
VALUES (%s, %s);
""", [
    ('Laptop', 1),
    ('Smartphone', 1),
    ('Tablet', 1),
    ('E-reader', 2),
    ('Novel', 2),
    ('Shirt', 3),
    ('Pants', 3),
    ('Dress', 3),
    ('Action Figure', 4),
    ('Board Game', 4),
    ('Desk', None),
    ('Chair', None),
    ('Lamp', None),
    ('Shelf', None),
    ('Table', None)
])

connection.commit()

cursor.execute("""
SELECT c.category_name, p.product_name
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
WHERE p.category_id IS NOT NULL;
""")
print(cursor.fetchall())

cursor.execute("""
SELECT c.category_name, p.product_name
FROM categories c
FULL OUTER JOIN products p ON c.category_id = p.category_id;
""")
print(cursor.fetchall())

cursor.execute("""
SELECT c.category_name, p.product_name
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
WHERE p.category_id IS NULL;
""")
print(cursor.fetchall())

cursor.execute("""
SELECT c.category_name
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
WHERE p.product_id IS NULL;
""")
print(cursor.fetchall())

cursor.execute("""
SELECT c.category_name, p.product_name
FROM categories c
CROSS JOIN products p;
""")
print(cursor.fetchall())

cursor.execute("""
SELECT c.category_name, p.product_name
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
WHERE p.category_id IS NOT NULL;
""")

print(cursor.fetchall())

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    manager_id INT
);
""")

cursor.executemany("""
INSERT INTO employees (name, manager_id)
VALUES (%s, %s);
""", [
    ('Alice', None),
    ('Bob', 1),
    ('Charlie', 1),
    ('David', 2),
    ('Eve', 3)
])

connection.commit()

cursor.execute("""
SELECT e1.name AS Employee, e2.name AS Manager
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.employee_id;
""")
print(cursor.fetchall())

cursor.close()
connection.close()
