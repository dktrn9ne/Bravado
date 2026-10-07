import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { composition, validateBrief, CUTS, soundtrack } from '../build.mjs';
const brief=JSON.parse(await readFile(new URL('../brief.json',import.meta.url),'utf8'));
test('input copy cannot inject markup or timeline script',()=>{
  const b=structuredClone(brief);b.scenes[0].headline='<script>alert(1)</script>';
  const html=composition(b);assert.ok(html.includes('&lt;script&gt;'));assert.ok(!html.includes('<script>alert(1)</script>'));
});
test('invalid palette and scene count fail before generation',()=>{
  const b=structuredClone(brief);b.palette.accent='red; }';assert.throws(()=>validateBrief(b),/palette/);
  const c=structuredClone(brief);c.scenes.pop();assert.throws(()=>validateBrief(c),/seven/);
});
test('seven windows cover the full export and sound is deterministic stereo PCM',()=>{
  assert.equal(CUTS[0],0);assert.equal(CUTS.at(-1),31);assert.equal(CUTS.length,8);
  const a=soundtrack();assert.equal(a.readUInt16LE(22),2);assert.equal(a.readUInt32LE(24),48000);assert.equal(a.length,44+31*48000*4);assert.deepEqual(a,soundtrack());
});
