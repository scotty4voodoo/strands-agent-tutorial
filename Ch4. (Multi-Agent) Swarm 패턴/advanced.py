"""
Swarm 패턴 심화: 자율 협업을 '안전하게' 운영하기 위한 설정과 결과 분석.

이 파일은 두 가지 심화 주제를 독립 함수로 다룬다.
    1) run_safe_swarm()      — 폭주/무한 이관을 막는 안전 파라미터 설정
    2) inspect_swarm_result() — SwarmResult에서 실행 내역·노드별 결과 꺼내기

Swarm은 흐름이 자율적인 만큼, 다음 위험을 통제해야 한다.
    - 두 Agent가 서로에게 계속 넘기는 '핑퐁(반복 이관)'
    - 작업이 끝나지 않고 무한히 도는 상황
    - 토큰/시간 폭주
Swarm 생성자의 안전 파라미터가 이를 제어한다.
"""

from strands import Agent
from strands.multiagent import Swarm


def build_agents():
    """심화 예제 공용: 역할이 다른 Agent 3종을 생성."""
    writer = Agent(
        name="writer",
        system_prompt=(
            "You draft concise technical explanations. Hand off to 'editor' to "
            "polish the draft."
        ),
    )
    editor = Agent(
        name="editor",
        system_prompt=(
            "You improve clarity and fix errors. If the text still needs facts "
            "checked, hand off to 'fact_checker'; otherwise finalize."
        ),
    )
    fact_checker = Agent(
        name="fact_checker",
        system_prompt=(
            "You verify technical claims. Hand back to 'editor' with corrections "
            "if needed, or confirm the text is accurate."
        ),
    )
    return [writer, editor, fact_checker]


# ---------------------------------------------------------------------------
# 1) 안전 파라미터로 Swarm 폭주 방지
# ---------------------------------------------------------------------------
def run_safe_swarm():
    """
    핵심 안전 파라미터:
      - max_handoffs           : 전체 작업 이관 횟수 상한
      - max_iterations         : Agent 실행 총 횟수 상한
      - execution_timeout      : 전체 Swarm 제한 시간(초)
      - node_timeout           : 개별 Agent 1회 실행 제한 시간(초)
      - repetitive_handoff_detection_window / _min_unique_agents :
            최근 N번의 이관 안에 '서로 다른 Agent'가 최소 M명은 등장해야 한다.
            (A→B→A→B 같은 핑퐁을 감지해 중단)
    """
    swarm = Swarm(
        build_agents(),
        max_handoffs=10,
        max_iterations=12,
        execution_timeout=180.0,          # 전체 3분
        node_timeout=45.0,                # 개별 Agent 45초
        repetitive_handoff_detection_window=6,
        repetitive_handoff_min_unique_agents=2,
    )

    result = swarm("Explain how TLS 1.3 improves on TLS 1.2 in 3 bullet points.")
    print("[run_safe_swarm]")
    print(f"  Status: {result.status}")
    print(f"  이관 경로: {[n.node_id for n in result.node_history]}")
    return result


# ---------------------------------------------------------------------------
# 2) SwarmResult 뜯어보기 — 무슨 일이 있었는지 분석
# ---------------------------------------------------------------------------
def inspect_swarm_result():
    """
    SwarmResult의 주요 필드:
      - status          : COMPLETED / FAILED 등 종료 상태
      - node_history    : 작업을 거친 Agent 순서(핑퐁·분배 패턴 확인)
      - results         : 노드별 상세 결과 딕셔너리 (node_id -> NodeResult)
      - execution_time  : 총 실행 시간(ms)
    """
    swarm = Swarm(build_agents(), max_handoffs=8, max_iterations=10)
    result = swarm("Write one sentence on why zero-trust matters, then verify it.")

    print("[inspect_swarm_result]")
    print(f"  Status: {result.status}")
    print(f"  거친 Agent 수: {len(result.node_history)}")
    print(f"  실행 시간(ms): {result.execution_time}")

    # 특정 노드의 결과만 선택적으로 꺼내기
    if "editor" in result.results:
        editor_out = result.results["editor"].result
        print(f"  editor 노드 결과: {editor_out}")
    return result


if __name__ == "__main__":
    run_safe_swarm()
    print("-" * 60)
    inspect_swarm_result()
