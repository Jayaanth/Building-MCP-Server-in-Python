from fastmcp import FastMCP
from datetime import datetime

# Server initialization
mcp = FastMCP("TaskTracker") # Creates the MCP server with a name

tasks = [] # List that stores all the tasks
tasks_id_counter = 1 # Generates unique ids for each task

# Tool creation
# Tool 1 to add tasks to the list

@mcp.tool()
def add_task(title: str, description: str ="")-> dict:

    """
    Takes a task title (required) and an optional description.
    Creates a task dictionary with a unique ID, status, and timestamp.
    Adds it to our tasks list.
    Returns the created task.

    """

    global tasks_id_counter
    task = {
        "id" : tasks_id_counter,
        "title": title,
        "description": description,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }

    tasks.append(task)
    tasks_id_counter+=1

    return task

@mcp.tool()
def complete_task(task_id: int)-> dict:

    """The tool searches the task list for a matching ID, updates its status to “completed”, 
    and stamps it with a completion timestamp.
    It then returns the updated task or an error message if no match is found."""

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "completed"
            task["completed_at"]= datetime.now().isoformat()
            return task
        
    return ["error":f"Task{task_id} not found"]


@mcp.tool()
def delete_task(task_id: int)-> dict:
    """This tool searches for a task, removes it from the list, 
    and returns confirmation with the deleted task data."""

    for i, task in enumerate(tasks):
        if task["id"]==task_id:
            deleted_task =task.pop(i)
            return {"success":True, "deleted":deleted_task}
    return {"success":False, "error":f"Task {task_id} not found"}

