(() => {
  const $ = s => document.querySelector(s);
  const papers = [...document.querySelectorAll('.paper')];
  const search = $('#search'), topic = $('#topic-filter'), scope = $('#scope-filter'), priority = $('#priority-filter');
  function filter() {
    if (!search) return;
    const q = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    let count = 0;
    papers.forEach(p => {
      const visible = q.every(w => p.dataset.keywords.includes(w)) && (!topic.value || p.dataset.topic.split(' ').includes(topic.value)) && (!scope.value || p.dataset.scope === scope.value) && (!priority.value || p.dataset.priority === priority.value);
      p.hidden = !visible; if (visible) count++;
    });
    $('#result-count').textContent = `${count} / ${papers.length} 项 · 专题筛选包含交叉标签`;
    $('#empty').style.display = count ? 'none' : 'block';
  }
  function reset() { if (!search) return; [search, topic, scope, priority].forEach(x => x.value = ''); filter(); }
  if (search) {
    [search,topic,scope,priority].forEach(x => x.addEventListener('input',filter));
    $('#reset-filters').addEventListener('click',reset);
    $('#expand-visible').addEventListener('click',()=>{ const visible=papers.filter(x=>!x.hidden); const open=visible.some(x=>!x.open); visible.forEach(x=>x.open=open); $('#expand-visible').textContent=open?'收起当前结果':'展开当前结果'; });
    document.querySelectorAll('[data-topic-jump]').forEach(a=>a.addEventListener('click',()=>{reset();topic.value=a.dataset.topicJump;filter();}));
    filter();
  }
  function followHash() {
    const id = decodeURIComponent(location.hash.slice(1));
    const target = document.getElementById(id);
    if (target?.classList.contains('paper')) { reset(); target.open=true; requestAnimationFrame(()=>target.scrollIntoView({block:'start'})); }
  }
  addEventListener('hashchange',followHash); followHash();
  if (!$('#gauge-svg')) return;
  const ns='http://www.w3.org/2000/svg';
  const points=[[-1,1],[0,2],[2,1],[1,3]], cams=[[-2,-3],[3,-2],[0,-4]];
  function renderGauge(){
    const idx=+$('#gauge-ref').value,angle=+$('#gauge-angle').value*Math.PI/180,s=+$('#gauge-scale').value;
    $('#angle-value').value=`${$('#gauge-angle').value}°`;$('#scale-value').value=s.toFixed(2);
    const origin=idx<0?[0,0]:cams[idx],c=Math.cos(angle),sn=Math.sin(angle);
    const tx=p=>{const x=p[0]-origin[0],z=p[1]-origin[1];return [s*(c*x-sn*z),s*(sn*x+c*z)];};
    const transformed=points.map(tx), tcams=cams.map(tx),svg=$('#gauge-svg');svg.replaceChildren();
    function node(tag,attrs,text){const e=document.createElementNS(ns,tag);Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,v));if(text)e.textContent=text;svg.append(e);return e;}
    function panel(ps,cs,left,title,rotation){
      const all=[...ps,...cs,[0,0]],xs=all.map(p=>p[0]),zs=all.map(p=>p[1]),minx=Math.min(...xs)-1,maxx=Math.max(...xs)+1,minz=Math.min(...zs)-1,maxz=Math.max(...zs)+1;
      const unit=Math.min(355/(maxx-minx),240/(maxz-minz));
      const map=p=>[left+33+(355-(maxx-minx)*unit)/2+(p[0]-minx)*unit,285-(p[1]-minz)*unit];
      node('rect',{x:left+5,y:8,width:432,height:305,rx:8,fill:'#f1f3e9'});
      node('text',{x:left+25,y:34,fill:'#526654','font-size':14},title);
      let a=map([0,minz]),b=map([0,maxz]);node('line',{x1:a[0],y1:a[1],x2:b[0],y2:b[1],stroke:'#cad4c3','stroke-dasharray':'4 4'});
      a=map([minx,0]);b=map([maxx,0]);node('line',{x1:a[0],y1:a[1],x2:b[0],y2:b[1],stroke:'#cad4c3','stroke-dasharray':'4 4'});
      ps.forEach((p,i)=>{const [x,y]=map(p);node('circle',{cx:x,cy:y,r:i===0?7:5,fill:i===0?'#b3793f':'#6f9178'});node('text',{x:x+10,y:y-5,'font-size':12,fill:'#526654'},`P${i+1}`);});
      const focus=map(ps[0]);const ca=map(cs[0]);node('line',{x1:ca[0],y1:ca[1],x2:focus[0],y2:focus[1],stroke:'#bd8b52','stroke-width':1.5,'stroke-dasharray':'4 3'});
      cs.forEach((p,i)=>{const [x,y]=map(p);node('path',{d:`M${x-9},${y+6} L${x+9},${y+6} L${x},${y-10} Z`,fill:'#1d6958',transform:`rotate(${-rotation*180/Math.PI} ${x} ${y})`});node('text',{x:x+13,y:y+14,'font-size':13,fill:'#215344'},String.fromCharCode(65+i));});
    }
    const mobile=innerWidth<650;
    svg.setAttribute('viewBox',mobile?'0 0 445 645':'0 0 900 325');
    panel(points,cams,0,'原始世界坐标',0);
    const firstCount=svg.children.length;
    panel(transformed,tcams,455,'统一相似变换后的坐标',angle);
    if(mobile){const children=[...svg.children].slice(firstCount);const group=document.createElementNS(ns,'g');group.setAttribute('transform','translate(-455 325)');children.forEach(e=>group.append(e));svg.append(group);}
    const px=points[0][0]-cams[0][0],pz=points[0][1]-cams[0][1];
    const dx=transformed[0][0]-tcams[0][0],dz=transformed[0][1]-tcams[0][1];
    const lx=c*dx+sn*dz,lz=-sn*dx+c*dz;
    $('#gauge-result').textContent=`相机 A 观察 P1：原局部坐标 (${px.toFixed(2)}, ${pz.toFixed(2)}) → (${lx.toFixed(2)}, ${lz.toFixed(2)})；归一化像素 x/z：${(px/pz).toFixed(4)} → ${(lx/lz).toFixed(4)}。世界坐标和长度改变，投影保持不变。`;
  }
  ['gauge-ref','gauge-angle','gauge-scale'].forEach(id=>document.getElementById(id).addEventListener('input',renderGauge));addEventListener('resize',renderGauge);renderGauge();
})();
