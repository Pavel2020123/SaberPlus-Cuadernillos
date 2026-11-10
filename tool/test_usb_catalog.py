import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import usb_pdf_catalog as catalog


class CatalogTests(unittest.TestCase):
    def test_exact_duplicate_removal_and_restore_keep_canonical(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/'allowed';root.mkdir();audit=root/'_SaberPlus_catalogo'
            a,b=root/'2026-a.pdf',root/'2026-b.pdf'
            a.write_bytes(b'Identical fixture, no user data');b.write_bytes(a.read_bytes())
            with patch.object(catalog,'ROOT',root),patch.object(catalog,'AUDIT',audit),patch.object(catalog,'serial',return_value='test'):
                with catalog.db() as conn:
                    catalog.inventory(conn)
                    for row in conn.execute('SELECT * FROM files').fetchall():
                        conn.execute('UPDATE files SET sha256=? WHERE id=?',(catalog.digest(root/row['current_path']),row['id']))
                    conn.commit();catalog.dedup(conn,True)
                    removed=conn.execute("SELECT * FROM files WHERE status='eliminado_duplicado'").fetchone()
                    kept=conn.execute('SELECT * FROM files WHERE id=?',(removed['duplicate_of'],)).fetchone()
                    self.assertTrue((root/kept['current_path']).exists())
                    self.assertFalse((root/removed['current_path']).exists())
                    catalog.restore(conn,removed['id'])
                    self.assertEqual((root/removed['current_path']).read_bytes(),(root/kept['current_path']).read_bytes())
                conn.close()

    def test_binary_compare_rejects_same_size_different_bytes(self):
        with tempfile.TemporaryDirectory() as folder:
            left,right=Path(folder)/'a.pdf',Path(folder)/'b.pdf'
            left.write_bytes(b'abc');right.write_bytes(b'abd')
            self.assertFalse(catalog.identical(left,right))
            right.write_bytes(b'abc');self.assertTrue(catalog.identical(left,right))

    def test_scope_rejects_sibling_and_root(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/'allowed';root.mkdir()
            with patch.object(catalog,'ROOT',root):
                self.assertEqual(catalog.safe(root/'x.pdf'),(root/'x.pdf').resolve())
                with self.assertRaises(ValueError):catalog.safe(root/'../outside.pdf')
                with self.assertRaises(ValueError):catalog.safe(root)

    def test_years_are_prioritized_not_confirmed(self):
        self.assertGreater(catalog.priority(Path('2026-1.pdf'))[0],catalog.priority(Path('LYON.pdf'))[0])
        self.assertIn('no fecha confirmada',catalog.priority(Path('2026-1.pdf'))[1])
        self.assertGreater(catalog.priority(Path('X1.pdf'))[0],catalog.priority(Path('T1.pdf'))[0])

    def test_question_starts_are_explicitly_only_candidates(self):
        text='25. Pregunta con una diferencia real\nA. texto de respuesta\n2026. Esto no es una pregunta\nI. Una lectura de tabla de datos'
        self.assertEqual([q['number'] for q in catalog.candidates(text)],[25,1])


if __name__=='__main__':unittest.main()
