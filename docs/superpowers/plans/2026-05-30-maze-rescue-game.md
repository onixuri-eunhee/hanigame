# 미로 구출 게임 (maze.html) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 손가락으로 미로를 그려 갇힌 영웅(소방관·경찰관·의사)을 구출하는 단일 HTML 캔버스 게임을 만들고 허브에 등록한다. 갈림길마다 영어 단어 힌트, 도착 시 영어 문장 따라말하기.

**Architecture:** 독립 `maze.html` 파일 하나. 순수 로직(시드 RNG·미로생성·해답경로·분기탐지)을 먼저 만들고 `window.__maze`로 노출해 테스트, 그 위에 DPR 대응 캔버스 렌더(정적 미로는 오프스크린 캐시 1회)·터치 입력(리시+갈림길 커밋 이동)·영어 힌트(TTS)·화면 흐름(미로→도착카드→축하)을 얹는다. 기존 게임(balloon.html)의 TTS·iOS unlock·헤더·CSS 관례 재사용.

**Tech Stack:** Vanilla HTML/CSS/JS, Canvas 2D, requestAnimationFrame, Web Speech API(speechSynthesis). 테스트: node + Playwright(헤드리스), 로컬 `python3 -m http.server`.

설계 근거: `docs/superpowers/specs/2026-05-30-maze-rescue-game-design.md` (v2).

---

## 테스트 환경 (모든 Task 공통)

이 저장소엔 테스트 프레임워크가 없다. 테스트는 **node + Playwright 스크립트**로 한다.
Playwright 모듈은 gstack 것을 절대경로로 import한다.

**로컬 서버 한 번 띄워두기** (Task 시작 전):
```bash
cd /Users/eunhuismacbook/Desktop/hanigame
lsof -ti:8765 >/dev/null 2>&1 || (python3 -m http.server 8765 >/dev/null 2>&1 &)
```

**공용 테스트 헬퍼** — 파일 생성 `/Users/eunhuismacbook/Desktop/hanigame/.maze_test_lib.mjs`:
```js
import pw from '/Users/eunhuismacbook/.claude/skills/gstack/node_modules/playwright/index.js';
const { chromium } = pw;

export async function launch() {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({
    viewport: { width: 820, height: 1100 }, deviceScaleFactor: 2,
    isMobile: true, hasTouch: true,
    userAgent: 'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
  });
  const page = await ctx.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error' && !/favicon/.test(m.text())) errors.push(m.text()); });
  page.on('pageerror', e => errors.push('PAGEERR: ' + e.message));
  await page.goto('http://localhost:8765/maze.html', { waitUntil: 'load' });
  return { browser, page, errors, close: () => browser.close() };
}
```

각 Task의 테스트 파일은 `.maze_t<N>.mjs`로 만들고, **확인 후 삭제**(저장소에 안 남김).
`.maze_test_lib.mjs`와 `.maze_t*.mjs`는 `.gitignore`에 추가(아래 Task 0).

---

## File Structure

- **Create** `maze.html` — 게임 전체(단일 파일). 내부 논리 영역:
  - 시드 RNG `mulberry32`, `genMaze(n, seed)`, `pruneDeadEnds`, `solvePath`, `forksOnPath`
  - 렌더 `sizeCanvas`, `buildMazeCache`, `drawFrame`(trail·hero·goal·signposts·onboarding)
  - 입력/이동 `setFinger`, `tickMove`
  - 영어 힌트 `placeSignposts`, `speak`, 보상
  - 화면 흐름 `startLevel`, `onArrive`, `showArrival`, `nextLevel`, `showCelebration`
  - 테스트 훅 `window.__maze`
- **Modify** `index.html` — 허브에 미로 카드 1개 추가.
- **Modify** `.gitignore` — 테스트 임시파일 제외.

데이터(영웅 3종)는 `maze.html` 내부 상수. speech.html 대사 재활용.

---

### Task 0: 스캐폴드 — maze.html 셸 + 허브 카드 + gitignore

게임 뼈대(헤더·캔버스·화면 div·TTS·iOS unlock)만. 로직 없음.

**Files:**
- Create: `/Users/eunhuismacbook/Desktop/hanigame/maze.html`
- Modify: `/Users/eunhuismacbook/Desktop/hanigame/index.html` (카드 1개 추가)
- Modify: `/Users/eunhuismacbook/Desktop/hanigame/.gitignore`
- Create: `/Users/eunhuismacbook/Desktop/hanigame/.maze_test_lib.mjs` (위 헬퍼)

- [ ] **Step 1: `.gitignore`에 테스트 임시파일 제외 추가**

`/Users/eunhuismacbook/Desktop/hanigame/.gitignore` 끝에 추가:
```
# maze test scratch
.maze_test_lib.mjs
.maze_t*.mjs
```

- [ ] **Step 2: `maze.html` 셸 작성**

`/Users/eunhuismacbook/Desktop/hanigame/maze.html` 생성:
```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>🌀 미로 구출</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    height: 100vh; height: 100dvh; overflow: hidden;
    background: #0E1117; color: #fff;
    font-family: 'Arial Rounded MT Bold', Arial, sans-serif;
    display: flex; flex-direction: column; touch-action: none;
  }
  #header {
    flex-shrink: 0; display: flex; align-items: center; justify-content: space-between;
    padding: 8px 14px; background: rgba(255,255,255,0.06);
    border-bottom: 1px solid rgba(255,255,255,0.1);
  }
  #header a { font-size: 13px; color: #ccc; text-decoration: none;
    border: 1.5px solid #555; border-radius: 12px; padding: 3px 10px; }
  #level-disp { font-size: 16px; font-weight: 900; color: #FF7A5A; }
  #hint-btn { font-size: 20px; background: rgba(255,255,255,0.1);
    border: none; border-radius: 50%; width: 40px; height: 40px; color: #fff; }
  #maze-wrap { flex: 1; position: relative; display: flex;
    align-items: center; justify-content: center; }
  #maze-canvas { display: block; touch-action: none; }
  .screen { position: absolute; inset: 0; display: none;
    flex-direction: column; align-items: center; justify-content: center;
    background: rgba(8,10,15,0.92); text-align: center; padding: 24px; gap: 14px; }
  .screen.show { display: flex; }
  .big-en { font-size: 30px; font-weight: 900; }
  .ko { font-size: 18px; color: #bbb; }
  .pill { font-size: 18px; font-weight: 900; border: none; border-radius: 50px;
    padding: 12px 28px; color: #fff; }
  #ar-next { background: #FF7A5A; }
  #ar-replay { background: rgba(255,255,255,0.14); }
  .icon-btn { font-size: 22px; background: rgba(255,255,255,0.12);
    border: none; border-radius: 50%; width: 48px; height: 48px; color: #fff; }
</style>
</head>
<body>
  <div id="header">
    <a href="index.html">← 홈</a>
    <span id="level-disp">단계 1 / 3</span>
    <button id="hint-btn" aria-label="다시 듣기">🔊</button>
  </div>
  <div id="maze-wrap">
    <canvas id="maze-canvas"></canvas>
    <!-- 도착 카드 -->
    <div class="screen" id="arrival">
      <div id="ar-hero" style="font-size:64px">🚒</div>
      <div class="big-en" id="ar-en">Firefighters are brave.</div>
      <div class="ko" id="ar-ko">소방관은 용감해요</div>
      <button class="icon-btn" id="ar-say">🔊</button>
      <button class="pill" id="ar-next">다음 ▶</button>
    </div>
    <!-- 축하 -->
    <div class="screen" id="celebration">
      <div style="font-size:64px">🎉</div>
      <div class="big-en">All heroes rescued!</div>
      <div class="ko">모든 영웅을 구했어요!</div>
      <button class="pill" id="ar-replay">다시 하기 🔁</button>
    </div>
  </div>

<script>
// ── iOS AUDIO/SPEECH UNLOCK (balloon.html 패턴 재사용) ──
let audioUnlocked = false, pendingSpeak = null;
function _unlockAudio() {
  try {
    const AC = window.AudioContext || window.webkitAudioContext;
    if (AC) { const ctx = new AC(); const b = ctx.createBuffer(1,1,ctx.sampleRate);
      const s = ctx.createBufferSource(); s.buffer = b; s.connect(ctx.destination); s.start(0); ctx.resume(); }
    audioUnlocked = true;
    document.removeEventListener('touchstart', _unlockAudio);
    document.removeEventListener('touchend', _unlockAudio);
    document.removeEventListener('click', _unlockAudio);
    if (window.speechSynthesis) speechSynthesis.speak(new SpeechSynthesisUtterance(''));
    if (pendingSpeak) { const w = pendingSpeak; pendingSpeak = null; speak(w); }
  } catch(e) {}
}
document.addEventListener('touchstart', _unlockAudio, { passive: true });
document.addEventListener('touchend', _unlockAudio, { passive: true });
document.addEventListener('click', _unlockAudio);

// ── TTS ──
if (window.speechSynthesis) speechSynthesis.getVoices();
function speak(text) {
  if (!window.speechSynthesis) return;
  if (!audioUnlocked) { pendingSpeak = text; return; }
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = 'en-US'; u.rate = 0.8; u.pitch = 1.15;
  const vs = speechSynthesis.getVoices();
  const best = vs.find(v => v.name === 'Samantha') || vs.find(v => v.lang === 'en-US' && v.localService);
  if (best) u.voice = best;
  speechSynthesis.speak(u);
}

// ── 영웅 데이터 (speech.html 대사 재활용) ──
const HEROES = [
  { name:'소방관', emoji:'🧑‍🚒', goal:'🚒', word:'fire truck', color:'#FF5722',
    en:'Firefighters are brave.', ko:'소방관은 용감해요', n:9 },
  { name:'경찰관', emoji:'👮', goal:'🚓', word:'police car', color:'#1565C0',
    en:'Police officers are strong.', ko:'경찰관은 강해요', n:11 },
  { name:'의사', emoji:'👨‍⚕️', goal:'🚑', word:'ambulance', color:'#2E7D32',
    en:'Doctors are kind.', ko:'의사는 친절해요', n:13 },
];
const canvas = document.getElementById('maze-canvas');
const ctx = canvas.getContext('2d');

// 이후 Task에서 로직 추가. 테스트 훅:
window.__maze = {};
</script>
</body>
</html>
```

- [ ] **Step 3: 허브 카드 추가 — `index.html`**

`index.html`에서 마지막 카드(`<a class="card full" href="tetris.html">...</a>`) 바로 다음, `</div>`(카드 컨테이너 닫힘) 앞에 추가:
```html
  <a class="card full" href="maze.html">
    <div style="width:120px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:52px;background:rgba(0,0,0,0.15);">🌀</div>
    <div class="card-body">
      <div class="card-name">🌀 미로 구출 <span class="badge-new">NEW</span></div>
      <div class="card-desc">영어 듣고 길 찾아<br>영웅 구출!</div>
    </div>
  </a>
```
(정확한 삽입 위치: `index.html`의 tetris 카드 `</a>` 다음 줄. 카드 컨테이너 `</div>`는 `index.html:322` 근처.)

- [ ] **Step 4: 로드 스모크 테스트** — `.maze_t0.mjs`:
```js
import { launch } from './.maze_test_lib.mjs';
const { page, errors, close } = await launch();
const r = await page.evaluate(() => ({
  hasCanvas: !!document.getElementById('maze-canvas'),
  hasSpeak: typeof speak === 'function',
  heroes: typeof HEROES !== 'undefined' && HEROES.length,
  hook: typeof window.__maze === 'object',
}));
console.log(JSON.stringify({ ...r, errors }, null, 2));
await close();
```
Run:
```bash
cd /Users/eunhuismacbook/Desktop/hanigame
lsof -ti:8765 >/dev/null 2>&1 || (python3 -m http.server 8765 >/dev/null 2>&1 &); sleep 1
node .maze_t0.mjs
```
Expected: `{ "hasCanvas": true, "hasSpeak": true, "heroes": 3, "hook": true, "errors": [] }`

- [ ] **Step 5: 정리 + 커밋**
```bash
cd /Users/eunhuismacbook/Desktop/hanigame
rm -f .maze_t0.mjs
git add maze.html index.html .gitignore
git commit -m "feat(maze): 게임 셸 + 허브 카드 + TTS/오디오 unlock 스캐폴드"
```

---

### Task 1: 시드 RNG + 미로 생성(완벽미로)

`window.__maze`에 순수 로직 노출. 셀 격자 + 벽 비트마스크.

**표현:** 미로는 `n×n` 셀. 각 셀은 벽 비트 `{N:1,E:2,S:4,W:8}` (1=벽 있음). 시작=(0,0), 목표=(n-1,n-1).

**Files:**
- Modify: `/Users/eunhuismacbook/Desktop/hanigame/maze.html` (`<script>` 안, `window.__maze = {}` 위에 함수 추가; 훅 갱신)

- [ ] **Step 1: 실패 테스트 작성** — `.maze_t1.mjs`:
```js
import { launch } from './.maze_test_lib.mjs';
const { page, close } = await launch();
const r = await page.evaluate(() => {
  const M = window.__maze;
  const n = 9;
  const a = M.genMaze(n, 12345);
  const b = M.genMaze(n, 12345);
  const c = M.genMaze(n, 999);
  // 결정성: 같은 시드 = 같은 결과
  const deterministic = JSON.stringify(a) === JSON.stringify(b) && JSON.stringify(a) !== JSON.stringify(c);
  // 완벽미로: 모든 칸 BFS 도달 + 통로(열린 인접쌍) 수 = 칸수-1 (스패닝 트리)
  const idx = (r,col) => r*n+col;
  const seen = new Array(n*n).fill(false); let stack=[0], cnt=0, edges=0;
  seen[0]=true;
  while(stack.length){ const v=stack.pop(); cnt++; const r0=Math.floor(v/n), c0=v%n; const w=a[v];
    const nb=[[ -1,0,1],[0,1,2],[1,0,4],[0,-1,8]];
    for(const [dr,dc,bit] of nb){ if(w&bit) continue; const nr=r0+dr,nc=c0+dc;
      if(nr<0||nc<0||nr>=n||nc>=n) continue; const u=idx(nr,nc); if(!seen[u]){seen[u]=true;stack.push(u);} }
  }
  // edges 세기(중복 제거: 동쪽·남쪽 열린 것만)
  for(let r0=0;r0<n;r0++)for(let c0=0;c0<n;c0++){const w=a[idx(r0,c0)];
    if(!(w&2)&&c0<n-1)edges++; if(!(w&4)&&r0<n-1)edges++; }
  return { deterministic, allReached: cnt===n*n, edges, want: n*n-1 };
});
console.log(JSON.stringify(r));
await close();
```
- [ ] **Step 2: 실패 확인**
```bash
node .maze_t1.mjs
```
Expected: 에러 또는 `M.genMaze is not a function` (아직 미구현).

- [ ] **Step 3: 구현** — `maze.html` `<script>`에서 `window.__maze = {};`를 아래로 교체:
```js
// ── 시드 RNG (mulberry32) ──
function mulberry32(seed){ let t = seed >>> 0; return function(){
  t += 0x6D2B79F5; let x = Math.imul(t ^ (t>>>15), 1 | t);
  x ^= x + Math.imul(x ^ (x>>>7), 61 | x); return ((x ^ (x>>>14)) >>> 0) / 4294967296; }; }

// ── 완벽미로 생성 (재귀 백트래커, 반복 스택) ──
// 반환: 길이 n*n 배열, 각 원소 = 벽 비트마스크 {N:1,E:2,S:4,W:8}
function genMaze(n, seed){
  const rnd = mulberry32(seed);
  const idx = (r,c) => r*n+c;
  const cells = new Array(n*n).fill(15); // 처음엔 사방 벽
  const visited = new Array(n*n).fill(false);
  const stack = [0]; visited[0] = true;
  const DIRS = [[-1,0,1,4],[0,1,2,8],[1,0,4,1],[0,-1,8,2]]; // dr,dc,bit,opp
  while(stack.length){
    const v = stack[stack.length-1];
    const r = Math.floor(v/n), c = v%n;
    // 미방문 이웃 수집
    const opts = [];
    for(const [dr,dc,bit,opp] of DIRS){
      const nr=r+dr, nc=c+dc;
      if(nr<0||nc<0||nr>=n||nc>=n) continue;
      if(!visited[idx(nr,nc)]) opts.push([nr,nc,bit,opp]);
    }
    if(opts.length===0){ stack.pop(); continue; }
    const [nr,nc,bit,opp] = opts[Math.floor(rnd()*opts.length)];
    cells[v] &= ~bit;             // 현재 칸의 벽 허물기
    cells[idx(nr,nc)] &= ~opp;    // 이웃 칸의 반대벽 허물기
    visited[idx(nr,nc)] = true;
    stack.push(idx(nr,nc));
  }
  return cells;
}

window.__maze = { mulberry32, genMaze, N:1, E:2, S:4, W:8 };
```
- [ ] **Step 4: 통과 확인**
```bash
node .maze_t1.mjs
```
Expected: `{"deterministic":true,"allReached":true,"edges":80,"want":80}` (9×9 → 81칸, 스패닝트리 80간선).

- [ ] **Step 5: 커밋**
```bash
rm -f .maze_t1.mjs
git add maze.html
git commit -m "feat(maze): 시드 RNG + 완벽미로 생성(재귀 백트래커)"
```

---

### Task 2: 해답경로 + 분기탐지 + 막다른길 단축 + 최소분기 보장

**Files:**
- Modify: `/Users/eunhuismacbook/Desktop/hanigame/maze.html`

- [ ] **Step 1: 실패 테스트** — `.maze_t2.mjs`:
```js
import { launch } from './.maze_test_lib.mjs';
const { page, close } = await launch();
const r = await page.evaluate(() => {
  const M = window.__maze;
  const n = 9;
  const lvl = M.buildLevel(n, 42); // {cells, path, forks}
  // path: 시작(0,0)→목표(n-1,n-1) 셀 인덱스 배열, 인접 셀은 벽 없이 연결
  const idx=(r,c)=>r*n+c;
  let ok = lvl.path[0]===0 && lvl.path[lvl.path.length-1]===n*n-1;
  for(let i=1;i<lvl.path.length;i++){
    const a=lvl.path[i-1], b=lvl.path[i];
    const ar=Math.floor(a/n),ac=a%n, br=Math.floor(b/n),bc=b%n;
    const adj = Math.abs(ar-br)+Math.abs(ac-bc)===1;
    let open=false; const w=lvl.cells[a];
    if(br<ar&&!(w&1))open=true; if(bc>ac&&!(w&2))open=true;
    if(br>ar&&!(w&4))open=true; if(bc<ac&&!(w&8))open=true;
    if(!adj||!open){ ok=false; }
  }
  return { connected: ok, forks: lvl.forks.length, forksOK: lvl.forks.length>=3 };
});
console.log(JSON.stringify(r));
await close();
```
- [ ] **Step 2: 실패 확인**
```bash
node .maze_t2.mjs
```
Expected: `M.buildLevel is not a function`.

- [ ] **Step 3: 구현** — `maze.html`에서 `genMaze` 함수 다음, `window.__maze = {...}` 줄 위에 추가:
```js
// ── BFS 해답경로 ──
function solvePath(cells, n, start, goal){
  const idx=(r,c)=>r*n+c;
  const prev = new Array(n*n).fill(-1);
  const seen = new Array(n*n).fill(false);
  const q=[start]; seen[start]=true;
  const DIRS=[[-1,0,1],[0,1,2],[1,0,4],[0,-1,8]];
  while(q.length){
    const v=q.shift(); if(v===goal) break;
    const r=Math.floor(v/n),c=v%n, w=cells[v];
    for(const [dr,dc,bit] of DIRS){ if(w&bit) continue;
      const nr=r+dr,nc=c+dc; if(nr<0||nc<0||nr>=n||nc>=n) continue;
      const u=idx(nr,nc); if(!seen[u]){seen[u]=true;prev[u]=v;q.push(u);} }
  }
  const path=[]; let cur=goal; while(cur!==-1){ path.unshift(cur); cur=prev[cur]; }
  return path;
}

// ── 열린 이웃 개수/목록 ──
function openNeighbors(cells, n, v){
  const r=Math.floor(v/n),c=v%n, w=cells[v], out=[];
  const DIRS=[[-1,0,1],[0,1,2],[1,0,4],[0,-1,8]];
  for(const [dr,dc,bit] of DIRS){ if(w&bit) continue;
    const nr=r+dr,nc=c+dc; if(nr<0||nc<0||nr>=n||nc>=n) continue; out.push(r*0+ (nr*n+nc)); }
  return out;
}

// ── 막다른길 단축: 막다른 칸(열린 이웃 1개)에서 시작해 길이>cap이면 벽 하나 텀 ──
function pruneDeadEnds(cells, n, cap, rnd){
  for(let v=0; v<n*n; v++){
    if(v===0 || v===n*n-1) continue;
    let nb = openNeighbors(cells, n, v);
    if(nb.length!==1) continue;
    // 막다른 가지를 따라가며 길이 측정
    let chain=[v], cur=v, came=-1, len=1;
    while(true){
      const ns = openNeighbors(cells, n, cur).filter(x=>x!==came);
      if(ns.length!==1) break;          // 분기/막힘 도달
      came=cur; cur=ns[0]; chain.push(cur); len++;
      if(cur===0||cur===n*n-1) break;
      const deg = openNeighbors(cells, n, cur).length;
      if(deg>2) break;
    }
    if(len>cap){
      // chain의 cap번째 칸과 인접 '벽 있는' 이웃을 하나 터서 루프/지름길 생성 → 가지 단축
      const cell = chain[cap];
      const r=Math.floor(cell/n),c=cell%n;
      const cand=[[-1,0,1,4],[0,1,2,8],[1,0,4,1],[0,-1,8,2]]
        .map(([dr,dc,bit,opp])=>({nr:r+dr,nc:c+dc,bit,opp}))
        .filter(o=>o.nr>=0&&o.nc>=0&&o.nr<n&&o.nc<n && (cells[cell]&o.bit)); // 벽 있는 방향
      if(cand.length){ const o=cand[Math.floor(rnd()*cand.length)];
        cells[cell]&=~o.bit; cells[o.nr*n+o.nc]&=~o.opp; }
    }
  }
}

// ── 해답경로 상의 분기 칸(들어온 칸 제외 열린 이웃 ≥2) ──
function forksOnPath(cells, n, path){
  const out=[];
  for(let i=0;i<path.length-1;i++){
    const v=path[i]; const prev = i>0 ? path[i-1] : -1;
    const nb = openNeighbors(cells, n, v).filter(x=>x!==prev);
    if(nb.length>=2) out.push({ cell:v, next:path[i+1], branches:nb });
  }
  return out;
}

// ── 한 판 구성: 최소 분기 3개 보장(미달 시 시드 증가 재생성) ──
function buildLevel(n, seed){
  const cap = 3;
  for(let s=seed; s<seed+50; s++){
    const cells = genMaze(n, s);
    pruneDeadEnds(cells, n, cap, mulberry32(s ^ 0x9e3779b9));
    const path = solvePath(cells, n, 0, n*n-1);
    const forks = forksOnPath(cells, n, path);
    if(forks.length>=3) return { cells, path, forks, seed:s };
  }
  // 폴백: 마지막 생성분 반환
  const cells = genMaze(n, seed); pruneDeadEnds(cells, n, cap, mulberry32(seed));
  const path = solvePath(cells, n, 0, n*n-1);
  return { cells, path, forks: forksOnPath(cells, n, path), seed };
}
```
그리고 `window.__maze = {...}` 줄을 교체:
```js
window.__maze = { mulberry32, genMaze, solvePath, openNeighbors, pruneDeadEnds, forksOnPath, buildLevel, N:1, E:2, S:4, W:8 };
```
- [ ] **Step 4: 통과 확인**
```bash
node .maze_t2.mjs
```
Expected: `{"connected":true,"forks":N,"forksOK":true}` (N≥3).

- [ ] **Step 5: 커밋**
```bash
rm -f .maze_t2.mjs
git add maze.html
git commit -m "feat(maze): 해답경로(BFS)+분기탐지+막다른길 단축+최소분기 보장"
```

---

### Task 3: DPR 캔버스 + 오프스크린 미로 캐시 + 정적 렌더

화면에 미로 벽·시작·목표를 그린다(아직 이동 없음). 게임 상태 객체 `G` 도입.

**Files:**
- Modify: `/Users/eunhuismacbook/Desktop/hanigame/maze.html`

- [ ] **Step 1: 실패 테스트** — `.maze_t3.mjs`:
```js
import { launch } from './.maze_test_lib.mjs';
const { page, errors, close } = await launch();
const r = await page.evaluate(() => {
  window.__maze.startLevel(0, 42);     // 1판, 고정 시드
  const cv = document.getElementById('maze-canvas');
  const dpr = window.devicePixelRatio || 1;
  // 캔버스 백킹스토어가 DPR 반영됐는지 + 셀 크기 = min(가용)/n
  const G = window.__maze._state();
  const wallPixel = window.__maze._sampleWall(); // 캐시에서 벽 픽셀 밝기(>0이면 그려짐)
  return { cw: cv.width, ch: cv.height, dpr, cell: G.cell, n: G.n, wallDrawn: wallPixel };
});
console.log(JSON.stringify({ ...r, errors }, null, 2));
await close();
```
- [ ] **Step 2: 실패 확인**
```bash
node .maze_t3.mjs
```
Expected: `startLevel is not a function`.

- [ ] **Step 3: 구현** — `maze.html` `<script>`의 `window.__maze = {...}` 다음에 추가:
```js
// ── 게임 상태 ──
let G = null;            // 현재 판 상태
let mazeCache = null;    // 오프스크린 캔버스(정적 벽)
let DPR = 1;

function sizeCanvas(n){
  const wrap = document.getElementById('maze-wrap');
  DPR = window.devicePixelRatio || 1;
  const availW = wrap.clientWidth - 8, availH = wrap.clientHeight - 8;
  const cell = Math.floor(Math.min(availW, availH) / n);
  const px = cell * n;
  canvas.style.width = px + 'px'; canvas.style.height = px + 'px';
  canvas.width = px * DPR; canvas.height = px * DPR;
  ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
  return { cell, px };
}

// 정적 미로(벽)를 오프스크린에 1회 렌더
function buildMazeCache(){
  const { n, cell, px } = G;
  mazeCache = document.createElement('canvas');
  mazeCache.width = px * DPR; mazeCache.height = px * DPR;
  const g = mazeCache.getContext('2d');
  g.setTransform(DPR,0,0,DPR,0,0);
  g.fillStyle = '#11151C'; g.fillRect(0,0,px,px);
  g.strokeStyle = '#3A4250'; g.lineWidth = Math.max(2, cell*0.08); g.lineCap='round';
  const line=(x1,y1,x2,y2)=>{ g.beginPath(); g.moveTo(x1,y1); g.lineTo(x2,y2); g.stroke(); };
  for(let r=0;r<n;r++)for(let c=0;c<n;c++){
    const w=G.cells[r*n+c], x=c*cell, y=r*cell;
    if(w&1) line(x,y,x+cell,y);
    if(w&2) line(x+cell,y,x+cell,y+cell);
    if(w&4) line(x,y+cell,x+cell,y+cell);
    if(w&8) line(x,y,x,y+cell);
  }
}

function cellCenter(v){ const c=v%G.n, r=Math.floor(v/G.n); return { x:(c+0.5)*G.cell, y:(r+0.5)*G.cell }; }

function startLevel(levelIdx, seed){
  const hero = HEROES[levelIdx];
  const n = hero.n;
  const { cell, px } = sizeCanvas(n);
  const lvl = buildLevel(n, seed != null ? seed : (1000 + levelIdx*777 + Math.floor((window.__seedNonce=(window.__seedNonce||0)+1))));
  G = { levelIdx, hero, n, cell, px, cells: lvl.cells, path: lvl.path, forks: lvl.forks,
        player: 0, goal: n*n-1, trail: [0], finger: null, arrived: false,
        idle: 0, signs: null, activeFork: null };
  buildMazeCache();
  document.getElementById('level-disp').textContent = `단계 ${levelIdx+1} / 3`;
  document.getElementById('arrival').classList.remove('show');
  document.getElementById('celebration').classList.remove('show');
  drawFrame();
}

function drawFrame(){
  if(!G) return;
  ctx.clearRect(0,0,G.px,G.px);
  ctx.drawImage(mazeCache, 0,0, G.px*DPR, G.px*DPR, 0,0, G.px, G.px);
  // 목표(영웅)
  const gp = cellCenter(G.goal);
  ctx.font = `${Math.round(G.cell*0.7)}px serif`; ctx.textAlign='center'; ctx.textBaseline='middle';
  ctx.fillText(G.hero.goal, gp.x, gp.y);
  // trail (단색 코럴, 글로우 없음)
  if(G.trail.length>1){
    ctx.strokeStyle = '#FF7A5A'; ctx.lineWidth = Math.max(4, G.cell*0.28); ctx.lineCap='round'; ctx.lineJoin='round';
    ctx.beginPath();
    G.trail.forEach((v,i)=>{ const p=cellCenter(v); i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y); });
    ctx.stroke();
  }
  // 플레이어 토큰
  const pp = cellCenter(G.player);
  ctx.font = `${Math.round(G.cell*0.6)}px serif`;
  ctx.fillText('🤖', pp.x, pp.y);
}

// 테스트 훅 확장
window.__maze.startLevel = startLevel;
window.__maze._state = () => G;
window.__maze._sampleWall = () => { // 캐시 좌상단 셀의 위쪽 벽 픽셀 밝기 합
  const g = mazeCache.getContext('2d'); const d = g.getImageData(2*DPR, 1*DPR, 1, 1).data; return d[0]+d[1]+d[2]; };
```
- [ ] **Step 4: 통과 확인**
```bash
node .maze_t3.mjs
```
Expected: `cw === px*dpr` (예 cell*9*2), `cell>=44`(아이패드 뷰포트 820폭 → cell≈ (min(812,~1000)/9)=90), `n:9`, `wallDrawn>0`, `errors:[]`.

- [ ] **Step 5: 커밋**
```bash
rm -f .maze_t3.mjs
git add maze.html
git commit -m "feat(maze): DPR 캔버스+오프스크린 벽 캐시+정적 렌더(미로·영웅·trail·플레이어)"
```

---

### Task 4: 입력(터치) + 이동(리시 + 갈림길 커밋 + 되돌리기) + 도착

**이동 규칙(spec B):**
- 손가락 픽셀 → 셀 좌표 `fc`. 플레이어 셀 `pv`.
- 리시: `fc`가 `pv` 또는 그 인접 칸일 때만 이동 후보.
- 후보 칸 = `fc`가 플레이어의 **열린 인접 칸**과 일치하면 그 칸. (방향추정 X)
- 되돌리기: `fc`가 `trail[len-2]`이면 trail pop(되돌아감).
- 갈림길 커밋: 분기여도 손가락이 실제 인접 통로 칸에 들어와야 이동(위 규칙이 자연히 보장).
- 한 tick에 한 칸. 큐 없음(손가락 위치 기반이라 자연 제한).

**Files:**
- Modify: `/Users/eunhuismacbook/Desktop/hanigame/maze.html`

- [ ] **Step 1: 실패 테스트** — `.maze_t4.mjs`:
```js
import { launch } from './.maze_test_lib.mjs';
const { page, errors, close } = await launch();
const r = await page.evaluate(async () => {
  const M = window.__maze;
  M.startLevel(0, 42);
  const G = M._state();
  // 해답경로 따라 칸 중심에 손가락 주입 → tick 반복
  let arrived=false, steps=0;
  for(let i=1;i<G.path.length && steps<500;i++){
    const cell = G.path[i];
    const cx = (cell%G.n+0.5)*G.cell, cy=(Math.floor(cell/G.n)+0.5)*G.cell;
    M.setFinger(cx, cy);
    // 한 칸 이동까지 여러 tick
    let guard=0; while(M._state().player!==cell && guard<20){ M.tick(); guard++; steps++; }
  }
  arrived = M._state().player === G.goal;
  // 벽 방향 주입: 임의 칸에서 벽 있는 쪽 좌표 주면 제자리
  M.startLevel(0, 42); const G2=M._state();
  const before = G2.player;
  M.setFinger(-50, -50); M.tick(); // 캔버스 밖
  const stillSame = M._state().player === before;
  return { arrived, stillSame };
});
console.log(JSON.stringify({ ...r, errors }, null, 2));
await close();
```
- [ ] **Step 2: 실패 확인**
```bash
node .maze_t4.mjs
```
Expected: `setFinger is not a function`.

- [ ] **Step 3: 구현** — `maze.html`에 추가(테스트 훅 줄들 앞):
```js
// ── 입력 → finger(셀 좌표) ──
function pxToCell(x,y){
  const c = Math.floor(x / G.cell), r = Math.floor(y / G.cell);
  if(r<0||c<0||r>=G.n||c>=G.n) return null;
  return r*G.n + c;
}
function setFinger(x,y){ if(!G) return; G.finger = pxToCell(x,y); G.idle = 0; }

function cellsAdjacentOpen(v){ return openNeighbors(G.cells, G.n, v); }

// 한 tick: 손가락 칸 기준 1칸 이동
function tickMove(){
  if(!G || G.arrived) return;
  const f = G.finger;
  if(f==null) return;
  const pv = G.player;
  if(f===pv) return;
  // 되돌리기: 손가락이 직전 trail 칸
  if(G.trail.length>=2 && f===G.trail[G.trail.length-2]){
    G.trail.pop(); G.player = f; afterMove(); return;
  }
  // 전진: 손가락 칸이 플레이어의 열린 인접 칸이어야 함(리시+커밋 동시 만족)
  const open = cellsAdjacentOpen(pv);
  if(open.includes(f)){
    // 이미 trail에 있으면(우회) 되감기 처리
    const existing = G.trail.indexOf(f);
    if(existing>=0){ G.trail.length = existing+1; }
    else { G.trail.push(f); }
    G.player = f; afterMove(); return;
  }
  // 그 외(벽/멀리): 제자리
}

function afterMove(){
  if(G.player===G.goal){ G.arrived = true; onArrive(); }
}

// rAF 루프
let rafId=null, lastT=0;
function loop(t){
  const dt = Math.min((t-lastT)/1000, 0.05); lastT=t;
  if(G && !G.arrived){
    G.idle += dt;
    tickMove();
  }
  drawFrame();
  rafId = requestAnimationFrame(loop);
}
function startLoop(){ if(!rafId) rafId = requestAnimationFrame(loop); }

// 캔버스 입력 핸들러
function evtCell(e){
  const rect = canvas.getBoundingClientRect();
  const t = e.touches ? e.touches[0] : e;
  if(!t) return null;
  return { x: t.clientX - rect.left, y: t.clientY - rect.top };
}
canvas.addEventListener('touchstart', e=>{ e.preventDefault(); const p=evtCell(e); if(p) setFinger(p.x,p.y); }, {passive:false});
canvas.addEventListener('touchmove',  e=>{ e.preventDefault(); const p=evtCell(e); if(p) setFinger(p.x,p.y); }, {passive:false});
canvas.addEventListener('touchend',   e=>{ e.preventDefault(); if(G) G.finger=null; }, {passive:false});
canvas.addEventListener('mousedown',  e=>{ const p=evtCell(e); if(p) setFinger(p.x,p.y); });
canvas.addEventListener('mousemove',  e=>{ if(e.buttons){ const p=evtCell(e); if(p) setFinger(p.x,p.y); } });
canvas.addEventListener('mouseup',    ()=>{ if(G) G.finger=null; });

// onArrive: Task 7에서 채움(임시 빈 함수)
function onArrive(){ /* Task 7 */ }

// 테스트 훅
window.__maze.setFinger = setFinger;
window.__maze.tick = tickMove;
```
그리고 `startLevel` 끝의 `drawFrame();` 다음 줄에 `startLoop();` 추가.

- [ ] **Step 4: 통과 확인**
```bash
node .maze_t4.mjs
```
Expected: `{"arrived":true,"stillSame":true,"errors":[]}`.

- [ ] **Step 5: 커밋**
```bash
rm -f .maze_t4.mjs
git add maze.html
git commit -m "feat(maze): 터치 입력+이동(리시·갈림길 커밋·너그러운 되돌리기)"
```

---

### Task 5: 표지판 + 영어 힌트(선교육·발화·보상) + 다시듣기 버튼

**Files:**
- Modify: `/Users/eunhuismacbook/Desktop/hanigame/maze.html`

표지판 어휘 풀(영웅 이모지 제외 배포):
```
DISTRACTORS = [['🐶','dog'],['🍎','apple'],['⭐','star'],['🌸','flower'],['🎈','balloon'],['🐱','cat']]
```
정답 표지판 = 영웅 goal 이모지/word.

- [ ] **Step 1: 실패 테스트** — `.maze_t5.mjs`:
```js
import { launch } from './.maze_test_lib.mjs';
const { page, errors, close } = await launch();
const r = await page.evaluate(() => {
  const M = window.__maze;
  const spoken=[]; window.__speakSpy = s => spoken.push(s);
  M.startLevel(0, 42);
  const G = M._state();
  // 첫 분기로 플레이어 이동(해답경로 따라 분기 직전까지)
  const firstFork = G.forks[0];
  // path에서 firstFork.cell까지 순차 이동
  const pi = G.path.indexOf(firstFork.cell);
  for(let i=1;i<=pi;i++){ const cell=G.path[i];
    const cx=(cell%G.n+0.5)*G.cell, cy=(Math.floor(cell/G.n)+0.5)*G.cell;
    M.setFinger(cx,cy); let g=0; while(M._state().player!==cell&&g<30){M.tick();g++;} }
  const st = M._state();
  const signs = st.signs; // {cell, items:[{branch,emoji,word,correct}]}
  const correctOnPath = signs && signs.items.find(s=>s.correct).branch === firstFork.next;
  const heroExcluded = signs && !signs.items.some(s=>!s.correct && s.emoji===G.hero.goal);
  return { hasSigns: !!signs, correctOnPath, heroExcluded, spokeWord: spoken.includes(G.hero.word) };
});
console.log(JSON.stringify({ ...r, errors }, null, 2));
await close();
```
- [ ] **Step 2: 실패 확인**
```bash
node .maze_t5.mjs
```
Expected: `hasSigns:false` 또는 에러(미구현).

- [ ] **Step 3: 구현** — `maze.html`:

(a) `speak` 함수 안 맨 위에 테스트 스파이 훅 추가 — `speechSynthesis.cancel();` 바로 위:
```js
  if (window.__speakSpy) window.__speakSpy(text);
```

(b) 상수 추가(HEROES 아래):
```js
const DISTRACTORS = [['🐶','dog'],['🍎','apple'],['⭐','star'],['🌸','flower'],['🎈','balloon'],['🐱','cat']];
```

(c) 표지판 생성/해제 + 보상. `afterMove` 함수를 아래로 교체:
```js
function enterCellFork(){
  // 현재 칸이 해답경로 분기이고 아직 표지판 없으면 생성
  const fork = G.forks.find(f=>f.cell===G.player);
  if(fork && (!G.signs || G.signs.cell!==G.player)){
    const rnd = mulberry32(G.player*131 + G.levelIdx*7 + 1);
    const pool = DISTRACTORS.filter(d=>d[0]!==G.hero.goal).slice();
    // 셔플
    for(let i=pool.length-1;i>0;i--){ const j=Math.floor(rnd()*(i+1)); [pool[i],pool[j]]=[pool[j],pool[i]]; }
    const items = fork.branches.map(br=>{
      if(br===fork.next) return { branch:br, emoji:G.hero.goal, word:G.hero.word, correct:true };
      const d = pool.pop() || ['❓','box'];
      return { branch:br, emoji:d[0], word:d[1], correct:false };
    });
    G.signs = { cell:G.player, items };
    G.activeFork = fork;
    speak(G.hero.word);            // 선교육: 정답 단어 발화
  }
}
function afterMove(){
  // 정답 표지판 통로 진입 시 보상
  if(G.signs && G.activeFork && G.activeFork.cell===G.trail[G.trail.length-2]){
    const taken = G.signs.items.find(s=>s.branch===G.player);
    if(taken && taken.correct){ spawnSpark(); speak(G.hero.word); }
    G.signs=null; G.activeFork=null;
  }
  enterCellFork();
  if(G.player===G.goal){ G.arrived = true; onArrive(); }
}

// 반짝 보상(간단 파티클)
let sparks=[];
function spawnSpark(){ const p=cellCenter(G.player);
  for(let i=0;i<10;i++){ const a=Math.PI*2*i/10; sparks.push({x:p.x,y:p.y,vx:Math.cos(a)*2,vy:Math.sin(a)*2,life:1}); } }
```

(d) `drawFrame`에 표지판+반짝 그리기 추가 — 플레이어 토큰 그린 직후:
```js
  // 표지판
  if(G.signs){
    const sz = Math.max(40, G.cell*0.7);
    G.signs.items.forEach(it=>{
      const p = cellCenter(it.branch);
      ctx.font = `${Math.round(sz)}px serif`; ctx.fillText(it.emoji, p.x, p.y);
    });
  }
  // 반짝
  if(sparks.length){ sparks.forEach(s=>{ s.x+=s.vx; s.y+=s.vy; s.life-=0.04; });
    sparks = sparks.filter(s=>s.life>0);
    sparks.forEach(s=>{ ctx.globalAlpha=Math.max(0,s.life); ctx.fillStyle='#FFD54A';
      ctx.beginPath(); ctx.arc(s.x,s.y,Math.max(2,G.cell*0.06),0,Math.PI*2); ctx.fill(); });
    ctx.globalAlpha=1;
  }
```

(e) 🔊 다시듣기 버튼 — `<script>` 아무 곳(핸들러 영역):
```js
document.getElementById('hint-btn').addEventListener('click', ()=>{ if(G && G.signs) speak(G.hero.word); });
```

(f) `startLevel`에서 첫 칸이 분기일 수도 있으니 초기 `enterCellFork()` 호출 — `buildMazeCache();` 다음 줄에 추가:
```js
  G.signs=null; G.activeFork=null;
```

- [ ] **Step 4: 통과 확인**
```bash
node .maze_t5.mjs
```
Expected: `{"hasSigns":true,"correctOnPath":true,"heroExcluded":true,"spokeWord":true,"errors":[]}`.

- [ ] **Step 5: 커밋**
```bash
rm -f .maze_t5.mjs
git add maze.html
git commit -m "feat(maze): 표지판+영어 힌트(선교육 발화·정답 보상)+다시듣기"
```

---

### Task 6: 온보딩(시작 안내) 상태

**Files:**
- Modify: `/Users/eunhuismacbook/Desktop/hanigame/maze.html`

- [ ] **Step 1: 실패 테스트** — `.maze_t6.mjs`:
```js
import { launch } from './.maze_test_lib.mjs';
const { page, errors, close } = await launch();
const r = await page.evaluate(async () => {
  const M = window.__maze;
  M.startLevel(0, 42);
  // idle 누적 시뮬: 2초치 강제
  M._state().idle = 2.0; M._forceDraw();
  const onbAfterIdle = M._onboardingVisible();
  // 터치 시작하면 사라짐
  M.setFinger((0.5)*M._state().cell, (0.5)*M._state().cell);
  M._forceDraw();
  const onbAfterTouch = M._onboardingVisible();
  return { onbAfterIdle, onbAfterTouch };
});
console.log(JSON.stringify({ ...r, errors }, null, 2));
await close();
```
- [ ] **Step 2: 실패 확인**
```bash
node .maze_t6.mjs
```
Expected: `_onboardingVisible is not a function`.

- [ ] **Step 3: 구현** — `maze.html`:

(a) 온보딩 표시 상태 + 첫 안내 1회 발화 플래그. `drawFrame` 안, 플레이어 토큰 그린 뒤(표지판 앞)에 추가:
```js
  // 온보딩: 입력 전 + idle>1.5s
  G._onbShown = (G.trail.length===1 && G.idle>1.5);
  if(G._onbShown){
    const p = cellCenter(G.player);
    const pulse = 0.6 + 0.4*Math.abs(Math.sin(performance.now()/300));
    ctx.globalAlpha = pulse;
    ctx.font = `${Math.round(G.cell*0.6)}px serif`; ctx.fillText('👆', p.x, p.y+G.cell*0.5);
    ctx.globalAlpha = 1;
    if(!G._onbSpoke){ G._onbSpoke=true; speak('Drag to the hero!'); }
  }
```

(b) 테스트 훅 추가(훅 영역):
```js
window.__maze._forceDraw = () => drawFrame();
window.__maze._onboardingVisible = () => !!(G && G._onbShown);
```

(c) `startLevel`에서 초기화 — `G.signs=null; G.activeFork=null;` 다음에:
```js
  G._onbSpoke = false;
```

- [ ] **Step 4: 통과 확인**
```bash
node .maze_t6.mjs
```
Expected: `{"onbAfterIdle":true,"onbAfterTouch":false,"errors":[]}`.

- [ ] **Step 5: 커밋**
```bash
rm -f .maze_t6.mjs
git add maze.html
git commit -m "feat(maze): 온보딩 안내(손가락 펄스+음성)"
```

---

### Task 7: 도착 카드 + 3판 진행 + 축하 + 다시하기

**Files:**
- Modify: `/Users/eunhuismacbook/Desktop/hanigame/maze.html`

- [ ] **Step 1: 실패 테스트** — `.maze_t7.mjs`:
```js
import { launch } from './.maze_test_lib.mjs';
const { page, errors, close } = await launch();
function playToGoal(){ /* injected below */ }
const r = await page.evaluate(async () => {
  const M = window.__maze;
  const sleep = ms => new Promise(r=>setTimeout(r,ms));
  function clearLevel(){
    const G = M._state();
    for(let i=1;i<G.path.length;i++){ const cell=G.path[i];
      const cx=(cell%G.n+0.5)*G.cell, cy=(Math.floor(cell/G.n)+0.5)*G.cell;
      M.setFinger(cx,cy); let g=0; while(M._state().player!==cell&&g<40){M.tick();g++;} }
    return M._state().arrived;
  }
  M.startLevel(0, 42);
  const a1 = clearLevel();
  const arrivalShown = document.getElementById('arrival').classList.contains('show');
  const en1 = document.getElementById('ar-en').textContent;
  // 다음 판
  M._next();
  const lvl2 = M._state().levelIdx;
  const a2 = clearLevel(); M._next();
  const a3 = clearLevel(); M._next();
  const celebShown = document.getElementById('celebration').classList.contains('show');
  return { a1, arrivalShown, en1, lvl2, a2, a3, celebShown };
});
console.log(JSON.stringify({ ...r, errors }, null, 2));
await close();
```
- [ ] **Step 2: 실패 확인**
```bash
node .maze_t7.mjs
```
Expected: `_next is not a function` 또는 `arrivalShown:false`.

- [ ] **Step 3: 구현** — `maze.html`:

(a) `onArrive` 빈 함수를 아래로 교체:
```js
function onArrive(){
  const hero = G.hero;
  setTimeout(()=>{
    document.getElementById('ar-hero').textContent = hero.goal;
    document.getElementById('ar-en').textContent = hero.en;
    document.getElementById('ar-ko').textContent = hero.ko;
    document.getElementById('arrival').classList.add('show');
    speak(hero.en);
  }, 350); // 구출 연출 잠깐 뒤
}
function nextLevel(){
  document.getElementById('arrival').classList.remove('show');
  const next = G.levelIdx + 1;
  if(next >= HEROES.length){ showCelebration(); return; }
  startLevel(next, null);
}
function showCelebration(){ document.getElementById('celebration').classList.add('show'); }
function replayAll(){ document.getElementById('celebration').classList.remove('show'); startLevel(0, null); }
```

(b) 버튼 핸들러:
```js
document.getElementById('ar-next').addEventListener('click', nextLevel);
document.getElementById('ar-say').addEventListener('click', ()=>{ if(G) speak(G.hero.en); });
document.getElementById('ar-replay').addEventListener('click', replayAll);
```

(c) 테스트 훅:
```js
window.__maze._next = nextLevel;
```

(d) 첫 진입: 페이지 로드 시 1판 시작 — `<script>` 맨 끝에:
```js
startLevel(0, null);
```

- [ ] **Step 4: 통과 확인**
```bash
node .maze_t7.mjs
```
Expected: `a1,a2,a3` 모두 true, `arrivalShown:true`, `en1:"Firefighters are brave."`, `lvl2:1`, `celebShown:true`, `errors:[]`.

- [ ] **Step 5: 커밋**
```bash
rm -f .maze_t7.mjs
git add maze.html
git commit -m "feat(maze): 도착 카드+3판 진행+축하+다시하기"
```

---

### Task 8: 통합 E2E + iPad 터치 실주행 + 정리

**Files:**
- 없음(검증 전용). 실패 시 해당 Task로 돌아가 수정.

- [ ] **Step 1: 통합 E2E 테스트** — `.maze_t8.mjs`:
```js
import { launch } from './.maze_test_lib.mjs';
const { page, errors, close } = await launch();
const r = await page.evaluate(async () => {
  const M = window.__maze;
  // 실제 터치 이벤트로 1판 일부 주행(핸들러 경유)
  const cv = document.getElementById('maze-canvas');
  const rect = cv.getBoundingClientRect();
  function touch(type, cell){ const G=M._state();
    const cx=rect.left+(cell%G.n+0.5)*G.cell, cy=rect.top+(Math.floor(cell/G.n)+0.5)*G.cell;
    const t=new Touch({identifier:1,target:cv,clientX:cx,clientY:cy});
    cv.dispatchEvent(new TouchEvent(type,{bubbles:true,cancelable:true,touches:type==='touchend'?[]:[t],changedTouches:[t]}));
  }
  M.startLevel(0,42); const G=M._state();
  touch('touchstart', G.path[1]);
  for(let i=1;i<4 && i<G.path.length;i++){ touch('touchmove', G.path[i]); for(let k=0;k<10;k++) M.tick(); }
  const moved = M._state().player !== 0;
  // 전체 3판은 tick 주입으로 빠르게
  function clear(){ const G=M._state(); for(let i=1;i<G.path.length;i++){ const c=G.path[i];
    M.setFinger((c%G.n+0.5)*G.cell,(Math.floor(c/G.n)+0.5)*G.cell); let g=0; while(M._state().player!==c&&g<40){M.tick();g++;} } return M._state().arrived; }
  M.startLevel(0,42); const a=[clear()]; M._next(); a.push(clear()); M._next(); a.push(clear()); M._next();
  const celeb=document.getElementById('celebration').classList.contains('show');
  return { touchMoved: moved, allCleared: a.every(Boolean), celeb };
});
console.log(JSON.stringify({ ...r, errors }, null, 2));
await close();
```
Run:
```bash
node .maze_t8.mjs
```
Expected: `{"touchMoved":true,"allCleared":true,"celeb":true,"errors":[]}`.

- [ ] **Step 2: 레이아웃 스크린샷 육안 확인**
```bash
cat > .maze_shot.mjs <<'EOF'
import { launch } from './.maze_test_lib.mjs';
const { page, close } = await launch();
await page.evaluate(()=>{ window.__maze.startLevel(0,42); window.__maze._state().idle=2; window.__maze._forceDraw(); });
await page.waitForTimeout(300);
await page.screenshot({ path:'.maze-shot.png' });
await close();
EOF
node .maze_shot.mjs
```
`.maze-shot.png`를 열어 확인: 미로 벽 선명(DPR), 셀 널찍, 시작 🤖, 목표 🚒, 온보딩 👆. 문제 없으면 통과.

- [ ] **Step 3: 정리 + 최종 커밋(코드 변경 없으면 생략)**
```bash
rm -f .maze_t8.mjs .maze_shot.mjs .maze-shot.png
# lsof -ti:8765 | xargs kill 2>/dev/null  # 서버 종료(선택)
git status   # 깨끗해야 함(테스트 임시파일은 gitignore)
```

- [ ] **Step 4: 배포 게이트(대표 컨펌 후)**
구현·검증 완료 보고. push·Netlify 배포는 **대표 승인 후** 진행:
```bash
git push
netlify deploy --prod --dir=.
```

---

## 구현 후 검증(요약)
- Task별 node-Playwright 테스트 통과(genMaze 완벽미로·해답·분기·이동·표지판·온보딩·도착·E2E).
- iPad 뷰포트 터치 이벤트로 실주행 + 레이아웃 스크린샷 육안.
- 콘솔 에러 0.
- 배포는 대표 승인 게이트.
