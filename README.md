# Building Effective Agents

This repo demonstrates how to construct effective AI agents, closely mirroring the best practices outlined in [building-effective-agents](https://www.anthropic.com/research/building-effective-agents) by Anthropic. 

My goal is to combine principles inspired by anthropic with multiple frameworks — **pydanticAI**, **crewAI**, **instructor**, etc. — to help developers orchestrate robust workflows for AI solutions.

## Overview

The core mission of this project is to distill the knowledge from building effective agents into a workable template and practical codebase. 

By adhering to these best practices, you can implement agents that:

- **Understand** diverse prompts and respond accurately.
- **Scale** with parallelization and routing techniques.
- **Improve** continuously through evaluation and optimization.

I aim for an extensible, modular approach: each component (prompt design, routing, orchestration, evaluation) is encapsulated and easy to adapt.

## Principles & Workflow

The heart of **building-effective-agents.md** is the six-step workflow:

### 1. The Augmented LLM
Introduce an augmented language model that can integrate external tools, services, and knowledge bases. The LLM is not just a text generator but an **intelligent router** that leverages specialized modules for improved results.

```mmd
graph TD
    A[In] --> B{LLM}
    B --> C[Out]
    D[Retrieval] -- Query/Results --> B
    E[Tools] -- Call/Response --> B
    F[Memory] -- Read/Write --> B
```

### 2. The Prompt Chaining Workflow
Create a chain (or pipeline) of prompts and sub-prompts that lead from raw user queries to high-quality structured responses. This includes:
- Breaking down complex questions into smaller tasks.
- Iterating on partial solutions to refine the final output.
- Ensuring context is passed along properly.

```mmd
graph LR
    A[In] -->| | B(LLM Call 1)
    B -->|Output 1| C{Gate}
    C -- Pass --> D(LLM Call 2)
    C -- Fail --> E[Exit]
    D -->|Output 2| F(LLM Call 3)
    F -->| | G[Out]
```

### 3. The Routing Workflow
Route tasks to specialized workers or sub-agents. For example, a **sales agent** might handle commerce-related tasks, while a **database agent** might handle data storage. The routing workflow ensures:
- The correct agent is called for each job.
- Error handling if the wrong route is chosen.
- Logging, tracing, or monitoring of agent activities.

```mmd
graph LR
    A[In] --> B(LLM Call Router)
    B -.-> C(LLM Call 2)
    B -...-> D(LLM Call 3)
    B ..-> E(LLM Call 1)
    C -.-> F[Out]
    D -...-> F
    E ..-> F
```

### 4. The Parallelization Workflow
Allow independent parts of the workflow to occur in parallel, speeding up complex tasks. This includes:
- Orchestrating multiple tasks concurrently.
- Synchronizing results efficiently.
- Handling concurrency conflicts and rate limits.

```mmd
graph LR
    A[In] --> B(Orchestrator)
    B -.-> C(LLM Call 1)
    B -...-> D(LLM Call 2)
    B -..-> E(LLM Call 3)
    C -.-> F(Synthesizer)
    D -...-> F
    E -..-> F
    F --> G[Out]
```

### 5. The Orchestrator-Workers Workflow
Establish a high-level orchestrator that coordinates multiple workers (agents). The orchestrator:
- Spawns or assigns tasks to workers.
- Aggregates partial results.
- Monitors progress and handles retries.

```mmd
graph LR
    A[In] --> B(Orchestrator)
    B -.-> C(LLM Call 1)
    C -.-> E(Synthesizer)
    B -.-> D(LLM Call 2)
    D -.-> E
    B -.-> F(LLM Call 3)
    F -.-> E
    E --> G(Out)
    style A fill:#ffe8e8,stroke:#c74343
    style G fill:#ffe8e8,stroke:#c74343
```

### 6. The Evaluator-Optimizer Workflow
Implement a feedback loop to evaluate agent performance and optimize prompts, parameters, or code:
- Automatic performance scoring.
- Human feedback integration.
- Iterative improvement of the entire pipeline.

```mmd
graph LR
    A[In] --> B(LLM Call Generator)
    B ~~~ C(LLM Call Evaluator)
    C -- Accepted --> D[Out]
    B -- Solution --> C
    C -- Rejected + Feedback --> B
```

## Framework Integrations

This repository showcases how to achieve these workflows using multiple frameworks side by side. The goal is a pluggable architecture where you can select the framework of your choice or even mix-and-match.

### pydanticAI (currently implemented)
- **Schema-first Approach**: Uses pydantic for strict data validation and structured outputs.
- **Agent Modules**: Each agent can have well-defined data schemas for inputs/outputs.
- **Integration**: Ties neatly into Python-based tools and databases.

### crewAI (future implementations)
- **Task Management**: A higher-level interface for orchestrating multiple agents or workers.
- **Built-in Router**: CrewAI can automatically route tasks based on skill sets or expertise.
- **Scalability**: Parallelism is a first-class concept, making concurrency straightforward.

### instructor (future implementations)
- **Language Model Guidance**: Provides advanced prompting techniques, letting you create instruct-style prompts and parse the responses accordingly.
- **Training & Fine-tuning**: Works well if you plan to fine-tune an existing model for domain-specific tasks.
- **Evaluation**: Comes with built-in tools for metric-based or human-in-the-loop evaluations.

## Directory Structure

Below is a simplified overview of the repository structure:

```
01-the-augmented-LLM/
pydantic_agents/
  ├── agents/
  ├── clients/
  ├── models/
  ├── tools/
02-the-prompt-chaining-workflow/
03-the-routing-workflow/
04-the-parallelization-workflow/
05-the-orchestrator-workers-workflow/
06-the-evaluator-optimizer-workflow/
```

## Getting Started

1. **Clone** the repo and install dependencies:

   ```bash
   git clone https://github.com/slavakurilyak/building-effective-agents.git
   cd building-effective-agents
   pip install -r requirements.txt
   ```

2. **Try** out the sample agents in `pydantic_agents/agents/` or create your own by following the examples.
3. **Extend** with your chosen frameworks — `crewAI`, `instructor`, or others — to replicate best practices.

## Contributing

I welcome contributions! Submit PRs for bug fixes, improvements, or new features. Please create an issue beforehand to discuss major changes or new modules.

## License

This project is licensed under the [MIT License](LICENSE). Feel free to use it for your own projects. If you find it valuable, please consider contributing back!