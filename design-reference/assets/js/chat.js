/* ICS assistant: demo chat launcher with scripted answers. In the live site this is the 247 AI chatbot trained on ICS content. */
(function(){
  var css='\
.icsbot-btn{position:fixed;right:calc(20px + env(safe-area-inset-right,0px));bottom:calc(20px + env(safe-area-inset-bottom,0px));z-index:65;width:62px;height:62px;border-radius:50%;border:0;cursor:pointer;background:var(--ochre);color:var(--on-accent);display:grid;place-items:center;box-shadow:0 14px 30px -10px rgba(29,23,77,.55);transition:transform .25s ease}\
.icsbot-btn:hover{transform:translateY(-3px) scale(1.04)}\
.icsbot-btn svg{width:28px;height:28px}\
.icsbot-btn::after{content:"";position:absolute;inset:0;border-radius:50%;box-shadow:0 0 0 0 rgba(139,197,63,.55);animation:icsPing 2.6s ease-out 3}\
@keyframes icsPing{to{box-shadow:0 0 0 16px rgba(139,197,63,0)}}\
.icsbot-tip{position:fixed;right:calc(92px + env(safe-area-inset-right,0px));bottom:calc(34px + env(safe-area-inset-bottom,0px));z-index:65;background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:10px;padding:8px 12px;font-size:.88rem;box-shadow:0 10px 24px -14px rgba(29,23,77,.4);max-width:calc(100vw - 120px)}\
.icsbot{position:fixed;right:calc(20px + env(safe-area-inset-right,0px));bottom:calc(94px + env(safe-area-inset-bottom,0px));z-index:66;width:min(370px,calc(100vw - 40px));height:min(520px,calc(100vh - 130px));background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:14px;box-shadow:0 24px 60px -20px rgba(29,23,77,.5);display:flex;flex-direction:column;overflow:hidden}\
.icsbot header{background:var(--band);color:var(--band-fg);padding:14px 16px;display:flex;align-items:center;gap:12px}\
.icsbot header .av{width:36px;height:36px;border-radius:50%;background:var(--ochre);color:var(--on-accent);display:grid;place-items:center;font-family:var(--f-display);font-size:.9rem;flex:none}\
.icsbot header b{display:block;font-weight:600;line-height:1.2}\
.icsbot header small{color:var(--band-soft);font-size:.78rem;display:flex;align-items:center;gap:6px}\
.icsbot header small::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--ochre)}\
.icsbot header button{margin-left:auto;background:none;border:0;color:var(--band-fg);font:inherit;font-size:1.3rem;cursor:pointer;line-height:1}\
.icsbot .log2{flex:1;overflow:auto;padding:16px;display:flex;flex-direction:column;gap:10px;background:var(--paper)}\
.icsbot .m{max-width:85%;padding:10px 12px;border-radius:12px;font-size:.92rem;line-height:1.45}\
.icsbot .m.bot{background:var(--surface);border:1px solid var(--line);border-bottom-left-radius:4px;align-self:flex-start}\
.icsbot .m.me{background:var(--band);color:var(--band-fg);border-bottom-right-radius:4px;align-self:flex-end}\
.icsbot .m a{color:var(--ochre-ink);font-weight:600}\
.icsbot .qs{display:flex;flex-wrap:wrap;gap:6px;padding:10px 12px;border-top:1px solid var(--line);background:var(--surface)}\
.icsbot .qs button{font:inherit;font-size:.8rem;border:1px solid var(--line);background:var(--paper);color:var(--ink);border-radius:999px;padding:6px 10px;cursor:pointer}\
.icsbot .qs button:hover{border-color:var(--ochre)}\
.icsbot form{display:flex;gap:8px;padding:10px 12px;border-top:1px solid var(--line);background:var(--surface)}\
.icsbot form input{flex:1;min-width:0;font:inherit;font-size:.92rem;padding:.6em .7em;border:1px solid var(--line);border-radius:8px;background:var(--paper);color:var(--ink)}\
.icsbot form button{font:inherit;font-weight:600;border:0;border-radius:8px;padding:0 14px;background:var(--ochre);color:var(--on-accent);cursor:pointer}\
.icsbot .dots{display:inline-flex;gap:4px}.icsbot .dots i{width:6px;height:6px;border-radius:50%;background:var(--ink-soft);animation:icsDot 1s infinite}\
.icsbot .dots i:nth-child(2){animation-delay:.15s}.icsbot .dots i:nth-child(3){animation-delay:.3s}\
@keyframes icsDot{50%{opacity:.25;transform:translateY(-2px)}}\
@media (prefers-reduced-motion:reduce){.icsbot-btn::after,.icsbot .dots i{animation:none}}';
  var st=document.createElement('style');st.textContent=css;document.head.appendChild(st);

  var home=document.querySelector('.hero')?'':'./';
  var A={
    cost:'Every retainer is a fixed monthly fee, scoped to the hours or days your business needs. The best place to start is the HR Health Check: you get a written recommendation in about 2 days. <a href="'+home+'#contact" data-jump>Book an HR Health Check</a>',
    check:'It starts with a 5-minute online questionnaire. We then review your contracts, policies and records, and send a written report on what\'s compliant, what\'s exposed and what to fix first, in about 2 days.',
    disc:'Don\'t act before you have advice. We can help you investigate, prepare the notice of allegations and chair the hearing independently. Leave your details and Barbara will call you back today.',
    fractional:'Fractional HR means a senior HR executive works for your business part-time: a few hours a week or a couple of days a month, on a fixed fee. You get the experience of an HR manager without the full-time salary.',
    book:'Great. The form takes about 2 minutes, and we\'ll call you back within one business day. <a href="'+home+'#contact" data-jump>Go to the form</a>',
    other:'Thanks. In the live site, our AI assistant is trained on ICS\'s services and answers here in your words. Anything it can\'t answer goes straight to Barbara, with your details, so nothing gets lost.'
  };
  var Q=[['What does it cost?','cost'],['How does the health check work?','check'],['I have a disciplinary issue','disc'],['What is fractional HR?','fractional'],['Book an HR Health Check','book']];

  var btn=document.createElement('button');btn.className='icsbot-btn';btn.type='button';btn.setAttribute('aria-label','Chat with ICS');btn.setAttribute('aria-expanded','false');
  btn.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20.5l1.4-4.9A8 8 0 1 1 21 12z"/><path d="M8.5 11.5h.01M12 11.5h.01M15.5 11.5h.01"/></svg>';
  var tip=document.createElement('div');tip.className='icsbot-tip';tip.textContent='Questions about HR? Ask us.';
  var panel=document.createElement('section');panel.className='icsbot';panel.hidden=true;panel.setAttribute('aria-label','ICS assistant');
  panel.innerHTML='<header><span class="av" aria-hidden="true">ICS</span><div><b>ICS assistant</b><small>Typically replies instantly</small></div><button type="button" aria-label="Close chat">×</button></header><div class="log2" role="log" aria-live="polite"></div><div class="qs"></div><form><label for="icsbot-in" style="position:absolute;left:-9999px">Type your question</label><input id="icsbot-in" placeholder="Type your question" autocomplete="off"><button type="submit">Send</button></form>';
  document.body.appendChild(panel);document.body.appendChild(tip);document.body.appendChild(btn);
  var log=panel.querySelector('.log2'),qs=panel.querySelector('.qs'),started=false;

  function msg(html,who){var d=document.createElement('div');d.className='m '+who;d.innerHTML=html;log.appendChild(d);log.scrollTop=log.scrollHeight;return d}
  function reply(key){var t=msg('<span class="dots"><i></i><i></i><i></i></span>','bot');setTimeout(function(){t.innerHTML=A[key];log.scrollTop=log.scrollHeight},700)}
  Q.forEach(function(q){var b=document.createElement('button');b.type='button';b.textContent=q[0];b.addEventListener('click',function(){msg(q[0],'me');reply(q[1])});qs.appendChild(b)});
  function open(o){panel.hidden=!o;tip.hidden=true;btn.setAttribute('aria-expanded',o);
    if(o&&!started){started=true;msg('Hi, I\'m the ICS assistant. I can answer questions about outsourced and fractional HR, or help you book an HR Health Check. What can I help with?','bot')}
    if(o)panel.querySelector('input').focus();}
  btn.addEventListener('click',function(){open(panel.hidden)});
  panel.querySelector('header button').addEventListener('click',function(){open(false);btn.focus()});
  tip.addEventListener('click',function(){open(true)});
  setTimeout(function(){tip.hidden=true},9000);
  panel.querySelector('form').addEventListener('submit',function(e){e.preventDefault();var i=panel.querySelector('input'),v=i.value.trim();if(!v)return;
    var safe=v.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]});msg(safe,'me');i.value='';
    var l=v.toLowerCase();reply(/cost|price|fee|how much|rand|\br\d/.test(l)?'cost':/health|check|questionnaire|audit/.test(l)?'check':/disciplin|hearing|ccma|dismiss|warning/.test(l)?'disc':/fraction/.test(l)?'fractional':/book|call|contact/.test(l)?'book':'other')});
  panel.addEventListener('click',function(e){var a=e.target.closest('a[data-jump]');if(!a)return;if(home){try{sessionStorage.setItem('ics-jump','#contact')}catch(err){}}else{open(false)}});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!panel.hidden){open(false);btn.focus()}});
})();
