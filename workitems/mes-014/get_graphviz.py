from pathlib import Path
import urllib.request,hashlib,zipfile
R=Path(__file__).resolve().parents[2];D=R/'tools/vendor/graphviz';D.mkdir(parents=True,exist_ok=True)
url='https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/16.1.0/windows_10_cmake_Release_Graphviz-16.1.0-win64.zip'
p=D/'graphviz.zip'
if not p.exists():urllib.request.urlretrieve(url,p)
expected=urllib.request.urlopen(url+'.sha256').read().decode().split()[0]
assert hashlib.sha256(p.read_bytes()).hexdigest()==expected
with zipfile.ZipFile(p) as z:
 for info in z.infolist():
  target=(D/info.filename).resolve();assert target.is_relative_to(D.resolve())
 z.extractall(D)
print(next(D.rglob('dot.exe')))
