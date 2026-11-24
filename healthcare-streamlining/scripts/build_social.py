#!/usr/bin/env python3
"""Social graphics for the lean-clinic report (BRAND.md section 12: 4:5, number first, brand glow, cell strip).
Run: python -I -X utf8 scripts/build_social.py  ->  social/render.html and social/out/lean-clinic-*.png (1080 x 1350).
Template and drawing code are reused from healthcare-cost/scripts/build_social.py; figures come from data/model.json and data/worldbank.csv."""
import base64, csv, json, os, struct, subprocess, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(os.path.join(root, "data", "model.json"), encoding="utf-8"))
WB = {(r["country"], r["indicator"], r["year"]): float(r["value"]) for r in csv.DictReader(open(os.path.join(root, "data", "worldbank.csv"), encoding="utf-8"))}
oop_ng, oop_rw = WB[("NGA", "SH.XPD.OOPC.CH.ZS", "2023")], WB[("RWA", "SH.XPD.OOPC.CH.ZS", "2023")]
b = M["base"]; sc = {s["name"]: s for s in M["scenarios"]}
payback = b["payback_months"]; up = sc["Faster service brings 20% more visits"]
rec = M["recurrent_C_excl_rent"]; ep = M["episode"]
tot = {k: ep[k]["consult"] + ep[k]["tests"] + ep[k]["drugs"] + ep[k]["transport"] for k in "AC"}
URL = "consilium.ng/reports/lean-clinic"; TAG = "The lean clinic · 2026"
S = [
    dict(id="post", tag=TAG, fig=str(M["breakeven_visits_per_day"]), cap="Patients a day: where a lean clinic starts to earn more than a paper one.",
         strip=dict(kind="cells", cells=10, fill=10 * M["breakeven_visits_per_day"] / 20), limit="Illustrative model on stated assumptions. 10 cells = 20 patients a day."),
    dict(id="c1", n=1, tag="Who pays", fig=f"{oop_ng:.0f}%", cap=f"of Nigeria's health spending is paid by households out of pocket. Rwanda: {oop_rw:.0f}%.",
         strip=dict(kind="pct", cells=50, fill=round(oop_ng / 2)), limit="World Bank, 2023. Per person, Nigeria spends more than Rwanda."),
    dict(id="c2", n=2, tag="One patient", fig="5¾ h", cap="to treat a child with fever in a traditional clinic. In a lean clinic: about 75 minutes.",
         limit="Illustrative composite. Timings are assumed, not measured."),
    dict(id="c3", n=3, tag="The family's bill", fig=f"₦{tot['A']-tot['C']:,.0f}", cap="less per visit for the family when the tests are done in the room, plus about 4½ hours saved.",
         limit=f"Illustrative: ₦{tot['A']:,.0f} against ₦{tot['C']:,.0f}, transport included."),
    dict(id="c4", n=4, tag="The operator", fig=f"{payback:.0f} months", cap="to pay back the extra set-up cost at 20 patients a day. Below 14 a day, there is no gain.",
         limit="Set-up ₦{:.1f}m against ₦{:.1f}m for a paper clinic.".format(b["C"]["capex"]/1e6, b["A"]["capex"]/1e6)),
    dict(id="c5", n=5, tag="The unproven lever", fig="+20%", cap=f"more patients from faster service would cut payback to about {up['payback']:.0f} months. No Nigerian study has measured it.",
         limit="An upside scenario, not the base case."),
    dict(id="c6", n=6, tag="The ₦100m question", fig=f"₦{rec/1e6:.0f}m", cap=f"a year to run a lean clinic, before rent. It passes a ₦100m build cost in {100e6/rec:.1f} years.",
         limit="Illustrative. A private clinic is not a primary health centre."),
    dict(id="c7", n=7, tag=TAG, kind="cta", head="What keeps a ₦100 million health centre running?", sub="Break-even, risks and next steps for clinic operators and planners.", cta=URL),
]
logo = base64.b64encode(open(os.path.join(root, "..", "assets", "consilium-logo-white.png"), "rb").read()).decode()
HTML = """<!doctype html><html><head><meta charset="utf-8"><title>social</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700&family=Hanken+Grotesk:wght@300;400;600&display=swap" rel="stylesheet">
<style>html,body{margin:0;background:#123184}canvas{display:block}</style></head><body><canvas id="cv" width="1080" height="1350"></canvas>
<script>
var DATA=__DATA__, URLTXT="__URL__", LOGO="data:image/png;base64,__LOGO__";
var C={ink:'#123184',blue:'#3D35EB',lime:'#C8F5A0',sky:'#2CB1F4'}, W=1080, H=1350, PAD=72;
var cv=document.getElementById('cv'), ctx=cv.getContext('2d');
function ls(px){try{ctx.letterSpacing=px+'px'}catch(e){}}
function font(w,s,f){ctx.font=w+' '+Math.round(s)+'px '+(f||"'Hanken Grotesk'")+', system-ui, sans-serif'}
function ell(cx,cy,rx,ry,col,stop,alpha){ctx.save();ctx.translate(cx,cy);ctx.scale(rx,ry);var g=ctx.createRadialGradient(0,0,0,0,0,1);g.addColorStop(0,col);g.addColorStop(stop,col.replace(/[\\d.]+\\)$/,'0)'));g.addColorStop(1,col.replace(/[\\d.]+\\)$/,'0)'));ctx.globalAlpha=alpha;ctx.fillStyle=g;ctx.fillRect(-1,-1,2,2);ctx.restore()}
function glow(){ctx.fillStyle=C.ink;ctx.fillRect(0,0,W,H);ell(.85*W,.05*H,1.2*W,.9*H,'rgba(61,53,235,1)',.6,1);ell(1.0*W,1.0*H,.9*W,.7*H,'rgba(44,177,244,1)',.62,1);ell(.1*W,1.1*H,.6*W,.5*H,'rgba(200,245,160,.55)',.7,1)}
function rr(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.arcTo(x+w,y,x+w,y+h,r);ctx.arcTo(x+w,y+h,x,y+h,r);ctx.arcTo(x,y+h,x,y,r);ctx.arcTo(x,y,x+w,y,r);ctx.closePath()}
function chip(x,y,text,size){font(600,size);ls(size*.14);var tw=ctx.measureText(text.toUpperCase()).width,h=size*2,w=tw+size*1.6;ctx.strokeStyle='rgba(255,255,255,.5)';ctx.lineWidth=2;rr(x+1,y+1,w-2,h-2,h/2);ctx.stroke();ctx.fillStyle='#fff';ctx.textBaseline='middle';ctx.fillText(text.toUpperCase(),x+size*.8,y+h/2+1);ctx.textBaseline='alphabetic';ls(0);return w}
function fit(text,maxW,start,weight,track,face){var s=start;while(s>40){font(weight,s,face);ls(track*s);if(ctx.measureText(text).width<=maxW)break;s-=8}return s}
function wrap(text,maxW){var words=text.split(/\\s+/),lines=[],cur='';words.forEach(function(w){var t=cur?cur+' '+w:w;if(ctx.measureText(t).width>maxW&&cur){lines.push(cur);cur=w}else cur=t});if(cur)lines.push(cur);return lines}
function strip(s){
  var cols=s.cells>30?25:s.cells, rows=s.cells>30?2:1, gap=s.cells===10?12:s.cells===30?4:6, size=(936-(cols-1)*gap)/cols, x0=PAD, y0=s.cells>30?1010:s.cells===30?1020:1000, r=Math.max(4,size*.26);
  for(var i=0;i<s.cells;i++){var cx=x0+(i%cols)*(size+gap),cy=y0+Math.floor(i/cols)*(size+gap),a=Math.max(0,Math.min(1,s.fill-i));
    ctx.fillStyle='rgba(255,255,255,.26)';rr(cx,cy,size,size,r);ctx.fill();
    if(a>0){ctx.fillStyle='rgba(200,245,160,'+(a<1?Math.max(a,.35):1)+')';rr(cx,cy,size,size,r);ctx.fill()}}
  if(s.ring){var k=Math.min(s.cells-1,Math.floor(s.ring)),cx2=x0+(k%cols)*(size+gap)-8,cy2=y0-8;ctx.save();ctx.setLineDash([10,8]);ctx.strokeStyle='rgba(255,255,255,.85)';ctx.lineWidth=3;rr(cx2,cy2,size+16,size+16,r+6);ctx.stroke();ctx.restore();
    font(600,28);ctx.fillStyle='#fff';ctx.textAlign='center';ctx.fillText(s.ringlabel,cx2+(size+16)/2,cy2-14);ctx.textAlign='left'}
}
function draw(d,img){
  glow(); chip(PAD,72,d.tag,22);
  if(d.n){font(600,24);ls(2);ctx.fillStyle='rgba(255,255,255,.72)';ctx.textAlign='right';ctx.fillText(d.n+' / 7',W-PAD,108);ctx.textAlign='left';ls(0)}
  if(d.kind==='cta'){
    font(700,104,"Fraunces, Georgia, serif");ls(-.004*104);ctx.fillStyle='#fff';
    var L=wrap(d.head,936);L.forEach(function(l,i){ctx.fillText(l,PAD,420+i*112)});ls(0);
    font(400,42);ctx.fillStyle='rgba(255,255,255,.92)';wrap(d.sub,860).forEach(function(l,i){ctx.fillText(l,PAD,420+L.length*112+30+i*58)});
    var sz=fit(d.cta,936,150,600,-.02);font(600,sz);ls(-.02*sz);ctx.fillStyle=C.lime;ctx.fillText(d.cta,PAD,1060);ls(0);
  } else {
    var sz=fit(d.fig,936,420,300,-.045);font(300,sz);ls(-.045*sz);ctx.fillStyle=C.lime;ctx.fillText(d.fig,PAD,640);ls(0);
    font(400,46);ctx.fillStyle='rgba(255,255,255,.92)';wrap(d.cap,800).slice(0,3).forEach(function(l,i){ctx.fillText(l,PAD,640+46*1.7+34+i*60)});
    if(d.strip)strip(d.strip);
    if(d.limit){font(400,28);ctx.fillStyle='rgba(255,255,255,.78)';wrap(d.limit,936).slice(0,2).forEach(function(l,i){ctx.fillText(l,PAD,1150+i*38)})}
  }
  var lh=42,w=lh*img.naturalWidth/img.naturalHeight;ctx.drawImage(img,PAD,1240,w,lh);
  font(600,26);ctx.fillStyle='#fff';ctx.textAlign='right';ctx.fillText(URLTXT,W-PAD,1240+lh*.72);ctx.textAlign='left';
}
var id=(location.search.match(/id=([\\w]+)/)||[])[1]||'post', d=DATA.filter(function(x){return x.id===id})[0];
var img=new Image();
Promise.all([document.fonts.load("300 100px 'Hanken Grotesk'"),document.fonts.load("400 40px 'Hanken Grotesk'"),document.fonts.load("600 40px 'Hanken Grotesk'"),document.fonts.load("700 80px Fraunces"),new Promise(function(r){img.onload=r;img.src=LOGO})]).then(function(){draw(d,img);document.title='ready-'+id});
</script></body></html>"""
out = os.path.join(root, "social"); os.makedirs(os.path.join(out, "out"), exist_ok=True)
html = HTML.replace("__DATA__", json.dumps(S, ensure_ascii=False)).replace("__URL__", URL).replace("__LOGO__", logo)
open(os.path.join(out, "render.html"), "w", encoding="utf-8").write(html)
edge = next((p for p in (r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Microsoft\Edge\Application\msedge.exe", r"C:\Program Files\Google\Chrome\Application\chrome.exe") if os.path.exists(p)), None)
if not edge: sys.exit("No Edge or Chrome found: open social/render.html?id=post in a browser instead")
IDS = set(sys.argv[1:])
for s_ in S:
    if IDS and s_["id"] not in IDS: continue
    png = os.path.join(out, "out", f"lean-clinic-{s_['id']}.png")
    subprocess.run([edge, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", "--window-size=1080,1350", "--virtual-time-budget=15000",
                    f"--screenshot={png}", "file:///" + os.path.join(out, "render.html").replace("\\", "/") + f"?id={s_['id']}"], capture_output=True, timeout=120)
    w, h = struct.unpack(">II", open(png, "rb").read(24)[16:24]) if os.path.exists(png) else (0, 0)
    print(s_["id"], f"{w}x{h}", s_["fig"] if "fig" in s_ else "(cta)", "|", s_.get("cap", s_.get("head")))
