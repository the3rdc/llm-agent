import openai

class Agent:
  def __init__(self, name, persona, task, actions):
    self.name = name
    self.persona = persona
    self.task = task
    self.actions = actions
    self.log = ""

  def prompt(self):
    return f"""
{self.persona}

{self.task}

The following is a LOG of {self.name}'s actions as they perform this task. Log entries have the following format:
ACTION_NAME||Argument_1_value|||
RESPONSE||Result_of_action|||
ACTION2_NAME||Argument_1_value||Argument_N_value|||
RESPONSE||Result_of_action_2|||

{self.name} is limited to the following actions:
{self.action_list()}
TASK_COMPLETED
- Arg:Message: Text to return when the task has been completed
- Returns: None

--LOG--
{self.log}
    """.strip()

  def action_list(self):
    alist = ''
    for action in self.actions:
      alist += action.list_entry()
    return alist

  def get_next_action(self):
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=self.prompt(),
      temperature=0.5,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=["|||"]
    )
    return response.choices[0].text.strip()
  
  def handle_action(self, action):
    parts = action.split('||')
    name = parts[0]
    args = parts[1:]
    if name == 'TASK_COMPLETED':
      return (args[0], True)
    for act in self.actions:
      if act.name == name:
        return (act.call(args), False)
    return ("INVALID ACTION", False)

  def run(self, max_tries, max_log_length):
    for i in range(max_tries):
      next_action = self.get_next_action()
      (response, complete) = self.handle_action(next_action)
      if complete:
        return response
      self.log += f"\n{next_action}|||\nRESPONSE||{response.strip()}|||"
      if(len(self.log.split("\n")) > max_log_length):
        self.log = "\n".join(self.log.split("\n")[(0 - max_log_length):])
    
    return "Hit max tries without a complete message."
    



class Action:
  def __init__(self, name, args, returns, impl):
    self.name = name
    self.args = args
    self.returns = returns
    self.impl = impl

  def list_entry(self):
    entry = f"{self.name}\n"
    for arg in self.args:
      entry += f"- Arg:{arg['name']}: {arg['desc']}\n"
    entry += f"- Returns:{self.returns}"
    return entry

  def call(self, args):
    try:
      return self.impl(*args)
    except Exception as e:
      return f"Error calling {self.name}: {e.message}"