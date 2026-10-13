import mysql.connector

# Paso 1. Los datos
libros = [
    {"titulo": "Don Quijote", "paginas": 863, "generos": ["novela", "aventuras", "humor"]},
    {"titulo": "Platero y yo", "paginas": 144, "generos": ["poesía", "infantil"]},
    {"titulo": "Marianela", "paginas": 256, "generos": ["novela"]},
]

# Paso 2. El tipo de cada dato
muestra = libros[0]
for clave in muestra.keys():
    print(clave, type(muestra[clave]))

# Paso 3. Conexión
conn = mysql.connector.connect(
    host="localhost",
    user="desfase",
    password="desfase",
    database="desfase",
)
cursor = conn.cursor()

# Paso 4. Borrar tablas antiguas
cursor.execute("DROP TABLE IF EXISTS libros_generos")
cursor.execute("DROP TABLE IF EXISTS libros")

# Paso 5. Tabla principal
cursor.execute("""
CREATE TABLE libros (
    Identificador INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255),
    paginas INT
)
""")

# Paso 6. Tabla para la lista de géneros
cursor.execute("""
CREATE TABLE libros_generos (
    Identificador INT AUTO_INCREMENT PRIMARY KEY,
    libros_id INT,
    valor VARCHAR(255),
    FOREIGN KEY (libros_id) REFERENCES libros(Identificador)
)
""")

# Paso 7. Guardar
for libro in libros:
    cursor.execute(
        "INSERT INTO libros (titulo, paginas) VALUES (%s, %s)",
        (libro["titulo"], libro["paginas"]),
    )
    id_libro = cursor.lastrowid
    for genero in libro["generos"]:
        cursor.execute(
            "INSERT INTO libros_generos (libros_id, valor) VALUES (%s, %s)",
            (id_libro, genero),
        )

conn.commit()

# Paso 8. Recuperar
cursor.execute("SELECT Identificador, titulo, paginas FROM libros")
filas = cursor.fetchall()
recuperados = []
for (id_libro, titulo, paginas) in filas:
    cursor.execute(
        "SELECT valor FROM libros_generos WHERE libros_id = %s",
        (id_libro,),
    )
    generos = [fila[0] for fila in cursor.fetchall()]
    recuperados.append({"titulo": titulo, "paginas": paginas, "generos": generos})

print(recuperados)
print(recuperados == libros)

# Reto extra. Libros que son novelas
cursor.execute("""
SELECT libros.titulo
FROM libros
JOIN libros_generos ON libros.Identificador = libros_generos.libros_id
WHERE libros_generos.valor = %s
""", ("novela",))
print([fila[0] for fila in cursor.fetchall()])

conn.close()
