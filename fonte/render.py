"""Renderiza os esboços HTML em PNG e o documento HTML em PDF usando o Edge headless."""
import subprocess, sys, pathlib, tempfile
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
ROOT = pathlib.Path(__file__).resolve().parent.parent

def shot(html: pathlib.Path, png: pathlib.Path, w=1440, h=900, scale=1.5):
    prof = tempfile.mkdtemp()
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={prof}",
                    f"--window-size={w},{h}", f"--force-device-scale-factor={scale}", "--virtual-time-budget=3000",
                    f"--screenshot={png}", html.as_uri()], check=True, capture_output=True)

def pdf(html: pathlib.Path, out: pathlib.Path):
    prof = tempfile.mkdtemp()
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", f"--user-data-dir={prof}", "--no-pdf-header-footer",
                    "--print-to-pdf-no-header", "--virtual-time-budget=5000", f"--print-to-pdf={out}", html.as_uri()],
                   check=True, capture_output=True)

if __name__ == "__main__":
    what = sys.argv[1]
    if what == "telas":
        for f in sorted((ROOT / "fonte" / "telas").glob("t*.html")):
            if len(sys.argv) > 2 and sys.argv[2] not in f.name: continue
            out = ROOT / "telas" / (f.stem + ".png"); shot(f, out); print(out)
    elif what == "slides":
        for f in sorted((ROOT / "fonte" / "video").glob("s*.html")):
            out = ROOT / "fonte" / "video" / (f.stem + ".png"); shot(f, out, 1920, 1080, 1); print(out)
    elif what == "pdf":
        pdf(ROOT / "fonte" / "documento.html", ROOT / sys.argv[2]); print("ok")
