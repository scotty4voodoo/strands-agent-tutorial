# 01. Agent 기초 (Basic Agent)

**Strands Agents SDK**로 단일 Agent를 생성·실행하고, 도구(Tool)를 연결하는 가장 기본적인 방법을 다룹니다.

## 🧠 핵심 개념

Strands Agent의 본질은 **"LLM + 도구 + 반복 루프"** 입니다.

```
입력 ──> ┌─────────────────────────────┐ ──> 응답
          │  Reasoning (LLM)            │
          │     ↓                        │
          │  Tool Selection (도구 선택)  │
          │     ↓                        │
          │  Tool Execution (도구 실행)  │
          │     ↑__________↓ (반복)      │
          └─────────────────────────────┘
```

- **Agent**: LLM을 감싸 입력을 받고, 필요하면 도구를 호출하며, 최종 응답을 만드는 단위
- **Tool**: Agent가 호출할 수 있는 기능 (내장 도구 또는 `@tool`로 만든 커스텀 함수)
- **Agent Loop**: Agent가 "추론 → 도구 선택 → 도구 실행"을 **스스로 판단해 반복**하는 흐름
- **AgentResult**: 실행 결과 + 추적(trace)·메트릭 등 관측 데이터를 함께 담은 반환 객체

> 💡 Strands는 기본적으로 **Amazon Bedrock + Claude** 모델을 사용합니다. 모델은 문자열 ID나 `BedrockModel` 인스턴스로 바꿀 수 있습니다.

## 📂 파일 구성

| 파일 | 수준 | 내용 |
|------|:----:|------|
| `main.py` | 기초 | Agent 생성 · 내장 도구 · 커스텀 `@tool` · 실행 |
| `advanced.py` | 심화 | 모델 지정 · 콜백/스트리밍 · 메트릭·트레이스 확인 |

## 🚀 실행 방법

```bash
python 01_basic_agent/main.py
```

> ⚠️ 실행하려면 AWS 자격 증명과 Amazon Bedrock 모델 접근 권한이 필요합니다. (루트 [README](../README.md)의 사전 요구사항 참고)

---

## 📘 main.py — 기초

내장 도구와 직접 만든 커스텀 도구를 함께 쓰는 Agent입니다.

```python
from strands import Agent, tool
from strands_tools import calculator, current_time

# @tool 데코레이터로 일반 파이썬 함수를 도구로 등록
@tool
def letter_counter(word: str, letter: str) -> int:
    """단어 안에서 특정 글자의 등장 횟수를 센다."""
    return word.lower().count(letter.lower())

# 내장 도구 + 커스텀 도구를 가진 Agent
agent = Agent(tools=[calculator, current_time, letter_counter])

agent("지금 몇 시야? 그리고 'strawberry'에 R이 몇 개 있어?")
```

- **도구 선택은 Agent가 자동으로** 합니다 — 질문 내용에 따라 어떤 도구를 쓸지 스스로 판단합니다.
- `@tool` 함수의 **docstring과 타입힌트**가 곧 도구 설명서가 되므로 명확히 작성해야 합니다.

---

## 📗 advanced.py — 심화

| 주제 | 내용 |
|------|------|
| **모델 지정** | 문자열 ID 또는 `BedrockModel`(region·temperature 등)로 모델 제어 |
| **콜백/스트리밍** | `callback_handler=None`로 출력 끄기, `stream_async()`로 실시간 스트리밍 |
| **관측(Observability)** | `result.metrics.get_summary()`로 토큰·지연·도구 사용 통계 확인 |

```python
from strands import Agent
from strands.models import BedrockModel

model = BedrockModel(model_id="anthropic.claude-sonnet-4-20250514-v1:0",
                     region_name="us-west-2", temperature=0.3)
agent = Agent(model=model)

result = agent("What is the square root of 144?")
print(result.metrics.get_summary())   # 토큰·지연·도구 사용 요약
```

> 💡 메트릭·트레이스는 디버깅과 비용 최적화의 출발점입니다. 자세한 관측성은 [08장](../08_observability)에서 다룹니다.

---

## 🔗 관련 챕터

- [02. Agent-to-Agent 통신](../02_agent_to_agent) — 여러 Agent를 잇는 첫걸음
- [03. Graph 패턴](../03_graph_pattern) — 본격 Multi-Agent 오케스트레이션
- [Strands 공식 Quickstart](https://strandsagents.com/latest/documentation/docs/user-guide/quickstart/)
