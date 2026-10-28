(function(){
  var root = document.body.getAttribute('data-root') || '';
  var CO = window.CLBI_CO || [];
  var icon = '<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="7" cy="7" r="5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M11 11l3.5 3.5" stroke="currentColor" stroke-width="1.6"/></svg>';
  function norm(s){return (s||'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();}
  var idx = CO.map(function(c){return {c:c, k:norm(c[0]+' '+c[1])};});
  function find(q){
    q = norm(q); if(!q) return [];
    var out=[], starts=[], words=[];
    idx.forEach(function(o){
      var n = norm(o.c[1]), s = norm(o.c[0]);
      if(n.indexOf(q)===0 || s.indexOf(q)===0) starts.push(o.c);
      else if(o.k.indexOf(q)>-1) words.push(o.c);
    });
    return starts.concat(words).slice(0,10);
  }
  var uid=0;
  document.querySelectorAll('[data-search]').forEach(function(host){
    uid++;
    var lg = host.hasAttribute('data-lg');
    var ph = host.getAttribute('data-placeholder') || 'Search 500 companies by name or NSE symbol';
    host.innerHTML = '<div class="search'+(lg?' lg':'')+'" role="combobox" aria-haspopup="listbox" aria-owns="srl'+uid+'" aria-expanded="false">'+icon+
      '<input type="search" autocomplete="off" spellcheck="false" aria-autocomplete="list" aria-controls="srl'+uid+'" aria-label="'+ph+'" placeholder="'+ph+'">'+
      '<ul class="sr-list" id="srl'+uid+'" role="listbox" hidden></ul></div>';
    var box = host.firstChild, inp = box.querySelector('input'), ul = box.querySelector('ul'), sel=-1, res=[];
    function render(){
      if(!inp.value.trim()){ul.hidden=true;box.setAttribute('aria-expanded','false');return;}
      res = find(inp.value);
      if(!res.length){ul.innerHTML='<li class="none">No company matches. Try the NSE symbol.</li>';}
      else ul.innerHTML = res.map(function(c,i){
        return '<li role="option" id="o'+uid+'_'+i+'" aria-selected="'+(i===sel)+'"><a href="'+root+'company/'+c[2]+'.html"><span>'+c[1]+'</span><span class="g">'+c[0]+' · '+c[3]+'</span><span class="r">'+c[4]+'</span></a></li>';
      }).join('');
      ul.hidden=false; box.setAttribute('aria-expanded','true');
    }
    inp.addEventListener('input', function(){sel=-1;render();});
    inp.addEventListener('keydown', function(ev){
      if(ev.key==='ArrowDown'){sel=Math.min(sel+1,res.length-1);render();ev.preventDefault();}
      else if(ev.key==='ArrowUp'){sel=Math.max(sel-1,0);render();ev.preventDefault();}
      else if(ev.key==='Enter'){var c=res[sel<0?0:sel]; if(c){location.href=root+'company/'+c[2]+'.html';}}
      else if(ev.key==='Escape'){ul.hidden=true;}
    });
    document.addEventListener('click', function(ev){if(!box.contains(ev.target)) ul.hidden=true;});
  });
  // tabs
  document.querySelectorAll('.tabs').forEach(function(tl){
    var btns = tl.querySelectorAll('.tab');
    btns.forEach(function(b){
      b.addEventListener('click', function(){
        btns.forEach(function(x){x.setAttribute('aria-selected','false'); var p=document.getElementById(x.getAttribute('data-tab')); if(p) p.hidden=true;});
        b.setAttribute('aria-selected','true'); var p=document.getElementById(b.getAttribute('data-tab')); if(p) p.hidden=false;
      });
    });
  });
  // sortable tables
  document.querySelectorAll('table[data-sortable]').forEach(function(t){
    var ths = t.querySelectorAll('th[data-sort]');
    ths.forEach(function(th){
      th.setAttribute('tabindex','0');
      function go(){
        var i = Array.prototype.indexOf.call(th.parentNode.children, th);
        var asc = th.getAttribute('aria-sort')!=='ascending';
        ths.forEach(function(x){x.removeAttribute('aria-sort');});
        th.setAttribute('aria-sort', asc?'ascending':'descending');
        var tb = t.tBodies[0], rows = Array.prototype.slice.call(tb.rows);
        rows.sort(function(a,b){
          var x=a.cells[i], y=b.cells[i];
          var xv=x.getAttribute('data-v'), yv=y.getAttribute('data-v');
          if(xv!==null && yv!==null){xv=parseFloat(xv);yv=parseFloat(yv);return asc?xv-yv:yv-xv;}
          xv=x.textContent.trim().toLowerCase(); yv=y.textContent.trim().toLowerCase();
          return asc?xv.localeCompare(yv):yv.localeCompare(xv);
        });
        rows.forEach(function(r){tb.appendChild(r);});
      }
      th.addEventListener('click', go);
      th.addEventListener('keydown', function(ev){if(ev.key==='Enter'){go();}});
    });
  });
  // company list filter
  var f = document.getElementById('co-filter');
  if(f){
    var g = document.getElementById('co-group'), st = document.getElementById('co-status'), cnt = document.getElementById('co-count');
    var rows = Array.prototype.slice.call(document.querySelectorAll('#co-table tbody tr'));
    function apply(){
      var q = norm(f.value), gv = g.value, sv = st.value, n=0;
      rows.forEach(function(r){
        var ok = (!q || norm(r.getAttribute('data-k')).indexOf(q)>-1) && (!gv || r.getAttribute('data-g')===gv) && (!sv || r.getAttribute('data-s')===sv || (sv==='unranked' && r.getAttribute('data-s')!=='ranked'));
        r.hidden = !ok; if(ok) n++;
      });
      cnt.textContent = n + ' of ' + rows.length + ' companies';
    }
    [f,g,st].forEach(function(x){x.addEventListener('input',apply);x.addEventListener('change',apply);});
    apply();
  }
})();
