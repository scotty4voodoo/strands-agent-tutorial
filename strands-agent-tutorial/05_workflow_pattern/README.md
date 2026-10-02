# 05. Workflow 패턴 (Workflow Pattern)

각 Agent가 **정해진 순서**대로 전문 작업을 수행하고, 앞 단계의 출력이 다음 단계의 입력이 되는 **재현 가능한 파이프라인** 패턴입니다.

## 🧠 핵심 개념

세 Multi-Agent 패턴 중 Workflow는 **"정해진 절차를 매번 똑같이"** 돌릴 때 가장 명확합니다.

```
Graph    : 노드/엣지로 흐름을 그린다        (분기·병렬·반복, 그래프 구조)
Swarm    : 흐름이 자율적                     (Agent가 handoff로 결정)
Workflow : 흐름이 선형적이고 반복 가능하다   (정해진 단계의 재현 가능한 실행)
```

Workflow 아키텍처의 3요소:

1. **작업 정의·분배** — 각 Agent가 무엇을 할지 명확히 규정하고 적임자에게 배정
2. **의존성 관리** — 순차 의존 / 병렬 실행 / 합류(join) 지점
3. **정보 흐름** — 한 Agent의 출력 → 다음 Agent의 입력, 단계별 상태 추적

> 💡 가장 기본적인 Workflow는 **별도 오케스트레이터 없이 함수로 단계를 잇는 것**으로 충분합니다.
> 복잡한 조정이 필요하면 Strands의 내장 `workflow` 도구를 쓸 수도 있습니다.

### 언제 Workflow를 쓰나

- 뚜렷한 **순차 단계**가 있는 복잡한 다단계 프로세스
- 단계마다 **다른 전문성**이 필요할 때
- 특정 작업이 **다른 작업의 완료를 기다려야** 할 때 (의존성)
- 실패한 단계만 **재시도**하고 전체는 재시작하지 않아야 할 때 (에러 복구)
- 각 단계의 **감사·추적**이 필요할 때

> 반대로, 흐름이 유동적이거나 Agent 간 대화가 많이 필요하면 [Swarm](../04_swarm_pattern)·[Graph](../03_graph_pattern)를 고려하세요.

## 📂 파일 구성

| 파일 | 수준 | 내용 |
|------|:----:|------|
| [`main.py`](./main.py) | 기초 | 선형 순차 파이프라인 (research → analysis → report) |
| [`advanced.py`](./advanced.py) | 심화 | 병렬 후 합류(join) · 단계별 재시도(retry) |

## 🚀 실행 방법

```bash
# 기초 예제
python 05_workflow_pattern/main.py

# 심화 예제 (병렬+합류, 재시도)
python 05_workflow_pattern/advanced.py
```

---

## 📘 main.py — 기초

```
researcher(조사) ──> analyst(분석) ──> writer(작성)
```

- 각 단계의 **출력이 다음 단계의 입력**으로 그대로 전달됩니다.
- 별도 프레임워크 없이 **함수로 Agent를 순서대로 호출**하는 가장 단순한 형태입니다.
- `callback_handler=None` 으로 중간 스트리밍을 꺼 파이프라인 로그를 깔끔하게 유지합니다.

---

## 📗 advanced.py — 심화

| 함수 | 기법 | 흐름 |
|------|------|------|
| `run_parallel_then_join()` | **병렬 후 합류** — 독립 단계를 동시에 실행하고 결과를 하나로 합침 | `research → (risk ∥ cost) → summary` |
| `run_with_retry()` | **단계별 재시도** — 실패한 단계만 다시 실행 (전체 재시작 X) | `research → risk → report` (각 단계 재시도) |

```
run_parallel_then_join():

    research ──┬──> risk_analysis ──┐
               │                     ├──> summary
               └──> cost_analysis ──┘
```

> 💡 **단계별 재시도**는 긴 다단계 프로세스에서 Workflow가 Swarm/Graph보다 유리한 지점입니다.
> 한 단계가 실패해도 그 단계만 다시 돌려 비용·시간을 아낄 수 있습니다.

---

## 🔗 관련 챕터

- [03. Graph 패턴](../03_graph_pattern) — 명시적 노드/엣지 오케스트레이션
- [04. Swarm 패턴](../04_swarm_pattern) — 자율 협업 Multi-Agent
- [06. 패턴 비교](../06_pattern_comparison) — Graph vs Swarm vs Workflow, 언제 무엇을 쓸까
