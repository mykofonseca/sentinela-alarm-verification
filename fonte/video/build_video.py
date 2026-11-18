"""Gera o vídeo pitch: slides HTML -> PNG (Edge), narração (voz pt-BR do Windows) -> WAV, montagem com ffmpeg."""
import pathlib, subprocess, sys, wave, json
import imageio_ffmpeg
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent)); import render
FF = imageio_ffmpeg.get_ffmpeg_exe()

CSS = """*{box-sizing:border-box;margin:0;padding:0}html,body{width:1920px;height:1080px;overflow:hidden}
body{font-family:'Segoe UI',Arial,sans-serif;background:#14233A;color:#fff;padding:80px 100px;display:flex;flex-direction:column}
.brand{font-weight:800;letter-spacing:5px;font-size:28px;display:flex;align-items:center;gap:14px;opacity:.95}
.brand i{width:34px;height:34px;border:4px solid #fff;border-radius:50%;position:relative;display:inline-block}
.brand i:after{content:"";position:absolute;inset:6px;background:#fff;border-radius:50%}
h1{font-size:76px;line-height:1.08;margin:28px 0 20px} h2{font-size:56px;margin:26px 0 30px}
.k{color:#7FB0FF}.r{color:#FF8A80}.muted{opacity:.7}
p{font-size:34px;line-height:1.4;max-width:1500px}
.q{border-left:10px solid #7FB0FF;background:#ffffff12;padding:30px 40px;font-size:44px;line-height:1.3;font-weight:600;border-radius:0 14px 14px 0}
.flow{display:flex;gap:18px;align-items:stretch;margin-top:20px}
.flow div{flex:1;background:#ffffff12;border:2px solid #ffffff2a;border-radius:16px;padding:26px 22px;font-size:27px;line-height:1.3}
.flow b{display:block;font-size:31px;margin:10px 0 8px;color:#fff}.flow span{font-size:48px}
.flow .arrow{flex:0 0 30px;background:none;border:none;padding:0;display:flex;align-items:center;font-size:42px;color:#7FB0FF}
.grid4{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:10px}
.grid4 div{background:#ffffff12;border-radius:16px;padding:26px 30px;font-size:29px;line-height:1.45}
.grid4 b{display:block;font-size:24px;letter-spacing:2px;text-transform:uppercase;color:#7FB0FF;margin-bottom:8px}
.shots{display:flex;gap:28px;flex:1;align-items:flex-start;margin-top:6px}
.shots figure{flex:1;display:flex;flex-direction:column;gap:12px}
.shots img{width:100%;border-radius:10px;border:2px solid #ffffff33}
.shots figcaption{font-size:28px;font-weight:600}
.foot{margin-top:auto;font-size:22px;opacity:.55}
.steps{display:grid;grid-template-columns:1fr 1fr;gap:30px;margin-top:10px}
.steps div{background:#ffffff12;border-radius:16px;padding:30px 36px;font-size:30px;line-height:1.55}
.steps b{font-size:40px;display:block;margin-bottom:10px;color:#7FB0FF}
"""
T = "../../telas/"
SLIDES = [
 ("s1", f"""<div class="brand"><i></i>SENTINELA</div>
 <h1 style="font-size:96px;margin-top:150px">Do alarme à decisão<br><span class="k">em menos de um minuto.</span></h1>
 <p class="muted">Verificação inteligente de alarmes de perímetro em instalações críticas<br>Desafio FIAP × AMAZUL · Application Development · Sprints 1 e 2</p>
 <div class="foot">Protótipo acadêmico · todos os dados, locais e pessoas são fictícios</div>""",
 "Em uma instalação nuclear, todo alarme de perímetro precisa de uma resposta rápida: é real ou não é? Nós somos o grupo SENTINELA."),
 ("s2", """<div class="brand"><i></i>SENTINELA</div><h2>O problema</h2>
 <p>Hoje o operador <b>procura a câmera certa</b>, interpreta a imagem e, na dúvida, <b>manda uma equipe só para ver</b>. A maioria dos alarmes vem de <span class="r">animais, vento ou vegetação</span>.</p>
 <div class="q" style="margin-top:50px">Como podemos reduzir o tempo entre o disparo de um alarme no perímetro e uma decisão confiável do operador, acionando a equipe mais cedo e só quando necessário?</div>
 <div class="foot">Base: modelo detectar–retardar–responder (AIEA NSS nº 13; CNEN NN 2.01; Garcia, 2008)</div>""",
 "Hoje, o operador procura a câmera certa, interpreta a imagem e, na dúvida, manda uma equipe só para ver. A maioria dos alarmes vem de animais, vento ou vegetação. Nossa pergunta: como reduzir o tempo entre o disparo do alarme e uma decisão confiável, acionando a equipe mais cedo, e só quando for preciso?"),
 ("s3", """<div class="brand"><i></i>SENTINELA</div><h2>A solução</h2>
 <div class="flow"><div><span>📡</span><b>Sensor IoT</b>A cerca detecta vibração ou interrupção do feixe</div><div class="arrow">→</div>
 <div><span>🧠</span><b>IA na borda</b>Visão computacional classifica a imagem em milissegundos</div><div class="arrow">→</div>
 <div><span>🚁</span><b>Drone</b>Verificação aérea automática onde a câmera não alcança</div><div class="arrow">→</div>
 <div><span>🧑‍💻</span><b>Operador decide</b>Mapa, evidência e contexto em uma tela</div><div class="arrow">→</div>
 <div><span>🏃</span><b>Equipe</b>Ocorrência no celular, com foto e rota</div></div>
 <p style="margin-top:50px" class="muted">Humano sempre no controle: a IA e o drone trazem a informação, a pessoa decide.</p>""",
 "O SENTINELA une sensores IoT na cerca, câmeras com visão computacional processada na borda, drones que fazem a verificação aérea automática e um mapa operacional. O alarme já chega ao operador com imagem, classificação da IA e contexto. E quem decide é sempre uma pessoa."),
 ("s4", """<div class="brand"><i></i>SENTINELA</div><h2>17 personas mapeadas</h2>
 <div class="grid4"><div><b>Usam diretamente</b>Operadora da central · supervisor de turno · agente de resposta · piloto remota de drone</div>
 <div><b>Recebem informações</b>Coordenação de proteção física · direção · inspetor do regulador · força de apoio externa</div>
 <div><b>São afetados</b>Empregados · terceirizados de manutenção · visitantes · comunidade vizinha</div>
 <div><b>Mantêm a solução</b>Técnico de sistemas · técnico de drones · TI · cientista de dados · encarregado LGPD</div></div>""",
 "Mapeamos dezessete personas: quem usa, como a operadora, o agente de resposta e a piloto de drone; quem recebe informação, como a coordenação e o regulador; quem é afetado, como terceirizados e vizinhos; e quem mantém, como técnicos e o encarregado de dados."),
 ("s5", f"""<div class="brand"><i></i>SENTINELA</div><h2 style="margin-bottom:24px">Telas principais</h2>
 <div class="shots"><figure><img src="{T}t1-painel.png"><figcaption>T1 · Painel operacional</figcaption></figure>
 <figure><img src="{T}t2-verificacao.png"><figcaption>T2 · Verificação do alarme</figcaption></figure></div>""",
 "No painel, o alarme aparece no mapa e na fila, com cronômetro. Na verificação, a operadora vê a evidência e o contexto, e decide com um clique."),
 ("s6", f"""<div class="brand"><i></i>SENTINELA</div><h2 style="margin-bottom:24px">Telas principais</h2>
 <div class="shots"><figure><img src="{T}t3-drone.png"><figcaption>T3 · Missão do drone</figcaption></figure>
 <figure><img src="{T}t4-mobile-agente.png"><figcaption>T4 · App do agente</figcaption></figure>
 <figure><img src="{T}t5-dispositivos.png"><figcaption>T5 · Saúde dos dispositivos</figcaption></figure></div>""",
 "O drone vai até o ponto que a câmera não cobre. O agente recebe a ocorrência no celular. E a manutenção vê na hora quando um dispositivo para, e qual ponto cego isso cria."),
 ("s7", """<div class="brand"><i></i>SENTINELA</div><h2>Próximos passos</h2>
 <div class="steps"><div><b>Sprint 3</b>Navegação por perfil · mapa e status · fila de alarmes · simulador de eventos · verificação e decisão</div>
 <div><b>Sprint 4</b>Missão do drone · app do agente · saúde dos dispositivos · trabalhos autorizados · relatórios e auditoria</div></div>
 <p style="margin-top:46px">Sensores, IA e drones <b>simulados</b> com dados fictícios em JSON.<br>Meta: <span class="k"><b>decisão em menos de 60 segundos.</b></span></p>
 <div class="foot" style="font-size:30px;opacity:.9"><b>SENTINELA</b> · do alarme à decisão.</div>""",
 "Nas sprints três e quatro, vamos construir a aplicação web, com dados simulados de sensores, IA e drones. A meta: decisão em menos de um minuto. SENTINELA: do alarme à decisão."),
]

def tts(text, wav, rate=1):
    ps = f"""Add-Type -AssemblyName System.Speech; $s=New-Object System.Speech.Synthesis.SpeechSynthesizer;
$s.SelectVoice('Microsoft Maria Desktop'); $s.Rate={rate}; $s.SetOutputToWaveFile('{wav}');
$s.Speak([IO.File]::ReadAllText('{wav}.txt',[Text.Encoding]::UTF8)); $s.Dispose()"""
    pathlib.Path(str(wav) + ".txt").write_text(text, encoding="utf-8")
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
    with wave.open(str(wav)) as w: return w.getnframes() / w.getframerate()

if __name__ == "__main__":
    rate = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    out = HERE / "build"; out.mkdir(exist_ok=True)
    parts, total, roteiro = [], 0, []
    for sid, html, fala in SLIDES:
        h = HERE / f"{sid}.html"
        h.write_text(f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}</body></html>', encoding="utf-8")
        png = out / f"{sid}.png"; render.shot(h, png, 1920, 1080, 1)
        wav = out / f"{sid}.wav"; dur = tts(fala, wav, rate)
        seg = out / f"{sid}.mp4"; d = dur + 0.7
        subprocess.run([FF, "-y", "-loglevel", "error", "-loop", "1", "-i", str(png), "-i", str(wav),
                        "-af", "adelay=300|300,apad", "-t", f"{d:.2f}", "-r", "30", "-c:v", "libx264", "-tune", "stillimage",
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "2", str(seg)], check=True)
        parts.append(seg); roteiro.append((sid, round(total, 1), round(total + d, 1), fala)); total += d
    lst = out / "list.txt"; lst.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    final = ROOT / "video" / "pitch_sentinela.mp4"
    subprocess.run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(final)], check=True)
    print(json.dumps({"total_s": round(total, 1), "cenas": roteiro}, ensure_ascii=False, indent=1))
