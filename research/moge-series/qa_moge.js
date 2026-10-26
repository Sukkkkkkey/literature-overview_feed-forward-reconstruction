const {chromium}=require('C:/Users/26932/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'../..'),out=path.join(root,'research/qa/moge');fs.mkdirSync(out,{recursive:true});
const url=s=>'file:///'+path.join(root,'papers',s+'.html').replace(/\\/g,'/');
(async()=>{
const b=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
const c=await b.newContext({viewport:{width:1460,height:1050},reducedMotion:'reduce'}),p=await c.newPage();const errors=[],external=[],pages=[];
p.on('pageerror',e=>errors.push(String(e)));await c.route(/^https?:/,r=>{external.push(r.request().url());r.abort()});
for(const slug of ['moge','moge-1','moge-2','moge-3']){
 const row={slug};
 for(const [mode,width,height] of [['desktop',1460,1050],['mobile',390,844]]){
  await p.setViewportSize({width,height});await p.goto(url(slug));await p.locator('img').evaluateAll(es=>es.forEach(e=>e.loading='eager'));
  await p.evaluate(async()=>{await Promise.all([...document.images].map(im=>im.decode().catch(()=>{})))});
  row[mode+'Overflow']=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
  row[mode+'BrokenImages']=await p.locator('img[src]').evaluateAll(es=>es.filter(e=>!e.naturalWidth).map(e=>e.src));
  await p.screenshot({path:path.join(out,slug+'-'+mode+'.png')});
  for(const sec of ['method','experiment']){
   await p.locator('#'+sec).scrollIntoViewIfNeeded();await p.screenshot({path:path.join(out,slug+'-'+sec+'-'+mode+'.png')});
  }
  if(slug!=='moge'){
   await p.locator('.figure-open').first().click();row[mode+'Lightbox']=await p.locator('dialog').evaluate(e=>e.open);await p.locator('#dialog-zoom').click();row[mode+'Zoom']=await p.locator('.dialog-image-area').evaluate(e=>e.classList.contains('full-resolution'));await p.keyboard.press('Escape');row[mode+'Escape']=await p.locator('dialog').evaluate(e=>!e.open);
   await p.locator('[data-reading-size]').click();row[mode+'FontToggle']=await p.locator('body').evaluate(e=>e.classList.contains('large-reading'));
  }
  if(mode==='mobile'){
   await p.locator('.mobile-toc summary').click();await p.locator('.mobile-toc a[href="#discussion"]').click();row.mobileToc=await p.locator('.mobile-toc').evaluate(e=>!e.open);row.mobileAnchor=await p.locator('#discussion').evaluate(e=>Math.abs(e.getBoundingClientRect().top)<200);
  }
 }
 pages.push(row);
}
// Stable section and former figure anchors in the original moge.html URL.
await p.goto(url('moge'));const anchors=['motivation','method','training','experiment','discussion','reading','sources','figure-architecture','figure-ambiguity','figure-experiment'];
const legacy=await p.evaluate(ids=>ids.every(id=>document.getElementById(id)),anchors);
const nojs=await b.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});await nojs.route(/^https?:/,r=>r.abort());const np=await nojs.newPage();let jsOff=true;
for(const slug of ['moge','moge-1','moge-2','moge-3']){await np.goto(url(slug));jsOff&&=await np.locator('#method').isVisible()&&await np.locator('#experiment').isVisible()&&await np.locator('#discussion').isVisible();}
const report={pages,errors,external,legacyAnchors:legacy,jsOff};fs.writeFileSync(path.join(out,'browser.json'),JSON.stringify(report,null,2));await b.close();console.log(JSON.stringify(report,null,2));
if(errors.length||external.length||!legacy||!jsOff||pages.some(x=>x.desktopOverflow||x.mobileOverflow||x.desktopBrokenImages.length||x.mobileBrokenImages.length||!x.mobileAnchor||!x.mobileToc||Object.entries(x).some(([k,v])=>/Lightbox|Zoom|Escape|FontToggle/.test(k)&&!v)))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
