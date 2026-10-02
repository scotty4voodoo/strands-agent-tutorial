"""
패턴 비교 데모: 같은 목표를 Graph / Swarm / Workflow 세 방식으로 각각 구현해
'코드 구조가 어떻게 달라지는지'를 한눈에 보여준다.

공통 목표:
    주제를 조사(research) → 분석(analysis) → 리포트(report) 로 만든다.

세 방식의 차이:
    - Graph    : 흐름을 '노드/엣지'로 명시적으로 그린다.
    - Swarm    : 흐름을 그리지 않고 Agent가 handoff로 '스스로' 결정한다.
    - Workflow : 흐름을 '함수 호출 순서'로 선형적으로 잇는다.

주의: 세 함수 모두 AWS Bedrock 자격 증명이 있어야 실제 실행된다.
      이 파일의 목적은 '구조 비교'이므로, 코드를 읽는 것만으로 차이가 드러난다.
"""

from strands import Agent
from strands.multiagent import GraphBuilder, Swarm

TOPIC = "AI impact on cloud security operations"


def _make_agents():
    """세 방식이 공유하는 역할 Agent (이름은 handoff용으로 지정)."""
    researcher = Agent(name="researcher", system_prompt="You gather key information.")
    analyst = Agent(name="analyst", system_prompt="You analyze and extract insights.")
    writer = Agent(name="writer", system_prompt="You write a clear report. Finalize when done.")
    return researcher, analyst, writer


# ---- 1) Graph 방식: 흐름을 명시적으로 그린다 -------------------------------
def as_graph():
    researcher, analyst, writer = _make_agents()
    b = GraphBuilder()
    b.add_node(researcher, "research")
    b.add_node(analyst, "analysis")
    b.add_node(writer, "report")
    b.add_edge("research", "analysis")   # 흐름을 개발자가 직접 연결
    b.add_edge("analysis", "report")
    b.set_entry_point("research")
    graph = b.build()
    return graph(f"Research, analyze and report on: {TOPIC}")


# ---- 2) Swarm 방식: 흐름을 Agent가 스스로 결정한다 -------------------------
def as_swarm():
    researcher, analyst, writer = _make_agents()
    swarm = Swarm([researcher, analyst, writer], entry_point=researcher)  # 엣지 없음
    return swarm(f"Research, analyze and report on: {TOPIC}")


# ---- 3) Workflow 방식: 함수 호출로 순서를 잇는다 ---------------------------
def as_workflow():
    researcher, analyst, writer = _make_agents()
    research = researcher(f"Research: {TOPIC}")          # 선형 파이프라인
    analysis = analyst(f"Analyze:\n{research}")
    report = writer(f"Write a report:\n{analysis}")
    return report


if __name__ == "__main__":
    print("같은 목표를 세 방식으로 — 코드 구조의 차이를 비교하세요.")
    print("Graph    :", as_graph().status)
    print("Swarm    :", as_swarm().status)
    print("Workflow :", "COMPLETED (함수 반환)")
