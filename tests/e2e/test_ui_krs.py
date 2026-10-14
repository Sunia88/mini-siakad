import re
from playwright.sync_api import Page, expect

BASE = "http://localhost:5000"


def test_batas_sks_24_untuk_ipk_300(page: Page):
    page.goto(f"{BASE}/krs?nim=M001")
    batas = page.get_by_test_id("batas-sks")
    expect(batas).to_have_text("24")


def test_krs_melebihi_batas_ditolak(page: Page):
    page.goto(f"{BASE}/krs?nim=M002")
    for kode in ["IF201", "IF202", "IF203", "IF204",
                 "IF205", "IF206", "IF207"]:
        page.get_by_test_id(f"matkul-{kode}").check()
    page.get_by_role("button", name="Simpan KRS").click()
    expect(page.get_by_test_id("pesan")).to_have_text(
        re.compile("melebihi batas 20 SKS"))
