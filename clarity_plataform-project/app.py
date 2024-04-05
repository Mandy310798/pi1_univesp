from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import barcode
from barcode.writer import ImageWriter
import qrcode

app = Flask(__name__)

# Configurações do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'charity_db'
mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM charity")
    charities = cur.fetchall()
    cur.close()
    return render_template('index.html', charities=charities)

@app.route('/donate', methods=['POST'])
def donate():
    if request.method == 'POST':
        charity_id = request.form['charity_id']
        valor_doacao = float(request.form['valor_doacao'])
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO donation (charity_id, valor_doacao, confirmacao) VALUES (%s, %s, %s)", (charity_id, valor_doacao, False))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index.html'))

@app.route('/generate_barcode/<int:donation_id>')
def generate_barcode(donation_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM donation WHERE id = %s", (donation_id,))
    donation = cur.fetchone()
    cur.close()
    if donation:
        valor_doacao = donation['valor_doacao']
        ean = barcode.get_barcode_class('ean13')
        code = ean(str(donation_id), writer=ImageWriter())
        filename = f'barcode_{donation_id}.png'
        code.save(filename)
        return render_template('barcode.html', filename=filename, valor_doacao=valor_doacao)

@app.route('/generate_qrcode/<int:donation_id>')
def generate_qrcode(donation_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM donation WHERE id = %s", (donation_id,))
    donation = cur.fetchone()
    cur.close()
    if donation:
        valor_doacao = donation['valor_doacao']
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(f'Donation ID: {donation_id}, Valor: {valor_doacao}')
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        filename = f'qrcode_{donation_id}.png'
        img.save(filename)
        return render_template('qrcode.html', filename=filename, valor_doacao=valor_doacao)

if __name__ == '__main__':
    app.run(debug=True)
