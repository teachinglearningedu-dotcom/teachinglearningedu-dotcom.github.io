(() => {
  const search = document.getElementById('search');
  const searchResults = document.getElementById('search-results');
  const browse = document.getElementById('browse-grid');
  let data = [], active = 'all';
  const clean = s => s.toLowerCase().replace(/[-–]/g,' ').replace(/[^a-z0-9\s]/g,' ').replace(/\s+/g,' ').trim();
  const aliases = {mwb:'mini whiteboard',mwbs:'mini whiteboard',cfu:'checking for understanding',tt:'turn and talk',cc:'cold call',send:'special educational needs'};
  function normalise(s) { return clean(s).split(' ').map(t => aliases[t] || t).join(' '); }
  function escape(s) { const el=document.createElement('span');el.textContent=s;return el.innerHTML; }
  function card(r) { return `<a class="card" href="${r.url}"><div class="card-label">${escape(r.kind)}</div><h3>${escape(r.title)}</h3><p>${escape(r.desc)}</p><div class="card-bottom"><span>${escape(r.kind)}</span><span aria-hidden="true">↗</span></div></a>`; }
  function update() {
    if (!search) return;
    const terms=normalise(search.value).split(' ').filter(Boolean);
    const matches=data.map(r => { const title=normalise(r.title),hay=normalise(r.title+' '+r.desc+' '+r.text); return {...r,match:terms.every(t=>hay.includes(t)),score:terms.reduce((n,t)=>n+(title.includes(t)?4:hay.includes(t)?1:0),0)};}).filter(r=>r.match&&(active==='all'||r.category===active)).sort((a,b)=>b.score-a.score);
    if(browse) {
      const matched=new Set(matches.map(r=>r.url));
      browse.querySelectorAll('.card').forEach(el=>el.hidden=!matched.has(el.getAttribute('href')));
      document.getElementById('result-count').textContent=matches.length+' matching '+(matches.length===1?'page':'pages');
      document.getElementById('no-results').hidden=matches.length>0;
      searchResults.replaceChildren();
    } else {
      searchResults.innerHTML=terms.length ? (matches.length?matches.slice(0,12).map(card).join(''):'<p>No matching pages. Try a broader search.</p>') : '';
    }
  }
  if(search) {
    fetch('/assets/search.json').then(r=>{if(!r.ok)throw Error();return r.json();}).then(rows=>{data=rows;update();}).catch(()=>{const p=document.createElement('p');p.textContent='Search is temporarily unavailable. Browse the library using the links below.';searchResults.append(p);});
    search.addEventListener('input',update);
    document.getElementById('clear-search').addEventListener('click',()=>{search.value='';update();search.focus();});
    document.querySelectorAll('[data-filter]').forEach(btn=>btn.addEventListener('click',()=>{active=btn.dataset.filter;document.querySelectorAll('[data-filter]').forEach(el=>{el.classList.toggle('active',el===btn);el.setAttribute('aria-pressed',String(el===btn));});update();}));
  }
  function toast(text){const el=document.createElement('div');el.className='toast';el.setAttribute('role','status');el.textContent=text;document.body.append(el);setTimeout(()=>el.remove(),2800);}
  async function copy(text) {try{await navigator.clipboard.writeText(text);toast('Copied to clipboard');}catch{const el=document.createElement('textarea');el.value=text;el.style.position='fixed';el.style.opacity='0';document.body.append(el);el.select();const ok=document.execCommand('copy');el.remove();toast(ok?'Copied to clipboard':'Please select and copy the text on the page.');}}
  document.querySelectorAll('[data-copy-citation]').forEach(btn=>btn.addEventListener('click',()=>copy(btn.dataset.copyCitation+' — BSCS Teaching & Learning. '+window.location.origin+window.location.pathname+' (converted 12 October 2026).')));
  document.querySelectorAll('[data-copy-instructions]').forEach(btn=>btn.addEventListener('click',async()=>{try{const r=await fetch('/copilot-instructions.txt');if(!r.ok)throw Error();copy(await r.text());}catch{toast('Please copy the instructions from the page.');}}));
})();
