from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

s = s.replace('''   <div class="about">\n    <div class="title">ⓘ Об УФО</div>\n    <div id="aboutTotal">— упоминаний</div>\n    <div id="aboutDyn" class="pos">—</div>\n   </div>\n''', '')

s = s.replace('''   <div class="section">\n    <h3 id="cardsTitle">Ключевые показатели УФО — Депутаты</h3>\n    <div class="cards" id="cards"></div>\n   </div>''', '''   <div class="section">\n    <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:8px">\n     <h3 id="cardsTitle" style="margin:0">Ключевые показатели — Депутаты</h3>\n     <div class="ctrl" style="padding:5px 8px">\n      <label>Регион</label><select id="regionSelect"><option value="">Выберите регион</option></select>\n     </div>\n    </div>\n    <div class="cards" id="cards"></div>\n   </div>''')

old_map = '''   lyr.bindTooltip(`<div style=\\"font-weight:750\\">${r.name}</div><div>${fmt(v)}</div><div style=\\"color:${d===null?'#9db0bf':d>=0?'#35ee81':'#ff8078'}\\">${d===null?'—':pct(d)}</div>`,{sticky:true,direction:'center'});\n   lyr.on('mouseover',e=>{e.target.setStyle({weight:3,color:'#ffffff',fillOpacity:.92});e.target.bringToFront();hoveredRegion=r;renderTrend(r);});\n   lyr.on('mouseout',e=>{e.target.setStyle({weight:1.3,color:'#bfe9ff',fillOpacity:.78});hoveredRegion=null;renderTrend(selectedRegion);});\n   lyr.on('click',e=>{selectedRegion=r;map.fitBounds(e.target.getBounds(),{padding:[55,55],maxZoom:7});renderTrend(r);});'''
new_map = '''   lyr.on('mouseover',e=>{e.target.setStyle({weight:3,color:'#ffffff',fillOpacity:.92});e.target.bringToFront();});\n   lyr.on('mouseout',e=>{e.target.setStyle({weight:1.3,color:'#bfe9ff',fillOpacity:.78});});\n   lyr.on('click',e=>{\n    selectedRegion=r;\n    map.fitBounds(e.target.getBounds(),{padding:[55,55],maxZoom:7});\n    const rs=document.getElementById('regionSelect'); if(rs) rs.value=r.name;\n    render();\n   });'''
if old_map not in s: raise SystemExit('map handler block not found')
s = s.replace(old_map, new_map, 1)

s = s.replace(" document.getElementById('aboutTotal').textContent=fmt(total)+' упоминаний';\n document.getElementById('aboutDyn').textContent=dyn===null?'—':' '+pct(dyn)+' к '+compare.toLowerCase()+' 2026';\n", '')

old_cards_render = ''' document.getElementById('cardsTitle').textContent='Ключевые показатели УФО — '+cat.name;\n document.getElementById('chartTitle').textContent='Динамика упоминаний в УФО — '+cat.name;\n document.getElementById('mapSubtitle').textContent=month==='ALL'?'Апрель — Сентябрь 2026 · объём за весь доступный период':'Объём упоминаний и динамика к '+compare.toLowerCase()+' 2026';\n\n document.getElementById('cards').innerHTML=rows.map(x=>{\n  return `<div class="region-card"><div class="rname">${x.r.name}</div><div class="rval">${fmt(x.v)}</div><div class="rdyn">${x.d===null?'—':pct(x.d)}</div></div>`;\n }).join('');'''
new_cards_render = ''' document.getElementById('chartTitle').textContent='Динамика упоминаний — '+(selectedRegion ? selectedRegion.name+' — ' : 'УФО — ')+cat.name;\n document.getElementById('mapSubtitle').textContent=month==='ALL'?'Апрель — Сентябрь 2026 · объём за весь доступный период':'Объём упоминаний и динамика к '+compare.toLowerCase()+' 2026';\n const cards=document.getElementById('cards');\n const cardsTitle=document.getElementById('cardsTitle');\n if(selectedRegion){\n  cardsTitle.textContent='Ключевые показатели — '+cat.name+' · '+selectedRegion.name;\n  cards.innerHTML=MONTHS.map(m=>`<div class="region-card" style="min-height:78px"><div class="rname">${m} 2026</div><div class="rval">${fmt(value(selectedRegion,activeCat,m))}</div></div>`).join('');\n }else{\n  cardsTitle.textContent='Ключевые показатели — '+cat.name;\n  cards.innerHTML='<div style="grid-column:1/-1;color:#8ea3b5;padding:18px 8px;text-align:center">Выберите регион на карте или в списке выше</div>';\n }'''
if old_cards_render not in s: raise SystemExit('card render block not found')
s = s.replace(old_cards_render, new_cards_render, 1)

anchor = "let activeCat=CATS[0].key;\n"
selector_code = '''let activeCat=CATS[0].key;\n\nconst regionSelect=document.getElementById('regionSelect');\nif(regionSelect){\n regionSelect.innerHTML='<option value="">Выберите регион</option>'+DATA.map(r=>`<option value="${r.name}">${r.name}</option>`).join('');\n regionSelect.addEventListener('change',()=>{\n  selectedRegion=DATA.find(r=>r.name===regionSelect.value)||null;\n  if(selectedRegion) render();\n });\n}\n'''
if anchor not in s: raise SystemExit('activeCat anchor not found')
s = s.replace(anchor, selector_code, 1)

s = s.replace(''' selectedRegion=null; hoveredRegion=null;\n const all=layerGroup.getLayers();''', ''' selectedRegion=null; hoveredRegion=null;\n const rs=document.getElementById('regionSelect'); if(rs) rs.value='';\n const all=layerGroup.getLayers();''', 1)

p.write_text(s, encoding='utf-8')
print('dashboard patched')
