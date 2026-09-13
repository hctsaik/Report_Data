from pathlib import Path

# Keep Traditional Chinese copy consistent across the two new courses.
replacements={'够':'夠','结果':'結果','改变':'改變','合计':'合計','时间':'時間','条件':'條件','后续':'後續','后续':'後續','续':'續','数据':'資料','标记':'標記','宣称':'宣稱','手机':'手機'}
replacements.update({'S50 第一次執行，機台中斷，結果 Fail。':'S50 第一次量測，結果 Fail。','回到 S50 再執行；新 Run、新結果，前次仍可查。':'回到 S50 複測；新 Visit、新結果，前次仍可查。'})
for name in ['course-content.js','course.js','scenarios.js']:
    p=Path(name)
    text=p.read_text(encoding='utf-8')
    for old,new in replacements.items():text=text.replace(old,new)
    p.write_text(text,encoding='utf-8')
