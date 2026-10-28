/* =====================================================================
   BATITECH — moteur de mouvement
   - préchargement (1re visite) + rideau de transition entre les pages
   - films « scrubbés » au scroll (séquences d'images dans un canvas)
   - titres découpés, apparitions, bandeau à vitesse variable
   - menu mobile, en-tête intelligent, FAQ, avant/après, formulaire WhatsApp
   ===================================================================== */
(function(){
"use strict";
const C = window.EM_CONFIG || {};
const root = document.documentElement;
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const fine = matchMedia('(pointer: fine)').matches;
const lerp=(a,b,t)=>a+(b-a)*t, clamp=(v,a=0,b=1)=>Math.min(b,Math.max(a,v));
const ss=(a,b,v)=>{const t=clamp((v-a)/(b-a));return t*t*(3-2*t)};
const $=(s,c=document)=>c.querySelector(s), $$=(s,c=document)=>[...c.querySelectorAll(s)];
const store={get(k){try{return sessionStorage.getItem(k)}catch(e){return null}},set(k,v){try{sessionStorage.setItem(k,v)}catch(e){}}};

/* ---------- Coordonnées injectées ---------- */
const waBase = 'https://wa.me/' + (C.whatsappIntl||'');
$$('[data-phone]').forEach(el=>el.textContent=C.phoneDisplay||'');
$$('[data-tel]').forEach(el=>el.setAttribute('href','tel:+'+(C.phoneIntl||'')));
$$('[data-wa]').forEach(el=>{const msg=el.getAttribute('data-wa');el.setAttribute('href',waBase+(msg?'?text='+encodeURIComponent(msg):''));el.setAttribute('target','_blank');el.setAttribute('rel','noopener')});
$$('[data-address]').forEach(el=>el.textContent=C.address||'');
$$('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());
$$('[data-copy]').forEach(btn=>btn.addEventListener('click',()=>{
  const txt=C.phoneDisplay||'';const done=()=>{const o=btn.textContent;btn.textContent='Numéro copié';setTimeout(()=>btn.textContent=o,1600)};
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(txt).then(done,()=>selectText(btn))}else selectText(btn);
}));
function selectText(btn){const t=$('[data-phone]',btn.closest('.c-line')||document);if(!t)return;const r=document.createRange();r.selectNodeContents(t);const s=getSelection();s.removeAllRanges();s.addRange(r)}

/* ---------- Titres découpés ---------- */
function split(el){
  if(el.dataset.splitDone)return;el.dataset.splitDone='1';let i=0;
  const walk=node=>{[...node.childNodes].forEach(n=>{
    if(n.nodeType===3){const parts=n.textContent.split(/(\s+)/);const frag=document.createDocumentFragment();
      parts.forEach(p=>{if(!p)return;if(/^\s+$/.test(p)){frag.appendChild(document.createTextNode(p));return}
        const w=document.createElement('span');w.className='w';const s=document.createElement('span');s.textContent=p;s.style.setProperty('--i',i++);w.appendChild(s);frag.appendChild(w)});
      n.replaceWith(frag)}
    else if(n.nodeType===1)walk(n)})};
  walk(el);
}
const playSplit=el=>{split(el);el.classList.add('split-wait');requestAnimationFrame(()=>requestAnimationFrame(()=>el.classList.remove('split-wait')))};

/* ---------- Apparitions au scroll (uniquement sous la ligne de flottaison) ---------- */
function setupReveals(){
  if(reduce||!('IntersectionObserver' in window))return;
  const io=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;const el=e.target;io.unobserve(el);
    if(el.hasAttribute('data-split'))el.classList.remove('split-wait');else el.classList.remove('pending')}),{rootMargin:'0px 0px -12% 0px'});
  $$('[data-split]:not(.cap [data-split]), .rv, .rv-img').forEach(el=>{
    if(el.getBoundingClientRect().top<innerHeight*.95)return;
    if(el.hasAttribute('data-split')){split(el);el.classList.add('split-wait')}else el.classList.add('pending');
    io.observe(el)});
}

/* ---------- Films : séquence d'images pilotée par le scroll ---------- */
function Film(section){
  const canvas=$('canvas',section),ctx=canvas.getContext('2d');
  const base=section.dataset.seq,count=+section.dataset.count,ext=section.dataset.ext||'webp';
  const focus=+(section.dataset.focus||.5),z=(section.dataset.zoom||'1,1').split(',').map(Number);
  const remap=section.dataset.remap?section.dataset.remap.split(' ').map(s=>s.split(':').map(Number)):null;
  const caps=$$('.cap',section).map(el=>({el,a:+el.dataset.from,b:+el.dataset.to}));
  const tl=$('.tl',section),fill=tl&&$('.fill',tl),labels=tl?$$('span',tl):[],steps=tl?tl.dataset.steps.split(',').map(Number):[];
  const counter=$('[data-counter]',section);
  const imgs=new Array(count);let W=0,H=0,dpr=1,cur=0,target=0,lastDrawn=-1,loaded=0;
  const url=i=>`${base}/${String(i+1).padStart(4,'0')}.${ext}`;
  const resize=()=>{dpr=Math.min(devicePixelRatio||1,2);W=canvas.clientWidth;H=canvas.clientHeight;canvas.width=Math.round(W*dpr);canvas.height=Math.round(H*dpr);lastDrawn=-1};
  new ResizeObserver(resize).observe(canvas);resize();
  const loadOne=i=>new Promise(res=>{const im=new Image();im.decoding='async';im.onload=()=>{imgs[i]=im;loaded++;res()};im.onerror=()=>{loaded++;res()};im.src=url(i)});
  const first=loadOne(0);
  const all=first.then(()=>{const order=[];const step=Math.max(1,Math.floor(count/12));for(let i=step;i<count;i+=step)order.push(i);for(let i=1;i<count;i++)if(!order.includes(i))order.push(i);
    let k=0;const worker=()=>k<order.length?loadOne(order[k++]).then(worker):null;return Promise.all(Array.from({length:6},worker))});
  const pick=i=>{if(imgs[i])return imgs[i];for(let d=1;d<count;d++){if(imgs[i-d])return imgs[i-d];if(imgs[i+d])return imgs[i+d]}return null};
  const mapP=p=>{if(!remap)return p;for(let i=1;i<remap.length;i++){const [a0,b0]=remap[i-1],[a1,b1]=remap[i];if(p<=a1)return lerp(b0,b1,clamp((p-a0)/(a1-a0)))}return p};
  const draw=p=>{const idx=Math.round(clamp(mapP(p))*(count-1));const im=pick(idx);if(!im||!W)return;const key=idx*10+(im===imgs[idx]?1:0)+Math.round(p*1000)*1e4;if(key===lastDrawn)return;lastDrawn=key;
    const iw=im.naturalWidth,ih=im.naturalHeight,zz=lerp(z[0],z[1],p),s=Math.max(W/iw,H/ih)*dpr*zz,dw=iw*s,dh=ih*s;
    const fx=W/H<.85?focus:.5;const ox=clamp(canvas.width/2-dw*fx,canvas.width-dw,0),oy=(canvas.height-dh)/2;
    ctx.drawImage(im,ox,oy,dw,dh)};
  const measure=()=>{const r=section.getBoundingClientRect();target=clamp(-r.top/(r.height-innerHeight));return r.bottom>0&&r.top<innerHeight};
  let capsReady=false;
  function tick(){
    if(!measure())return;
    cur=reduce?target:lerp(cur,target,.12);if(Math.abs(cur-target)<1e-4)cur=target;
    draw(cur);
    if(capsReady)caps.forEach((c,i)=>{const o=ss(c.a,c.a+.05,cur)*(1-ss(c.b-.05,c.b,cur));
      c.el.style.opacity=o.toFixed(3);c.el.style.visibility=o<.01?'hidden':'visible';
      c.el.style.transform=`translateY(${((1-o)*(cur<c.a+.05?28:-28)).toFixed(1)}px)`});
    if(fill)fill.style.transform=`scaleX(${cur.toFixed(4)})`;
    labels.forEach((l,i)=>l.classList.toggle('on',i===0||cur>=steps[i-1]));
    if(counter)counter.textContent=String(Math.round(cur*100)).padStart(2,'0');
  }
  return{tick,first,all,progress:()=>loaded/count,ready(){capsReady=true;const c=caps[0];if(c){c.el.classList.remove('first');const h=$('[data-split]',c.el);if(h)playSplit(h)}}};
}

/* ---------- Bandeau ---------- */
function Band(track){
  track.innerHTML+=track.innerHTML;let x=0;
  return{tick(vel){if(reduce)return;x-=.7+Math.abs(vel)*.4;const half=track.scrollWidth/2;if(-x>half)x+=half;
    track.style.transform=`translateX(${x.toFixed(1)}px) skewX(${clamp(-vel*.25,-10,10).toFixed(2)}deg)`}};
}

/* ---------- En-tête, progression, menu ---------- */
const top=$('.top'),bar=$('.progress'),burger=$('.burger'),menu=$('.menu');
let lastY=scrollY,vel=0;
function headerTick(){
  const y=scrollY,dy=y-lastY;lastY=y;vel=lerp(vel,dy,.15);
  const max=document.documentElement.scrollHeight-innerHeight;if(bar)bar.style.transform=`scaleX(${max>0?(y/max).toFixed(4):0})`;
  if(top&&!menu?.classList.contains('open')){if(y>140&&dy>2)top.classList.add('hide');else if(dy<-2||y<140)top.classList.remove('hide');top.classList.toggle('solid',y>40)}
}
if(burger&&menu){burger.addEventListener('click',()=>{const open=burger.getAttribute('aria-expanded')!=='true';burger.setAttribute('aria-expanded',open);menu.classList.toggle('open',open);root.classList.toggle('lock',open);
  $$('nav a',menu).forEach((a,i)=>a.style.transitionDelay=open?(120+i*60)+'ms':'0ms');if(open)top.classList.remove('hide')});
  addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.classList.contains('open'))burger.click()})}

/* ---------- Boutons magnétiques ---------- */
if(fine&&!reduce)$$('[data-magnetic]').forEach(el=>{
  el.addEventListener('pointermove',e=>{const r=el.getBoundingClientRect();el.style.transform=`translate(${((e.clientX-r.left-r.width/2)*.25).toFixed(1)}px,${((e.clientY-r.top-r.height/2)*.35).toFixed(1)}px)`});
  el.addEventListener('pointerleave',()=>el.style.transform='')});

/* ---------- FAQ : un seul ouvert à la fois ---------- */
$$('.faq details').forEach(d=>d.addEventListener('toggle',()=>{if(d.open)$$('.faq details').forEach(o=>{if(o!==d)o.open=false})}));

/* ---------- Avant / après ---------- */
$$('.ba-frame').forEach(f=>{const r=$('input',f);const set=()=>f.style.setProperty('--x',r.value+'%');r.addEventListener('input',set);set()});

/* ---------- Formulaire -> WhatsApp ---------- */
const form=$('form.cf');
if(form)form.addEventListener('submit',e=>{
  e.preventDefault();const fd=new FormData(form),msg=$('.form-msg',form);
  const nom=(fd.get('nom')||'').trim(),tel=(fd.get('tel')||'').trim(),txt=(fd.get('message')||'').trim();
  if(!nom||!txt){msg.className='form-msg err';msg.textContent='Indiquez au moins votre nom et votre besoin.';return}
  const lines=[`Bonjour ${C.name||''}, je suis ${nom}.`,`Service : ${fd.get('service')||'—'}`,`Urgence : ${fd.get('urgence')||'Non'}`,fd.get('quartier')?`Quartier : ${fd.get('quartier')}`:'',tel?`Mon numéro : ${tel}`:'','',txt].filter((l,i)=>l!==''||i===6);
  const href=waBase+'?text='+encodeURIComponent(lines.join('\n'));
  const a=$('#wa-send');a.href=href;a.hidden=false;a.focus();
  msg.className='form-msg ok';msg.textContent='Message prêt. Ouvrez WhatsApp pour l’envoyer. Si rien ne s’ouvre, appelez le '+(C.phoneDisplay||'')+'.';
});

/* ---------- Transitions entre pages ---------- */
const curtain=$('.curtain');
document.addEventListener('click',e=>{
  const a=e.target.closest('a');if(!a||e.defaultPrevented||e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;
  const href=a.getAttribute('href');if(!href||a.target||a.hasAttribute('download')||/^(#|tel:|mailto:|https?:|\/\/)/.test(href)||!/\.html(#.*)?$/.test(href))return;
  if(reduce||!curtain)return;
  e.preventDefault();store.set('em-nav','1');if(menu?.classList.contains('open'))burger.click();
  curtain.classList.remove('out');curtain.classList.add('in');setTimeout(()=>{location.href=href},560);
});
addEventListener('pageshow',e=>{if(e.persisted&&curtain){curtain.classList.remove('in');curtain.classList.add('out')}});

/* ---------- Démarrage ---------- */
const films=$$('.film[data-seq]').map(Film);
const bands=$$('.band-track').map(Band);
const pageHero=$('.page-hero [data-split]');
const loader=$('.loader'),lf=$('.loader-bar i'),lp=$('.loader-pct');
const isFirst=root.classList.contains('first');

function loop(){films.forEach(f=>f.tick());headerTick();bands.forEach(b=>b.tick(vel));requestAnimationFrame(loop)}

function reveal(){
  store.set('em-seen','1');
  if(root.classList.contains('pt')&&curtain){root.classList.remove('pt');curtain.classList.add('out')}
  if(isFirst&&loader){loader.classList.add('done');setTimeout(()=>root.classList.remove('first'),900)}
  films.forEach(f=>f.ready());
  if(pageHero&&!reduce)playSplit(pageHero);
  setupReveals();
}

(async function boot(){
  requestAnimationFrame(loop);
  if(isFirst&&loader&&!reduce){
    let shown=0;const t0=performance.now();
    const prog=()=>films.length?films.reduce((s,f)=>s+f.progress(),0)/films.length:1;
    await new Promise(res=>{const step=()=>{const p=Math.min(prog(),(performance.now()-t0)/1400);shown=lerp(shown,p,.15);
      lf.style.transform=`scaleX(${shown.toFixed(3)})`;lp.textContent=Math.round(shown*100)+' %';
      if(shown>.985||performance.now()-t0>9000)res();else requestAnimationFrame(step)};step()});
  }else{
    await Promise.race([Promise.all(films.map(f=>f.first)),new Promise(r=>setTimeout(r,1500))]);
  }
  reveal();
})();
})();
