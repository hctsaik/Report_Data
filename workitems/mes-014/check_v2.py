from pathlib import Path
R=Path(__file__).resolve().parents[2]
p=R/'tests/check_er_atlas.py';s=p.read_text(encoding='utf-8').replace("'tests/evidence/mes-014'","'tests/evidence/mes-014/v2'").replace('er-model-v1','er-model-v2').replace('fab-er-v1','fab-er-v2').replace('==119','==121').replace('canonical_nodes=119','canonical_nodes=121').replace('119 canonical','121 canonical').replace("assert '已定位' in page.locator('#status').inner_text()", "assert page.locator('#path-list .edge-pair').count()>0")
# Verify real adjacency in every inspector pair and readable active text.
s=s.replace("assert not errors,errors\n   if route", """assert not errors,errors
   assert page.evaluate('''()=>[...document.querySelectorAll('.edge-pair')].every(p=>{const b=[...p.querySelectorAll('[data-inspect]')].map(b=>b.dataset.inspect);return ER_ATLAS.model.edges.some(e=>(e.a===b[0]&&e.b===b[1])||(e.b===b[0]&&e.a===b[1]))})''')
   scale=page.evaluate('document.querySelector(\"#canvas\").clientWidth/ER_ATLAS.getView()[2]')
   assert scale>=.79,(width,route,scale)
   if route""")
archive=R/'workitems/mes-014/baseline/check_er_atlas_v1.py'
if not archive.exists():archive.write_bytes(p.read_bytes())
p.write_text(s,encoding='utf-8')
exec(compile(s,str(p),'exec'),{'__file__':str(p),'__name__':'__main__'})
