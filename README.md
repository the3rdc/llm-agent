# llm-agent
Python framework to use LLMs like GPT-3 to perform tasks using a set of available functions.

## How To Use:
Check out demo.py for an example.

Import the Agent and Action classes:
```
from llm_agent import Agent
from llm_agent import Action
```

Agent takes four arguments, a name, persona, task and actions
```
class Agent:
  def __init__(self, name, persona, task, actions):
```
- Name: Is just a name for your agent. Be consistant if you use it in the persona or task descriptions.
- Persona: GPT is really good at "role playing". Describe a fictional person who would be good at your task.
- Task: This is a text description of what your agent should do and how. Persona and Task will be included in every call to the model, so keep these breif if you can.
- Actions: A list of Action instances.

Action takes four arguments as well:
```
class Action:
  def __init__(self, name, args, returns, impl):
```
- Name: Name of the action. Reccomended to keep this all caps and _.
- Args: A list of aruments the action takes (can be empty) each of which is a dict with a "name" and "desc" property.
- Returns: Text description of what the action returns (must return something, even if it's the word None)
- impl: A python function used to implement the action. Should accept any arguments specified in the order they are listed, and return text.

Once you've instantiated your agent, call run:
```
result = agent.run(max_tries=50,max_log_length=6)
```
- Max Tries: Is the maximum number of calls to make to the model. Execution will end when max tries is reached OR when the model chooses the TASK_COMPLETED action.
- Max Log Length: The max number of lines (each action + response is 2 lines) to included in the log in each prompt.
(TODO: Support limit based on Token count instead of lines.)

## Tips:
- Typos are death. Again, the model is good at role playing, and if you have typos it will role play someone who makes mistakes.
- Well written argument descriptions for your actions can serve as extra hints at how to use them when they align well with the task description.
- Less is more with log length. Think about the max history that will be helpful for your use case and don't go longer. Extra long logs seem to coax the model into a ditch of repetitiion. Try running the demo, for example, with 6 instead of 4 for max log length and see the difference.
- You still need to do "prompt engineering" here. Expect the first few versions of your agent to be close-but-not-quite and tweak task/action language until you get there.