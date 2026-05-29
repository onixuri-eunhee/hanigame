# 의사 미니게임 재설계 — "치료 순서 따라하기" (사이먼 메모리 게임)

날짜: 2026-05-29
대상 파일: `/Users/eunhuismacbook/Desktop/hanigame/speech.html`
대상 함수: `doctorMG(canvas, ctx)` (현 849~918행) 전체 교체

## 배경 / 문제

기존 `doctorMG`는 "환자에게 대시해서 치료" 액션 게임. 환자 스폰 코드 버그로
환자가 화면에 거의 안 나타남:

```js
patients.forEach(p=>{p.x+=p.spd; ...});   // spd=0.5, dt 미적용 → 초당 30px만 이동
patients.push({x:fromLeft?-20:W+20, ...}); // 화면 밖에서 시작
```

→ 환자가 화면 밖에서 매우 느리게 기어와 사실상 안 보임.

대표 요청: 버그 수정에 더해, 6살(한승한) 영어 말하기 대회 준비 앱에 맞게
**두뇌(기억력)를 쓰는 미니게임**으로 재설계.

## 게임 개념 — 사이먼(Simon) 방식

의사가 치료 순서를 보여주면 아이가 똑같은 순서로 버튼을 누른다. 기억력 게임.

치료 3종 (기존 하단 버튼 ◀✊▶ 재활용, 라벨만 교체):
- 0 = 💊 pill (약) — btn-left / ←
- 1 = 🩹 bandage (밴드) — btn-space / space
- 2 = 💉 shot (주사) — btn-right / →

각 버튼에 영어 단어도 표시 (말하기 대회 앱 보너스 학습).

## 게임 흐름

1. **showSequence(보여주기)**: 현재 순서 배열을 하나씩 깜빡임 + 음 재생.
   해당 치료 emoji를 화면 중앙에 크게 강조. 한 항목 ~0.55s, 사이 간격 ~0.2s.
2. **input(따라하기)**: 아이가 버튼 탭. 누른 값과 `sequence[inputIdx]` 비교.
   - 맞음 → 초록 반짝(burst) + 콤보(addCombo), `inputIdx++`.
   - 한 줄 완료(`inputIdx === sequence.length`) → stage 클리어.
   - 틀림 → `snd('hit')` + shake → 거기까지 stage 점수로 종료.
3. stage 클리어 시 `sequence.push(random 0..2)`, `stage++`, 다시 showSequence.
4. **stage 5(순서 5개) 성공 → 클리어** 🏆 (`mgEndGame`).

시작값: `sequence = [random 0..2]`, `stage = 1`, mode = 'show'.
**타이머 없음** (기억 게임이라 6살에게 시간 압박 제거).

## 상태 변수

- `sequence` : number[] (값 0/1/2)
- `stage` : 1..5
- `mode` : 'show' | 'input' | 'pause'
- `showIdx`, `showT` : 보여주기 진행 인덱스/타이머
- `inputIdx` : 입력 진행 인덱스
- `flash` : {btn, t} 현재 강조 중인 버튼 + 잔광
- `prevL/prevS/prevR` : 버튼 rising-edge 감지용 이전 상태

## 입력 처리

기존 터치/마우스/키보드 핸들러가 `mgKeys.left/space/right`를 이미 채워줌.
루프 안에서 rising-edge(이전 false → 현재 true) 감지로 "탭 1회"를 잡는다.
(fireFighterMG의 `mgSpacePrev` 패턴과 동일, 3버튼으로 확장.)

## 화면 (캔버스 그리기)

- 배경: 기존 의사 게임 초록 테마 재사용 (`#040F08`→`#080F04`, 의료 십자 패턴).
- 상단: 👨‍⚕️ 의사 + "단계 N/5" 텍스트, mode 안내("잘 봐!" / "따라 눌러!").
- 중앙: showSequence 중 강조되는 치료 emoji 크게.
- 하단: 치료 버튼 3개 그림(emoji + 영어 단어), 현재 강조/입력된 버튼 하이라이트.
- 파티클/콤보/shake: 기존 헬퍼(`burst`, `addCombo`, `drawCombo`, `applyShake`,
  `updateP/F`, `drawP/F`, `spawnStars`) 재사용.

## 소리

- 버튼별 음 구분: getAC()로 간단 tone (pill=523Hz, bandage=659Hz, shot=784Hz).
- 정답 콤보: 기존 `addCombo`(내부 snd) 활용. 오답: `snd('hit')`. 클리어: `mgEndGame`(내부 `snd('win')`).

## 버튼 라벨 복원

`doctorMG`가 하단 버튼 라벨을 💊🩹💉로 교체하므로,
`startMiniGame`에서 게임 호출 직전에 항상 `◀ ✊ ▶`로 먼저 초기화 →
fireFighter/police 게임은 영향 없음.

## 범위

- `speech.html`의 `doctorMG` 함수 1개 교체 + `startMiniGame`에 버튼 라벨 초기화 2~3줄 추가.
- 다른 미니게임·다른 파일 변경 없음.

## 검증

- 의사 게임 진입 → 순서 보여주기 동작 → 정답 따라하면 단계 증가 → 5단계 클리어 화면.
- 일부러 틀리면 종료 화면 + 도달 단계 표시.
- fireFighter/police 게임 버튼 라벨이 ◀✊▶로 정상 표시.
- iPad 터치/PC 키보드 둘 다 입력.
