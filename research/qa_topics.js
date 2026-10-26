const {chromium}=require('C:/Users/26932/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..'),out=path.join(root,'research/qa/topic-revision');
fs.mkdirSync(out,{recursive:true});
const names=fs.readdirSync(path.join(root,'topics')).filter(x=>x.endsWith('.html')).sort();
const url=name=>'file:///'+path.join(root,'topics',name).replace(/\\/g,'/');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
 const context=await browser.newContext({viewport:{width:1460,height:1050},reducedMotion:'reduce'});
 const page=await context.newPage(),errors=[],external=[],pages=[];
 page.on('pageerror',e=>errors.push(String(e)));
 await context.route(/^https?:/,r=>{external.push(r.request().url());r.abort()});
 for(const name of names){
  const row={name};
  for(const [mode,width,height] of [['desktop',1460,1050],['mobile',390,844]]){
   await page.setViewportSize({width,height});await page.goto(url(name));
   await page.locator('img').evaluateAll(es=>es.forEach(e=>e.loading='eager'));
   await page.evaluate(async()=>await Promise.all([...document.images].map(im=>im.decode().catch(()=>{}))));
   row[mode]=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,brokenImages:[...document.images].filter(x=>x.getAttribute('src')&&!x.naturalWidth).map(x=>x.src),answers:document.querySelectorAll('.topic-answer').length,methodAnswers:document.querySelectorAll('article.method .method-answer').length,methods:document.querySelectorAll('article.method').length,unexpanded:document.body.innerText.includes('{{')}));
   for(const id of ['question',name.startsWith('01')?'methods':'comparison','evidence']){
    await page.locator('#'+id).evaluate(e=>e.scrollIntoView({block:'start'}));
    await page.screenshot({path:path.join(out,name.replace('.html','')+'-'+id+'-'+mode+'.png')});
   }
   const fig=page.locator('#evidence .figure-open').first();
   if(await fig.count()){
    await fig.click();row[mode].lightbox=await page.locator('dialog').evaluate(e=>e.open);
    await page.keyboard.press('Escape');row[mode].escape=await page.locator('dialog').evaluate(e=>!e.open);
   }
   if(mode==='mobile'){
    await page.locator('.mobile-toc summary').click();await page.locator('.mobile-toc a[href="#evidence"]').click();
    row.mobile.tocClosed=await page.locator('.mobile-toc').evaluate(e=>!e.open);
    row.mobile.anchorVisible=await page.locator('#evidence').evaluate(e=>Math.abs(e.getBoundingClientRect().top)<200);
   }
  }
  pages.push(row);
 }
 const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}}),p=await nojs.newPage();
 let jsOff=true;
 for(const name of names){await p.goto(url(name));jsOff&&=await p.locator('.topic-answer').isVisible()&&await p.locator('#evidence .synthesis-table').first().isVisible();}
 const report={pages,errors,external,jsOff};
 fs.writeFileSync(path.join(out,'browser.json'),JSON.stringify(report,null,2));await browser.close();
 const failures=pages.filter(x=>['desktop','mobile'].some(m=>x[m].overflow||x[m].brokenImages.length||x[m].answers!==1||x[m].methods!==x[m].methodAnswers||x[m].unexpanded||x[m].lightbox===false||x[m].escape===false)||!x.mobile.tocClosed||!x.mobile.anchorVisible);
 console.log(JSON.stringify({pages:pages.length,methodCards:pages.reduce((n,x)=>n+x.desktop.methods,0),errors,external,jsOff,failures},null,2));
 if(errors.length||external.length||!jsOff||failures.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
