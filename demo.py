import openai
openai.api_key = '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'

from llm_agent import Agent
from llm_agent import Action

#Set Up Available Functions
fh = open("demo/business_ideas.txt", "r")

def get_next_pitch():
  next_line = fh.readline()
  if next_line == '':
    fh.close()
    return "No More Pitches."
  print(f"Evaulating pitch: {next_line.strip()}")
  return next_line

def accept(memo):
  print(f"Accepted with memo: {memo}\n---")
  return 'Saved'

def reject(note):
  print(f"Rejected with note: {note}\n---")
  return 'Sent'

#Create our Agent
agent = Agent(
  name="LOIS",
  persona="""
LOIS is an associate at a Venture Capital firm. 
She spends a lot of time reviewing pitches the firm receives from a variety of sources, and can quickly tell whether or not an idea merits further investigation.
""".strip(),
  task="""
LOIS's current task is to review emails with pitches the firm has received and sort them into two categories: Accepted or Rejected.
When she rejects a pitch, she also writes a polite response to the email explaining that the firm is not interested and including a reason why. 
When she accepts a pitch, she also writes a short memo for her manager describing why she thinks they should consider the pitch further. 
She must do this until GET_NEXT_PITCH returns "No More Pitches".
""".strip(),
  actions=[
    Action(
      impl=get_next_pitch,
      name="GET_NEXT_PITCH",
      args=[],
      returns="The text of the next pitch in the inbox, or \"No More Pitches\" if there were no pitches remaining."
    ),
    Action(
      impl=reject,
      name="REJECT",
      args=[{
        "name": "Response",
        "desc": "The text of the polite response that LOIS wrote in the rejection email."
      }],
      returns="Sent if the message was sent, or an error if not."
    ),
    Action(
      impl=accept,
      name="ACCEPT",
      args=[{
        "name": "Memo",
        "desc": "The text of the memo LOIS wrote for her manager."
      }],
      returns="Saved is the memo was saved, or an error if not."
    )
  ]
)

print(agent.run(max_tries=30,max_log_length=4))