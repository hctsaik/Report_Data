from pathlib import Path
p=Path('subject-er.js');s=p.read_text(encoding='utf-8').replace("'以 '+current.title+' 為主詞'","current.title")
s=s.replace("'改以 '+target.title+' 為主詞 →'","'改以 '+({lot:'Lot',carrier:'FOUP',equipment:'EQP',flow:'Flow'})[target.key]+' 為主詞 →'")
p.write_text(s,encoding='utf-8')
