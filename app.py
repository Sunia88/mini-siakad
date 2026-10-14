from flask import (Flask, jsonify, request,
                   render_template, abort)
from akademik.krs import batas_sks, jadwal_bentrok

app = Flask(__name__)

MAHASISWA = {
    "M001": {"nama": "Mahasiswa Uji 1", "ipk": 3.00},
    "M002": {"nama": "Mahasiswa Uji 2", "ipk": 2.99},
    "M003": {"nama": "Mahasiswa Baru", "ipk": None},
}
TOKEN = {"token-m001": "M001", "token-m002": "M002",
         "token-m003": "M003"}
MATKUL = {
    "IF201": ("Struktur Data", 4, ("Senin", 8, 10)),
    "IF202": ("Basis Data", 4, ("Selasa", 13, 15)),
    "IF203": ("Jaringan Komputer", 3, ("Selasa", 8, 10)),
    "IF204": ("Rekayasa Perangkat Lunak", 3,
              ("Rabu", 8, 10)),
    "IF205": ("Sistem Operasi", 3, ("Kamis", 8, 10)),
    "IF206": ("Kecerdasan Buatan", 3, ("Jumat", 8, 10)),
    "IF207": ("Pengujian Perangkat Lunak", 3,
              ("Jumat", 13, 15)),
    "IF208": ("Etika Profesi", 2, ("Senin", 9, 11)),
}
KRS = {}


def nim_dari_token():
    auth = request.headers.get("Authorization", "")
    nim = TOKEN.get(auth.removeprefix("Bearer "))
    if nim is None:
        abort(401)
    return nim


def validasi(nim, pilihan):
    batas = batas_sks(MAHASISWA[nim]["ipk"])
    total = sum(MATKUL[k][1] for k in pilihan)
    if total > batas:
        return (f"Total {total} SKS melebihi "
                f"batas {batas} SKS")
    for i, a in enumerate(pilihan):
        for b in pilihan[i + 1:]:
            if jadwal_bentrok(MATKUL[a][2], MATKUL[b][2]):
                return f"Jadwal {a} bentrok dengan {b}"
    return None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/mahasiswa/<nim>/krs")
def lihat_krs(nim):
    if nim_dari_token() != nim:
        abort(403)
    batas = batas_sks(MAHASISWA[nim]["ipk"])
    return jsonify(nim=nim, matkul=KRS.get(nim, []),
                   batas_sks=batas)


@app.post("/api/krs")
def simpan_krs():
    nim = nim_dari_token()
    data = request.get_json(silent=True, force=True) or {}
    pilihan = data.get("matkul", [])
    if any(k not in MATKUL for k in pilihan):
        return jsonify(kode="MATKUL_TIDAK_ADA"), 422
    pesan = validasi(nim, pilihan)
    if pesan:
        return jsonify(kode="KRS_DITOLAK",
                       pesan=pesan), 422
    KRS[nim] = pilihan
    total = sum(MATKUL[k][1] for k in pilihan)
    return jsonify(nim=nim, matkul=pilihan,
                   total_sks=total), 201


@app.route("/krs", methods=["GET", "POST"])
def halaman_krs():
    nim = request.values.get("nim", "M001")
    if nim not in MAHASISWA:
        abort(404)
    pesan, pilihan = None, KRS.get(nim, [])
    if request.method == "POST":
        pilihan = request.form.getlist("matkul")
        pesan = validasi(nim, pilihan)
        if pesan is None:
            KRS[nim] = pilihan
            pesan = "KRS berhasil disimpan"
    return render_template(
        "krs.html", nim=nim, mhs=MAHASISWA[nim],
        batas=batas_sks(MAHASISWA[nim]["ipk"]),
        matkul=MATKUL, pilihan=pilihan, pesan=pesan)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
