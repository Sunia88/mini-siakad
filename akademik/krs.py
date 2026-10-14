"""Aturan bisnis modul KRS (KEB-KRS-03, KEB-KRS-04)."""

BATAS_IPK_TINGGI = 3.00
SKS_IPK_TINGGI = 24
SKS_IPK_NORMAL = 20


def batas_sks(ipk):
    """Batas SKS menurut IPK; None = mahasiswa baru."""
    if ipk is None:
        return SKS_IPK_NORMAL
    if not isinstance(ipk, (int, float)):
        raise ValueError("IPK harus berupa angka")
    if ipk < 0.00 or ipk > 4.00:
        raise ValueError("IPK di luar rentang 0,00-4,00")
    if ipk >= BATAS_IPK_TINGGI:
        return SKS_IPK_TINGGI
    return SKS_IPK_NORMAL


def jadwal_bentrok(a, b):
    """True jika dua jadwal (hari, mulai, selesai)
    saling bertumpuk."""
    return a[0] == b[0] and a[1] < b[2] and b[1] < a[2]
