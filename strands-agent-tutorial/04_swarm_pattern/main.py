"""
Swarm 패턴: 중앙 제어(그래프의 명시적 엣지) 없이, Agent들이 스스로
'누구에게 넘길지(handoff)'를 판단하며 자율적으로 협업하는 방식.

Graph 패턴과의 차이:
    - Graph : 개발자가 노드/엣지로 실행 흐름을 '미리' 고정한다.
    - Swarm : 흐름이 고정돼 있지 않다. 각 Agent가 공유 컨텍스트를 보고
              필요하면 다른 Agent에게 작업을 넘긴다(동적 분배).

이 예제의 흐름(고정이 아니라 '전형적인 예시'):
    coordinator(조율) ──handoff──> researcher(조사)
                                      │ handoff
                                      ▼
                                  coder(구현) ──handoff──> reviewer(검토)
    - 각 Agent는 전체 작업 컨텍스트와 '지금까지 누가 무엇을 했는지'를 공유받는다.
    - 자기 역할이 끝나면 handoff_to_agent 도구로 다음 적임자에게 넘긴다.
    - 더 넘길 곳이 없다고 판단되면 Swarm이 종료된다.
"""

from strands import Agent
from strands.multiagent import Swarm

# 1. 서로 다른 전문성을 가진 Agent들을 정의
#    name은 handoff(작업 이관)의 대상 식별자로 쓰이므로 반드시 지정한다.
coordinator = Agent(
    name="coordinator",
    system_prompt=(
        "You break down the user request into steps and delegate to the right "
        "specialist. Hand off to 'researcher' for information gathering."
    ),
)
researcher = Agent(
    name="researcher",
    system_prompt=(
        "You gather accurate information. When enough is collected, hand off to "
        "'coder' to implement a solution."
    ),
)
coder = Agent(
    name="coder",
    system_prompt=(
        "You write clean Python code based on the research. When done, hand off "
        "to 'reviewer' for a quality check."
    ),
)
reviewer = Agent(
    name="reviewer",
    system_prompt=(
        "You review code for correctness and clarity. If it is good, provide the "
        "final answer. If not, hand back to 'coder' with specific feedback."
    ),
)

# 2. Agent들을 묶어 Swarm을 구성
#    엣지를 그리지 않는다 — 흐름은 Agent들이 런타임에 스스로 결정한다.
swarm = Swarm(
    [coordinator, researcher, coder, reviewer],
    entry_point=coordinator,   # 첫 번째로 작업을 받을 Agent
)

# 3. 실행 — 작업만 던지면 된다
result = swarm(
    "Build a Python function that checks whether a string is a valid palindrome, "
    "ignoring punctuation and case."
)

# 4. 결과 확인
print(f"Status: {result.status}")
print(f"작업을 거친 Agent 순서: {[node.node_id for node in result.node_history]}")
