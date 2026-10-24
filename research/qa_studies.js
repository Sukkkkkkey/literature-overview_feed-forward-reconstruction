const {chromium}=require('C:/Users/26932/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..'),qa=path.join(root,'research','qa-v2');
fs.mkdirSync(qa,{recursive:true});
const url=f=>'file:///'+path.join(root,f).replace(/\\/g,'/');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const ctx=await browser.newContext({viewport:{width:1460,height:1050},deviceScaleFactor:1});const page=await ctx.newPage();const errors=[],external=[];const report={pages:[],errors,external};
 page.on('pageerror',e=>errors.push(String(e)));await ctx.route(/^https?:/,r=>{external.push(r.request().url());r.abort();});
 const papers=JSON.parse(fs.readFileSync(path.join(root,'papers','registry.json'),'utf8'));
 const files=[...fs.readdirSync(path.join(root,'topics')).filter(f=>f.endsWith('.html')).map(f=>'topics/'+f),...papers.map(p=>p.path),'index.html','review.html'];
 for(const f of files){
  await page.goto(url(f));await page.locator('img').evaluateAll(es=>es.forEach(e=>e.loading='eager'));
  await page.evaluate(async()=>{await Promise.all([...document.images].map(im=>im.complete?Promise.resolve():new Promise(r=>{im.onload=r;im.onerror=r;})));});
  const data={file:f,desktopOverflow:await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),images:await page.locator('img[src]').count(),brokenImages:await page.locator('img[src]').evaluateAll(es=>es.filter(e=>!e.naturalWidth).map(e=>e.src))};
  if(f.startsWith('papers/')){
   data.sections=await page.locator('section').count();data.figures=await page.locator('.figure-plate').count();
   await page.locator('.figure-open').first().click();data.zoomOpens=await page.locator('dialog').evaluate(e=>e.open);await page.keyboard.press('Escape');data.escapeCloses=await page.locator('dialog').evaluate(e=>!e.open);
   const target=papers.find(p=>p.path===f);await page.goto(url(f)+'#discussion');await page.waitForFunction(()=>Math.abs(document.querySelector('#discussion').getBoundingClientRect().top)<200);data.anchorWorks=true;
   await page.goto(url(f));await page.screenshot({path:path.join(qa,target.slug+'-desktop.png')});
  }
  if(f==='topics/01-geometry.html'){
   data.studyTiles=await page.locator('.paper-tile').count();data.studyLinks=await page.locator('.study-links').count();
   await page.screenshot({path:path.join(qa,'chapter-desktop.png')});await page.locator('#paper-studies').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(qa,'chapter-studies-desktop.png')});
   await page.locator('#method-A08').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(qa,'chapter-method-desktop.png')});
   await page.locator('#gauge-scale').evaluate(e=>{e.value='1.5';e.dispatchEvent(new Event('input',{bubbles:true}));});data.gauge=await page.locator('#gauge-result').innerText();
   await page.locator('[data-reading-size]').click();data.fontToggle=await page.locator('body').evaluate(e=>e.classList.contains('large-reading'));
  }
  if(f==='index.html'){
   await page.locator('#search').fill('DA3');data.searchWorks=await page.locator('#paper-A10').evaluate(e=>!e.hidden);
   await page.goto(url(f)+'#paper-A10');data.hashOpens=await page.locator('#paper-A10').evaluate(e=>e.open&&!e.hidden);
  }
  if(f.startsWith('topics/')&&f!=='topics/01-geometry.html'){
   data.methodCards=await page.locator('article.method').count();data.sections=await page.locator('section').count();
   const stem=path.basename(f,'.html');await page.screenshot({path:path.join(qa,stem+'-desktop.png')});
   await page.locator('#comparison').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(qa,stem+'-comparison.png')});
   await page.locator('article.method').first().scrollIntoViewIfNeeded();await page.screenshot({path:path.join(qa,stem+'-method.png')});
  }
  await page.setViewportSize({width:390,height:844});await page.goto(url(f));
  data.mobileOverflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
  if(f.startsWith('topics/')&&f!=='topics/01-geometry.html'){
   await page.screenshot({path:path.join(qa,path.basename(f,'.html')+'-mobile.png')});
   await page.locator('.mobile-toc summary').click();await page.locator('.mobile-toc a[href="#methods"]').click();
   await page.waitForFunction(()=>Math.abs(document.querySelector('#methods').getBoundingClientRect().top)<150);data.mobileTocWorks=await page.locator('.mobile-toc').evaluate(e=>!e.open);
  }
  if(f==='topics/01-geometry.html'){await page.screenshot({path:path.join(qa,'chapter-mobile.png')});await page.locator('#paper-studies').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(qa,'chapter-studies-mobile.png')});await page.locator('.mobile-toc summary').click();await page.locator('.mobile-toc a[href="#gauge"]').click();await page.waitForFunction(()=>Math.abs(document.querySelector('#gauge').getBoundingClientRect().top)<150);data.mobileTocWorks=await page.locator('.mobile-toc').evaluate(e=>!e.open);}
  if(f==='papers/depth-anything-3.html'){
   await page.screenshot({path:path.join(qa,'da3-mobile.png')});await page.locator('#figure-architecture').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(qa,'da3-figure-mobile.png')});
   await page.locator('#figure-architecture .figure-open').click();await page.screenshot({path:path.join(qa,'da3-lightbox-mobile.png')});await page.locator('#dialog-zoom').click();data.originalSizeZoom=await page.locator('.dialog-image-area').evaluate(e=>e.scrollWidth>e.clientWidth&&e.classList.contains('full-resolution'));await page.screenshot({path:path.join(qa,'da3-originalsize-mobile.png')});await page.locator('#dialog-zoom').click();await page.keyboard.press('Escape');
  }
  report.pages.push(data);await page.setViewportSize({width:1460,height:1050});
 }
 await page.goto(url('papers/depth-anything-3.html'));await page.locator('#figure-architecture').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(qa,'da3-figure-desktop.png')});
 await page.locator('#figure-ablation').scrollIntoViewIfNeeded();await page.screenshot({path:path.join(qa,'da3-evidence-desktop.png')});
 await page.locator('#figure-ablation .figure-open').click();await page.screenshot({path:path.join(qa,'da3-lightbox-desktop.png')});await page.keyboard.press('Escape');
 fs.writeFileSync(path.join(qa,'browser-checks.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));await browser.close();
 if(errors.length||external.length||report.pages.some(p=>p.desktopOverflow||p.mobileOverflow||p.brokenImages.length||p.zoomOpens===false||p.escapeCloses===false||p.anchorWorks===false||p.originalSizeZoom===false||p.mobileTocWorks===false))process.exitCode=1;
})();
