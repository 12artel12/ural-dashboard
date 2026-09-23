from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Remove the bottom "Об УФО" block; it was explicitly requested as unnecessary.
old_about = '''   <div class="about">\n    <div class="title">ⓘ Об УФО</div>\n    <div id="aboutTotal">— упоминаний</div>\n    <div id="aboutDyn" class="pos">—</div>\n   </div>\n'''
s = s.replace(old_about, '')

# Replace the regional KPI cards area with a selected-region six-month view.
old_cards = '''   <div class="section">\n    <h3 id="cardsTitle">Ключевые показатели УФО — Депутаты</h3>\n    <div class="cards" id="cards"></div>\n   </div>'''
new_cards = '''   <div class="section">\n    <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:8px">\n     <h3 id="cardsTitle" style="margin:0">Ключевые показатели — Депутаты</h3>\n     <div class="ctrl" style="padding:5px 8px">\n      <label>Регион</label><select id="regionSelect"></select>\n     </div>\n    </div>\n    <div class="cards" id="cards"></div>\n   </div>'''
s = s.replace(old_cards, new_cards)

# Make map values click-driven: no sticky tooltip and no chart change on hover.
old_map = '''   lyr.bindTooltip(`<div style=\\"font-weight:750\\">${r.name}</div><div>${fmt(v)}</div><div style=\\"color:${d===null?'#9db0bf':d>=0?'#35ee81':'#ff8078'}\\">${d===null?'—':pct(d)}</div>`,{sticky:true,direction:'center'});\n   lyr.on('mouseover',e=>{e.target.setStyle({weight:3,color:'#ffffff',fillOpacity:.92});e.target.bringToFront();hoveredRegion=r;renderTrend(r);});\n   lyr.on('mouseout',e=>{e.target.setStyle({weight:1.3,color:'#bfe9ff',fillOpacity:.78});hoveredRegion=null;renderTrend(selectedRegion);});\n   lyr.on('click',e=>{selectedRegion=r;map.fitBounds(e.target.getBounds(),{padding:[55,55],maxZoom:7});renderTrend(r);});'''
new_map = '''   lyr.on('mouseover',e=>{e.target.setStyle({weight:3,color:'#ffffff',fillOpacity:.92});e.target.bringToFront();});\n   lyr.on('mouseout',e=>{e.target.setStyle({weight:1.3,color:'#bfe9ff',fillOpacity:.78});});\n   lyr.on('click',e=>{\n    selectedRegion=r;\n    map.fitBounds(e.target.getBounds(),{padding:[55,55],maxZoom:7});\n    const rs=document.getElementById('regionSelect'); if(rs) rs.value=r.name;\n    render();\n   });'''
s = s.replace(old_map, new_map)

# Replace card rendering with six monthly values for the selected region.
marker = "const cat=catMap[activeCat];\n const rows=filtered.map(r=>{"
if marker not in s:
    raise SystemExit('render marker not found')

# Inject selected-region monthly card renderer just before render()'s existing row logic.
injection = '''const cat=catMap[activeCat];\n const selected = selectedRegion || DATA[0];\n const cardsEl=document.getElementById('cards');\n const cardsTitle=document.getElementById('cardsTitle');\n if(cardsEl && selected){\n  cardsTitle.textContent='Ключевые показатели — '+cat.name+' · '+selected.name;\n  cardsEl.innerHTML=MONTHS.map(m=>`<div class="region-card" style="min-height:78px"><div class="rname">${m} 2026</div><div class="rval">${fmt(value(selected,activeCat,m))}</div></div>`).join('');\n }\n const rows=filtered.map(r=>{'''
s = s.replace(marker, injection, 1)

# Add the region selector initialization once after DATA/CATS are available.
anchor = "let activeCat=CATS[0].key;\n"
selector_code = '''let activeCat=CATS[0].key;\n\nconst regionSelect=document.getElementById('regionSelect');\nif(regionSelect){\n regionSelect.innerHTML=DATA.map(r=>`<option value="${r.name}">${r.name}</option>`).join('');\n regionSelect.addEventListener('change',()=>{\n  selectedRegion=DATA.find(r=>r.name===regionSelect.value)||DATA[0];\n  render();\n  const lyr=window.__selectedLayer;\n });\n}\n'''
if anchor in s:
    s=s.replace(anchor, selector_code, 1)
else:
    raise SystemExit('activeCat anchor not found')

# Ensure the selected region starts from the first region and is reflected in the selector.
s = s.replace("let selectedRegion=null;", "let selectedRegion=DATA[0];", 1)

p.write_text(s, encoding='utf-8')
print('dashboard patched')
