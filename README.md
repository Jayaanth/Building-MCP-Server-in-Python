# Building-MCP-Server-in-Python
Implementing the "Building a Simple MCP Server in Python" by MLM

![alt text](image.png)

## MCP Definition

* MCP standardizes how LLMs and other AI models interact with external systems
* Open protocol that defines how AI applications communicate with external systems.

## How MCP Works
* **Hosts** : That which has direct connection to the LLM
* **Clients** : Client instances enables the Host to connect with the MCP servers, one connection per instance
* **Servers** : API integrations, DB access, File operations which respond to client requests
* **User** : Interacts with the host

## 3 Core Primitive
* **Tools** : Functions that perform actions. Executable commands which the LLM can invoke - LLMs to Client
* **Resources** : They allow viewing information without changing it - Client to Server
* **Prompts** : Commands that decide how the model approaches tasks - User to LLM.