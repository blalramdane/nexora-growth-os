import unittest

from poc_importer import build_report, identity_key, map_row, normalize_phone, normalize_text

def row(name="مطعم النيل", region="الزرقا", phone="01012345678", stage="Lead جديد"):
    return {
        "المنطقة": region,
        "اسم النشاط": name,
        "الهاتف": phone,
        "مرحلة CRM": stage,
        "حالة QR": "",
        "حالة Website": "",
        "حالة POS": "",
        "مصدر البيانات": "public listing",
    }

class ImporterTests(unittest.TestCase):
    def test_arabic_normalization(self):
        self.assertEqual(normalize_text("أحمد ـ بيك"), normalize_text("احمد بيك"))

    def test_phone_preserves_leading_zero(self):
        self.assertEqual(normalize_phone("010 1234-5678"), "01012345678")

    def test_missing_required_fields_rejected(self):
        with self.assertRaises(ValueError):
            map_row({"المنطقة": "الزرقا"}, 2)

    def test_defaults_are_safe(self):
        mapped = map_row(row(), 2)
        self.assertEqual(mapped["qr_status"], "غير معروف")
        self.assertFalse(mapped["is_verified"])

    def test_duplicate_business_and_region_flagged(self):
        report = build_report([row(), row(name="مطعم النيل"), row(name="مطعم آخر")])
        self.assertEqual(report["summary"]["create_candidates"], 2)
        self.assertEqual(report["summary"]["skipped_duplicates"], 1)

    def test_same_phone_and_region_flagged(self):
        report = build_report([row(name="نشاط أ"), row(name="نشاط ب")])
        self.assertEqual(report["summary"]["skipped_duplicates"], 1)

    def test_same_name_different_region_not_merged(self):
        report = build_report([row(), row(region="دمياط الجديدة")])
        self.assertEqual(report["summary"]["create_candidates"], 2)

    def test_unknown_stage_warned_not_silently_mapped(self):
        mapped = map_row(row(stage="مرحلة غير معروفة"), 2)
        self.assertIn("stage_mapping_warning", mapped)

    def test_dry_run_never_mutates(self):
        report = build_report([row()])
        self.assertEqual(report["mutations_performed"], 0)
        self.assertEqual(report["mode"], "DRY_RUN_ONLY")

if __name__ == "__main__":
    unittest.main()
