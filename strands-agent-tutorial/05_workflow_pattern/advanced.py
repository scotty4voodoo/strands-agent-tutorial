"""
Workflow 패턴 심화: 선형 파이프라인을 넘어선 두 가지 실무 기법.

    1) run_parallel_then_join() — 독립 단계는 병렬 실행 후 합류(join)
    2) run_with_retry()         — 특정 단계만 실패 시 재시도 (전체 재시작 X)

Workflow의 강점은 '구조화된 실행 + 단계별 복구'다. 긴 다단계 프로세스에서
한 단계가 실패해도 그 단계만 다시 돌릴 수 있다는 점이 Swarm/Graph와 구별되는
실무적 이점이다.
"""

import concurrent.futures

from strands import Agent


def build_agents():
    """심화 공용 Agent 생성."""
    researcher = Agent(
        system_prompt="You find key information concisely.",
        callback_handler=None,
    )
    risk_analyst = Agent(
        system_prompt="You assess security/compliance risks from information.",
        callback_handler=None,
    )
    cost_analyst = Agent(
        system_prompt="You assess cost implications from information.",
        callback_handler=None,
    )
    writer = Agent(
        system_prompt="You merge multiple analyses into one executive summary.",
    )
    return researcher, risk_analyst, cost_analyst, writer


# ---------------------------------------------------------------------------
# 1) 병렬 실행 후 합류 (parallel + join)
# ---------------------------------------------------------------------------
def run_parallel_then_join():
    """
    research 결과를 받아, 서로 독립적인 risk/cost 분석을 '동시에' 수행하고,
    두 결과를 writer가 하나로 합친다.

        research ──┬──> risk_analysis ──┐
                   │                     ├──> summary
                   └──> cost_analysis ──┘
    """
    researcher, risk_analyst, cost_analyst, writer = build_agents()

    topic = "migrating an on-prem database to Amazon Aurora"
    research = researcher(f"Research key considerations for {topic}")

    # 독립적인 두 분석을 스레드로 병렬 실행
    with concurrent.futures.ThreadPoolExecutor() as pool:
        f_risk = pool.submit(risk_analyst, f"Assess risks:\n{research}")
        f_cost = pool.submit(cost_analyst, f"Assess costs:\n{research}")
        risk = f_risk.result()
        cost = f_cost.result()

    # 합류: 두 결과를 한 입력으로 합쳐 요약
    summary = writer(
        f"Combine into one executive summary.\n\n[RISK]\n{risk}\n\n[COST]\n{cost}"
    )
    print("[run_parallel_then_join]")
    print(summary)
    return summary


# ---------------------------------------------------------------------------
# 2) 단계별 재시도 (step-level retry)
# ---------------------------------------------------------------------------
def run_with_retry(max_retries: int = 2):
    """
    한 단계가 빈/실패 결과를 내면 '그 단계만' 다시 돌린다.
    전체 파이프라인을 처음부터 재시작하지 않는 것이 핵심.
    """
    researcher, risk_analyst, _, writer = build_agents()

    def run_step(name, agent, prompt):
        for attempt in range(1, max_retries + 1):
            try:
                out = agent(prompt)
                if out and str(out).strip():
                    return out
                print(f"  [{name}] 빈 결과 — 재시도 {attempt}/{max_retries}")
            except Exception as e:  # noqa: BLE001 - 예제용 간략 처리
                print(f"  [{name}] 오류: {e} — 재시도 {attempt}/{max_retries}")
        raise RuntimeError(f"{name} 단계가 {max_retries}회 재시도 후에도 실패")

    print("[run_with_retry]")
    research = run_step("research", researcher, "Research zero-trust network basics")
    risk = run_step("risk", risk_analyst, f"Assess risks:\n{research}")
    report = run_step("report", writer, f"Write a short brief:\n{risk}")
    print(report)
    return report


if __name__ == "__main__":
    run_parallel_then_join()
    print("-" * 60)
    run_with_retry()
