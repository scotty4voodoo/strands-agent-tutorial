"""
첫번째 에이전트 구현
아주 간단한 Agent를 Strand SDK 를 통해 구현 해봅니다.
사전 필요 사항 : awscli, aws credential 이 설정된 로컬머신
requirement.txt 에 정의된 패키지 (pip install strands)
"""
# Strands Agent 모듈 불러오기 
from strands import Agent

# 가장 기본적인 Agent를 구현해본다.
agent = Agent()

# Agent 기본 테스트
response = agent("Tell me about agentic AI")
print(response.last_message)