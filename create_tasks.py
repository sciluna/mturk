from dotenv import load_dotenv
import os
import boto3
import csv
import json

load_dotenv()

MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
mturk = boto3.client('mturk',
   aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
   aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
   region_name='us-east-1',
   endpoint_url = MTURK_SANDBOX
)

# Read the XML template
with open("questions.xml", "r") as file:
    question_template = file.read()

# Read CSV file
csv_filename = "sbgn_data.csv"
hit_ids = []

with open(csv_filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        # Replace placeholders in XML template
        question = question_template.replace("${url}", row["url"]) \
                                    .replace("${filename}", row["filename"]) \
                                    .replace("${nodeData}", row["nodeData"]) \
                                    .replace("${edgeData}", row["edgeData"]) \
                                    .replace("${refCardLink}", row["refCardLink"])

        # Create HIT
        new_hit = mturk.create_hit(
            Title='Create Hand-Drawn Versions of the Diagrams (Graphs)',
            Description='In this task, you will hand-draw a diagram (graph), replicating the structure and connections in the diagram.',
            Keywords='data collection, hand-drawn diagram, graph drawing, graph replication',
            Reward='0.50',
            MaxAssignments=1,
            LifetimeInSeconds=604800,
            AssignmentDurationInSeconds=1200,
            AutoApprovalDelayInSeconds=604800,
            Question=question
        )

        # Store the HIT ID
        hit_id = new_hit['HIT']['HITId']
        hit_ids.append(hit_id)
        print("https://workersandbox.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId'])
        print(f"Created HIT: {hit_id}")

# Print all HIT IDs
print("All HITs created:", hit_ids)
# Save the list of HIT IDs to a file
with open('hit_ids.json', 'w') as f:
    json.dump(hit_ids, f)

""" new_hit = mturk.create_hit(
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
# Use: https://worker.mturk.com/mturk/preview?groupId= """