import pytest
from app import app, KRS

TUJUH = ["IF201", "IF202", "IF203", "IF204",
         "IF205", "IF206", "IF207"]          # 23 SKS


@pytest.fixture
def klien():
    KRS.clear()
    app.config["TESTING"] = True
    return app.test_client()


def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_ipk_300_boleh_23_sks(klien):
    r = klien.post("/api/krs", json={"matkul": TUJUH},
                   headers=auth("token-m001"))
    assert r.status_code == 201
    assert r.get_json()["total_sks"] == 23


def test_ipk_299_ditolak_23_sks(klien):
    r = klien.post("/api/krs", json={"matkul": TUJUH},
                   headers=auth("token-m002"))
    assert r.status_code == 422
    assert "batas 20 SKS" in r.get_json()["pesan"]


def test_jadwal_bentrok_ditolak(klien):
    r = klien.post("/api/krs",
                   json={"matkul": ["IF201", "IF208"]},
                   headers=auth("token-m001"))
    assert r.status_code == 422
    assert "bentrok" in r.get_json()["pesan"]


def test_tanpa_token_ditolak(klien):
    r = klien.get("/api/mahasiswa/M001/krs")
    assert r.status_code == 401


def test_tidak_bisa_lihat_krs_orang_lain(klien):
    r = klien.get("/api/mahasiswa/M002/krs",
                  headers=auth("token-m001"))
    assert r.status_code == 403
