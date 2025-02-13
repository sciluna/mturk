from dotenv import load_dotenv
import os
import boto3

load_dotenv()

MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
mturk = boto3.client('mturk',
   aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
   aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
   region_name='us-east-1',
   endpoint_url = MTURK_SANDBOX
)

question = open('questions.xml', 'r').read()
new_hit = mturk.create_hit(
    Title = 'Create Hand-Drawn Versions of the Diagrams (Graphs)',
    Description = 'In this task, you will hand-draw a diagram (graph), replicating the structure and connections in the diagram.',
    Keywords = 'data collection, hand-drawn diagram, graph drawing, graph replication',
    Reward = '0.50',
    MaxAssignments = 1,
    LifetimeInSeconds = 604800,
    AssignmentDurationInSeconds = 1200,
    AutoApprovalDelayInSeconds = 604800,
    Question = question,
)
print("A new HIT has been created. You can preview it here:")
print("https://workersandbox.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId'])
print("HITID = " + new_hit['HIT']['HITId'] + " (Use to Get Results)")
# Remember to modify the URL above when you're publishing
# HITs to the live marketplace.
# Use: https://worker.mturk.com/mturk/preview?groupId=