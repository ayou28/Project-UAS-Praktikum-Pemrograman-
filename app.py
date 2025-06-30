from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Koneksi ke database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='database_mhs'
)
cursor = conn.cursor()

# GET semua data
@app.route('/akademik', methods=['GET'])
def get_all_akademik():
    cursor.execute("SELECT * FROM akademik")
    rows = cursor.fetchall()
    hasil = []
    for row in rows:
        hasil.append({
            'NIM': row[0],
            'Semester': row[1],
            'IPS': row[2],
            'IPK': row[3],
            'Total SKS yang Diambil': row[4],
            'Status Mahasiswa': row[5]
        })
    return jsonify(hasil)

# GET data by NIM
@app.route('/akademik/<string:nim>', methods=['GET'])
def get_akademik_by_nim(nim):
    cursor.execute("SELECT * FROM akademik WHERE NIM = %s", (nim,))
    row = cursor.fetchone()
    if row:
        data = {
            'NIM': row[0],
            'Semester': row[1],
            'IPS': row[2],
            'IPK': row[3],
            'Total SKS yang Diambil': row[4],
            'Status Mahasiswa': row[5]
        }
        return jsonify(data)
    return jsonify({'message': 'Data tidak ditemukan'}), 404

# POST data baru
@app.route('/akademik', methods=['POST'])
def tambah_data():
    data = request.get_json()
    cursor.execute("""
        INSERT INTO akademik (NIM, Semester, IPS, IPK, `Total SKS yang Diambil`, `Status Mahasiswa`)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data['NIM'],
        data['Semester'],
        data['IPS'],
        data['IPK'],
        data['Total SKS yang Diambil'],
        data['Status Mahasiswa']
    ))
    conn.commit()
    return jsonify({'message': 'Data berhasil ditambahkan'}), 201

# PUT / update data
@app.route('/akademik/<string:nim>', methods=['PUT'])
def update_data(nim):
    data = request.get_json()
    cursor.execute("""
        UPDATE akademik SET
            Semester = %s,
            IPS = %s,
            IPK = %s,
            `Total SKS yang Diambil` = %s,
            `Status Mahasiswa` = %s
        WHERE NIM = %s
    """, (
        data['Semester'],
        data['IPS'],
        data['IPK'],
        data['Total SKS yang Diambil'],
        data['Status Mahasiswa'],
        nim
    ))
    conn.commit()
    return jsonify({'message': 'Data berhasil diupdate'})

# DELETE data
@app.route('/akademik/<string:nim>', methods=['DELETE'])
def hapus_data(nim):
    cursor.execute("DELETE FROM akademik WHERE NIM = %s", (nim,))
    conn.commit()
    return jsonify({'message': 'Data berhasil dihapus'})

# Run server
if __name__ == '__main__':
    app.run(debug=True)
