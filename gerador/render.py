#!/usr/bin/env python3
"""Gera as artes do dia a partir de um plano JSON.

Uso:  python3 gerador/render.py planos/2026-11-06.json
Saída: posts/<data>/*.png, posts/<data>/previa.png e posts/<data>/manifesto.json
       (o manifesto traz a URL pública de cada imagem, na ordem, para agendar no Metricool)
"""
import html, json, os, sys
from PIL import Image
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOTOS = os.path.join(RAIZ, "fotos")
URL_BASE = "https://raw.githubusercontent.com/sportech338/sportech-posts/main/"
FOTOS_INFO = json.load(open(os.path.join(FOTOS, "fotos.json")))
NAVY, OR, CLARO = "#0c1f3f", "#ff6a13", "#f4f4f1"

def esc(t):
    return html.escape(str(t or "")).replace("\n", "<br>")

def foto(n):
    if n not in FOTOS_INFO:
        raise SystemExit(f"Foto desconhecida: {n}. Opções: {[k for k in FOTOS_INFO if not k.startswith('_')]}")
    return "file://" + os.path.join(FOTOS, n + ".jpg")

def fit_mode(n):
    return "contain;background:#fff" if FOTOS_INFO.get(n, {}).get("fundo_branco") else "cover"

def titulo(d, cls=""):
    t, dz = esc(d.get("titulo")), esc(d.get("destaque"))
    if not (t or dz): return ""
    sep = "<br>" if t and dz else ""
    return f'<h1 class="{cls}">{t}{sep}<span class="o">{dz}</span></h1>'

BASE = """<!doctype html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:WWpx;height:HHpx;overflow:hidden;position:relative;font-family:'Inter',sans-serif;color:#0c1f3f;background:#f4f4f1}
img{display:block}
h1{font-weight:900;letter-spacing:-0.025em;line-height:1.02}
.o{color:#ff6a13}
.brand{position:absolute;top:64px;left:70px;font-weight:800;letter-spacing:6px;font-size:28px;z-index:5;padding:10px 20px;border-radius:30px}
.num{position:absolute;top:64px;right:70px;font-size:28px;font-weight:700;z-index:5;padding:8px 18px;border-radius:24px;background:rgba(255,255,255,.85);color:#0c1f3f}
.pill{display:inline-block;align-self:flex-start;background:#ff6a13;color:#fff;font-weight:800;border-radius:60px}
.chips{display:flex;gap:14px;flex-wrap:wrap}
.chips div{border:3px solid #ff6a13;font-weight:700;border-radius:40px}
.box{position:absolute;display:flex;flex-direction:column;overflow:hidden}
CSS
</style></head><body>BODY
<script>
// Diminui o texto de cada .box até caber (evita sobreposição em qualquer texto)
window.__overflow = [];
function medir(b){
  var t=Infinity, bt=-Infinity, w=0;
  Array.prototype.forEach.call(b.children, function(c){
    var r=c.getBoundingClientRect(); t=Math.min(t,r.top); bt=Math.max(bt,r.bottom); w=Math.max(w,c.scrollWidth);
  });
  return {h: bt-t, w: w};
}
document.querySelectorAll('.box').forEach(function(b){
  var n = 0, m = medir(b);
  while ((m.h > b.clientHeight + 2 || m.w > b.clientWidth + 2) && n < 30) {
    b.querySelectorAll('*').forEach(function(e){
      var fs = parseFloat(getComputedStyle(e).fontSize);
      e.style.fontSize = (fs * 0.95) + 'px';
    });
    n++; m = medir(b);
  }
  if (m.h > b.clientHeight + 2) window.__overflow.push(b.className);
});
</script></body></html>"""

# ---------------------------------------------------------------- STORIES 1080x1920
def story_foto(d):
    css = f"""
.ph{{position:absolute;inset:0;width:1080px;height:1920px;object-fit:{fit_mode(d['foto'])};object-position:center {d.get('foco','30%')}}}
.grad{{position:absolute;bottom:0;left:0;width:1080px;height:1150px;background:linear-gradient(transparent,rgba(12,31,63,.96) 50%)}}
.brand{{color:#fff;background:rgba(12,31,63,.6)}}
.box{{left:80px;right:80px;bottom:170px;height:820px;justify-content:flex-end;gap:34px;color:#fff}}
h1{{font-size:112px;color:#fff}}
p{{font-size:42px;line-height:1.3;color:#dfe6f2}}
.pill{{font-size:40px;padding:26px 46px}}"""
    body = f"""<img class="ph" src="{foto(d['foto'])}"><div class="grad"></div><div class="brand">COOLERBAG</div>
<div class="box">{titulo(d)}<p>{esc(d.get('texto'))}</p><div class="pill">{esc(d.get('cta','Link na bio 👆'))}</div></div>"""
    return css, body

def story_cores(d):
    subs = d.get("subtitulos", ["a clássica", "cara de verão", "discreta e elegante"])
    cards = "".join(f'<div class="cd"><img src="{foto(f)}"><div><b>{n}</b><span>{esc(s)}</span></div></div>'
                    for f, n, s in zip(["preta_fundo_branco", "azul_fundo_branco", "cinza_fundo_branco"], ["Preta", "Azul", "Cinza"], subs))
    css = f"""
body{{background:{NAVY}}}
.brand{{color:{OR};left:50px}}
.box.t{{left:80px;right:80px;top:170px;height:340px;justify-content:center}}
h1{{font-size:118px;color:#fff}}
.cards{{position:absolute;top:540px;left:60px;width:960px;display:flex;flex-direction:column;gap:26px}}
.cd{{display:flex;align-items:center;gap:30px;background:#fff;border-radius:40px;padding:18px 40px 18px 18px}}
.cd img{{width:280px;height:300px;object-fit:contain}}
.cd b{{font-size:64px;font-weight:900;letter-spacing:-2px}}
.cd span{{display:block;font-size:30px;color:#7a8597;font-weight:600;margin-top:6px}}
.foot{{position:absolute;bottom:70px;left:60px;right:60px;height:110px;align-items:center;justify-content:center;color:#cfd8e6;font-size:38px;font-weight:700;text-align:center}}"""
    body = f"""<div class="brand">COOLERBAG</div><div class="box t">{titulo(d)}</div><div class="cards">{cards}</div>
<div class="box foot"><div>{esc(d.get('cta','Link na bio 👆'))}</div></div>"""
    return css, body

def story_oferta(d):
    chips = "".join(f"<div>{esc(c)}</div>" for c in d.get("chips", ["Frete grátis", "Até 12x", "3% off no PIX"]))
    css = f"""
.ph{{position:absolute;top:0;left:0;width:1080px;height:1180px;object-fit:{fit_mode(d['foto'])};object-position:center {d.get('foco','30%')}}}
.grad{{position:absolute;top:760px;left:0;width:1080px;height:430px;background:linear-gradient(transparent,{NAVY})}}
.panel{{position:absolute;top:1180px;left:0;width:1080px;height:740px;background:{NAVY}}}
.brand{{color:#fff;background:rgba(12,31,63,.6)}}
.box.t{{left:80px;right:80px;top:820px;height:340px;justify-content:flex-end}}
h1{{font-size:100px;color:#fff}}
.box.p{{left:80px;right:80px;top:1200px;height:470px;gap:18px;color:#fff}}
.pre{{font-size:36px;color:#cfd8e6;font-weight:600}}
.preco{{font-size:140px;font-weight:900;letter-spacing:-5px;line-height:1}}.preco small{{font-size:60px}}
.chips div{{font-size:30px;padding:12px 26px;color:#fff}}
.pill{{position:absolute;bottom:90px;left:80px;right:80px;text-align:center;font-size:44px;padding:30px}}"""
    body = f"""<img class="ph" src="{foto(d['foto'])}"><div class="grad"></div><div class="panel"></div><div class="brand">COOLERBAG</div>
<div class="box t">{titulo(d)}</div>
<div class="box p"><div class="pre">{esc(d.get('prefixo','a partir de'))}</div><div class="preco"><small>R$</small> {esc(d.get('preco','169,90'))}</div><div class="chips">{chips}</div></div>
<div class="pill">{esc(d.get('cta','Link na bio 👆'))}</div>"""
    return css, body

def story_frase(d):
    css = f"""
body{{background:{NAVY}}}
.brand{{color:{OR};left:50px}}
.box{{left:80px;right:80px;top:200px;height:820px;justify-content:center;gap:40px}}
h1{{font-size:120px;color:#fff}}
p{{font-size:44px;line-height:1.3;color:#cfd8e6}}
.circ{{position:absolute;top:1080px;left:240px;width:600px;height:600px;border-radius:50%;object-fit:{fit_mode(d['foto'])};border:10px solid {OR}}}
.pill{{position:absolute;bottom:110px;left:80px;right:80px;text-align:center;font-size:42px;padding:28px}}"""
    body = f"""<div class="brand">COOLERBAG</div><div class="box">{titulo(d)}<p>{esc(d.get('texto'))}</p></div>
<img class="circ" src="{foto(d['foto'])}"><div class="pill">{esc(d.get('cta','Link na bio 👆'))}</div>"""
    return css, body

# ---------------------------------------------------------------- FEED 1080x1350
def post_oferta(d):
    badges = "".join(f"<div>{esc(c)}</div>" for c in d.get("chips", ["Frete grátis", "Até 12x no cartão"]))
    css = f"""
.ph{{position:absolute;top:0;left:0;width:1080px;height:800px;object-fit:{fit_mode(d['foto'])};object-position:center {d.get('foco','50%')}}}
.panel{{position:absolute;top:800px;left:0;width:1080px;height:550px;background:{NAVY}}}
.brand{{color:#fff;background:rgba(12,31,63,.6);left:50px;top:50px}}
.box.t{{left:80px;right:80px;top:840px;height:190px;justify-content:center}}
h1{{font-size:76px;color:#fff}}
.row{{position:absolute;left:80px;right:80px;top:1040px;height:200px;display:flex;align-items:flex-end;justify-content:space-between;color:#fff}}
.pre{{font-size:32px;color:#cfd8e6;font-weight:600}}
.preco{{font-size:104px;font-weight:900;letter-spacing:-4px;line-height:1}}.preco small{{font-size:46px}}
.badges{{display:flex;flex-direction:column;gap:12px;align-items:flex-end}}
.badges div{{border:3px solid {OR};padding:10px 24px;border-radius:40px;font-size:28px;font-weight:700}}
.foot{{position:absolute;bottom:40px;left:80px;right:80px;display:flex;justify-content:space-between;font-size:30px;font-weight:700;color:#cfd8e6}}"""
    body = f"""<img class="ph" src="{foto(d['foto'])}"><div class="panel"></div><div class="brand">SPORTECH</div>
<div class="box t">{titulo(d)}</div>
<div class="row"><div><div class="pre">{esc(d.get('prefixo','a partir de'))}</div><div class="preco"><small>R$</small> {esc(d.get('preco','169,90'))}</div></div><div class="badges">{badges}</div></div>
<div class="foot"><span>Link na bio</span><span>@sportech</span></div>"""
    return css, body

def post_foto(d):
    css = f"""
.ph{{position:absolute;inset:0;width:1080px;height:1350px;object-fit:{fit_mode(d['foto'])};object-position:center {d.get('foco','40%')}}}
.grad{{position:absolute;bottom:0;left:0;width:1080px;height:800px;background:linear-gradient(transparent,rgba(12,31,63,.95) 55%)}}
.brand{{color:#fff;background:rgba(12,31,63,.6);left:50px;top:50px}}
.box{{left:80px;right:80px;bottom:130px;height:560px;justify-content:flex-end;gap:26px}}
h1{{font-size:96px;color:#fff}}
p{{font-size:38px;line-height:1.3;color:#dfe6f2}}
.foot{{position:absolute;bottom:50px;left:80px;right:80px;display:flex;justify-content:space-between;font-size:30px;font-weight:700;color:#cfd8e6}}"""
    body = f"""<img class="ph" src="{foto(d['foto'])}"><div class="grad"></div><div class="brand">SPORTECH</div>
<div class="box">{titulo(d)}<p>{esc(d.get('texto'))}</p></div>
<div class="foot"><span>Link na bio</span><span>@sportech</span></div>"""
    return css, body

def post_frase(d):
    css = f"""
.brand{{color:{NAVY}}}
.box{{left:80px;right:80px;top:170px;height:560px;justify-content:center;gap:30px}}
h1{{font-size:104px}}
p{{font-size:40px;line-height:1.3;color:#44506a}}
.card{{position:absolute;bottom:60px;right:60px;width:620px;height:540px;border-radius:40px;object-fit:{fit_mode(d['foto'])};box-shadow:0 12px 40px rgba(12,31,63,.15)}}
.foot{{position:absolute;bottom:70px;left:80px;font-size:30px;font-weight:800;display:flex;flex-direction:column;gap:16px}}
.foot .pill{{font-size:32px;padding:20px 36px}}"""
    body = f"""<div class="brand">SPORTECH</div><div class="box">{titulo(d)}<p>{esc(d.get('texto'))}</p></div>
<img class="card" src="{foto(d['foto'])}"><div class="foot"><div class="pill">Link na bio</div><span>@sportech</span></div>"""
    return css, body

# ---------------------------------------------------------------- SLIDES DE CARROSSEL 1080x1350
def capa(d, n, tot):
    css = f"""
.brand{{color:{NAVY};left:50px}}
.num{{background:none;color:#7a8597}}
.ph{{position:absolute;top:150px;left:80px;width:920px;height:740px;object-fit:{fit_mode(d['foto'])};object-position:center {d.get('foco','40%')};border-radius:48px}}
.box{{left:80px;right:80px;top:920px;height:300px;justify-content:center;gap:20px}}
h1{{font-size:86px}}
p{{font-size:36px;color:#44506a;font-weight:500}}
.swipe{{position:absolute;bottom:60px;right:80px;font-size:32px;font-weight:700}}"""
    body = f"""<div class="brand">SPORTECH</div><div class="num">{n}/{tot}</div>
<img class="ph" src="{foto(d['foto'])}"><div class="box">{titulo(d)}<p>{esc(d.get('texto'))}</p></div>
<div class="swipe">Arraste &rarr;</div>"""
    return css, body

def _foto_topo(d, n, tot, marcador):
    css = f"""
.ph{{position:absolute;top:0;left:0;width:1080px;height:840px;object-fit:{fit_mode(d['foto'])};object-position:center {d.get('foco','35%')}}}
.mk{{position:absolute;top:770px;left:80px;z-index:3}}
.mk.tag{{background:{OR};color:#fff;font-size:30px;font-weight:800;padding:14px 28px;border-radius:40px;letter-spacing:2px;top:780px}}
.mk.circ{{width:160px;height:160px;border-radius:50%;background:{OR};color:#fff;font-size:86px;font-weight:900;display:flex;align-items:center;justify-content:center;border:8px solid {CLARO}}}
.box{{left:80px;right:80px;top:950px;height:350px;gap:18px}}
h1{{font-size:80px}}
p{{font-size:38px;line-height:1.3;color:#44506a}}"""
    body = f"""<img class="ph" src="{foto(d['foto'])}"><div class="num">{n}/{tot}</div>{marcador}
<div class="box">{titulo(d)}<p>{esc(d.get('texto'))}</p></div>"""
    return css, body

def foto_tag(d, n, tot):
    return _foto_topo(d, n, tot, f'<div class="mk tag">{esc(d.get("tag",""))}</div>' if d.get("tag") else "")

def foto_numero(d, n, tot):
    return _foto_topo(d, n, tot, f'<div class="mk circ">{esc(d.get("numero", n-1))}</div>')

def tamanhos(d, n, tot):
    css = f"""
.brand{{color:{NAVY};left:50px}}.num{{background:none;color:#7a8597}}
.box{{left:80px;right:80px;top:150px;height:300px;justify-content:center;gap:16px}}
h1{{font-size:88px}}
p{{font-size:36px;color:#44506a}}
.rows{{position:absolute;top:480px;left:80px;width:920px;display:flex;flex-direction:column;gap:28px}}
.r{{display:flex;align-items:center;gap:40px;background:#fff;border-radius:40px;padding:32px 44px;box-shadow:0 6px 24px rgba(12,31,63,.08)}}
.r .l{{background:{OR};color:#fff;font-size:64px;font-weight:900;padding:12px 30px;border-radius:30px;min-width:200px;text-align:center}}
.r .t{{font-size:34px;color:#44506a;flex:1}}.r .t b{{display:block;color:{NAVY};font-size:50px}}
.r .p{{font-size:44px;font-weight:900}}
.note{{position:absolute;bottom:60px;left:80px;right:80px;font-size:26px;color:#7a8597}}"""
    d.setdefault("titulo", "Escolha o"); d.setdefault("destaque", "seu tamanho")
    body = f"""<div class="brand">SPORTECH</div><div class="num">{n}/{tot}</div>
<div class="box">{titulo(d)}<p>{esc(d.get('texto'))}</p></div>
<div class="rows">
 <div class="r"><div class="l">18L</div><div class="t"><b>12 a 15</b>latas</div><div class="p">R$ 169,90</div></div>
 <div class="r"><div class="l">20L</div><div class="t"><b>16 a 18</b>latas</div><div class="p">R$ 174,90</div></div>
 <div class="r"><div class="l">23L</div><div class="t"><b>19 a 22</b>latas</div><div class="p">R$ 179,90</div></div>
</div><div class="note">*Estimativa com latas de 350 ml. Gelo e outros itens ocupam espaço.</div>"""
    return css, body

def texto(d, n, tot):
    escuro = d.get("fundo", "escuro") == "escuro"
    css = f"""
body{{background:{NAVY if escuro else CLARO}}}
.brand{{color:{OR if escuro else NAVY};left:50px}}.num{{background:none;color:{'#9aa6ba' if escuro else '#7a8597'}}}
.box{{left:80px;right:80px;top:170px;bottom:120px;justify-content:center;gap:40px}}
h1{{font-size:104px;color:{'#fff' if escuro else NAVY}}}
p{{font-size:44px;line-height:1.35;color:{'#cfd8e6' if escuro else '#44506a'}}}"""
    body = f"""<div class="brand">SPORTECH</div><div class="num">{n}/{tot}</div><div class="box">{titulo(d)}<p>{esc(d.get('texto'))}</p></div>"""
    return css, body

def cta(d, n, tot):
    chips = "".join(f"<div>{esc(c)}</div>" for c in d.get("chips", ["Frete grátis", "Até 12x", "3% off no PIX", "3 cores"]))
    f = d.get("foto", "tres_cores_praia")
    css = f"""
body{{background:{NAVY}}}
.brand{{color:{OR};left:50px}}.num{{background:none;color:#9aa6ba}}
.ph{{position:absolute;top:150px;left:80px;width:920px;height:580px;object-fit:{fit_mode(f)};border-radius:40px}}
.box{{left:80px;right:80px;top:760px;height:380px;gap:30px}}
h1{{font-size:84px;color:#fff}}
.chips div{{font-size:30px;padding:12px 26px;color:#fff}}
.pill{{position:absolute;bottom:70px;left:80px;font-size:40px;padding:26px 52px}}
.handle{{position:absolute;bottom:95px;right:80px;color:#cfd8e6;font-size:32px;font-weight:700}}"""
    body = f"""<div class="brand">SPORTECH</div><div class="num">{n}/{tot}</div>
<img class="ph" src="{foto(f)}"><div class="box">{titulo(d)}<div class="chips">{chips}</div></div>
<div class="pill">Link na bio</div><div class="handle">@sportech</div>"""
    return css, body

LAYOUTS_STORY = {"story_foto": story_foto, "story_cores": story_cores, "story_oferta": story_oferta, "story_frase": story_frase}
LAYOUTS_POST = {"post_oferta": post_oferta, "post_foto": post_foto, "post_frase": post_frase}
LAYOUTS_SLIDE = {"capa": capa, "foto_tag": foto_tag, "foto_numero": foto_numero, "tamanhos": tamanhos, "texto": texto, "cta": cta}

def main(plano_path):
    plano = json.load(open(plano_path))
    data = plano["data"]
    out_dir = os.path.join(RAIZ, "posts", data); os.makedirs(out_dir, exist_ok=True)
    jobs, manifesto, problemas = [], [], []
    for pub in plano["publicacoes"]:
        tipo, pid = pub["tipo"], pub["id"]
        arquivos = []
        if tipo == "story":
            css, body = LAYOUTS_STORY[pub["layout"]](pub); nome = f"{pid}.png"
            jobs.append((nome, 1080, 1920, css, body)); arquivos.append(nome)
        elif tipo == "post":
            css, body = LAYOUTS_POST[pub["layout"]](pub); nome = f"{pid}.png"
            jobs.append((nome, 1080, 1350, css, body)); arquivos.append(nome)
        elif tipo == "carrossel":
            tot = len(pub["slides"])
            if not 2 <= tot <= 10: raise SystemExit(f"{pid}: carrossel precisa de 2 a 10 slides")
            for i, s in enumerate(pub["slides"], start=1):
                css, body = LAYOUTS_SLIDE[s["layout"]](s, i, tot); nome = f"{pid}_{i}.png"
                jobs.append((nome, 1080, 1350, css, body)); arquivos.append(nome)
        else:
            raise SystemExit(f"Tipo desconhecido: {tipo}")
        manifesto.append({"id": pid, "tipo": tipo, "hora": pub["hora"], "legenda": pub.get("legenda", ""),
                          "media": [f"{URL_BASE}posts/{data}/{a}" for a in arquivos], "arquivos": arquivos})

    with sync_playwright() as p:
        chrome = "/usr/bin/google-chrome" if os.path.exists("/usr/bin/google-chrome") else None
        b = p.chromium.launch(executable_path=chrome) if chrome else p.chromium.launch()
        for nome, w, h, css, body in jobs:
            path = os.path.join(out_dir, nome.replace(".png", ".html"))
            open(path, "w").write(BASE.replace("WW", str(w)).replace("HH", str(h)).replace("CSS", css).replace("BODY", body))
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.goto("file://" + path); pg.wait_for_timeout(500)
            ov = pg.evaluate("window.__overflow")
            if ov: problemas.append(f"{nome}: texto ainda não coube em {ov}")
            pg.screenshot(path=os.path.join(out_dir, nome)); pg.close()
            os.remove(path)
        b.close()

    # prévia para conferência visual
    linhas = []
    for m in manifesto:
        ims = [Image.open(os.path.join(out_dir, a)) for a in m["arquivos"]]
        ims = [i.resize((int(i.width * 480 / i.height), 480)) for i in ims]
        W = sum(i.width for i in ims) + 12 * (len(ims) - 1)
        lin = Image.new("RGB", (W, 480), "white"); x = 0
        for i in ims: lin.paste(i, (x, 0)); x += i.width + 12
        linhas.append(lin)
    W = max(l.width for l in linhas); H = sum(l.height for l in linhas) + 20 * (len(linhas) - 1)
    prev = Image.new("RGB", (W, H), "#dddddd"); y = 0
    for l in linhas: prev.paste(l, (0, y)); y += l.height + 20
    prev.save(os.path.join(out_dir, "previa.png"))

    json.dump(manifesto, open(os.path.join(out_dir, "manifesto.json"), "w"), ensure_ascii=False, indent=2)
    print(f"{len(jobs)} artes em posts/{data}/  |  prévia: posts/{data}/previa.png")
    for pr in problemas: print("ATENÇÃO:", pr)

if __name__ == "__main__":
    main(sys.argv[1])
