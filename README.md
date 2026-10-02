# 🤖 Strands Agent Tutorial

> **Strands Agents SDK**를 활용한 AI Agent 개발 실전 예제 모음 — 단일 Agent부터 Multi-Agent 오케스트레이션, 보안, 관측성까지.

<p align="center">
  <img src="https://img.shields.io/badge/Strands--Agents-SDK-blue?style=flat-square" alt="Strands Agents SDK" />
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/AWS-Bedrock-FF9900?style=flat-square&logo=amazonaws&logoColor=white" alt="AWS Bedrock" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License" />
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square" alt="PRs Welcome" />
</p>

---

## 📖 소개 (Overview)

이 저장소는 **Strands Agents SDK**를 사용해 AI Agent를 개발하는 방법을 단계별 예제로 정리한 튜토리얼입니다.
단일 Agent 구현에서 시작해 **Multi-Agent 협업 패턴(Graph · Swarm · Workflow)**, 그리고 **프로덕션 배포를 위한 보안과 관측성(Observability)**까지 실무 관점에서 다룹니다.

> 각 예제는 독립적으로 실행 가능하며, 개념 → 코드 → 실행 순서로 따라갈 수 있도록 구성되어 있습니다.

---

## 📑 목차 (Table of Contents)

- [소개](#-소개-overview)
- [다루는 내용](#-다루는-내용-whats-inside)
- [사전 요구사항](#-사전-요구사항-prerequisites)
- [설치 및 시작하기](#-설치-및-시작하기-getting-started)
- [예제 구성](#-예제-구성-examples)
- [프로젝트 구조](#-프로젝트-구조-project-structure)
- [기여하기](#-기여하기-contributing)
- [라이선스](#-라이선스-license)

---

## 🎯 다루는 내용 (What's Inside)

| # | 주제 | 설명 |
|:-:|------|------|
| 1 | **Agent 기초** | Strands SDK를 활용한 단일 Agent 구현 및 활용법 |
| 2 | **Agent-to-Agent 통신** | Multi-Agent 구현을 위한 Agent 간 통신 방법 |
| 3 | **Graph 패턴** | Graph 기반의 Multi-Agent 오케스트레이션 |
| 4 | **Swarm 패턴** | Swarm 기반의 자율 협업 Multi-Agent 구현 |
| 5 | **Workflow 패턴** | Workflow 기반의 Multi-Agent 파이프라인 |
| 6 | **패턴 비교** | Graph vs Swarm vs Workflow — 언제 무엇을 쓸까 |
| 7 | **보안 (Security)** | Multi-Agent 배포 시 보안 고려사항 및 적용 방법 |
| 8 | **모니터링 & 관측성** | Monitoring & Observability 구성 |

---

## 📋 사전 요구사항 (Prerequisites)

- **Python 3.10+**
- **AWS 계정** 및 자격 증명 (Amazon Bedrock 모델 접근 권한)
- `pip` 또는 `uv` 패키지 매니저

> 💡 Amazon Bedrock의 모델(예: Anthropic Claude)에 대한 접근이 활성화되어 있어야 합니다.

---

## 🚀 설치 및 시작하기 (Getting Started)

### 1. 저장소 클론

```bash
git clone https://github.com/<your-username>/strands-agent-tutorial.git
cd strands-agent-tutorial
```

### 2. 가상환경 생성 및 활성화

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### 3. 패키지 설치

예제에 필요한 패키지는 `requirements.txt`에 정의되어 있습니다.

```bash
pip install -r requirements.txt
```

### 4. AWS 자격 증명 설정

```bash
aws configure
# 또는 환경 변수로 설정
export AWS_ACCESS_KEY_ID=<your-key>
export AWS_SECRET_ACCESS_KEY=<your-secret>
export AWS_REGION=us-east-1
```

### 5. 예제 실행

```bash
python 01_basic_agent/main.py
```

---

## 📚 예제 구성 (Examples)

각 예제는 개념 설명과 실행 가능한 코드를 함께 제공합니다.

<details>
<summary><b>1. Strands SDK를 활용한 Agent 활용법</b></summary>

Strands Agents SDK의 기본 개념과 단일 Agent를 생성·실행하는 방법을 다룹니다. 도구(Tool) 연결, 프롬프트 구성, 모델 설정 등 기초를 학습합니다.
</details>

<details>
<summary><b>2. Multi-Agent를 위한 Agent-to-Agent 통신</b></summary>

여러 Agent가 서로 메시지를 주고받으며 협업하기 위한 통신 메커니즘을 구현합니다.
</details>

<details>
<summary><b>3. Graph 기반 Multi-Agent 패턴</b></summary>

명시적인 노드/엣지로 Agent 간 실행 흐름을 정의하는 Graph 기반 오케스트레이션 패턴을 구현합니다.
</details>

<details>
<summary><b>4. Swarm 기반 Multi-Agent 패턴</b></summary>

중앙 제어 없이 Agent들이 자율적으로 협업하는 Swarm 패턴을 구현합니다.
</details>

<details>
<summary><b>5. Workflow Multi-Agent 패턴</b></summary>

순차적/조건적 단계로 구성된 Workflow 기반 Multi-Agent 파이프라인을 구현합니다.
</details>

<details>
<summary><b>6. Multi-Agent 패턴 비교</b></summary>

Graph · Swarm · Workflow 패턴의 특성과 적합한 사용 시나리오를 비교합니다.
</details>

<details>
<summary><b>7. Multi-Agent 배포의 보안</b></summary>

Multi-Agent 시스템을 프로덕션에 배포할 때 고려해야 할 보안 요소(권한 분리, 입력 검증, 최소 권한 원칙 등)를 다룹니다.
</details>

<details>
<summary><b>8. Monitoring & Observability</b></summary>

Agent 실행에 대한 로깅, 추적(Tracing), 메트릭 수집 등 관측성 구성을 다룹니다.
</details>

---

## 🗂 프로젝트 구조 (Project Structure)

```
strands-agent-tutorial/
├── 01_basic_agent/            # Agent 기초
├── 02_agent_to_agent/         # A2A 통신
├── 03_graph_pattern/          # Graph 기반 패턴
├── 04_swarm_pattern/          # Swarm 기반 패턴
├── 05_workflow_pattern/       # Workflow 패턴
├── 06_pattern_comparison/     # 패턴 비교
├── 07_security/               # 배포 보안
├── 08_observability/          # 모니터링 & 관측성
├── requirements.txt           # 의존성 패키지
└── README.md
```

---

## 🤝 기여하기 (Contributing)

기여는 언제나 환영합니다! 이슈를 등록하거나 Pull Request를 보내주세요.

1. 저장소를 Fork 합니다.
2. 기능 브랜치를 생성합니다. (`git checkout -b feature/amazing-feature`)
3. 변경 사항을 커밋합니다. (`git commit -m 'Add amazing feature'`)
4. 브랜치에 Push 합니다. (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다.

---

## 📄 라이선스 (License)

이 프로젝트는 **MIT License**를 따릅니다. 자세한 내용은 [`LICENSE`](LICENSE) 파일을 참고하세요.

---

## 🔗 참고 자료 (References)

- [Strands Agents 공식 문서](https://strandsagents.com/)
- [Strands Agents GitHub](https://github.com/strands-agents)
- [Amazon Bedrock 문서](https://docs.aws.amazon.com/bedrock/)

---

<p align="center">
  <sub>Built with ❤️ using Strands Agents SDK</sub>
</p>
