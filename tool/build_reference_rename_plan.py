"""Write a reviewable rename manifest; performs no PDF renames or content edits."""
import json
import csv
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
folder=Path(r'C:\Users\LENOVO 14ALC6\Desktop\Icfes_SaberPlus')
inventory=json.loads((ROOT/'tmp/pdfs/naming-audit/inventory.json').read_text(encoding='utf-8'))
decisions=json.loads((ROOT/'tool/reference_pdf_names.json').read_text(encoding='utf-8'))
assert len(inventory)==len(decisions)==47
files=[]
for row,decision in zip(inventory,decisions):
    assert row['id']==decision['id']
    files.append({'id':row['id'],'original':row['original'],'new_name':decision['name'],
        'sha256':row['sha256'],'pages':row['pages'],'calendar':decision['calendar'],'evidence':decision['evidence']})
assert len({f['new_name'].lower() for f in files})==47
plan={'root':str(folder),'date':'2026-10-29','notice':'Catalogacion por portada y procedencia. No certifica autenticidad ni permisos de uso. No se elimina ningun archivo.', 'files':files}
stem='REGISTRO_RENOMBRADO_2026-10-29'
dest=folder/(stem+'.json')
if dest.exists():raise FileExistsError('El registro ya existe; no sobrescribir.')
dest.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
with (folder/(stem+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(files[0]),delimiter=';');writer.writeheader();writer.writerows(files)
counts=Counter(f['calendar'] for f in files)
text=['# Organizacion de PDF de referencia','',
    'Registro del 29 de octubre de 2026. Se revisaron portadas de 47 PDF y se buscaron datos textuales. No se validaron todas sus preguntas, autenticidad, claves ni permisos de uso.',
    '', '## Criterio de nombres','',
    '- ICFES_ano_Cal-A o Cal-B_Sesion: clasificacion segun la portada o el periodo declarado; no equivale a autenticacion.',
    '- Cal-por-confirmar y Cal-B/A-por-confirmar: hay datos ausentes o contradictorios. No se adivina el calendario.',
    '- Simulacro_Grupo-500 y Simulacro_La-Evaluacion: materiales editoriales, no clasificados como pruebas oficiales. S11-A/S11-B son versiones, no calendarios.',
    '- Ref001, Ref002, etc.: identificador estable para distinguir versiones. No es un codigo oficial.',
    '- Sesiones-1-y-2: se encontro la segunda portada dentro del mismo PDF.',
    '- Con-marcas: contiene anotaciones; no se certifica que todas sean correctas.',
    '',f'Clasificacion: A={counts["A"]}; B={counts["B"]}; pendientes={counts["pending"]}; simulacros sin calendario={counts["not-applicable"]}.',
    '', 'Las copias Ref031 y Ref032 son identicas por SHA-256 y se conservan ambas. Los demas archivos tienen hashes diferentes; eso no garantiza que todas sus preguntas sean distintas.',
    '', 'Los anos/periodos rotulados en algunas portadas contradicen los nombres anteriores o los identificadores. El detalle se conserva en los registros JSON y CSV.',
    '', '## Recuperar nombres anteriores','',
    'Conservar el JSON y el script junto a estos archivos. Para comprobar la reversión sin cambios:',
    '', '```powershell', '.\\Restaurar_nombres_PDF.ps1 -Root $PWD.Path -Plan .\\'+stem+'.json -Undo', '```',
    '', 'Para aplicarla, agregar `-Apply`. Antes de cualquier cambio se validan todos los archivos, los destinos y los hashes. No se sobrescribe nada. Si hubo un renombrado parcial por interrupcion, revisar el JSON y no forzar la operacion.',
    '', '## Fuentes de apoyo para calendarios','',
    '- Guia Icfes 2025-2, calendario A: https://www.icfes.gov.co/wp-content/uploads/2025/04/30-abril-guia-orientacion-saber-11o-2025-2.pdf',
    '- Guias 2025-1 y 2026-1 calendario B aportadas previamente por el usuario; los periodos de una portada no certifican su autenticidad.',
    '', '## Indice de archivos','']
for f in files:text.extend([f'### Ref{f["id"]:03d}',f'- Nuevo: `{f["new_name"]}`',f'- Anterior: `{f["original"]}`',f'- Paginas: {f["pages"]}. Criterio: {f["evidence"]}',''])
(folder/'LEEME_ORGANIZACION.md').write_text('\n'.join(text),encoding='utf-8')
print(json.dumps({'manifest':str(dest),'counts':dict(counts),'files':len(files)},ensure_ascii=True))
