# 미로 카드 선택형 v3 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan one task at a time. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 미로 갈림길에서 영어 단어를 듣고 화면 아래 그림 카드를 눌러야 그 방향 통로가 열리도록 바꾼다. 오답 카드는 그 길로 갔다 막다른 데서 '쿵'(삐+화면 흔들림) 후 되돌아온다.

**Architecture:** 기존 `maze.html` 단일 파일에 (1) WebAudio 합성 효과음, (2) 화면 흔들림 CSS, (3) 미로 아래 카드 트레이 DOM, (4) 갈림길 카드 게이트(카드 선택 전 전진 차단) 로직을 추가한다. 이동 locomotion(손가락 드래그 자동 따라가기)·미로 생성·도착/축하는 그대로 둔다.

**Tech Stack:** 순수 HTML/CSS/JS 단일 파일, Canvas 2D, WebAudio Oscillator, `speechSynthesis`. 검증은 Playwright 헤드리스 + `window.__maze` 훅.

---

## File Structure

- **Modify only:** `/Users/eunhuismacbook/Desktop/hanigame/maze.html`
  - `<style>`(7–40): 카드 트레이·흔들림 keyframe 추가
  - `#maze-wrap`(48–65): `#card-tray` div 추가
  - `_unlockAudio`(70–82): AudioContext resume 연결
  - script 본문: 효과음·흔들림·카드 트레이·게이트 함수 신규 + `enterCellFork`/`afterMove`/`tickMove` 수정
  - `window.__maze`(463–469): `chooseCard` 등 테스트 훅 노출
- **Create (검증용, 커밋 안 함):** `/tmp/maze-verify.mjs` — Playwright 헤드리스 점검 스크립트

기존 순수 함수(`genMaze`/`solvePath`/`forksOnPath`/`buildLevel`)·렌더·이동 규칙은 변경 없음. 카드 게이트는 분기 칸에서만 개입.

---

## Task 1: WebAudio 효과음 (딩동/삐) + 오디오 unlock 연결

**Files:**
- Modify: `/Users/eunhuismacbook/Desktop/hanigame/maze.html` (script 본문, TTS 블록 다음 ~100행 근처에 삽입; `_unlockAudio` 70–82)

- [ ] **Step 1: 효과음 함수 추가**

`speak()` 함수 정의 끝(약 100행 `}` 다음 줄)에 삽입:

```javascript
// ── WebAudio 효과음 (에셋 불필요, Oscillator 합성) ──
let _ac = null;
function ac(){
  if(!_ac){ const AC = window.AudioContext || window.webkitAudioContext; _ac = AC ? new AC() : null; }
  if(_ac && _ac.state === 'suspended') _ac.resume();
  return _ac;
}
function tone(freq, dur, type, delay){
  const a = ac(); if(!a) return;
  const o = a.createOscillator(), g = a.createGain();
  o.type = type || 'sine'; o.frequency.value = freq;
  o.connect(g); g.connect(a.destination);
  const t = a.currentTime + (delay || 0);
  g.gain.setValueAtTime(0.0001, t);
  g.gain.exponentialRampToValueAtTime(0.3, t + 0.01);
  g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
  o.start(t); o.stop(t + dur + 0.02);
}
function beepGood(){ tone(660, 0.12, 'sine', 0); tone(990, 0.16, 'sine', 0.11); }   // 딩-동(상승)
function beepBad(){ tone(200, 0.20, 'square', 0); }                                  // 삐(낮은 버저)
```

- [ ] **Step 2: `_unlockAudio`에서 AudioContext 깨우기**

`maze.html:75` `audioUnlocked = true;` 바로 위에 한 줄 추가:

```javascript
    try { ac(); } catch(e) {}
    audioUnlocked = true;
```

(기존 73–74행의 빈 버퍼 재생은 그대로 두고, 효과음용 `ac()`도 첫 터치에 resume)

- [ ] **Step 3: 브라우저에서 수동 확인**

`maze.html`을 사파리/크롬에서 열고 콘솔에서:
```javascript
window.__maze && (document.body.click(), beepGood())
```
Expected: 딩-동 상승음 1회. 콘솔 에러 0. (`beepBad()`도 호출해 삐 확인)

- [ ] **Step 4: Commit**

```bash
git add maze.html
git commit -m "feat(maze): WebAudio 딩동/삐 효과음 + unlock 연결"
```

---

## Task 2: 화면 흔들림 (진동 대체)

**Files:**
- Modify: `/Users/eunhuismacbook/Desktop/hanigame/maze.html` (`<style>` 39행 뒤, script 본문)

- [ ] **Step 1: 흔들림 keyframe CSS 추가**

`maze.html:39` `.icon-btn { ... }` 규칙 다음 줄(40행 `</style>` 직전)에 추가:

```css
  @keyframes shake {
    0%,100% { transform: translateX(0); }
    20% { transform: translateX(-8px); }
    40% { transform: translateX(8px); }
    60% { transform: translateX(-6px); }
    80% { transform: translateX(6px); }
  }
  #maze-wrap.shake { animation: shake 0.32s; }
```

- [ ] **Step 2: 흔들림 헬퍼 함수 추가**

Task 1의 `beepBad()` 정의 다음 줄에 삽입:

```javascript
// ── 화면 흔들림 (iPad 진동 미지원 → 시각 대체) ──
function shakeScreen(){
  const w = document.getElementById('maze-wrap');
  if(!w) return;
  w.classList.remove('shake');   // 연속 호출 시 재시작
  void w.offsetWidth;            // reflow 강제 → 애니메이션 재시작
  w.classList.add('shake');
  // 안드로이드 폰만 진동 추가(있으면), 없으면 무시
  if(navigator.vibrate){ try { navigator.vibrate(60); } catch(e){} }
}
document.getElementById('maze-wrap').addEventListener('animationend', e=>{
  if(e.animationName === 'shake') e.currentTarget.classList.remove('shake');
});
```

- [ ] **Step 3: 브라우저 수동 확인**

콘솔에서 `shakeScreen()` 실행 → 미로 영역이 좌우로 짧게 흔들림. 콘솔 에러 0.

- [ ] **Step 4: Commit**

```bash
git add maze.html
git commit -m "feat(maze): 오답용 화면 흔들림(진동 대체)"
```

---

## Task 3: 카드 트레이 DOM + CSS + show/hide

**Files:**
- Modify: `/Users/eunhuismacbook/Desktop/hanigame/maze.html` (`<style>`, `#maze-wrap` 48–65, script 본문)

- [ ] **Step 1: 카드 트레이 CSS 추가**

Task 2의 `#maze-wrap.shake` 규칙 다음 줄(`</style>` 직전)에 추가:

```css
  #card-tray { position: absolute; left: 0; right: 0; bottom: 14px;
    display: none; justify-content: center; gap: 14px; padding: 0 12px; z-index: 5; }
  #card-tray.show { display: flex; }
  .card { width: 84px; height: 100px; border-radius: 16px;
    background: rgba(255,255,255,0.12); border: 2px solid rgba(255,255,255,0.28);
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    gap: 4px; color: #fff; cursor: pointer; -webkit-tap-highlight-color: transparent; }
  .card:active { transform: scale(0.94); background: rgba(255,255,255,0.2); }
  .card .c-emoji { font-size: 44px; line-height: 1; }
  .card .c-label { font-size: 12px; color: #cfd3da; }
```

- [ ] **Step 2: 카드 트레이 div 추가**

`maze.html:49` `<canvas id="maze-canvas"></canvas>` 다음 줄에 추가:

```html
    <div id="card-tray"></div>
```

- [ ] **Step 3: show/hide 함수 추가**

Task 2의 `animationend` 리스너 등록 다음 줄에 삽입:

```javascript
// ── 카드 트레이 (분기에서 그림 카드 선택) ──
const cardTray = document.getElementById('card-tray');
function showCardTray(items){
  cardTray.innerHTML = '';
  items.forEach(it=>{
    const b = document.createElement('button');
    b.className = 'card';
    b.innerHTML = `<span class="c-emoji">${it.emoji}</span><span class="c-label">${it.word}</span>`;
    b.addEventListener('click', ()=> chooseCard(it));
    cardTray.appendChild(b);
  });
  cardTray.classList.add('show');
}
function hideCardTray(){ cardTray.classList.remove('show'); cardTray.innerHTML = ''; }
```

- [ ] **Step 4: 브라우저 수동 확인**

콘솔에서:
```javascript
showCardTray([{emoji:'🚒',word:'fire truck'},{emoji:'🍎',word:'apple'}]); 
```
Expected: 미로 아래 카드 2장 표시. `hideCardTray()` → 사라짐. (탭하면 `chooseCard is not defined` 에러는 Task 6에서 해결 — 지금은 표시/숨김만 확인)

- [ ] **Step 5: Commit**

```bash
git add maze.html
git commit -m "feat(maze): 카드 트레이 DOM/CSS + show/hide"
```

---

## Task 4: 분기 진입 시 카드 트레이 띄우기 + unlockedBranch 상태

**Files:**
- Modify: `/Users/eunhuismacbook/Desktop/hanigame/maze.html` (`startLevel` 268–284 의 G 초기화 275–276, `enterCellFork` 368–383)

- [ ] **Step 1: G 상태에 `unlockedBranch` 추가**

`maze.html:275-276` 의 G 초기화 객체에서 `activeFork: null` 옆에 추가:

```javascript
  G = { levelIdx, hero, n, cell, px, cells: lvl.cells, path: lvl.path, forks: lvl.forks,
        player: 0, goal: n*n-1, trail: [0], finger: null, arrived: false,
        idle: 0, signs: null, activeFork: null, unlockedBranch: null, _onbSpoke: false };
```

또한 `startLevel` 진입 시 이전 판 트레이 잔재 제거 — `maze.html:278` `sparks=[];` 다음 줄에 추가:

```javascript
  hideCardTray();
```

- [ ] **Step 2: `enterCellFork`에서 카드 트레이 표시 + unlockedBranch 리셋**

`maze.html:368-383` 의 `enterCellFork()`를 아래로 교체(기존 표지판 생성 유지 + 트레이 표시 추가):

```javascript
function enterCellFork(){
  const fork = G.forks.find(f=>f.cell===G.player);
  if(fork && (!G.signs || G.signs.cell!==G.player)){
    const rnd = mulberry32(G.player*131 + G.levelIdx*7 + 1);
    const pool = DISTRACTORS.filter(d=>d[0]!==G.hero.goal).slice();
    for(let i=pool.length-1;i>0;i--){ const j=Math.floor(rnd()*(i+1)); [pool[i],pool[j]]=[pool[j],pool[i]]; }
    const items = fork.branches.map(br=>{
      if(br===fork.next) return { branch:br, emoji:G.hero.goal, word:G.hero.word, correct:true };
      const d = pool.pop() || ['❓','box'];
      return { branch:br, emoji:d[0], word:d[1], correct:false };
    });
    G.signs = { cell:G.player, items };
    G.activeFork = fork;
    G.unlockedBranch = null;                 // 카드 선택 전까지 잠금
    // 카드 트레이는 표지판 순서와 다르게 셔플해 노출(매칭 난이도)
    const order = items.slice();
    for(let i=order.length-1;i>0;i--){ const j=Math.floor(rnd()*(i+1)); [order[i],order[j]]=[order[j],order[i]]; }
    showCardTray(order);
    if(!fork.taught){ fork.taught = true; speak(G.hero.word); }  // 분기 최초 1회 자동 발화
  }
}
```

- [ ] **Step 3: Playwright 헤드리스 확인 (분기 도달 시 트레이 표시)**

`/tmp/maze-verify.mjs` 작성:

```javascript
import { chromium } from 'playwright';
const url = 'file://' + process.cwd() + '/maze.html';
const b = await chromium.launch();
const p = await b.newPage();
const errs = [];
p.on('console', m => { if(m.type()==='error') errs.push(m.text()); });
await p.goto(url);
await p.evaluate(() => document.body.click());            // 오디오 unlock
// 1판 첫 분기 칸까지 해답경로 손가락 주입
const ok = await p.evaluate(() => {
  const M = window.__maze, G = M._state();
  const fork = G.forks[0];
  // 해답경로에서 fork.cell 까지 칸 좌표를 차례로 finger 주입
  const path = G.path; const n = G.n; const cell = G.cell;
  for(const v of path){
    const r = Math.floor(v/n), c = v%n;
    M.setFinger((c+0.5)*cell, (r+0.5)*cell); M.tick();
    if(M._state().player === fork.cell) break;
  }
  return M._state().player === fork.cell && document.getElementById('card-tray').classList.contains('show');
});
console.log('fork tray shown:', ok, 'console errors:', errs.length);
await b.close();
process.exit(ok && errs.length===0 ? 0 : 1);
```

Run: `cd /Users/eunhuismacbook/Desktop/hanigame && npx playwright@latest install chromium >/dev/null 2>&1; node /tmp/maze-verify.mjs`
Expected: `fork tray shown: true console errors: 0`, 종료코드 0.

> 주의: 분기 칸 도달 직전 단계에서 카드 게이트(Task 5) 아직 없으면 손가락이 분기를 지나칠 수 있음. 이 단계 검증은 "분기 칸에서 멈춰 트레이가 뜨는지"만 본다. 기존 `tickMove`는 분기에서 이미 멈추므로(fwd≥2 자동전진 안 함) 통과해야 정상.

- [ ] **Step 4: Commit**

```bash
git add maze.html
git commit -m "feat(maze): 분기 진입 시 카드 트레이 표시 + unlockedBranch 잠금상태"
```

---

## Task 5: 카드 게이트 — 선택 전 전진 차단, 선택 갈래만 진입

**Files:**
- Modify: `/Users/eunhuismacbook/Desktop/hanigame/maze.html` (`tickMove` 347–366)

- [ ] **Step 1: `tickMove`에 카드 게이트 삽입**

`maze.html:347-366` 의 `tickMove()`를 아래로 교체:

```javascript
// 한 tick: 손가락 칸 기준 이동 (너그러운 자동 따라가기 + 분기 카드 게이트)
function tickMove(){
  if(!G || G.arrived) return;
  const f = G.finger;
  if(f==null) return;
  const pv = G.player;
  if(f===pv) return;
  // 되돌리기: 손가락이 직전 칸 (분기 잠금과 무관하게 항상 허용)
  if(G.trail.length>=2 && f===G.trail[G.trail.length-2]){
    G.trail.pop(); G.player = f; afterMove(); return;
  }
  // 분기 카드 게이트: 분기 활성 + 카드 미선택이면 전진 전면 차단
  if(G.activeFork && G.activeFork.cell===pv && G.unlockedBranch==null) return;
  const open = cellsAdjacentOpen(pv);
  // 손가락이 인접 열린 칸이면 그 칸으로
  if(open.includes(f)){
    // 분기에서는 카드로 연 갈래로만 진입 허용
    if(G.activeFork && G.activeFork.cell===pv && f!==G.unlockedBranch) return;
    stepTo(f); return;
  }
  // 손가락이 멀리 있어도, 일직선 통로(분기 아님)면 손가락 쪽으로 한 칸 자동 전진.
  const prev = G.trail.length>=2 ? G.trail[G.trail.length-2] : -1;
  const fwd = open.filter(c=>c!==prev);
  if(fwd.length===1 && cellDist(fwd[0], f) < cellDist(pv, f)){ stepTo(fwd[0]); return; }
  // 그 외(분기·벽·뒤쪽): 제자리
}
```

- [ ] **Step 2: Playwright 확인 (선택 전 차단)**

`/tmp/maze-verify.mjs` 의 `ok` 평가 다음에 추가 검증 블록(또는 새 evaluate):

```javascript
const blocked = await p.evaluate(() => {
  const M = window.__maze, G = M._state();
  const fork = G.activeFork; const n=G.n, cell=G.cell;
  // 정답 갈래 칸으로 손가락 줘도 카드 선택 전이면 못 들어가야 함
  const br = fork.next; const r=Math.floor(br/n), c=br%n;
  M.setFinger((c+0.5)*cell, (r+0.5)*cell); M.tick();
  return M._state().player === fork.cell;   // 여전히 분기 칸(전진 차단됨)
});
console.log('gate blocks before card:', blocked);
```

Run: `node /tmp/maze-verify.mjs`
Expected: `gate blocks before card: true`. 콘솔 에러 0.

- [ ] **Step 3: Commit**

```bash
git add maze.html
git commit -m "feat(maze): 갈림길 카드 게이트(선택 전 전진 차단)"
```

---

## Task 6: chooseCard 핸들러 — 정답/오답 처리

**Files:**
- Modify: `/Users/eunhuismacbook/Desktop/hanigame/maze.html` (Task 3 의 `hideCardTray` 다음에 `chooseCard` 추가; `hint-btn` 핸들러 437 확인)

- [ ] **Step 1: `chooseCard` 함수 추가**

Task 3에서 추가한 `hideCardTray()` 정의 다음 줄에 삽입:

```javascript
function chooseCard(it){
  if(!G || !G.activeFork || G.unlockedBranch!=null) return;  // 분기 아님 / 이미 선택함
  G.unlockedBranch = it.branch;     // 이 갈래만 열림(정답이든 오답이든 가볼 수 있음)
  hideCardTray();
  if(it.correct){
    beepGood(); spawnSpark(); speak(G.hero.word);   // 정답 즉시 보상
  }
  // 오답이면: 그 갈래로 진입 가능 → 막다른 도달 시 afterMove에서 삐+흔들림(되돌아오기)
}
```

- [ ] **Step 2: Playwright 확인 (정답 카드 → 진입 가능)**

`/tmp/maze-verify.mjs` 에 이어서:

```javascript
const passed = await p.evaluate(() => {
  const M = window.__maze, G = M._state();
  const fork = G.activeFork; const n=G.n, cell=G.cell;
  const correct = G.signs.items.find(s=>s.correct);
  M.chooseCard(correct);                       // 정답 카드 선택
  const br = correct.branch; const r=Math.floor(br/n), c=br%n;
  M.setFinger((c+0.5)*cell, (r+0.5)*cell); M.tick();   // 이제 진입돼야 함
  return M._state().player === br && !document.getElementById('card-tray').classList.contains('show');
});
console.log('correct card opens branch:', passed);
```

(이를 위해 Task 8에서 `chooseCard`를 `window.__maze`에 노출 — 그 전엔 이 검증이 `M.chooseCard is not a function`로 실패하므로, Task 8 완료 후 함께 실행. 지금은 브라우저 콘솔에서 전역 `chooseCard(G.signs.items.find(s=>s.correct))` 로 수동 확인.)

브라우저 수동: 1판에서 분기까지 손가락으로 가 카드 뜨면, 정답(🚒) 카드 탭 → 딩동+그 길 열림 → 끌어서 통과. 오답(🍎) 카드 탭 → 그 길 열려 들어가다 막다른 데서 멈춤(Task 7 후 쿵).

- [ ] **Step 3: Commit**

```bash
git add maze.html
git commit -m "feat(maze): chooseCard 정답/오답 처리(정답 보상·오답 진입허용)"
```

---

## Task 7: afterMove — 분기 떠날 때 정리 + 막다른 '쿵'

**Files:**
- Modify: `/Users/eunhuismacbook/Desktop/hanigame/maze.html` (`afterMove` 384–395)

- [ ] **Step 1: `afterMove` 교체**

`maze.html:384-395` 의 `afterMove()`를 아래로 교체:

```javascript
function afterMove(){
  // 분기 칸을 떠나면(전진/후진) 표지판·트레이·잠금 해제
  if(G.activeFork && G.player!==G.activeFork.cell){
    G.signs=null; G.activeFork=null; G.unlockedBranch=null;
    hideCardTray();
  }
  enterCellFork();
  // 막다른 길 도달 = '쿵'(삐 + 화면 흔들림). 시작/목표 칸 제외, 들어온 길만 열린 칸.
  if(!G.arrived && G.player!==0 && G.player!==G.goal &&
     cellsAdjacentOpen(G.player).length===1){
    beepBad(); shakeScreen();
  }
  if(G.player===G.goal){ G.arrived = true; onArrive(); }
}
```

(기존 `taken.correct` 보상 블록은 제거 — 보상은 Task 6 `chooseCard`에서 카드 탭 즉시 처리하므로 중복 방지)

- [ ] **Step 2: Playwright 확인 (오답 갈래 → 막다른 쿵, 되돌아오면 트레이 재표시)**

`/tmp/maze-verify.mjs` 에 이어서:

```javascript
const bump = await p.evaluate(async () => {
  const M = window.__maze, G = M._state();
  // 새 1판 재시작해 깨끗한 상태에서 첫 분기로
  M.startLevel(0, 12345);
  document.body.click();
  const S = () => M._state();
  const goTo = (v) => { const n=S().n, cell=S().cell, r=Math.floor(v/n), c=v%n;
    M.setFinger((c+0.5)*cell,(r+0.5)*cell); M.tick(); };
  // 첫 분기까지
  for(const v of S().path){ goTo(v); if(S().activeFork) break; }
  if(!S().activeFork) return 'no-fork';
  const wrong = S().signs.items.find(s=>!s.correct);
  if(!wrong) return 'no-wrong';
  const forkCell = S().activeFork.cell;
  M.chooseCard(wrong);                 // 오답 카드
  // 오답 갈래로 끝까지(막다른) 끌기 — 갈래 방향으로 반복 주입
  let guard=0, hit=false;
  let cur = wrong.branch;
  while(guard++ < 40){
    goTo(cur);
    const open = M.openNeighbors(S().cells, S().n, S().player).filter(x=>x!==forkCell);
    if(open.length===0){ hit=true; break; }      // 막다른
    cur = open[0];
  }
  // 되돌아오기: 분기 칸으로
  for(let i=0;i<40 && S().player!==forkCell;i++){
    const t = S().trail; if(t.length<2) break; goTo(t[t.length-2]);
  }
  const trayBack = document.getElementById('card-tray').classList.contains('show');
  return { hit, trayBack, back: S().player===forkCell };
});
console.log('wrong-branch deadend + return:', JSON.stringify(bump));
```

Run: `node /tmp/maze-verify.mjs`
Expected: `wrong-branch deadend + return: {"hit":true,"trayBack":true,"back":true}`. 콘솔 에러 0.

- [ ] **Step 3: Commit**

```bash
git add maze.html
git commit -m "feat(maze): 분기 떠날 때 정리 + 막다른 쿵(삐+흔들림)"
```

---

## Task 8: 테스트 훅 노출 + 회귀 검증

**Files:**
- Modify: `/Users/eunhuismacbook/Desktop/hanigame/maze.html` (`window.__maze` 463–469, `hint-btn` 437)

- [ ] **Step 1: `chooseCard` 등 훅 노출**

`maze.html:463-469` 의 `Object.assign(window.__maze, {...})` 에 항목 추가:

```javascript
Object.assign(window.__maze, {
  startLevel, setFinger, tick: tickMove, _next: nextLevel,
  chooseCard,
  _state: () => G,
  _forceDraw: () => drawFrame(),
  _onboardingVisible: () => !!(G && G._onbShown),
  _cards: () => (G && G.signs ? G.signs.items : null),
  _trayVisible: () => document.getElementById('card-tray').classList.contains('show'),
  _sampleWall: () => { const g = mazeCache.getContext('2d'); const d = g.getImageData(2*DPR, 1*DPR, 1, 1).data; return d[0]+d[1]+d[2]; },
});
```

- [ ] **Step 2: 🔊 다시듣기 버튼 동작 확인**

`maze.html:437` 핸들러가 `G.signs` 있을 때 `speak(G.hero.word)` 호출 — 변경 없음. 분기 활성 중 🔊 누르면 정답 단어 재발화. 그대로 둔다(확인만).

- [ ] **Step 3: 전체 Playwright 회귀 — 3판 클리어**

`/tmp/maze-verify.mjs` 끝에 통합 클리어 검증 추가:

```javascript
const clear = await p.evaluate(() => {
  const M = window.__maze;
  const S = () => M._state();
  const goTo = (v) => { const n=S().n, cell=S().cell, r=Math.floor(v/n), c=v%n;
    M.setFinger((c+0.5)*cell,(r+0.5)*cell); M.tick(); };
  M.startLevel(0, 999); document.body.click();
  for(let lvl=0; lvl<3; lvl++){
    const path = S().path.slice();
    let guard=0;
    while(S().player !== S().goal && guard++ < 2000){
      // 분기면 정답 카드 선택
      if(S().activeFork && S().unlockedBranch==null){
        const correct = S().signs.items.find(s=>s.correct); M.chooseCard(correct);
      }
      // 해답경로 다음 칸으로 손가락
      const i = path.indexOf(S().player);
      const nextV = i>=0 && i<path.length-1 ? path[i+1] : path[Math.min(path.length-1, 1)];
      goTo(nextV);
    }
    if(S().player !== S().goal) return 'stuck at level '+lvl;
    M._next();   // 도착카드 → 다음 판(마지막은 축하)
  }
  return document.getElementById('celebration').classList.contains('show') ? 'celebrated' : 'no-celebration';
});
console.log('full clear:', clear);
```

Run: `node /tmp/maze-verify.mjs`
Expected: 모든 줄 true/정상 + `full clear: celebrated`. 콘솔 에러 0. 종료코드 0.

- [ ] **Step 4: Commit**

```bash
git add maze.html
git commit -m "test(maze): chooseCard/트레이 테스트 훅 노출 + 회귀 검증"
```

---

## Task 9: 실기기 느낌 수동 QA + 마무리

**Files:** 없음(확인만), 필요 시 미세 조정 후 `maze.html`

- [ ] **Step 1: 브라우저 수동 플레이**

`maze.html`을 크롬/사파리에서 열고 1판 플레이:
- 분기 도달 → 멈춤 + 아래 카드 2~3장 + "fire truck!" 음성.
- 정답 카드 탭 → 딩동 + ✨ + 길 열림 → 끌어 통과.
- 오답 카드 탭 → 그 길 가다 막다른 데서 삐 + 화면 흔들림 → 되돌아오면 카드 다시.
- 카드 안 누르면 분기 통과 불가 확인.
- 도착 → 영어 문장 + 따라 말하기 → 다음 판. 3판 후 축하.

- [ ] **Step 2: iPad 폭(좁은 화면) 확인**

크롬 기기 툴바로 iPad 세로(768px) 에뮬레이트 → 카드 트레이가 미로를 가리지 않고 아래 정렬되는지, 카드 탭 타깃 충분한지 확인. 가리면 `#card-tray bottom` 값 또는 `#maze-wrap` 패딩 조정.

- [ ] **Step 3: 콘솔 에러 0 최종 확인 후 정리 커밋(변경 있으면)**

```bash
git add maze.html
git commit -m "polish(maze): 카드 트레이 레이아웃 미세 조정"
```

(변경 없으면 생략)

---

## Self-Review 결과

- **Spec 커버리지:** v3 사양 A(카드↔길 그림매칭)=Task4, 카드게이트=Task5, 정답보상=Task6, 오답 되돌아오기/막다른 쿵=Task7, 소리(딩동/삐)=Task1, 진동 대체 흔들림=Task2, 카드 트레이 UI=Task3, 테스트 훅=Task8, iPad 레이아웃=Task9. 누락 없음.
- **막다른 단축:** 기존 `pruneDeadEnds(cap=3)` 유지로 오답 갈래 짧음 — 신규 작업 불필요(사양 F 기존 충족).
- **중복 보상 제거:** 기존 `afterMove`의 correct 보상 블록을 Task7에서 삭제, 보상은 `chooseCard`로 일원화(딩동·반짝·발화 1회).
- **타입/이름 일관성:** `unlockedBranch`, `chooseCard`, `showCardTray`/`hideCardTray`, `beepGood`/`beepBad`, `shakeScreen`, `ac`/`tone` 전 태스크 동일.
- **알려진 한계:** 오답 갈래가 드물게 하위 분기를 품으면(완벽미로 특성) 카드 없이 자동정지할 수 있음. cap=3 단축으로 빈도 낮음. 막히면 손가락 되돌리기로 복귀 가능. v1 허용(사양 YAGNI).
