from typing import Generic, TypeVar, Callable, Optional
from dataclasses import dataclass

from pydantic_ai.result import RunResult

D = TypeVar('D')  # Dependencies type
R = TypeVar('R')  # Result type

@dataclass
class RunContext(Generic[D]):
    deps: D

class ModelRetry(Exception):
    """Exception to trigger model retries"""
    pass

class Agent(Generic[D, R]):
    def __init__(
        self,
        model: str,
        base_system_prompt: str,
        deps_type: type[D],
        result_type: type[R]
    ):
        self.model = model
        self.base_system_prompt = base_system_prompt
        self.deps_type = deps_type
        self.result_type = result_type
        self._tools: dict[str, Callable] = {}
        self._validators: list[Callable] = []

    def tool(self, func: Callable):
        """Decorator to register a tool"""
        self._tools[func.__name__] = func
        return func

    def result_validator(self, func: Callable):
        """Decorator to register a result validator"""
        self._validators.append(func)
        return func

    def system_prompt(self, func: Callable):
        """Decorator to modify system prompt"""
        self.system_prompt = func
        return func

    def run_sync(
        self,
        deps: D,
        function_call: Optional[dict] = None
    ) -> RunResult[R]:
        if function_call:
            tool_name = function_call["name"]
            arguments = function_call["arguments"]
            # Invoke the registered tool
            result = self._tools[tool_name](RunContext(deps), **arguments)
            return RunResult(
                data=result,
                _all_messages=[],
                _new_message_index=0,
                _cost=0,
            )
        else:
            # For now, do nothing else. (You could call an LLM, etc.)
            result = None
    
        # Validate the result
        for validator in self._validators:
            result = validator(RunContext(deps), result)
    
        return RunResult(data=result)