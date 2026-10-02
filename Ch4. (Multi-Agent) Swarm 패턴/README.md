# 04. Swarm 패턴 (Swarm Pattern)

중앙 제어 없이, 여러 Agent가 **스스로 다음 적임자에게 작업을 넘기며(handoff)** 자율적으로 협업하는 Multi-Agent 패턴입니다.

## 🧠 핵심 개념

Graph 패턴이 **개발자가 흐름을 고정**한다면, Swarm 패턴은 **흐름을 Agent들이 런타임에 결정**합니다.

```
Graph : 개발자가 노드/엣지를 미리 그린다  (명시적 · 결정적)
Swarm : 각 Agent가 공유 컨텍스트를 보고   (자율적 · 동적)
        "다음은 누가 해야 할지" 스스로 판단해 넘긴다
```

- **자율 분배(Dynamic distribution)**: 흐름이 코드에 고정돼 있지 않다
- **공유 컨텍스트(Shared context)**: 각 Agent는 전체 작업과 "지금까지 누가 무엇을 했는지"를 함께 본다
- **작업 이관(Handoff)**: `handoff_to_agent` 도구로 다음 Agent에게 넘긴다
- **집단 지성(Collective intelligence)**: 여러 전문 Agent의 기여가 공유 지식으로 누적된다

> 💡 "흐름을 모를 때, 혹은 문제에 따라 흐름이 달라져야 할 때" Swarm이 빛납니다.
> 반대로 흐름이 명확히 고정돼 있다면 [03장 Graph](../03_graph_pattern)가 더 예측 가능합니다.

## 📂 파일 구성

| 파일 | 수준 | 내용 |
|------|:----:|------|
| [`main.py`](./main.py) | 기초 | Swarm 구성 · 자율 handoff 기본 흐름 |
| [`advanced.py`](./advanced.py) | 심화 | 폭주 방지 안전 파라미터 · 결과(SwarmResult) 분석 |

## 🚀 실행 방법

```bash
# 기초 예제
python 04_swarm_pattern/main.py

# 심화 예제 (안전 설정 + 결과 분석)
python 04_swarm_pattern/advanced.py
```

---

## 📘 main.py — 기초

`coordinator → researcher → coder → reviewer` 로 **이어질 수 있는** 자율 협업을 구현합니다. (고정된 순서가 아니라 Agent들이 판단해 넘깁니다.)

```
coordinator(조율) ──handoff──> researcher(조사)
                                 │ handoff
                                 ▼
                             coder(구현) ──handoff──> reviewer(검토)
```

- 엣지를 **그리지 않습니다**. `entry_point`만 지정하면 나머지는 Agent들이 결정합니다.
- 각 Agent의 `name`은 handoff 대상 식별자이므로 **반드시 지정**해야 합니다.
- 넘길 곳이 없다고 판단되면 Swarm이 스스로 종료됩니다.

---

## 📗 advanced.py — 심화

자율성이 높은 만큼 **폭주를 막는 안전장치**가 핵심입니다. 각 기법은 독립 함수로 분리되어 골라 실행할 수 있습니다.

| 함수 | 주제 | 다루는 것 |
|------|------|-----------|
| `run_safe_swarm()` | **안전 파라미터** | 이관/반복 상한, 타임아웃, 핑퐁(반복 이관) 감지 |
| `inspect_swarm_result()` | **결과 분석** | `SwarmResult`에서 실행 경로·노드별 결과 꺼내기 |

### 안전 파라미터 요약

| 파라미터 | 역할 |
|----------|------|
| `max_handoffs` | 전체 작업 이관 횟수 상한 |
| `max_iterations` | Agent 실행 총 횟수 상한 |
| `execution_timeout` | 전체 Swarm 제한 시간(초) |
| `node_timeout` | 개별 Agent 1회 실행 제한 시간(초) |
| `repetitive_handoff_detection_window` | 핑퐁 감지 구간(최근 N회 이관) |
| `repetitive_handoff_min_unique_agents` | 그 구간에 등장해야 할 최소 Agent 수 |

> ⚠️ `A→B→A→B` 처럼 두 Agent가 서로에게만 계속 넘기는 **핑퐁**은
> `repetitive_handoff_*` 설정으로 감지해 중단시킬 수 있습니다.

### SwarmResult 주요 필드

| 필드 | 의미 |
|------|------|
| `status` | `COMPLETED` / `FAILED` 등 종료 상태 |
| `node_history` | 작업을 거친 Agent 순서 (분배·핑퐁 패턴 확인) |
| `results` | 노드별 상세 결과 (`node_id → NodeResult`) |
| `execution_time` | 총 실행 시간(ms) |

---

## 🔗 관련 챕터

- [03. Graph 패턴](../03_graph_pattern) — 개발자가 흐름을 고정하는 방식 (Swarm과 대비)
- [05. Workflow 패턴](../05_workflow_pattern) — 순차/조건 기반 파이프라인
- [06. 패턴 비교](../06_pattern_comparison) — Graph vs Swarm vs Workflow, 언제 무엇을 쓸까
