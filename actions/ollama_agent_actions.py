"""
Ollama Agent Actions
This module provides action classes for the Ollama-based agent to perform specific tasks.
"""

import os
import subprocess
import platform
from typing import Dict, Any, List
from attrs import define


@define
class BaseAction:
    """Base class for all agent actions."""
    name: str
    description: str
    
    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """Execute the action and return results."""
        raise NotImplementedError("Subclasses must implement execute method")


@define
class SystemInfoAction(BaseAction):
    """Action to collect system information."""
    name: str = "system_info"
    description: str = "Collects information about the current system"
    
    def execute(self) -> Dict[str, Any]:
        system_info = {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "hostname": platform.node(),
            "python_version": platform.python_version(),
        }
        
        return {
            "success": True,
            "data": system_info
        }


@define
class RunCommandAction(BaseAction):
    """Action to run a shell command and return the output."""
    name: str = "run_command"
    description: str = "Runs a system command and returns the output"
    allowed_commands: List[str] = ["echo", "dir", "ls", "whoami", "pwd", "hostname", "python --version"]
    
    def is_command_allowed(self, command: str) -> bool:
        """Check if the command is allowed to run."""
        command_base = command.split()[0].lower()
        
        # Direct match check
        if command in self.allowed_commands:
            return True
            
        # Base command check
        return command_base in [cmd.split()[0].lower() for cmd in self.allowed_commands]
    
    def execute(self, command: str) -> Dict[str, Any]:
        """Execute a shell command."""
        if not self.is_command_allowed(command):
            return {
                "success": False,
                "error": f"Command '{command}' is not allowed for security reasons."
            }
        
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=10  # Timeout after 10 seconds
            )
            
            return {
                "success": True,
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Command execution timed out"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


@define
class FileOperationAction(BaseAction):
    """Action to perform basic file operations."""
    name: str = "file_operation"
    description: str = "Performs basic file operations like reading, listing directories"
    base_dir: str = os.getcwd()  # Restrict to current directory for safety
    
    def execute(self, operation: str, file_path: str = "", content: str = "") -> Dict[str, Any]:
        """Execute a file operation."""
        # Normalize and validate the path
        path = file_path
        target_path = os.path.normpath(os.path.join(self.base_dir, path))
        
        # Security check - ensure path is within base_dir
        if not target_path.startswith(self.base_dir):
            return {
                "success": False,
                "error": "Access denied: Cannot access paths outside the base directory"
            }
            
        try:
            if operation == "read":
                if not os.path.exists(target_path):
                    return {"success": False, "error": f"File not found: {path}"}
                    
                if os.path.isdir(target_path):
                    return {"success": False, "error": f"{path} is a directory, not a file"}
                    
                with open(target_path, 'r') as file:
                    content = file.read()
                return {"success": True, "content": content}
                
            elif operation == "list":
                if not os.path.exists(target_path):
                    return {"success": False, "error": f"Directory not found: {path}"}
                    
                if not os.path.isdir(target_path):
                    return {"success": False, "error": f"{path} is not a directory"}
                
                items = os.listdir(target_path)
                return {
                    "success": True,
                    "items": items,
                    "path": path
                }
            elif operation == "write":
                if not os.path.exists(os.path.dirname(target_path)):
                    return {"success": False, "error": f"Directory not found: {os.path.dirname(path)}"}
                    
                with open(target_path, 'w') as file:
                    file.write(content)
                return {"success": True, "message": f"File written: {path}"}
                
            else:
                return {"success": False, "error": f"Unsupported operation: {operation}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
