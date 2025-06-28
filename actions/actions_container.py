from typing import Dict, Any, Optional
from attrs import define

from actions.ollama_agent_actions import BaseAction, FileOperationAction, RunCommandAction, SystemInfoAction


class ActionRegistry:
    """Registry for available agent actions."""
    
    def __init__(self):
        self._actions: Dict[str, BaseAction] = {}
        
    def register(self, action: BaseAction) -> None:
        """Register an action with the registry."""
        self._actions[action.name] = action
        
    def get_action(self, name: str) -> Optional[BaseAction]:
        """Get an action by name."""
        return self._actions.get(name)
    
    def list_actions(self) -> Dict[str, str]:
        """List all available actions and their descriptions."""
        return {name: action.description for name, action in self._actions.items()}
    
    def execute_action(self, name: str, *args, **kwargs) -> Dict[str, Any]:
        """Execute an action by name."""
        action = self.get_action(name)
        if not action:
            return {"success": False, "error": f"Action '{name}' not found"}
            
        return action.execute(*args, **kwargs)
    


# Create and populate the default registry
default_registry = ActionRegistry()
default_registry.register(SystemInfoAction())
default_registry.register(RunCommandAction())
default_registry.register(FileOperationAction())