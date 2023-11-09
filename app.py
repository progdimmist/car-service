from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'db/database.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn


@app.route('/add_worker', methods=['POST'])
def add_worker():
    conn = get_db()
    cursor = conn.cursor()
    worker_id = request.form['worker_id']
    surname_worker = request.form['surname_worker']
    first_name_worker = request.form['first_name_worker']
    patronymic_worker = request.form['patronymic_worker']
    date_birth_worker = request.form['date_birth_worker']
    address_worker = request.form['address_worker']
    phone_number_worker = request.form['phone_number_worker']
    position_worker = request.form['position_worker']
    salary_worker = request.form['salary_worker']
    length_service = request.form['length_service']
    operating_mode = request.form['operating_mode']
    seniority_allowance = request.form['seniority_allowance']

    cursor.execute(
        "INSERT INTO worker (worker_id, surname_worker, first_name_worker, patronymic_worker, date_birth_worker, address_worker, phone_number_worker, position_worker, salary_worker, length_service, operating_mode, seniority_allowance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (worker_id, surname_worker, first_name_worker, patronymic_worker, date_birth_worker, address_worker,
         phone_number_worker, position_worker, salary_worker, length_service, operating_mode, seniority_allowance))

    conn.commit()
    conn.close()

    return redirect(url_for('index') + '#contacts')


@app.route('/add_car', methods=['POST'])
def add_car():
    conn = get_db()
    cursor = conn.cursor()
    client_id = request.form['client_id']
    surname_client = request.form['surname_client']
    first_name_client = request.form['first_name_client']
    patronymic_client = request.form['patronymic_client']
    phone_number_client = request.form['phone_number_client']

    car_number = request.form['car_number']
    model = request.form['model']
    release_date = request.form['release_date']
    cursor.execute(
        "INSERT INTO client (client_id, surname_client, first_name_client, patronymic_client, phone_number_client) VALUES (?, ?, ?, ?, ?)",
        (client_id, surname_client, first_name_client, patronymic_client, phone_number_client))

    cursor.execute(
        "INSERT INTO car (car_number, model, release_date, client_id) VALUES (?, ?, ?, ?)",
        (car_number, model, release_date, client_id))
    conn.commit()
    conn.close()

    return redirect(url_for('index') + '#contacts')


@app.route('/')
def index():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM worker")
    workers = cursor.fetchall()
    cursor.execute("SELECT * FROM client")
    clients = cursor.fetchall()
    cursor.execute("SELECT * FROM car")
    cars = cursor.fetchall()
    conn.close()
    return render_template('index.html', workers=workers, clients=clients, cars=cars)


@app.route('/client_details/<int:client_id>')
def client_details(client_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM client WHERE client_id=?", (client_id,))
    client = cursor.fetchone()
    conn.close()
    return render_template('client_details.html', client=client)


@app.route('/edit_worker/<int:worker_id>', methods=['GET', 'POST'])
def edit_worker(worker_id):
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        surname_worker = request.form['surname_worker']
        first_name_worker = request.form['first_name_worker']
        patronymic_worker = request.form['patronymic_worker']
        date_birth_worker = request.form['date_birth_worker']
        address_worker = request.form['address_worker']
        phone_number_worker = request.form['phone_number_worker']
        position_worker = request.form['position_worker']
        salary_worker = request.form['salary_worker']
        length_service = request.form['length_service']
        operating_mode = request.form['operating_mode']
        seniority_allowance = request.form['seniority_allowance']

        cursor.execute("""
            UPDATE worker
            SET surname_worker=?, first_name_worker=?, patronymic_worker=?, date_birth_worker=?, address_worker=?, phone_number_worker=?, position_worker=?, salary_worker=?, length_service=?, operating_mode=?, seniority_allowance=?
            WHERE worker_id=?
        """, (surname_worker, first_name_worker, patronymic_worker, date_birth_worker, address_worker,
              phone_number_worker, position_worker, salary_worker, length_service, operating_mode,
              seniority_allowance, worker_id))

        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM worker WHERE worker_id=?", (worker_id,))
    worker = cursor.fetchone()
    conn.close()
    return render_template('edit_worker.html', worker=worker)


@app.route('/more_worker/<int:worker_id>', methods=['GET', 'POST'])
def more_worker(worker_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM worker WHERE worker_id=?", (worker_id,))
    worker = cursor.fetchone()
    conn.close()
    return render_template('more_worker.html', worker=worker)


@app.route('/delete_worker/<int:worker_id>')
def delete_worker(worker_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM worker WHERE worker_id=?", (worker_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index') + '#contacts')


@app.route('/delete_car/<string:car_number>')
def delete_car(car_number):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM car WHERE car_number=?", (car_number,))
    conn.commit()
    conn.close()
    return redirect(url_for('index') + '#contacts')


@app.route('/edit_car/<string:car_number>', methods=['GET', 'POST'])
def edit_car(car_number):
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        car_number = request.form['car_number']
        model = request.form['model']
        release_date = request.form['release_date']

        cursor.execute("""
            UPDATE car
            SET car_number=?, model=?, release_date=?
        """, (car_number, model, release_date))

        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    cursor.execute("SELECT * FROM car WHERE car_number=?", (car_number,))
    car = cursor.fetchone()
    conn.close()
    return render_template('edit_car.html', car=car)


if __name__ == '__main__':
    app.run()
