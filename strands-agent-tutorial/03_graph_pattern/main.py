"""
Graph 패턴: 여러 Agent의 실행 흐름을 노드(Agent)와 엣지(연결)로 정의하는 방식.

이 예제의 흐름:
    research(연구) ──┬──> analysis(분석) ──┐
                     │                      ├──> report(리포트)
                     └──> fact_check(검증) ─┘

    - analysis와 fact_check는 research 완료 후 '병렬'로 실행된다.
    - report는 analysis와 fact_check가 모두 끝나야 실행된다.
    - 각 노드는 원본 입력 + 앞선 노드들의 결과를 함께 전달받는다.
"""

from strands import Agent
from strands.multiagent import GraphBuilder

# 1. 노드가 될 Agent들을 정의
researcher = Agent(
    name="researcher",
    system_prompt="You gather comprehensive information on topics.",
)
analyst = Agent(
    name="analyst",
    system_prompt="You analyze data, identify patterns, and provide insights.",
)
fact_checker = Agent(
    name="fact_checker",
    system_prompt="You verify facts and validate information accuracy.",
)
report_writer = Agent(
    name="report_writer",
    system_prompt="You create clear, well-structured reports.",
)

# 2. 그래프에 노드를 추가하고 엣지로 흐름을 연결
builder = GraphBuilder()

builder.add_node(researcher, "research")
builder.add_node(analyst, "analysis")
builder.add_node(fact_checker, "fact_check")
builder.add_node(report_writer, "report")

builder.add_edge("research", "analysis")     # research -> analysis
builder.add_edge("research", "fact_check")   # research -> fact_check (analysis와 병렬)
builder.add_edge("analysis", "report")       # analysis -> report
builder.add_edge("fact_check", "report")     # fact_check -> report

builder.set_entry_point("research")          # 시작 노드

# 3. 빌드 후 실행
graph = builder.build()
result = graph("Research AI impact on healthcare and create a comprehensive report")

# 4. 결과 확인
print(f"Status: {result.status}")
print(f"실행 순서: {[node.node_id for node in result.execution_order]}")
