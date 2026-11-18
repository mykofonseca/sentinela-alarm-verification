"""Converte plano.md em fonte/documento.html (com capa e estilo de impressão) e gera o PDF."""
import pathlib, re, sys
from markdown_it import MarkdownIt
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import render

ROOT = pathlib.Path(__file__).resolve().parent.parent
md = (ROOT / "plano.md").read_text(encoding="utf-8")

# separa o cabeçalho (vira capa) do corpo
body_md = md.split("\n---\n", 1)[1]
aviso = re.search(r"> \*\*Aviso:\*\*(.*)", md).group(1).strip()

mdi = MarkdownIt("commonmark", {"html": True}).enable("table")
body = mdi.render(body_md).replace('src="telas/', 'src="../telas/')
aviso_html = MarkdownIt().renderInline(aviso)

# figuras com legenda
body = re.sub(r'<p><img src="([^"]+)" alt="([^"]+)" ?/?></p>',
              r'<figure><img src="\1" alt="\2"><figcaption>Figura – \2 (esboço, dados fictícios)</figcaption></figure>', body)
# sumário a partir dos h2
toc = "".join(f'<li>{re.sub("<.*?>","",h)}</li>' for h in re.findall(r"<h2>(.*?)</h2>", body))

integrantes = (ROOT / "integrantes.txt").read_text(encoding="utf-8") if (ROOT / "integrantes.txt").exists() else ""
linhas = [l.strip() for l in integrantes.splitlines() if re.match(r"^\s*\d+\.", l)]
membros = "".join(f"<li>{l.split('.',1)[1].strip()}</li>" for l in linhas)

html = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>SENTINELA – Planejamento Sprints 1 e 2</title>
<style>
@page {{ size: A4; margin: 18mm 16mm 18mm 16mm; }}
@page :first {{ margin: 0; }}
:root {{ --navy:#14233A; --blue:#1F5FBF; --ink:#1B2430; --ink2:#4A5568; --line:#D5DAE1; }}
* {{ box-sizing: border-box; }}
body {{ font-family: "Segoe UI", Arial, sans-serif; color: var(--ink); font-size: 10.2pt; line-height: 1.5; margin: 0; }}
.cover {{ height: 258mm; display: flex; flex-direction: column; justify-content: space-between; page-break-after: always;
  background: var(--navy); color: #fff; margin: 0; padding: 24mm 22mm; height: 296mm; overflow: hidden; }}
.cover .brand {{ font-size: 13pt; letter-spacing: 4px; font-weight: 800; display:flex; align-items:center; gap:10px }}
.cover .brand i {{ width:22px;height:22px;border:3px solid #fff;border-radius:50%;display:inline-block;position:relative }}
.cover .brand i:after {{ content:"";position:absolute;inset:4px;background:#fff;border-radius:50% }}
.cover h1 {{ font-size: 34pt; line-height: 1.1; margin: 0 0 10px; }}
.cover .sub {{ font-size: 14pt; opacity: .85; max-width: 150mm }}
.cover .meta {{ font-size: 10.5pt; opacity: .9; line-height: 1.7 }}
.cover .meta ol {{ margin: 4px 0 0 18px; padding: 0 }}
.cover .aviso {{ border: 1px solid #ffffff55; border-radius: 6px; padding: 10px 14px; font-size: 9pt; opacity: .85 }}
.cover img {{ width: 100%; border-radius: 6px; border: 1px solid #ffffff33; }}
.toc {{ page-break-after: always; }}
.toc ol {{ font-size: 12pt; line-height: 2 }}
h2 {{ font-size: 17pt; color: var(--navy); border-bottom: 3px solid var(--blue); padding-bottom: 4px; margin: 0 0 12px; page-break-before: always; }}
h2:first-of-type {{ page-break-before: auto }}
h3 {{ font-size: 12.5pt; color: var(--blue); margin: 18px 0 6px; page-break-after: avoid; }}
p, li {{ orphans: 3; widows: 3; }}
table {{ border-collapse: collapse; width: 100%; margin: 8px 0 14px; font-size: 8.6pt; line-height: 1.38; }}
th {{ background: #EEF2F8; text-align: left; font-weight: 700; color: var(--navy); }}
th, td {{ border: 1px solid var(--line); padding: 5px 6px; vertical-align: top; }}
tr {{ page-break-inside: avoid; }}
blockquote {{ margin: 10px 0; padding: 10px 14px; background: #EEF4FD; border-left: 5px solid var(--blue); border-radius: 0 6px 6px 0; }}
blockquote h3 {{ margin: 0; color: var(--navy); font-size: 13pt; line-height: 1.35 }}
pre {{ background: #F4F6F9; border: 1px solid var(--line); border-radius: 6px; padding: 10px; font-size: 8.2pt; line-height: 1.35; white-space: pre; overflow: hidden; page-break-inside: avoid; }}
code {{ font-family: Consolas, monospace; font-size: 8.8pt; }}
figure {{ margin: 8px 0 6px; page-break-inside: avoid; }}
figure img {{ width: 100%; border: 1px solid var(--line); border-radius: 4px; }}
figcaption {{ font-size: 8.5pt; color: var(--ink2); text-align: center; margin-top: 3px; font-style: italic; }}
h3 + figure {{ page-break-before: avoid }}
hr {{ display: none }}
a {{ color: var(--blue); word-break: break-all; }}
</style></head><body>
<section class="cover">
  <div class="brand"><i></i>SENTINELA</div>
  <div>
    <h1>Verificação inteligente de alarmes de perímetro</h1>
    <div class="sub">Documento de planejamento — Sprints 1 e 2 · Application Development<br>Desafio FIAP × AMAZUL: Segurança Física em Instalações Nucleares</div>
  </div>
  <img src="../telas/t1-painel.png" alt="Painel operacional">
  <div class="meta">Ciências da Computação · FIAP · Prof. Rodrigo Settervall Moraes · novembro de 2026
    {'<br><b>Integrantes:</b><ol>' + membros + '</ol>' if membros else ''}</div>
  <div class="aviso"><b>Aviso:</b> {aviso_html}</div>
</section>
<section class="toc"><h3 style="font-size:16pt;color:#14233A">Sumário</h3><ol>{toc}</ol></section>
{body}
</body></html>"""
(ROOT / "fonte" / "documento.html").write_text(html, encoding="utf-8")
render.pdf(ROOT / "fonte" / "documento.html", ROOT / "Planejamento_SENTINELA_Sprints1-2.pdf")
print("PDF gerado")
