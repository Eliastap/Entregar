from flask import render_template, request, redirect, url_for, Flask
import csv
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="pythonm09"
)

# Ruta para la página principal
@app.route('/')
def pagina_principal():
    return render_template('paginaPrincipal.html')

# Ruta para la página de registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['password']
        cursor = db.cursor()
        sql_insert = "INSERT INTO nombres_y_correos (email, contraseña) VALUES (%s, %s)"
        cursor.execute(sql_insert, (email, contraseña))
        db.commit()
        return redirect(url_for('login'))  # Redirige al login después del registro
    return render_template('registro.html')

# Ruta para la página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['password']
        cursor = db.cursor()
        sql = "SELECT * FROM nombres_y_correos WHERE email = %s AND contraseña = %s"
        cursor.execute(sql, (email, contraseña))
        usuario = cursor.fetchone()
        if usuario:
            return redirect(url_for('entrada'))
        else:
            return "Credenciales incorrectas. Inténtalo de nuevo o regístrate si eres un nuevo usuario."
    return render_template('login.html')

# Ruta para la página de encuesta
@app.route('/entrada/encuesta')
def encuesta():
    return render_template('encuesta.html')

@app.route('/entrada')
def entrada():
    return render_template('entrada.html')


#-----Practica--

with open('nom-email-ASIX2-2324.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    email_dict = {row['NOM']: row['EMAIL'] for row in csv_reader}

@app.route('/success/<name>')
def dashboard(name):
    email = email_dict.get(name, 'no hay ningun correo encontrado')
    return f"Hola {name}, tu email es el siguiente: {email}"

@app.route('/logins',methods = ['POST', 'GET'])
def logins():
   if request.method == 'POST':
      user = request.form['name']
      return redirect(url_for('dashboard',name = user))
   else:
      user = request.args.get('name')
      return render_template('logins.html')

@app.route('/addmail', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        new_name = request.form['new_name']
        new_email = request.form['new_email']

        # Agrega el nuevo nombre y correo al diccionario y guarda en el archivo CSV
        email_dict[new_name] = new_email
        with open('nom-email-ASIX2-2324.csv', 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([new_name, new_email])

        return redirect(url_for('dashboard', name=new_name))
    else:
        return render_template('newcorreo.html')


if __name__ == '__main__':
    app.run(debug=True)
