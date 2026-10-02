# 06. 패턴 비교 (Pattern Comparison)

**Graph · Swarm · Workflow** — 세 Multi-Agent 패턴을 비교하고, **언제 무엇을 써야 하는지** 판단 기준을 정리합니다.

## 🧠 한눈에 보는 비교

| 기준 | 🕸 Graph | 🐝 Swarm | ➡️ Workflow |
|------|---------|---------|------------|
| **흐름 결정 주체** | 개발자 (명시적) | Agent (자율) | 개발자 (선형) |
| **구조** | 노드 + 엣지 (DAG/반복) | 공유 컨텍스트 + handoff | 함수 호출 순서 |
| **분기/조건** | ✅ 강력 (조건부 엣지) | ✅ Agent가 판단 | △ 코드로 직접 |
| **병렬 실행** | ✅ 자동 (의존성 기반) | △ 비결정적 | ✅ 직접 구현 |
| **예측 가능성** | 높음 | **낮음** (동적) | **가장 높음** |
| **유연성** | 중간 | **높음** | 낮음 |
| **디버깅 난이도** | 중간 | 어려움 | **쉬움** |
| **단계별 재시도** | △ | △ | ✅ 자연스러움 |
| **대표 위험** | 그래프 복잡도 | 핑퐁·폭주 | 경직성 |

## 🎯 선택 가이드 (의사결정)

```
흐름이 매번 똑같고 재현·감사가 중요한가?
   └─ 예 → Workflow  (명확·디버깅 쉬움·단계별 재시도)
   └─ 아니오 ↓

흐름을 미리 그릴 수 있는가? (분기·병렬·합류가 정해져 있음)
   └─ 예 → Graph     (명시적 제어 + 자동 병렬)
   └─ 아니오 ↓

문제에 따라 흐름이 달라지고, Agent 협업/판단이 핵심인가?
   └─ 예 → Swarm     (자율 분배 + 집단 지성)
```

## 📌 상황별 추천

| 상황 | 추천 | 이유 |
|------|------|------|
| CI/CD 같은 **고정 다단계 파이프라인** | Workflow | 재현성·단계별 복구 |
| **분기·병렬**이 명확한 오케스트레이션 | Graph | 조건부 엣지 + 자동 병렬 |
| **탐색적 문제**, 흐름이 유동적 | Swarm | 동적 handoff |
| **감사·추적**이 중요한 규제 업무 | Workflow | 단계별 로깅 명확 |
| 품질 **검토→반복** 루프 | Graph | 조건부 엣지로 반복 |
| 전문가들이 **자유롭게 협업** | Swarm | 공유 컨텍스트 |

## 🧪 데모 — 같은 목표, 세 가지 구조

[`main.py`](./main.py)는 **동일한 목표**(조사→분석→리포트)를 세 패턴으로 각각 구현해, 코드 구조가 어떻게 달라지는지 비교합니다.

```bash
python 06_pattern_comparison/main.py
```

핵심 차이 (코드만 읽어도 드러남):

```python
# Graph    : 흐름을 '그린다'
b.add_edge("research", "analysis"); b.add_edge("analysis", "report")

# Swarm    : 흐름이 '없다' — Agent가 스스로 handoff
swarm = Swarm([researcher, analyst, writer], entry_point=researcher)

# Workflow : 흐름을 '함수 순서'로 잇는다
research = researcher(...); analysis = analyst(...); report = writer(...)
```

## 💡 조합도 가능하다

세 패턴은 배타적이지 않습니다. 실무에서는 자주 섞입니다:

- **Graph 노드 안에 Swarm** — 복잡한 한 단계를 Swarm으로 처리 (03장 `run_swarm_as_node` 참고)
- **Workflow의 한 스텝을 Graph로** — 선형 파이프라인 중 분기가 필요한 구간만 Graph
- **Swarm이 Workflow를 도구로 호출** — 자율 Agent가 정형 파이프라인을 실행

---

## 🔗 관련 챕터

- [03. Graph 패턴](../03_graph_pattern)
- [04. Swarm 패턴](../04_swarm_pattern)
- [05. Workflow 패턴](../05_workflow_pattern)
- [07. 보안](../07_security) · [08. 관측성](../08_observability) — 어떤 패턴을 쓰든 프로덕션에 필요한 공통 토대
