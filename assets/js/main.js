/* =====================================================================
   BATITECH — interactions (v2, sobre)
   - titres qui montent mot par mot (à l'apparition)
   - léger fondu des blocs sous la ligne de flottaison
   - films plein écran pilotés par le scroll (séquences d'images),
     chargées à l'approche de la section
   - menu mobile, FAQ, comparateurs avant/après, formulaire WhatsApp
   ===================================================================== */
(function(){
"use strict";
const C = window.EM_CONFIG || {};
const root = document.documentElement;
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const lerp=(a,b,t)=>a+(b-a)*t, clamp=(v,a=0,b=1)=>Math.min(b,Math.max(a,v));
const $=(s,c=document)=>c.querySelector(s), $$=(s,c=document)=>[...c.querySelectorAll(s)];

/* ---------- Coordonnées injectées ---------- */
const waBase='https://wa.me/'+(C.whatsappIntl||'');
$$('[data-phone]').forEach(el=>el.textContent=C.phoneDisplay||'');
$$('[data-tel]').forEach(el=>el.setAttribute('href','tel:+'+(C.phoneIntl||'')));
$$('[data-wa]').forEach(el=>{const m=el.getAttribute('data-wa');el.setAttribute('href',waBase+(m?'?text='+encodeURIComponent(m):''));el.setAttribute('target','_blank');el.setAttribute('rel','noopener')});
$$('[data-address]').forEach(el=>el.textContent=C.address||'');
$$('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());
$$('[data-copy]').forEach(btn=>btn.addEventListener('click',()=>{
  const txt=C.phoneDisplay||'',label=btn.textContent;
  const done=()=>{btn.textContent='Numéro copié';setTimeout(()=>btn.textContent=label,1600)};
  const fallback=()=>{const t=$('[data-phone]',btn.closest('.c-line')||document);if(!t)return;const r=document.createRange();r.selectNodeContents(t);const s=getSelection();s.removeAllRanges();s.addRange(r)};
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(txt).then(done,fallback);else fallback();
}));

/* ---------- Titres mot par mot ---------- */
function split(el){
  if(el.dataset.splitDone)return;el.dataset.splitDone='1';let i=0;
  const walk=node=>[...node.childNodes].forEach(n=>{
    if(n.nodeType===3){const frag=document.createDocumentFragment();
      n.textContent.split(/(\s+)/).forEach(p=>{if(!p)return;if(/^\s+$/.test(p)){frag.appendChild(document.createTextNode(p));return}
        const w=document.createElement('span');w.className='w';const s=document.createElement('span');s.textContent=p;s.style.setProperty('--i',i++);w.appendChild(s);frag.appendChild(w)});
      n.replaceWith(frag)}
    else if(n.nodeType===1)walk(n)});
  walk(el);
}
function play(el){split(el);el.classList.add('split-wait');requestAnimationFrame(()=>requestAnimationFrame(()=>el.classList.remove('split-wait')))}

if(!reduce&&'IntersectionObserver' in window){
  const io=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;io.unobserve(e.target);
    if(e.target.hasAttribute('data-split'))play(e.target);else e.target.classList.remove('pending')}),{rootMargin:'0px 0px -10% 0px'});
  $$('[data-split]').forEach(el=>{if(el.closest('.cap'))return;split(el);el.classList.add('split-wait');io.observe(el)});
  $$('.rv').forEach(el=>{if(el.getBoundingClientRect().top>innerHeight*.92){el.classList.add('pending');io.observe(el)}});
}

/* ---------- Films plein écran pilotés par le scroll ---------- */
function Film(section){
  const canvas=$('canvas',section),ctx=canvas.getContext('2d');
  const base=section.dataset.seq,count=+section.dataset.count;
  const focus=+(section.dataset.focus||.5),z=(section.dataset.zoom||'1,1').split(',').map(Number);
  const remap=section.dataset.remap?section.dataset.remap.split(' ').map(x=>x.split(':').map(Number)):null;
  const caps=$$('.cap',section).map(el=>({el,a:+el.dataset.from,b:+el.dataset.to,h:$('[data-split]',el),played:false}));
  const tl=$('.tl',section),fill=tl&&$('.fill',tl),labels=tl?$$('span',tl):[],tsteps=tl?tl.dataset.steps.split(',').map(Number):[];
  const counter=$('[data-counter]',section);
  const imgs=new Array(count);let W=0,H=0,dpr=1,cur=0,target=0,last=-1,started=false;
  const url=i=>`${base}/${String(i+1).padStart(4,'0')}.webp`;
  const resize=()=>{dpr=Math.min(devicePixelRatio||1,2);W=canvas.clientWidth;H=canvas.clientHeight;canvas.width=Math.round(W*dpr);canvas.height=Math.round(H*dpr);last=-1};
  new ResizeObserver(resize).observe(canvas);resize();
  const loadOne=i=>new Promise(res=>{const im=new Image();im.decoding='async';im.onload=()=>{imgs[i]=im;last=-1;res()};im.onerror=res;im.src=url(i)});
  loadOne(0);
  function start(){if(started)return;started=true;
    const order=[];const step=Math.max(1,Math.floor(count/12));for(let i=step;i<count;i+=step)order.push(i);for(let i=1;i<count;i++)if(!order.includes(i))order.push(i);
    let k=0;const worker=()=>k<order.length?loadOne(order[k++]).then(worker):null;for(let n=0;n<5;n++)worker()}
  new IntersectionObserver(es=>{if(es.some(e=>e.isIntersecting))start()},{rootMargin:'150% 0px'}).observe(section);
  const pick=i=>{if(imgs[i])return imgs[i];for(let d=1;d<count;d++){if(imgs[i-d])return imgs[i-d];if(imgs[i+d])return imgs[i+d]}return null};
  const mapP=p=>{if(!remap)return p;for(let i=1;i<remap.length;i++){const [a0,b0]=remap[i-1],[a1,b1]=remap[i];if(p<=a1)return lerp(b0,b1,clamp((p-a0)/(a1-a0)))}return p};
  function draw(p){const idx=Math.round(clamp(mapP(p))*(count-1)),im=pick(idx);if(!im||!W)return;
    const key=idx+(im===imgs[idx]?.5:0)+Math.round(p*400)*1000;if(key===last)return;last=key;
    const iw=im.naturalWidth,ih=im.naturalHeight,s=Math.max(W/iw,H/ih)*dpr*lerp(z[0],z[1],p),dw=iw*s,dh=ih*s;
    const ox=clamp(canvas.width/2-dw*(W/H<1.6?focus:.5),canvas.width-dw,0);ctx.drawImage(im,ox,(canvas.height-dh)/2,dw,dh)}
  caps.forEach(c=>{if(c.h&&!reduce){split(c.h);if(c.a>0)c.h.classList.add('split-wait')}});
  return{tick(){
    const r=section.getBoundingClientRect();if(r.bottom<0||r.top>innerHeight)return false;
    target=clamp(-r.top/(r.height-innerHeight));cur=reduce?target:lerp(cur,target,.12);if(Math.abs(cur-target)<1e-4)cur=target;
    draw(cur);
    caps.forEach(c=>{const o=clamp((cur-c.a)/.035)*(1-clamp((cur-(c.b-.035))/.035));
      c.el.style.opacity=o.toFixed(3);c.el.style.visibility=o<.01?'hidden':'visible';c.el.classList.remove('first');
      if(o>.5&&!c.played&&c.h){c.played=true;c.h.classList.remove('split-wait')}
      if(o<.01&&c.played&&c.h&&!reduce&&c.a>0){c.played=false;c.h.classList.add('split-wait')}});
    if(fill)fill.style.transform=`scaleX(${cur.toFixed(4)})`;
    labels.forEach((l,i)=>l.classList.toggle('on',i===0||cur>=tsteps[i-1]));
    if(counter)counter.textContent=String(Math.round(cur*100)).padStart(2,'0');
    return true;
  }};
}
const reels=$$('.film[data-seq]').map(Film);

/* ---------- Menu mobile ---------- */
const burger=$('.burger'),menu=$('.menu');
if(burger&&menu){
  burger.addEventListener('click',()=>{const open=burger.getAttribute('aria-expanded')!=='true';burger.setAttribute('aria-expanded',open);menu.classList.toggle('open',open);root.classList.toggle('lock',open)});
  addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.classList.contains('open'))burger.click()});
  $$('a',menu).forEach(a=>a.addEventListener('click',()=>{if(menu.classList.contains('open'))burger.click()}));
}

/* ---------- WhatsApp flottant : discret sur le pied de page et les séquences (mobile) ---------- */
const wa=$('.wa-float'),foot=$('.foot');let footIn=false;
if(wa&&foot&&'IntersectionObserver' in window)new IntersectionObserver(es=>{footIn=es[0].isIntersecting},{threshold:0}).observe(foot);

/* ---------- FAQ : un seul ouvert ---------- */
$$('.faq details').forEach(d=>d.addEventListener('toggle',()=>{if(d.open)$$('.faq details').forEach(o=>{if(o!==d)o.open=false})}));

/* ---------- Avant / après ---------- */
$$('.ba-frame').forEach(f=>{const r=$('input',f);const set=()=>f.style.setProperty('--x',r.value+'%');r.addEventListener('input',set);set()});

/* ---------- Formulaire -> WhatsApp ---------- */
const form=$('form.cf');
if(form)form.addEventListener('submit',e=>{
  e.preventDefault();const fd=new FormData(form),msg=$('.form-msg',form);
  const nom=(fd.get('nom')||'').trim(),tel=(fd.get('tel')||'').trim(),txt=(fd.get('message')||'').trim();
  if(!nom||!txt){msg.className='form-msg err';msg.textContent='Indiquez au moins votre nom et votre besoin.';return}
  const lines=[`Bonjour ${C.name||''}, je suis ${nom}.`,`Service : ${fd.get('service')||'—'}`,`Urgence : ${fd.get('urgence')||'Non'}`];
  if(fd.get('quartier'))lines.push(`Quartier : ${fd.get('quartier')}`);if(tel)lines.push(`Mon numéro : ${tel}`);lines.push('',txt);
  const a=$('#wa-send');a.href=waBase+'?text='+encodeURIComponent(lines.join('\n'));a.hidden=false;a.focus();
  msg.className='form-msg ok';msg.textContent='Message prêt. Ouvrez WhatsApp pour l’envoyer. Si rien ne s’ouvre, appelez le '+(C.phoneDisplay||'')+'.';
});

/* ---------- Boucle ---------- */
const mobile=matchMedia('(max-width:900px)');
(function loop(){
  let onReel=false;reels.forEach(r=>{if(r.tick())onReel=true});
  if(wa)wa.classList.toggle('off',footIn||onReel);
  requestAnimationFrame(loop);
})();
})();
