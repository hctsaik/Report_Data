from pathlib import Path
p=Path('er-atlas.js');s=p.read_text(encoding='utf-8')
s=s.replace("showTeaching(nodes.get(id).category in teaching?nodes.get(id).category:'lot')", "showTeaching(teachingForNode(id))")
s=s.replace("function showTeaching(key)", """function teachingForNode(id){
 for(const key of ['recipe','equipment','carrier','lot','flow'])if(teaching[key].refs.some(ref=>model.mapping[ref]===id))return key;
 const recipeRefs=['2677:recipe-key','2677:recipe-eqp','2677:pd','2677:pd-key','2677:pd-eqp','2673:lr-eqp-link'];
 if(recipeRefs.some(ref=>model.mapping[ref]===id))return 'recipe';
 return 'overview';
}
function showTeaching(key)""")
p.write_text(s,encoding='utf-8')
