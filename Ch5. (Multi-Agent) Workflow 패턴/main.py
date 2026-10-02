"""
Workflow 패턴: 각 Agent가 '정해진 순서'대로 전문 작업을 수행하고,
앞 단계의 출력이 다음 단계의 입력이 되는 파이프라인 방식.

세 패턴의 자리매김:
    - Graph : 노드/엣지로 흐름을 그린다 (분기·병렬·반복 포함, 그래프 자료구조)
    - Swarm : 흐름이 자율적 (Agent가 handoff로 스스로 결정)
    - Workflow : 흐름이 '선형적이고 반복 가능'하다 (정해진 단계의 재현 가능한 실행)

이 예제의 흐름 (가장 단순한 순차 파이프라인):
    researcher(조사) ──> analyst(분석) ──> writer(작성)
    - 각 단계의 출력(output)이 다음 단계의 입력(input)으로 그대로 전달된다.
    - "정해진 절차를 매번 똑같이" 돌려야 할 때 가장 명확하고 디버깅하기 쉽다.

가장 기본적인 Workflow는 별도 오케스트레이터 없이 '함수로 단계를 잇는' 것으로 충분하다.
"""

from strands import Agent

# 1. 단계별 전문 Agent를 정의
#    callback_handler=None 으로 중간 스트리밍 출력을 끄면 파이프라인 로그가 깔끔하다.
researcher = Agent(
    system_prompt="You are a research specialist. Find key, accurate information.",
    callback_handler=None,
)
analyst = Agent(
    system_prompt="You analyze research data and extract the most important insights.",
    callback_handler=None,
)
writer = Agent(
    system_prompt="You create a clear, well-structured report from the analysis.",
)


# 2. 단계를 순서대로 잇는 파이프라인 함수
def process_workflow(topic: str) -> str:
    """research -> analysis -> report 순으로 실행하는 선형 Workflow."""
    # Step 1: 조사
    research_results = researcher(f"Research the latest developments in {topic}")

    # Step 2: 분석 (1단계 출력을 입력으로 사용)
    analysis = analyst(f"Analyze these research findings:\n{research_results}")

    # Step 3: 리포트 작성 (2단계 출력을 입력으로 사용)
    final_report = writer(f"Create a report based on this analysis:\n{analysis}")

    return final_report


# 3. 실행
if __name__ == "__main__":
    report = process_workflow("cloud security posture management (CSPM)")
    print("=" * 60)
    print("최종 리포트:")
    print(report)
