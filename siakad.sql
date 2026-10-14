CREATE TABLE mahasiswa (
  nim  VARCHAR(10) PRIMARY KEY,
  nama VARCHAR(60) NOT NULL,
  ipk  NUMERIC(3,2)
);
CREATE TABLE nilai (
  id      SERIAL PRIMARY KEY,
  nim     VARCHAR(10) REFERENCES mahasiswa(nim),
  kode_mk VARCHAR(10) NOT NULL,
  nilai   CHAR(2) NOT NULL
);
INSERT INTO mahasiswa VALUES
  ('M001', 'Mahasiswa Uji 1', 3.00),
  ('M002', 'Mahasiswa Uji 2', 2.99),
  ('M003', 'Mahasiswa Baru', NULL);
INSERT INTO nilai (nim, kode_mk, nilai) VALUES
  ('M001', 'IF101', 'A'), ('M001', 'IF102', 'B+'),
  ('M002', 'IF101', 'B'), ('M002', 'IF102', 'C+');
