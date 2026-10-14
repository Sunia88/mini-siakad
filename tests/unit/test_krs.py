import pytest
from akademik.krs import batas_sks, jadwal_bentrok


@pytest.mark.parametrize("ipk, harapan", [
    (0.00, 20),   # batas bawah partisi valid
    (2.99, 20),   # tepat di bawah ambang
    (3.00, 24),   # tepat pada ambang (TC-KRS-014)
    (3.01, 24),   # tepat di atas ambang
    (4.00, 24),   # batas atas
    (None, 20),   # mahasiswa baru tanpa IPK
])
def test_batas_sks_valid(ipk, harapan):
    assert batas_sks(ipk) == harapan


@pytest.mark.parametrize("ipk", [-0.01, 4.01, "abc"])
def test_batas_sks_tidak_valid(ipk):
    with pytest.raises(ValueError):
        batas_sks(ipk)


def test_jadwal_bentrok():
    senin_8 = ("Senin", 8, 10)
    assert jadwal_bentrok(senin_8, ("Senin", 9, 11))
    assert not jadwal_bentrok(senin_8, ("Senin", 10, 12))
    assert not jadwal_bentrok(senin_8, ("Selasa", 8, 10))
