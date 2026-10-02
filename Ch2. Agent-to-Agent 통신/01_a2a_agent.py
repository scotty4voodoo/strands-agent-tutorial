from strands import Agent
from typing import Dict,List,Any,Optional
from dataclasses import dataclass
from datetime import datetime
import asyncio

### A2A 기능 정의

#1. Message Format - Structured communication between agents
@dataclass
class A2AMessage:
    """Standarized message format for agent-to-agent communication"""
    sender_id: str
    recipient_id: str
    message_type: str
    payload: Dict[str, Any]
    timestamp: datetime
    correlation_id: str
    
    def to_dict(self) -> Dict[str,Any]:
        return {
            'sender':self.sender_id,
            'recipient': self.recipient_id,
            'type':self.message_type,
            'payload':self.payload,
            'timestamp':self.timestamp.isoformat(),
            'correlation_id': self.correlation_id
        }

#2. CAPABILITY DISCCOVERY - Agents advertse their capabilities
class AgentCapability:
    """Define what an agent can do"""
    def __init__(self,agent_id:str, capabilities:List[str],description: str, agent: Agent):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.description = description
        self.agent = agent

#3. DYNAMIC AGENT DISCOVERY - Agent registry for dynamic discovery
AGENT_REGISTRY: Dict[str,AgentCapability] = {}

def register_agent(agent_id:str, capabilities:List[str], description:str, agent: Agent):
    """Register an agent's capabilities for discovery"""
    AGENT_REGISTRY[agent_id] = AgentCapability(agent_id,capabilities,description,agent)
    print(f"Registered agent '{agent_id}' with capabilities: {capabilities}")
    
def discover_agents(required_capability:str) -> List[AgentCapability]:
    """Discover agents that have a specific capability"""
    matching_agents = [
        capability for agent_id, capability in AGENT_REGISTRY.items() if required_capability in capability.capabilities
    ]
    print(f"Found {len(matching_agents)} agent(s) with '{required_capability}' capability")
    return matching_agents

async def async_send_message(message: A2AMessage, recipient_agent:Agent) -> str:
    """Send message asynchronously, allowing sender to continue other work"""
    print(f"-> sending async message from {message.sender_id} to {message.recipient_id}")
    
    # Simulate async process
    await asyncio.sleep(0.1)
    
    # Process message with recipient agent
    response = recipient_agent(message.payload.get('content',''))
    response_text = str(response)
    print(f"Response from {message.recipient_id} received")
    
    return response_text


### 에이전트 워크플로우 정의 (Sequential)
def multi_agent_collaboration_example():
    """Demonstrate  complete multi-agent collaboration using A2A protocol"""
    print ("=== Multi-Agent Collaboration Workflow ===\n")
    
    # Create specialized agents with distinct capabilities
    research_agent = Agent(
        name="researcher",
        system_prompt="You are a research specialist who gather comprehensive in on  topics"
    )
    
    analysis_agent = Agent(
        name="analyst",
        system_prompt="You analyze data and identity key patterns, trends, and insights."
    )
    
    summary_agent = Agent(
        name="summarizer",
        system_prompt="You create concise, excutive-level summaries of complex information"
    )
    
    # Register all agents with their capabilities
    register_agent("researcher",["research","information_gathering"],"Gathers comprehensive information", research_agent)
    register_agent("analyst",["analysis","data_interpretation","pattern_recognition"],"Analyzes data and identifies insights",analysis_agent)
    register_agent("summarizer",["summarization","synthesis","reporting"],"Create excutive summaries",summary_agent)
    
    print("\n=== Step 1: Coordinator Discovers Required Agents ===")
    # Cordinator discovers agents for each phase of work
    research_specialists = discover_agents("research")
    analysis_specialists = discover_agents("analysis")
    summary_specialists = discover_agents("summarization")
    
    print(f"\nWorkflow Plan: ")
    print(f" Phase 1: {research_specialists[0].agent_id} (research)")
    print(f" Phase 2: {analysis_specialists[0].agent_id} (analysis)")
    print(f" Phase 3: {summary_specialists[0].agent_id} (summary) \n")
    
    # Define the Task
    task = "인공지능이 의료 진단에 미치는 영향 분석"
    
    print(f"=== Step 2: Phase 1 - Research ===")
    # Phase 1: Research
    research_msg = A2AMessage(
        sender_id="coordinator",
        recipient_id="researcher",
        message_type ="request",
        payload={"content": task,"depth":"comprehensive"},
        timestamp=datetime.now(),
        correlation_id="workflow-001-research"
    )
    
    print(f"Coordinator -> Researcher: '{task}'")
    research_result = research_specialists[0].agent(research_msg.payload['content'])
    research_result_text = str(research_result)
    print(f"Research completed: {len(research_result_text)} characters \n")
    
    print(f"=== Step 3: Phase 2 - Analysis ===")
    # Phase 2: Analysis (receives research results)
    analysis_msg = A2AMessage(
        sender_id = "researcher",
        recipient_id="analyst",
        message_type="request",
        payload={
            "content":f"Analyzer this research and identify key trends: \n\n {research_result_text}",
            "focus":"trends and implications"
        },
        timestamp= datetime.now(),
        correlation_id="workflow-001-analysis"
    )
    
    print(f"Research -> Analyst: Passing research results for analysis")
    analysis_result = analysis_specialists[0].agent(analysis_msg.payload['content'])
    analysis_result_text = str(analysis_result)
    print(f"Analysis completed: {len(analysis_result_text)} characters \n")
    
    print(f"=== Step 4: Phase 3 - Summary ===")
    # Phase 3: Summary (receives analysis results)
    summary_msg = A2AMessage(
        sender_id="analyst",
        recipient_id="summarizer",
        message_type="request",
        payload={
            "content":f"Create an executive summary: \n\n{analysis_result_text}",
            "format":"executive brief"
        },
        timestamp=datetime.now(),
        correlation_id="workflow-001-summary"
    )
    
    print(f"Analyst -> Summarizer: Passing analysis for executive summary")
    final_result = summary_specialists[0].agent(summary_msg.payload['content'])
    final_result_text = str(final_result)
    print(f"Summary completed: {len(final_result_text)} characters \n")
    
    print(f"=== Workflow Complete ===")
    print(f"Final deliverable preview : ")
    print(f"{final_result_text[:300]}...")
    
    # Show message tracking
    print(f"=== Message Tracking ===")
    print(f"Correlation IDs tracked: ")
    print(f" - {research_msg.correlation_id}")
    print(f" - {analysis_msg.correlation_id}")
    print(f" - {summary_msg.correlation_id}")
    print(f"\n Complete audit trail maintained for compliance and debugging \n")
    
### 에이전트 워크플로우 정의 (Parallel)
async def parallel_collaboration_example():
    """Demonstrate parallel agent collaboration using async A2A"""
    
    print("=== parallel Multi-agent collaboration ===\n")
    
    # Create multiple specialists agents
    tech_researcher = Agent(
        name="tech_researcher",
        system_prompt="You research technical aspects and innovations."
    )
    
    market_researcher = Agent(
        name="market_researcher",
        system_prompt="You research market trends and business implications."
    )
    
    policy_researcher = Agent(
        name="policy_researcher",
        system_prompt="You research regulatory and policy considerations."
    )
    
    # Register agents
    register_agent("tech_researcher",["research","technical_analysis"],"Technical research specialist",tech_researcher)
    register_agent("market_researcher",["research","market_analysis"],"Market research specialist",market_researcher)
    register_agent("policy_researcher",["research","policy_analysis"],"Policy research specialist",policy_researcher)
    
    topic = "AI in autonomous vehicles"
    
    #Create parallel research tasks
    tech_msg = A2AMessage(
        sender_id="coordinator",
        recipient_id="tech_researcher",
        message_type="request",
        payload={"content":f"Research technical aspects of {topic}"},
        timestamp=datetime.now(),
        correlation_id="parallel-001-tech"
    )
    
    market_msg = A2AMessage(
        sender_id="coordinator",
        recipient_id="market_researcher",
        message_type="request",
        payload={"content":f"research market implications of {topic}"},
        timestamp=datetime.now(),
        correlation_id="parallel-001-market"
    )
    
    policy_msg = A2AMessage(
        sender_id="coordinator",
        recipient_id="policy_researcher",
        message_type="request",
        payload={"content":f"research policy cosideration for {topic}"},
        timestamp=datetime.now(),
        correlation_id="parallel-001-policy"
    )
    
    print(f"Launching 3 parallel research tasks on: {topic}\n")
    
    # Excute all research task in parallel
    results = await asyncio.gather(
        async_send_message(tech_msg,tech_researcher),
        async_send_message(market_msg,market_researcher),
        async_send_message(policy_msg,policy_researcher)
    )
    
    print(f"\n All parallel task completed!")
    print(f" - Technical research : {len(results[0])} characters")
    print(f" - Market research: {len(results[1])} characters")
    print(f" - Policy research: {len(results[2])} characters")
    print(f"\nTime saved through parallel execution vs sequential \n")
    
# Run demonstrations
if __name__ == "__main__":
    #Sequential multi-agent collaboration
    multi_agent_collaboration_example()
    
    # Parallel multi-agent collaboration
    print("\n" + "="*60 + "\n")
    asyncio.run(parallel_collaboration_example())