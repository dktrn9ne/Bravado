/** Bravado's seven-scene grammar, exported as editable HyperFrames HTML. */
import { readFile, writeFile, mkdir, copyFile } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
export const CUTS = [0, 3, 7.5, 12, 17.5, 23, 27, 31];
const here = dirname(fileURLToPath(import.meta.url));
const escape = s => s.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#39;');
export function validateBrief(b) {
  const text = (s, field, limit) => {
    if (typeof s !== 'string' || !s.trim() || s.length > limit) throw new Error(`${field}: nonempty text, at most ${limit} characters required`);
  };
  if (!b || typeof b !== 'object') throw new Error('Brief must be an object');
  for (const k of ['source', 'accessed', 'status']) text(b[k], k, 1000);
  text(b.brand, 'brand', 24); text(b.cta, 'cta', 80);
  for (const k of ['background', 'text', 'accent']) if (!/^#[0-9a-f]{6}$/i.test(b.palette?.[k] ?? '')) throw new Error(`palette.${k}: six-digit hex required`);
  if (!Array.isArray(b.scenes) || b.scenes.length !== 7) throw new Error('Exactly seven scenes required');
  b.scenes.forEach((s, i) => {
    text(s.headline, `scenes[${i}].headline`, 32); text(s.detail, `scenes[${i}].detail`, 100);
    if (!Array.isArray(s.labels) || s.labels.length !== 3) throw new Error(`scenes[${i}].labels: three labels required`);
    s.labels.forEach((l, j) => text(l, `scenes[${i}].labels[${j}]`, 24));
  });
  return b;
}
export function composition(b) {
  validateBrief(b);
  const scenes = b.scenes.map((s, i) => `<section id="scene-${i}" class="clip scene" data-start="${CUTS[i]}" data-duration="${CUTS[i+1]-CUTS[i]}" data-track-index="0">
    <div class="content"><p class="eyebrow">${escape(b.brand)} / ${String(i+1).padStart(2,'0')}</p>
    <h1>${escape(s.headline)}</h1><p class="detail">${escape(s.detail)}</p>
    <div class="flow">${s.labels.map((l,j) => `<div class="node"><span class="number">0${j+1}</span><span>${escape(l)}</span></div>`).join('')}</div>
    <p class="footer">${i===6 ? escape(b.cta) : 'A PRODUCT STORY, GROUNDED IN THE WORK.'}</p></div></section>`).join('\n');
  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=1920, height=1080"><title>${escape(b.brand)} — HyperFrames</title>
<script src="assets/gsap.min.js"></script><style>
*{box-sizing:border-box}body{margin:0;color:${b.palette.text};font-family:system-ui,sans-serif}
#root{position:relative;width:100%;height:100%;overflow:hidden;background:${b.palette.background}}
.scene{position:absolute;inset:0}.content{position:absolute;inset:80px 100px}.eyebrow{font-size:28px;letter-spacing:5px;margin:0;color:${b.palette.accent}}
h1{font-size:94px;line-height:1.08;letter-spacing:-4px;margin:72px 0 28px;font-weight:900}.detail{font-size:34px;line-height:1.4;max-width:1600px;margin:0}
.flow{position:absolute;top:510px;left:0;right:0;display:flex;gap:40px}.node{flex:1;min-width:0;border:2px solid ${b.palette.accent};padding:35px 28px;font-size:27px;font-weight:700;display:flex;flex-direction:column;gap:24px;background:${b.palette.background}}
.number{font-size:42px;color:${b.palette.accent}}.footer{position:absolute;bottom:0;left:0;font-size:25px;letter-spacing:2px;margin:0}
</style></head><body><div id="root" data-composition-id="bravado" data-start="0" data-width="1920" data-height="1080" data-duration="31">
${scenes}
<audio id="bravado-score" class="clip" src="assets/sound-design.wav" data-start="0" data-duration="31" data-track-index="1"></audio>
</div><script>
const tl = gsap.timeline({paused:true});
${CUTS.slice(0,-1).map((t,i) => `tl.fromTo('#scene-${i} .content', {opacity:0}, {opacity:1,duration:0.25}, ${t});
tl.fromTo('#scene-${i} h1', {y:55,opacity:0}, {y:0,opacity:1,duration:0.65,ease:'power3.out'}, ${t+0.12});
tl.fromTo('#scene-${i} .detail', {y:24,opacity:0}, {y:0,opacity:1,duration:0.45}, ${t+0.35});
tl.fromTo('#scene-${i} .node', {x:60,opacity:0}, {x:0,opacity:1,duration:0.5,stagger:0.18,ease:'power3.out'}, ${t+0.65});
tl.to('#scene-${i} .number', {y:-8,duration:0.45,stagger:0.18,yoyo:true,repeat:1}, ${t+1.3});`).join('\n')}
window.__timelines['bravado'] = tl;
</script></body></html>`;
}
export function soundtrack() {
  const sr=48000, count=sr*31, wav=Buffer.alloc(44+count*4);
  wav.write('RIFF'); wav.writeUInt32LE(wav.length-8,4); wav.write('WAVEfmt ',8); wav.writeUInt32LE(16,16);
  wav.writeUInt16LE(1,20);wav.writeUInt16LE(2,22);wav.writeUInt32LE(sr,24);wav.writeUInt32LE(sr*4,28);wav.writeUInt16LE(4,32);wav.writeUInt16LE(16,34);wav.write('data',36);wav.writeUInt32LE(count*4,40);
  const hits=CUTS.slice(0,-1).flatMap(t=>[t+0.12,t+0.65,t+0.83,t+1.01]);
  for(let n=0;n<count;n++) {
    const t=n/sr, fade=Math.min(t/0.2,1,(31-t)/0.6);
    let pulse=0;
    for(const hit of hits) {const d=t-hit;if(d>=0&&d<0.3) pulse+=0.12*Math.sin(2*Math.PI*660*d)*(1-Math.exp(-d*150))*Math.exp(-d*18);}
    for(let ch=0;ch<2;ch++) {
      const bed=[110,164.8138,220].reduce((a,f)=>a+0.012*Math.sin(2*Math.PI*f*t+ch*0.12),0);
      wav.writeInt16LE(Math.round((bed+pulse)*fade*32767),44+n*4+ch*2);
    }
  }
  return wav;
}
export async function build(briefPath=resolve(here,'brief.json')) {
  const b=validateBrief(JSON.parse(await readFile(briefPath,'utf8')));
  await mkdir(resolve(here,'assets'),{recursive:true});
  await copyFile(resolve(here,'node_modules/gsap/dist/gsap.min.js'),resolve(here,'assets/gsap.min.js'));
  await writeFile(resolve(here,'assets/sound-design.wav'),soundtrack());
  await writeFile(resolve(here,'index.html'),composition(b));
  await writeFile(resolve(here,'beat-sheet.json'),JSON.stringify({fps:60,duration:31,source:b.source,accessed:b.accessed,status:b.status,scenes:b.scenes.map((s,i)=>({...s,start:CUTS[i],end:CUTS[i+1],startFrame:CUTS[i]*60,endFrame:CUTS[i+1]*60,headlineHit:CUTS[i]+0.12,nodeHits:[0.65,0.83,1.01].map(t=>CUTS[i]+t)}))},null,2));
  console.log('Built index.html, beat-sheet.json and original stereo soundtrack. Inspect and adapt the scene graphics for your product.');
}
if(process.argv[1] && resolve(process.argv[1])===fileURLToPath(import.meta.url)) await build(process.argv[2] ? resolve(process.argv[2]) : undefined);
