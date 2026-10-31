(function(){
  var d=document;
  // ---------- theme toggle ----------
  var btn=d.getElementById('themeBtn');
  function apply(t){d.documentElement.setAttribute('data-theme',t);
    if(btn)btn.textContent=t==='dark'?'☀':'🌙';
    try{localStorage.setItem('gc-theme',t)}catch(e){}}
  var saved=null;try{saved=localStorage.getItem('gc-theme')}catch(e){}
  apply(saved||(window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'));
  if(btn)btn.onclick=function(){apply(d.documentElement.getAttribute('data-theme')==='dark'?'light':'dark')};
  // ---------- back to top ----------
  var top=d.getElementById('topBtn');
  if(top){window.onscroll=function(){top.style.display=scrollY>600?'block':'none'};
    top.onclick=function(){scrollTo({top:0,behavior:'smooth'})}}
  // ---------- homepage global search: Enter -> papers.html?q=… ----------
  var gq=d.getElementById('globalQ');
  if(gq)gq.addEventListener('keydown',function(e){
    if(e.key==='Enter'){var v=gq.value.trim();
      location.href='papers.html'+(v?'?q='+encodeURIComponent(v):'');}
  });
  // ---------- paper grid filter/search ----------
  var grid=d.getElementById('paperGrid');
  if(grid){
    var cards=grid.querySelectorAll('.card[data-group]');
    var q=d.getElementById('q');
    function refilter(){
      var f=(d.querySelector('.fbtn.on')||{}).dataset?d.querySelector('.fbtn.on').dataset.g:'*';
      var kw=(q&&q.value||'').toLowerCase();
      cards.forEach(function(c){
        var ok=(f==='*'||c.dataset.group===f)&&(!kw||c.textContent.toLowerCase().indexOf(kw)>=0);
        c.style.display=ok?'':'none';});
    }
    d.querySelectorAll('.fbtn').forEach(function(b){b.onclick=function(){
      d.querySelectorAll('.fbtn').forEach(function(x){x.classList.remove('on')});
      b.classList.add('on');refilter();};});
    if(q)q.oninput=refilter;
    // 从 URL 参数恢复状态(index 搜索框 / 分组卡片跳转)
    try{
      var usp=new URLSearchParams(location.search);
      var qq=usp.get('q'), gg=usp.get('g');
      if(qq)q.value=qq;
      if(gg&&/^[ABC]$/.test(gg)){var b=d.querySelector('.fbtn[data-g="'+gg+'"]');if(b)b.click();}
      if(qq||gg)refilter();
    }catch(e){}
  }
  // ---------- CSV interactive table ----------
  var holder=d.getElementById('csv-data');
  if(holder){
    var cols=[],rows=[];
    try{rows=JSON.parse(holder.textContent)}catch(e){rows=[]}
    if(rows.length){cols=Object.keys(rows[0]);}
    var mount=d.getElementById('csvTable');
    function cell(v){var s=String(v==null?'':v);return s;}
    function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
    function render(filter){
      var kw=(filter||'').toLowerCase();
      var h='<table class="tbl sortable"><thead><tr>';
      cols.forEach(function(c){h+='<th data-c="'+c+'">'+c+' ⇅</th>'});
      h+='</tr></thead><tbody>';
      var shown=0;
      rows.forEach(function(r){
        var line=cols.map(function(c){return cell(r[c])}).join('\u0001');
        if(kw&&line.toLowerCase().indexOf(kw)<0)return;
        shown++;h+='<tr>'+cols.map(function(c){return '<td>'+esc(cell(r[c]))+'</td>'}).join('')+'</tr>';});
      h+='</tbody></table>';
      mount.innerHTML=h;
      d.getElementById('csvCount').textContent='显示 '+shown+' / '+rows.length+' 篇';
      bindSort(mount.querySelector('table'));
    }
    function bindSort(tbl){
      if(!tbl)return;
      var ths=tbl.querySelectorAll('th'),asc=true,last=null;
      ths.forEach(function(th){
        th.onclick=function(){
          var c=th.dataset.c;if(last===c)asc=!asc;else{asc=true;last=c}
          rows.sort(function(a,b){
            var x=String(a[c]),y=String(b[c]);
            var nx=parseFloat(x.replace(/[^\d.\-eE]/g,'')),ny=parseFloat(y.replace(/[^\d.\-eE]/g,''));
            if(!isNaN(nx)&&!isNaN(ny)&&x.match(/[\d]/)&&y.match(/[\d]/))return asc?nx-ny:ny-nx;
            return asc?x.localeCompare(y,'zh'):y.localeCompare(x,'zh');});
          render(d.getElementById('csvQ')?d.getElementById('csvQ').value:'');};});
    }
    var sq=d.getElementById('csvQ');
    if(sq)sq.oninput=function(){render(sq.value)};
    render('');
  }
})();
