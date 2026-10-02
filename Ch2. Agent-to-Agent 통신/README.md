# 02. Agent-to-Agent 통신 (A2A)

여러 Agent가 서로 **발견(discover)하고, 통신하고, 협업**하도록 잇는 방법을 다룹니다. Strands는 개방형 표준인 **A2A(Agent-to-Agent) 프로토콜**을 지원합니다.

## 🧠 핵심 개념

Multi-Agent 패턴(Graph·Swarm·Workflow)으로 들어가기 전, **"Agent끼리 어떻게 말을 거는가"** 를 이해하는 단계입니다.

```
┌───────────────┐        A2A 프로토콜        ┌───────────────┐
│ 오케스트레이터 │ ───(discover/invoke)───>  │  원격 Agent    │
│   (클라이언트)  │ <──(AgentResult 응답)──── │  (A2A 서버)    │
└───────────────┘                            └───────────────┘
```

- **A2A 프로토콜**: AI Agent가 플랫폼·구현에 상관없이 서로 발견·통신·협업하도록 정의한 **개방 표준**
- **A2A 서버**: 하나의 Strands Agent를 네트워크에 노출(expose)한 것
- **A2A 클라이언트(`A2AAgent`)**: 원격 Agent를 **로컬 Agent처럼** 호출하는 래퍼
- **Agent Card**: 원격 Agent의 이름·설명·보유 스킬 등 메타데이터

### 왜 A2A인가 (Use Cases)

- **Multi-Agent 워크플로우**: 전문 Agent들을 체인으로 연결
- **Agent 마켓플레이스**: 서로 다른 제공자의 Agent를 발견·사용
- **크로스 플랫폼 통합**: Strands Agent를 다른 A2A 호환 시스템과 연결
- **분산 AI 시스템**: 확장 가능한 분산 Agent 아키텍처 구축

## 📂 파일 구성

| 파일 | 수준 | 내용 |
|------|:----:|------|
| `server.py` | 기초 | Strands Agent를 A2A 서버로 노출 |
| `client.py` | 기초 | `A2AAgent`로 원격 Agent 호출 |
| `advanced.py` | 심화 | 원격 Agent를 도구(tool)로 래핑 · Agent Card 조회 |

## ⚙️ 설치

A2A 기능은 별도 extra가 필요합니다.

```bash
pip install 'strands-agents[a2a]'
```

## 🚀 실행 방법

```bash
# 터미널 1 — 서버 실행 (기본 127.0.0.1:9000)
python 02_agent_to_agent/server.py

# 터미널 2 — 클라이언트에서 원격 호출
python 02_agent_to_agent/client.py
```

---

## 📘 기초 — 서버와 클라이언트

### 서버: Agent를 네트워크에 노출

```python
from strands import Agent
from strands.multiagent.a2a import A2AServer
from strands_tools.calculator import calculator

strands_agent = Agent(
    name="Calculator Agent",
    description="기본 산술 연산을 수행하는 계산기 에이전트",
    tools=[calculator],
    callback_handler=None,
)

A2AServer(agent=strands_agent).serve()   # 기본 127.0.0.1:9000
```

### 클라이언트: 원격 Agent를 로컬처럼 호출

```python
from strands.agent.a2a_agent import A2AAgent

a2a_agent = A2AAgent(endpoint="http://localhost:9000")
result = a2a_agent("Show me 10 ^ 6")
print(result.message)   # 로컬 Agent와 동일한 AgentResult 반환
```

> 💡 `A2AAgent` 없이 하면 Agent Card 해석·HTTP 클라이언트 구성·메시지 빌드·응답 파싱을 전부 수동으로 해야 합니다. `A2AAgent`가 이 모두를 자동 처리합니다.

---

## 📗 advanced.py — 심화

| 기법 | 내용 |
|------|------|
| **원격 Agent를 도구로** | `@tool` 안에서 `A2AAgent`를 호출해 오케스트레이터의 도구로 편입 |
| **Agent Card 조회** | `get_agent_card()`로 원격 Agent의 이름·설명·스킬 확인 |
| **비동기/스트리밍** | `invoke_async()` · `stream_async()`로 async 워크플로우 통합 |

```python
from strands import Agent, tool
from strands.agent.a2a_agent import A2AAgent

calculator_agent = A2AAgent(endpoint="http://calculator-service:9000", name="calculator")

@tool
def calculate(expression: str) -> str:
    """수학 계산을 수행한다."""
    result = calculator_agent(expression)
    return str(result.message["content"][0]["text"])

orchestrator = Agent(system_prompt="계산은 calculate 도구를 써라.", tools=[calculate])
```

### ⚠️ 패턴별 지원 현황

| 패턴 | A2AAgent 지원 |
|------|:---:|
| 오케스트레이터 **도구(tool)** | ✅ |
| **Graph** 워크플로우 노드 | ✅ |
| **Swarm** | ❌ (handoff가 요구하는 기능 미지원 → Graph 사용) |

---

## 🔗 관련 챕터

- [01. Agent 기초](../01_basic_agent) — 단일 Agent·도구의 기본
- [03. Graph 패턴](../03_graph_pattern) — 원격 A2A Agent를 노드로 혼합 가능
- [A2A 공식 문서](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/multi-agent/agent-to-agent/)
