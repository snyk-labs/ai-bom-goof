from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware, HumanInTheLoopMiddleware, ModelCallLimitMiddleware, ToolCallLimitMiddleware, TodoListMiddleware
from crewai import Agent

model = ChatOpenAI(
    model="gpt-4o",
    openai_proxy="http://proxy.remote-llm-gateway.com:8080"
)

agent_with_all_middleware = create_agent(
    model="gpt-4o",
    middleware=[
        PIIMiddleware(
            "email",
            strategy="redact",
            apply_to_input=True,
        ),
        HumanInTheLoopMiddleware(
            interrupt_on={
                "your_send_email_tool": {
                    "allowed_decisions": ["approve", "edit", "reject"],
                },
                "your_read_email_tool": False,
            }
        ),
        ModelCallLimitMiddleware(
            thread_limit=10,
            run_limit=5,
            exit_behavior="end",
        ),
        ToolCallLimitMiddleware(thread_limit=20, run_limit=10),
        TodoListMiddleware()
    ],
)

agent_with_pii_middleware = create_agent(
    model="gpt-4o",
    middleware=[
        PIIMiddleware(
            "email",
            strategy="redact",
            apply_to_input=True,
        ),
    ],
)

agent_without_middleware = Agent()