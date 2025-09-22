async function setTheme(t){
  const r = await fetch('/set-theme', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({theme:t})});
  const data = await r.json();
  log(data.message); renderState(data.state);
}

async function resetGame(){
  const r = await fetch('/reset', {method:'POST'});
  const data = await r.json();
  log(data.message); renderState(data.state);
}

async function buildLevel(){
  const r = await fetch('/build-level', {method:'POST'});
  const data = await r.json();
  log(data.message); renderState(data.state);
}

async function spawn(kind){
  const r = await fetch('/spawn/'+kind, {method:'POST'});
  const data = await r.json();
  log(data.message); renderState(data.state);
}

function log(msg){
  const el = document.getElementById('log');
  msg = msg + "\n"
  el.textContent = (new Date()).toLocaleTimeString()+": "+msg+ " " + el.textContent;
}

function renderState(state){
  const el = document.getElementById('state');
  el.innerHTML = `
    <div><span class="tag">Tema:</span> <strong>${state.theme}</strong></div>
    <div><span class="tag">Nivel:</span> <strong>${state.level}</strong></div>
    <div><span class="tag">Fondo:</span> ${state.background}</div>
    <div><span class="tag">Enemigos:</span> ${state.enemies.map(e=>e.kind+" ("+e.skin+", hp "+e.hp+")").join(', ') || '—'}</div>
  `;
}

// Estado inicial
(async ()=>{
  const r = await fetch('/state');
  const data = await r.json();
  renderState(data);
})();