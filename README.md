# diagram-design-mono

Claude Code에서 아키텍처, 플로차트, 시퀀스 등 45종 다이어그램을 HTML/SVG로 그리는 스킬. 모든 글자는 JetBrains Mono, 모든 박스는 직각, 노드에 마우스를 올리면 주황색으로 바뀜.

[cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design)(MIT)을 고친 포크. 레이아웃 규칙과 다이어그램 유형은 원본과 같고, 스타일만 다름.

## 원본과 다른 점

| 항목 | 원본 | 이 스킬 |
|---|---|---|
| 폰트 | Instrument Serif, Geist, Geist Mono | JetBrains Mono 하나 (한글은 Noto Sans KR) |
| 박스 모서리 | `rx=6` 둥근 모서리 | 직각 (`rx` 없음) |
| 연결선 꺾임 | 둥근 꺾임 `r=8` | 원본과 같음 |
| 색상 | 회백색 바탕, 다홍색 강조 | turbopuffer.com 참고: 슬레이트 바탕 `#f8fafc`, 남색 글자 `#0f172a`, 주황 강조 |
| 호버 | 없음 | 노드, 카드, 셀, 막대에 마우스를 올리면 `#fdba75` 주황 배경 |
| 첫 실행 | 브랜드 설정 질문 | 질문 없이 바로 그림 |

호버 제외: Sankey와 polar 차트. 이 두 유형의 검증 스크립트가 도형에 CSS 적용을 막음.

## 1. 설치

Claude Code에서 아래 두 줄 실행.

```
/plugin marketplace add OWNER/diagram-design-mono
/plugin install diagram-design-mono@diagram-design-mono
```

- `OWNER`: 이 저장소를 올린 GitHub 계정
- 비공개 저장소면 설치하는 사람에게 저장소 읽기 권한과 git 인증 필요

플러그인 없이 쓰려면 스킬 폴더만 복사.

```bash
# 나만 쓰기
cp -r skills/diagram-design-mono ~/.claude/skills/
# 프로젝트 팀과 같이 쓰기 (git에 커밋)
cp -r skills/diagram-design-mono <프로젝트>/.claude/skills/
```

claude.ai 웹이나 데스크톱 앱에서 쓰려면 `skills/diagram-design-mono` 폴더를 zip으로 압축한 뒤 Settings의 Capabilities(Skills)에 업로드.

## 2. 사용

Claude Code에 그리고 싶은 내용을 말하면 스킬이 자동으로 선택됨.

```
결제 서비스 아키텍처를 다이어그램으로 그려줘. API Gateway, 결제 API, PostgreSQL, Kafka 포함
```

결과는 HTML 파일 하나. 브라우저로 열어서 노드 위에 마우스를 올리면 호버 확인 가능.

PNG/SVG 내보내기, draw.io/Mermaid/Excalidraw 가져오기는 원본과 같은 명령 사용: `/export-diagram`, `/import-drawio`, `/import-mermaid`, `/import-excalidraw`.

## 3. 스타일 바꾸기

색상만 바꾸려면 `skills/diagram-design-mono/references/style-guide.md`의 토큰 표 수정. 폰트, 직각 모서리, 호버 규칙은 `SKILL.md` 4장, 5장, 6장, 9장에 있음.

## 저장소 구성

| 경로 | 내용 |
|---|---|
| `skills/diagram-design-mono/SKILL.md` | 스킬 본문 |
| `skills/diagram-design-mono/references/` | 유형별 규칙, 스타일 가이드 |
| `skills/diagram-design-mono/assets/` | 템플릿과 예제 HTML 217개 |
| `commands/` | 슬래시 명령 |
| `scripts/` | 원본의 검증 스크립트 (새 스타일 기준으로 수정) |

예제 HTML은 원본 예제를 스크립트로 변환한 것. 레이아웃은 원본 폰트 기준이라, 긴 라벨은 박스에 빠듯할 수 있음.

## 라이선스

MIT. 원저작권 Cathryn Lavery, 수정분 포함 전체 조건은 [LICENSE](LICENSE).
