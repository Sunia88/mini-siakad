"""Menghitung skor SUS dari berkas sus.csv."""
import csv

def skor_sus(jawaban):
    """jawaban: 10 nilai 1-5 sesuai urutan butir."""
    if len(jawaban) != 10:
        raise ValueError("SUS harus berisi 10 butir")
    total = 0
    for i, r in enumerate(jawaban, start=1):
        total += (r - 1) if i % 2 == 1 else (5 - r)
    return total * 2.5

with open("sus.csv", encoding="utf-8") as f:
    skor = [skor_sus([int(x) for x in baris[1:]])
            for baris in csv.reader(f) if baris]
for n, s in enumerate(skor, start=1):
    print(f"Responden {n}: {s:.1f}")
print(f"Rata-rata SUS: {sum(skor) / len(skor):.1f}")
