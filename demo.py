import openai
openai.api_key = ''

from llm_agent import Agent
from llm_agent import Action

#Set Up Available Functions
fh = open("demo/tweets.txt", "r")

def get_next_tweet():
  next_line = fh.readline()
  if next_line == '':
    fh.close()
    return "None"
  print(f"Evaulating tweet: {next_line.strip()}")
  return next_line

def respond(text):
  print(f"Responded with tweet: {text}\n---")
  return 'True'

def flag(tweet):
  print(f"Flagged for further discussion\n---")
  return 'True'

def save(tweet):
  print(f"Saved as potential testimonial\n---")
  return 'True'

#Create our Agent
agent = Agent(
  name="LOIS",
  persona="""
LOIS works for "FauxCo", a sustainable fashion brand that uses eco-friendly materials and ethical manufacturing practices.
She manages FauxCo's social media, among other things, and is exceptionally good at interacting with customers.
""".strip(),
  task="""
LOIS's current task is to review recent tweets about FauxCo".
For most tweets, she'll respond with an appropriate comment.
For tweets that are exceptionally positive, she will save them in a separate file as possible customer testimonials for the website.
For tweets that are exceptionally negative, she'll flag them for further discussion with her team.
She does this until she's reviewed all tweets.
""".strip(),
  actions=[
    Action(
      impl=get_next_tweet,
      name="GET_NEXT_TWEET",
      args=[],
      returns="The text of the next tweet, or \"None\" if there are no tweets remaining."
    ),
    Action(
      impl=respond,
      name="RESPOND",
      args=[{
        "name": "Text",
        "desc": "The comment LOIS posts in response to the tweet"
      }],
      returns="True if the comment posted, or an error if not."
    ),
    Action(
      impl=flag,
      name="FLAG",
      args=[{
        "name": "Tweet",
        "desc": "The text of the negative flagged tweet."
      }],
      returns="True is the tweet was flagged, or an error if not."
    ),
    Action(
      impl=save,
      name="SAVE",
      args=[{
        "name": "Tweet",
        "desc": "The text of the positive saved tweet."
      }],
      returns="True is the tweet was saved, or an error if not."
    )
  ]
)

print(agent.run(max_tries=50,max_log_length=4))