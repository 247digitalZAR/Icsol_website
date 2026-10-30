/* ICS motion layer. Decorative only; the page reads fully without it. */
(function(){
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Header shadow + reading progress */
  var header=document.querySelector('header.site');
  if(header){
    var bar=document.createElement('span');bar.className='progress';bar.setAttribute('aria-hidden','true');header.appendChild(bar);
    var tick=false;
    function onScroll(){
      if(tick)return;tick=true;
      requestAnimationFrame(function(){
        var y=window.scrollY,max=document.documentElement.scrollHeight-innerHeight;
        header.classList.toggle('scrolled',y>8);
        bar.style.transform='scaleX('+(max>0?Math.min(1,y/max):0)+')';
        scrub();tick=false;
      });
    }
    addEventListener('scroll',onScroll,{passive:true});addEventListener('resize',onScroll);
  }

  /* Split headline into words */
  function splitWords(el,cls){
    var words=el.textContent.trim().split(/\s+/);
    el.setAttribute('aria-label',el.textContent.trim());
    el.innerHTML=words.map(function(w,i){return '<span class="'+cls+'" aria-hidden="true" style="--i:'+i+'">'+w+'</span>'}).join(' ');
    return el.querySelectorAll('.'+cls);
  }
  if(!reduce){document.querySelectorAll('[data-split]').forEach(function(el){splitWords(el,'split-w')})}

  /* Scroll-scrubbed statement */
  var scrubWords=[];
  if(!reduce){document.querySelectorAll('[data-scrub]').forEach(function(el){scrubWords.push({el:el,w:splitWords(el,'scrub-w')})})}
  function scrub(){
    scrubWords.forEach(function(s){
      var r=s.el.getBoundingClientRect(),start=innerHeight*.9,end=innerHeight*.35;
      var p=Math.max(0,Math.min(1,(start-r.top)/(start-end)));
      var n=s.w.length;
      s.w.forEach(function(w,i){var t=Math.max(0,Math.min(1,p*n-i));w.style.opacity=(.18+.82*t).toFixed(3)});
    });
  }
  scrub();

  /* Scroll reveal, staggered within each group */
  var sel=['.band .eyebrow','.band h2','.band .lede','.why li','.ai-line','.weekcard','.log li','.compare tbody tr','.tool',
    '.svc article','.steps li','.steps-cta','.quote','.person','.chips span','.post','.magnet','details','.contact .addr > div','form.check',
    '.feature','.card','.filters'].join(',');
  if(!reduce&&'IntersectionObserver' in window){
    var els=[].slice.call(document.querySelectorAll(sel)).filter(function(el){return !el.hasAttribute('data-scrub')&&!el.closest('.hero')&&!el.closest('.ins-hero')&&!el.closest('[hidden]')});
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(!e.isIntersecting)return;
        var el=e.target;el.classList.add('rv-in');el.classList.remove('rv-wait');io.unobserve(el);
        setTimeout(function(){el.classList.remove('rv-in');el.style.removeProperty('--d')},1600);
      });
    },{rootMargin:'0px 0px -8% 0px',threshold:.08});
    els.forEach(function(el){
      if(el.getBoundingClientRect().top<innerHeight*.92)return; // already on screen: leave it alone
      var sib=el.parentElement?[].slice.call(el.parentElement.children).filter(function(c){return c.matches(sel)}):[el];
      var idx=Math.max(0,sib.indexOf(el));
      el.style.setProperty('--d',Math.min(idx,6)*90+'ms');
      el.classList.add('rv-wait');io.observe(el);
    });
  }

  /* Week card: mark today's row (Mon to Fri) */
  var days=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'],today=days[new Date().getDay()];
  document.querySelectorAll('.log li').forEach(function(li){var t=li.querySelector('time');if(t&&t.textContent.trim()===today)li.classList.add('now')});

  /* Headcount tool: animate the result on change */
  var range=document.getElementById('headcount'),res=document.querySelector('.result'),last='';
  if(range&&res&&!reduce){
    range.addEventListener('input',function(){
      var t=document.getElementById('r-title').textContent;
      if(t!==last){last=t;res.classList.remove('bump');void res.offsetWidth;res.classList.add('bump')}
    });
    last=document.getElementById('r-title').textContent;
  }
})();
