"""
Graph 심화 (2) — 조건부 엣지 (Conditional Forwarding)

엣지에 condition을 걸어, 리뷰 결과에 따라 흐름을 분기하거나 반복(loop)시킨다.

흐름: writer -> reviewer -> (통과 시 publisher / 미달 시 writer 재작성)
"""

from strands import Agent
from strands.multiagent import GraphBuilder
from strands.multiagent.graph import GraphState
from strands.multiagent.base import Status


def quality_check_passed(state: GraphState) -> bool:
    """리뷰 통과 여부 판정."""
    reviewer_result = state.results.get("reviewer")
    if not reviewer_result or reviewer_result.status != Status.COMPLETED:
        return False
    return "APPROVED" in str(reviewer_result.result)


def run_conditional_edges():
    """흐름: writer -> reviewer -> (통과 시 publisher / 미달 시 writer 재작성)"""
    writer = Agent(name="writer", system_prompt="You write content. Include 'DRAFT' in your output.")
    reviewer = Agent(
        name="reviewer",
        system_prompt=(
            "You review content quality. "
            "If good, respond with 'APPROVED: [feedback]'. "
            "If it needs work, respond with 'NEED_REVISION: [feedback]'."
        ),
    )
    publisher = Agent(name="publisher", system_prompt="You publish approved content.")

    builder = GraphBuilder()
    builder.add_node(writer, "writer")
    builder.add_node(reviewer, "reviewer")
    builder.add_node(publisher, "publisher")

    builder.add_edge("writer", "reviewer")
    builder.add_edge("reviewer", "publisher", condition=quality_check_passed)
    builder.add_edge("reviewer", "writer", condition=lambda s: not quality_check_passed(s))

    builder.set_entry_point("writer")
    builder.set_execution_timeout(300)

    result = builder.build()("Write a brief introduction to AI")
    print(f"[조건부 엣지] order={[n.node_id for n in result.execution_order]}")


if __name__ == "__main__":
    run_conditional_edges()
