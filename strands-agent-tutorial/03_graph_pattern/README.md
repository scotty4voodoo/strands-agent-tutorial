# 03. Graph 패턴 (Graph Pattern)

여러 Agent의 실행 흐름을 **노드(Agent)**와 **엣지(연결)**로 명시적으로 정의하는 Multi-Agent 오케스트레이션 패턴입니다.

## 🧠 핵심 개념

Graph 패턴의 본질은 단 4단계입니다.

```
1. Agent 정의        → 노드가 될 재료
2. add_node/add_edge → 노드 추가 + 흐름 연결
3. build() + 실행
4. 결과 확인
```

- **노드(Node)**: 하나의 작업 단위 (Agent, 함수, 또는 Swarm까지 가능)
- **엣지(Edge)**: 노드 간 실행 순서와 데이터 흐름
- **병렬 실행**: 같은 노드에 의존하는 여러 노드는 자동으로 병렬 실행
- **입력 전파**: 각 노드는 `원본 입력 + 앞선 노드들의 결과`를 함께 전달받음

## 📂 파일 구성

| 파일 | 수준 | 내용 |
|------|:----:|------|
| [`main.py`](./main.py) | 기초 | 노드·엣지·병렬 흐름의 기본 |
| [`advanced.py`](./advanced.py) | 심화 | 커스텀 노드 · Swarm 합성 · 조건부 엣지 |

## 🚀 실행 방법

```bash
# 기초 예제
python 03_graph_pattern/main.py

# 심화 예제 (3가지 기법 모두 실행)
python 03_graph_pattern/advanced.py
```

---

## 📘 main.py — 기초

`research → (analysis + fact_check 병렬) → report` 흐름을 구현합니다.

```
research(연구) ──┬──> analysis(분석) ──┐
                 │                      ├──> report(리포트)
                 └──> fact_check(검증) ─┘
```

- `analysis`와 `fact_check`는 `research` 완료 후 **병렬**로 실행됩니다.
- `report`는 두 노드가 **모두 끝나야** 실행됩니다.
- 이 구조 덕분에 순차 실행 대비 `min(T_analysis, T_fact_check)` 만큼 시간을 절약합니다.

---

## 📗 advanced.py — 심화

기초 흐름을 이해한 뒤 볼 것을 권장합니다. 각 기법은 독립 함수로 분리되어 골라 실행할 수 있습니다.

| 함수 | 기법 | 흐름 |
|------|------|------|
| `run_custom_nodes()` | **커스텀 함수 노드** — Agent가 아닌 일반 파이썬 함수를 노드로 사용 | `validate(함수) → process(Agent) → format(함수)` |
| `run_swarm_as_node()` | **Swarm 합성** — Swarm 자체를 하나의 그래프 노드로 사용 (패턴 조합) | `Swarm → verify → finalize` |
| `run_conditional_edges()` | **조건부 엣지** — 리뷰 결과에 따라 분기/반복 | `writer → reviewer → (통과: publisher / 미달: writer 반복)` |

> 💡 **커스텀 함수 노드**는 LLM 호출 없이 결정적인 로직(검증·포맷팅 등)을 그래프 안에 넣을 때 유용합니다.
> **Swarm 합성**은 Graph와 Swarm 패턴을 조합하는 방법을 보여줍니다 (자세한 Swarm은 [04장](../04_swarm_pattern) 참고).

---

## 🔗 관련 챕터

- [04. Swarm 패턴](../04_swarm_pattern) — 자율 협업 Multi-Agent
- [05. Workflow 패턴](../05_workflow_pattern) — 순차/조건 기반 파이프라인
- [06. 패턴 비교](../06_pattern_comparison) — Graph vs Swarm vs Workflow
