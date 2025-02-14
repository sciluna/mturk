from dotenv import load_dotenv
import os
import boto3
import json

MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
mturk = boto3.client('mturk',
   aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
   aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY"),
   region_name='us-east-1',
   endpoint_url = MTURK_SANDBOX
)
# You will need the following library
# to help parse the XML answers supplied from MTurk
# Install it in your local environment with
# pip install xmltodict
import xmltodict

# Read the HIT IDs from the file
with open('hit_ids.json', 'r') as f:
    hit_ids = json.load(f)

""" hit_ids = ['3EHVO81VOUR4II75BID54J9QKZH1HF', '3IH9TRB0G054EDIPH0VQ4VA5KCW1I8', '3IVEC1GSME509O2VZIGQGWP5XRL1JK', '3W0XM68Y0E1VK88DH3G2HBPICGL1KJ'] """

all_results = []
# Loop through all HIT IDs and fetch results
for hit_id in hit_ids:
    print(f"\nFetching results for HIT: {hit_id}")
    
    worker_results = mturk.list_assignments_for_hit(HITId=hit_id, AssignmentStatuses=['Submitted'])
    
    if worker_results['NumResults'] > 0:
        hit_data = {"HITId": hit_id, "Assignments": []}
        for assignment in worker_results['Assignments']:
            xml_doc = xmltodict.parse(assignment['Answer'])

            assignment_data = {
               "WorkerId": assignment['WorkerId'],
               "AssignmentId": assignment['AssignmentId'],
               "Answers": []
            }
            
            print(f"Worker's answer for HIT {hit_id}:")
            if type(xml_doc['QuestionFormAnswers']['Answer']) is list:
                # Multiple fields in HIT layout
                for answer_field in xml_doc['QuestionFormAnswers']['Answer']:
                    question = answer_field['QuestionIdentifier']
                    answer = answer_field['FreeText']
                    print(f"  For input field: {answer_field['QuestionIdentifier']}")
                    print(f"  Submitted answer: {answer_field['FreeText']}")
                    assignment_data["Answers"].append({"Question": question, "Answer": answer})                    
            else:
                # One field found in HIT layout
                question = xml_doc['QuestionFormAnswers']['Answer']['QuestionIdentifier']
                answer = xml_doc['QuestionFormAnswers']['Answer']['FreeText']
                print(f"  For input field: {xml_doc['QuestionFormAnswers']['Answer']['QuestionIdentifier']}")
                print(f"  Submitted answer: {xml_doc['QuestionFormAnswers']['Answer']['FreeText']}")
                assignment_data["Answers"].append({"Question": question, "Answer": answer})

            hit_data["Assignments"].append(assignment_data)
        all_results.append(hit_data)
        
    else:
        print(f"No results for HIT {hit_id} yet.")

with open('hit_results.json', 'w') as f:
   json.dump(all_results, f, indent=4)