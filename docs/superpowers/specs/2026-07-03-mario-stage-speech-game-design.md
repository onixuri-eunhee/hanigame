# 🍄 마리오 무대 계단 — 영어 말하기 대회 최종 연습 게임 (설계)

날짜: 2026-07-03 · 대회 D-2 · 대상: 승한 (6세)
파일: `stage.html` (단일 HTML, index.html 등록)

## 1. 목적

영어 말하기 대회 원고(14문장)를 **외우기 불안 → 자신감** 순서로 훈련.
성공 경험 중심 — 실패해도 혼내지 않고 힌트로 이어감.

## 2. 원고 (문장 분할, 14계단)

| # | 문장 | 그림 (images/) |
|---|---|---|
| 1 | Hello, everyone! | 01_hello.png |
| 2 | My name is 승한. | 02_my_name.png |
| 3 | I am six years old. | 03_six_years.png |
| 4 | Today, I want to talk about my future jobs. | — (신규 생성) |
| 5 | I want to be a firefighter. | 04_want_firefighter.png |
| 6 | Firefighters are brave. | 05_brave_firefighter.png |
| 7 | They help people and save lives. Woo-woo! | 06_help_people.png / 07_save_lives.png / 08_woo_woo.png |
| 8 | I also want to be a police officer. | 09_police.png |
| 9 | Police officers are strong and catch bad guys to keep us safe. | 10_strong.png / 11_catch.png / 12_keep_safe.png |
| 10 | I would also like to be a doctor. | 13_doctor_child.png |
| 11 | Doctors are kind because help sick people feel better. | 14_doctors_kind.png / 15_help_sick.png |
| 12 | A firefighter, police officer and doctor are what I want to be! | — (신규 생성) |
| 13 | I want to help people! That is my dream. | — (신규 생성) |
| 14 | Thank you! | — (신규 생성) |

- 원고 텍스트는 대회 원고 그대로 유지 (11번 문법 포함 — 아이가 외운 그대로 인정).
- "승한" 이름: 영어 인식기가 한국 이름을 못 알아들으므로 **이름 단어는 자동 통과 처리**.

## 3. 훈련 3단계 (월드 1 → 2 → 3)

| 월드 | 이름 | 화면에 보이는 것 | 통과 조건 |
|---|---|---|---|
| 1 | 보고 말하기 | 문장 전체 + 그림 | 문장 말하면 통과 |
| 2 | 힌트만 보기 | 각 문장 첫 단어 + 그림 | 기억해서 말하면 통과 |
| 3 | 진짜 무대 | 아무것도 안 보임 (그림만 작게) | 처음부터 끝까지 순서대로 |

- 월드 클리어마다 "WORLD CLEAR!" 팡파레 + 별 획득.
- 월드 3 클리어 = 우승 트로피 + 폭죽 + 관중 환호.

## 4. 3D 무대 (Three.js)

- **Three.js r160** CDN 로드 (인터넷 필요).
- 장면: 마리오풍 벽돌 계단 14칸 → 정상에 깃대 + 성. 하늘, 구름, 물음표 블록 장식.
- 캐릭터: 마리오풍 소년 영웅 스프라이트(gpt-image-2 생성, 투명 배경) 빌보드.
  - 포즈 3종: 서있기 / 점프 / 만세(승리).
- 문장 성공 → 점프 애니메이션으로 한 칸 위로, 카메라 부드럽게 따라감, 코인 +1.
- 14칸 정상 도달 → 깃대 잡고 미끄러져 내려오는 마리오식 클리어 연출 → 성 문에서 폭죽.
- 계단마다 밟으면 조명 켜짐(밟은 칸은 금색으로 변함) — 진행 상황이 한눈에 보임.
- 3D 실시간 애니메이션으로 충분하므로 **seedance 영상 생성은 사용하지 않음** (필요 시 우승 컷신용으로 예약, FAL 키 위치: `~/Documents/2026plans/.env` 확인 완료).

## 5. 이미지 (gpt-image-2 생성)

생성 스크립트: `~/.claude/skills/blog-auto-pipeline/scripts/gpt_image_2.py` 방식 재사용
(OPENAI_API_KEY: `~/Documents/2026plans/.env` 확인 완료). 저장: `images/stage/`.

| 파일 | 내용 | 비고 |
|---|---|---|
| hero_idle.png | 마리오풍 소년(빨간 모자 S 마크, 파란 멜빵바지) 서있기 | 투명 배경 |
| hero_jump.png | 같은 캐릭터 점프 | 투명 배경 |
| hero_win.png | 같은 캐릭터 만세 | 투명 배경 |
| bg_castle.png | 마리오풍 성 + 언덕 + 하늘 파노라마 | 배경 텍스처 |
| 04_future_jobs.png 등 4장 | 표의 "신규 생성" 문장 그림 (기존 그림체와 통일) | 흰 배경 카드 |

- 상표 캐릭터 그대로 복제 금지 → "마리오 스타일의 오리지널 소년 영웅"으로 생성 (개인 가정용).
- rule-stacking-check 준수: 프롬프트는 자연어 1~2문장, 룰 자동 삽입 없음.

## 6. 소리 (완전 설계)

### 6-1. 효과음 — WebAudio 칩튠 합성 (파일 없음, 코드로 생성, 저작권 무관)

| 이벤트 | 소리 | 구성 |
|---|---|---|
| 시작 버튼 | 뿅 | 사각파 상승 2음 |
| 마이크 켜짐 | 띠링 | 사인파 고음 1회 |
| 정답 | 코인 소리 | B5→E6 사각파 (마리오 코인 오마주, 오리지널 합성) |
| 점프 | 슝~ | 주파수 스윕 상승 |
| 오답/못 알아들음 | 붕 (부드럽게) | 낮은 삼각파 1음 — 무섭지 않게 |
| 힌트 열기 | 딸깍 | 노이즈 버스트 짧게 |
| 월드 클리어 | 팡파레 | 아르페지오 5음 + 화음 |
| 최종 우승 | 대형 팡파레 + 환호 | 화음 진행 + 노이즈 셰이핑 박수/환호 |

### 6-2. 배경음악 — 오리지널 칩튠 루프 (WebAudio 시퀀서)

- 밝은 장조 8마디 루프, 사각파 멜로디 + 삼각파 베이스 + 노이즈 하이햇.
- 볼륨 낮게(효과음의 40%). 🔊 버튼으로 켜고 끄기.
- **음성 인식 중 자동 일시정지** — 마이크가 음악을 주워듣는 오인식 방지 (핵심).

### 6-3. 문장 듣기 (TTS)

- robot.html의 speechSynthesis 방식 재사용: en-US 여성 음성, 속도 0.85.
- "들려줘 🔈" 버튼 — 막힌 문장을 원어민 음성으로 들려줌.
- 힌트 3단계 마지막에 자동 재생.

## 7. 음성 인식

- `webkitSpeechRecognition`, lang `en-US`, continuous=false, interimResults=true.
- 매칭: 소문자화 + 구두점 제거 후 단어 단위 비교. **60% 이상 일치 = 통과** (6세 발음 관대 기준).
- "승한"·의성어("Woo-woo") 단어는 매칭에서 제외(자동 인정).
- 인식 중 화면에 실시간 자막 표시 — 아이가 자기 말이 전달되는 걸 봄.
- 3회 연속 실패 → 힌트 자동 확장 (첫 단어 → 절반 → 전체+TTS). 실패 벌점 없음.
- 브라우저: Chrome 전제 (기존 게임들과 동일).

## 8. 화면 구성

```
┌──────────────────────────────┐
│  🍄 WORLD 1-1   ⭐×2  🪙×9   │  ← 상단 HUD
│                              │
│      [ 3D 무대 계단 ]         │  ← Three.js 캔버스 (화면 70%)
│                              │
├──────────────────────────────┤
│  그림 카드 │ 문장/힌트 표시    │  ← 하단 패널
│  🎤 말하기  🔈 들려줘  💡 힌트 │  ← 큰 버튼 3개 (6세 손가락 크기)
└──────────────────────────────┘
```

- 태블릿/PC 가로 화면 기준. 버튼 최소 64px.
- 시작 화면: 월드 선택 (1·2·3) + 소리 켜기 버튼(브라우저 오디오 정책상 첫 터치 필요).

## 9. 오류 처리

- 마이크 권한 거부 → 안내 그림 + "설정에서 마이크 허용" 한국어 안내.
- 인터넷 없음(Three.js 로드 실패) → 2D 계단 폴백 화면으로 동일 게임 진행.
- 음성 인식 미지원 브라우저 → "Chrome으로 열어주세요" 안내.

## 10. 검증 계획

- Playwright/브라우저로 실제 렌더 확인 (verification-grounding: 진짜 렌더러 실행).
- 음성 인식은 콘솔 주입 테스트 함수(`window.__testSay("hello everyone")`)로 14문장 전체 통과 시나리오 자동 검증.
- 3단계 월드 전환·클리어 연출·폴백 화면 수동 확인.

## 11. 범위 제외 (YAGNI)

- 점수 서버 저장, 다국어, 다른 원고 편집 UI — 안 함.
- seedance 영상 컷신 — 기본 제외, 3D 연출로 충분.
