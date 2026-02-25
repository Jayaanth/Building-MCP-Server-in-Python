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
        
    return {"error":f"Task{task_id} not found"}


@mcp.tool()
def delete_task(task_id: int)-> dict:
    """This tool searches for a task, removes it from the list, 
    and returns confirmation with the deleted task data."""

    for i, task in enumerate(tasks):
        if task["id"]==task_id:
            deleted_task =task.pop(i)
            return {"success":True, "deleted":deleted_task}
    return {"success":False, "error":f"Task {task_id} not found"}


# Adding Resources
@mcp.resource("tasks://all")
def get_all_tasks()-> str:
    """Get all tasks as formatted text."""
    if not tasks:
        return "No tasks found."
    
    result = "Current Tasks:\n\n"
    for task in tasks:
        status_emoji = "✅" if task["status"] == "completed" else "⏳"
        result += f"{status_emoji} [{task['id']}] {task['title']}\n"
        if task["description"]:
            result += f"   Description: {task['description']}\n"
        result += f"   Status: {task['status']}\n"
        result += f"   Created: {task['created_at']}\n\n"
    return result

@mcp.resource("tasks://pending")
def get_pending_tasks()-> str:
    """Get only pending tasks as formatted text."""
    pending_tasks = [task for task in tasks if task["status"] == "pending"]
    if not pending_tasks:
        return "No pending tasks found."
    
    result = "Pending Tasks:\n\n"
    for task in pending_tasks:
        result += f"⏳ [{task['id']}] {task['title']}\n"
        if task["description"]:
            result += f"   Description: {task['description']}\n"
        result += f"   Created: {task['created_at']}\n\n"
    return result

# Defining Prompts
@mcp.prompt()
def task_summary_prompt()-> str:
    """A prompt that provides a summary of all tasks, including counts of pending and completed tasks."""
    total_tasks = len(tasks)
    pending_tasks = len([task for task in tasks if task["status"] == "pending"])
    completed_tasks = len([task for task in tasks if task["status"] == "completed"])

    summary = f"Task Summary:\nTotal Tasks: {total_tasks}\nPending Tasks: {pending_tasks}\nCompleted Tasks: {completed_tasks}"
    return summary

# Running and Testing the Server
if __name__ == "__main__":
    mcp.run()

