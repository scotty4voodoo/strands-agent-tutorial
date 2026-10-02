"""
Agent 를 구현할 때, Agent의 이름, 역할, 그리고 사용할 도구들을 지정할 수 있다.
아래 예제에서는 Agent에게 Researcher(연구자) 역할을 부여하고,
이에 필요한 System Prompt를 제공한다.
그리고 답변을 얻기까지 필요한 Tool 을 정의한다. 
"""

from strands import Agent
from strands_tools import calculator, current_time

# Agent 선언 시, Agent의 이름, System Prompt, tool 을 정의할 수 있다.
research_agent = Agent(
    name = "research_assistant",
    system_prompt = """You are a research spcialist who provides factual, well-sourced information. Always cite your sources.
    """,
    tools = [calculator, current_time]
)

# Agent 호출
result = research_agent("Calculate the compound interest on $10,000 at 5% at for 10 years")
print(result.last_message)
