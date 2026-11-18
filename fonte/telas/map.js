// Mapa ESQUEMÁTICO de um sítio 100% FICTÍCIO ("Sítio Ilha Azul"). Não representa nenhuma instalação real.
const P=[[90,110],[420,58],[760,78],[930,225],[905,470],[640,585],[285,595],[70,430]];
function mid(a,b,t=.5){return [a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t]}
function inset(p,k){const c=[500,330];return [c[0]+(p[0]-c[0])*k,c[1]+(p[1]-c[1])*k]}
function sensors(){const s=[];P.forEach((a,i)=>{const b=P[(i+1)%P.length];for(let t=.15;t<.9;t+=.233){s.push({z:i+1,p:mid(a,b,t),id:`S${i+1}-${s.filter(x=>x.z==i+1).length+1}`})}});return s}
function drawMap(el,o={}){
  const W=1000,H=650;let g=`<svg viewBox="0 0 ${W} ${H}" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" style="display:block;font-family:Segoe UI,Arial">`;
  g+=`<defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#E4E7EC" stroke-width="1"/></pattern>
  <radialGradient id="pulse"><stop offset="0" stop-color="#C62828" stop-opacity=".45"/><stop offset="1" stop-color="#C62828" stop-opacity="0"/></radialGradient></defs>`;
  g+=`<rect width="${W}" height="${H}" fill="#F7F8FA"/><rect width="${W}" height="${H}" fill="url(#grid)"/>`;
  // lago fictício
  g+=`<path d="M0 470 C60 450 40 560 150 600 C210 625 230 650 230 650 L0 650Z" fill="#DCE8F5"/><text x="12" y="490" font-size="12" fill="#6b88a8" font-style="italic">lago (fictício)</text>`;
  // vegetação
  g+=`<path d="M940 40 C990 60 1000 140 1000 200 L1000 0 L900 0Z" fill="#E3EEDF"/>`;
  // zona controlada (externa)
  g+=`<polygon points="${P.map(p=>p.join(',')).join(' ')}" fill="#FFFFFF" stroke="#7A8494" stroke-width="3"/>`;
  g+=`<polygon points="${P.map(p=>inset(p,.93).join(',')).join(' ')}" fill="none" stroke="#7A8494" stroke-width="1.5" stroke-dasharray="6 5"/>`;
  // zonas
  P.forEach((a,i)=>{const b=P[(i+1)%P.length];const m=mid(a,b);const c=[500,330];const lx=m[0]+(m[0]-c[0])*.09,ly=m[1]+(m[1]-c[1])*.09;
    const off=(o.offlineZones||[]).includes(i+1);const al=o.alarmZone==i+1;
    if(al) g+=`<line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}" stroke="#C62828" stroke-width="7" stroke-linecap="round" opacity=".85"/>`;
    if(off) g+=`<line x1="${a[0]}" y1="${a[1]}" x2="${b[0]}" y2="${b[1]}" stroke="#A86100" stroke-width="7" stroke-linecap="round" stroke-dasharray="10 7" opacity=".8"/>`;
    g+=`<g><rect x="${lx-17}" y="${ly-11}" width="34" height="21" rx="10" fill="${al?'#C62828':off?'#A86100':'#14233A'}"/><text x="${lx}" y="${ly+4}" font-size="12" font-weight="700" fill="#fff" text-anchor="middle">Z${i+1}</text></g>`});
  // edificações genéricas
  const B=[[330,200,130,80,'Edifício A'],[520,170,150,95,'Edifício B'],[360,330,110,95,'Laboratório C'],[540,330,170,120,'Área D'],[230,430,90,60,'Almox.'],[700,230,80,60,'Utilidades']];
  B.forEach(b=>{g+=`<rect x="${b[0]}" y="${b[1]}" width="${b[2]}" height="${b[3]}" fill="#EDEFF3" stroke="#AEB5C0"/><text x="${b[0]+b[2]/2}" y="${b[1]+b[3]/2+4}" font-size="12" fill="#7A8494" text-anchor="middle">${b[4]}</text>`});
  // vias e portaria
  g+=`<path d="M370 650 L372 590 L390 470 L400 455" stroke="#C9CED6" stroke-width="14" fill="none"/>`;
  g+=`<rect x="350" y="578" width="44" height="26" fill="#14233A"/><text x="372" y="595" font-size="10" fill="#fff" text-anchor="middle">Portaria</text>`;
  // central
  g+=`<rect x="250" y="250" width="58" height="40" fill="#E8F0FC" stroke="#1F5FBF"/><text x="279" y="274" font-size="10" fill="#1F5FBF" text-anchor="middle" font-weight="700">CENTRAL</text>`;
  // base drone
  g+=`<g><circle cx="640" cy="520" r="20" fill="#E8F0FC" stroke="#1F5FBF" stroke-width="2"/><text x="640" y="524" font-size="12" font-weight="700" fill="#1F5FBF" text-anchor="middle">H</text><text x="640" y="556" font-size="11" fill="#1F5FBF" text-anchor="middle">Base drones</text></g>`;
  // edge nodes
  if(o.edge!==false)[[200,150],[790,170],[820,420],[250,520]].forEach((e,i)=>{g+=`<g><rect x="${e[0]-9}" y="${e[1]-9}" width="18" height="18" fill="#fff" stroke="#5B3FA6" stroke-width="2" transform="rotate(45 ${e[0]} ${e[1]})"/><text x="${e[0]+14}" y="${e[1]+4}" font-size="10" fill="#5B3FA6">EDGE-0${i+1}</text></g>`});
  // câmeras nos vértices
  if(o.cams!==false)P.forEach((p,i)=>{const c=[500,330];const ang=Math.atan2(c[1]-p[1],c[0]-p[0]);const r=70;
    const a1=ang-.5,a2=ang+.5;const off=(o.offlineCams||[]).includes(i+1);
    g+=`<path d="M${p[0]} ${p[1]} L${p[0]+r*Math.cos(a1)} ${p[1]+r*Math.sin(a1)} A${r} ${r} 0 0 1 ${p[0]+r*Math.cos(a2)} ${p[1]+r*Math.sin(a2)}Z" fill="${off?'#A8610022':'#1F5FBF1c'}" stroke="none"/>`;
    g+=`<rect x="${p[0]-8}" y="${p[1]-8}" width="16" height="16" rx="3" fill="${off?'#A86100':'#1F5FBF'}"/><text x="${p[0]}" y="${p[1]+4}" font-size="9" fill="#fff" text-anchor="middle" font-weight="700">C${i+1}</text>`});
  // sensores
  if(o.sensors!==false)sensors().forEach(s=>{const off=(o.offlineSensors||[]).includes(s.id);g+=`<circle cx="${s.p[0]}" cy="${s.p[1]}" r="4.5" fill="${off?'#A86100':'#2E7D32'}" stroke="#fff" stroke-width="1.5"/>`});
  // alarme
  if(o.alarm){const a=o.alarm;g+=`<circle cx="${a[0]}" cy="${a[1]}" r="46" fill="url(#pulse)"/><circle cx="${a[0]}" cy="${a[1]}" r="11" fill="#C62828" stroke="#fff" stroke-width="3"/><text x="${a[0]-8}" y="${a[1]-20}" font-size="12" font-weight="700" fill="#C62828" text-anchor="end">${o.alarmLabel||'ALARME'}</text>`}
  // drone rota
  if(o.route){const r=o.route;g+=`<path d="M640 520 Q${r.qx||820} ${r.qy||360} ${r.to[0]} ${r.to[1]+18}" fill="none" stroke="#1F5FBF" stroke-width="3" stroke-dasharray="9 6"/>`;
    if(r.at){g+=`<g transform="translate(${r.at[0]},${r.at[1]})"><circle r="15" fill="#1F5FBF"/><path d="M-9 -9 L9 9 M9 -9 L-9 9" stroke="#fff" stroke-width="2.5"/><circle cx="-9" cy="-9" r="3.5" fill="#fff"/><circle cx="9" cy="9" r="3.5" fill="#fff"/><circle cx="9" cy="-9" r="3.5" fill="#fff"/><circle cx="-9" cy="9" r="3.5" fill="#fff"/></g><text x="${r.at[0]+20}" y="${r.at[1]+4}" font-size="12" font-weight="700" fill="#1F5FBF">D1 · ${r.eta||'ETA 0:41'}</text>`}}
  // agentes
  (o.agents||[]).forEach(a=>{g+=`<g><circle cx="${a.p[0]}" cy="${a.p[1]}" r="9" fill="#2E7D32" stroke="#fff" stroke-width="2"/><text x="${a.p[0]+13}" y="${a.p[1]+4}" font-size="11" font-weight="700" fill="#2E7D32">${a.n}</text></g>`;
    if(a.to)g+=`<path d="M${a.p[0]} ${a.p[1]} L${a.to[0]} ${a.to[1]}" stroke="#2E7D32" stroke-width="2.5" stroke-dasharray="4 5"/>`});
  if(o.legend!==false){g+=`<g transform="translate(14,${H-(o.legendH||84)-30})"><rect width="250" height="${o.legendH||84}" rx="6" fill="#ffffffee" stroke="#C9CED6"/>
   <circle cx="16" cy="18" r="5" fill="#2E7D32"/><text x="28" y="22" font-size="11" fill="#4A5568">Sensor de cerca (IoT) – ativo</text>
   <circle cx="16" cy="38" r="5" fill="#A86100"/><text x="28" y="42" font-size="11" fill="#4A5568">Dispositivo sem sinal / falha</text>
   <rect x="10" y="52" width="12" height="12" rx="2" fill="#1F5FBF"/><text x="28" y="62" font-size="11" fill="#4A5568">Câmera com visão computacional</text>
   <rect x="11" y="71" width="9" height="9" fill="#fff" stroke="#5B3FA6" stroke-width="2" transform="rotate(45 15.5 75.5)"/><text x="28" y="80" font-size="11" fill="#4A5568">Nó de edge computing</text></g>`}
  g+=`<text x="${W-12}" y="${H-10}" font-size="11" fill="#9aa3af" text-anchor="end" font-style="italic">Planta esquemática fictícia – sem relação com instalações reais</text>`;
  el.innerHTML=g+`</svg>`;
}
// cena de câmera (térmica estilizada) com bounding box
function camScene(el,o={}){
  const w=640,h=360;let g=`<svg viewBox="0 0 ${w} ${h}" width="100%" height="100%" preserveAspectRatio="xMidYMid slice" style="display:block">
  <defs><linearGradient id="sky${o.k||''}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a424c"/><stop offset="1" stop-color="#555e69"/></linearGradient></defs>
  <rect width="${w}" height="${h}" fill="url(#sky${o.k||''})"/>
  <path d="M0 230 L${w} 200 L${w} ${h} L0 ${h}Z" fill="#454c55"/>
  <path d="M0 90 C120 70 200 110 300 95 C420 80 520 100 640 85 L640 200 L0 230Z" fill="#3d444d"/>`;
  for(let x=0;x<=w;x+=40){const y1=150-x*.045,y2=232-x*.047;g+=`<line x1="${x}" y1="${y1}" x2="${x}" y2="${y2}" stroke="#8b939c" stroke-width="3"/>`}
  for(let k=0;k<6;k++){g+=`<line x1="0" y1="${150+k*16}" x2="${w}" y2="${121+k*16}" stroke="#7b838c" stroke-width="1" opacity=".7"/>`}
  // silhueta
  const sx=o.x||390,sy=o.y||150,s=o.s||1;
  g+=`<g transform="translate(${sx},${sy}) scale(${s})" fill="#f2f2f2"><circle cx="0" cy="0" r="11"/><path d="M-14 14 L14 14 L18 60 L10 60 L8 100 L-2 100 L-1 66 L-4 100 L-14 100 L-12 60 L-19 60Z"/></g>`;
  if(o.box!==false)g+=`<rect x="${sx-30*s}" y="${sy-20*s}" width="${60*s}" height="${128*s}" fill="none" stroke="#FF4D4D" stroke-width="3"/><rect x="${sx-30*s}" y="${sy-20*s-22}" width="${o.lw||118}" height="22" fill="#FF4D4D"/><text x="${sx-30*s+6}" y="${sy-20*s-6}" font-size="14" font-family="Consolas,monospace" fill="#fff" font-weight="700">${o.label||'PESSOA 0.91'}</text>`;
  g+=`</svg>`;el.innerHTML=g;
}
