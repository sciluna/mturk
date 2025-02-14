import boto3
import os
import xmltodict
import json

# Initialize the MTurk client
MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
mturk = boto3.client('mturk',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name='us-east-1',
    endpoint_url=MTURK_SANDBOX
)

def fetch_assignments(hit_id):
    """Fetch all submitted assignments for a HIT."""
    return mturk.list_assignments_for_hit(HITId=hit_id, AssignmentStatuses=['Submitted'])

# Load HIT IDs from JSON file
def load_hit_ids(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save updated HITs back to JSON
def save_hit_ids(filename, hit_ids):
    with open(filename, 'w') as f:
        json.dump(hit_ids, f, indent=4)

def republish_hit(hit_id):
    """Republish a rejected HIT with the same settings."""
    hit_details = mturk.get_hit(HITId=hit_id)
    new_hit = mturk.create_hit(
        Title=hit_details['HIT']['Title'],
        Description=hit_details['HIT']['Description'],
        Keywords=hit_details['HIT']['Keywords'],
        Reward=hit_details['HIT']['Reward'],
        MaxAssignments=1,
        LifetimeInSeconds=int((hit_details['HIT']['Expiration'] - hit_details['HIT']['CreationTime']).total_seconds()),
        AssignmentDurationInSeconds=hit_details['HIT']['AssignmentDurationInSeconds'],
        AutoApprovalDelayInSeconds=hit_details['HIT']['AutoApprovalDelayInSeconds'],
        Question=hit_details['HIT']['Question']
    )
    print(f"Republished HIT with new ID: {new_hit['HIT']['HITId']}")
    return new_hit['HIT']['HITId']

def review_submissions(filename):
    hit_ids = load_hit_ids(filename)
    """Interactive session to review HIT submissions."""
    while True:
        hit_id = input("\nEnter HIT ID (or type 'exit' to quit): ").strip()
        if hit_id.lower() == "exit":
            break

        if hit_id not in hit_ids:
          print("❌ HIT ID not found in the JSON file.")
          continue
        
        # Fetch assignments
        worker_results = fetch_assignments(hit_id)
        
        if worker_results['NumResults'] == 0:
            print("No results ready yet.")
            continue
        
        for assignment in worker_results['Assignments']:
            assignment_id = assignment['AssignmentId']
            xml_doc = xmltodict.parse(assignment['Answer'])

            # Extract answers
            if isinstance(xml_doc['QuestionFormAnswers']['Answer'], list):
                answers = {ans['QuestionIdentifier']: ans['FreeText'] for ans in xml_doc['QuestionFormAnswers']['Answer']}
            else:
                answers = {xml_doc['QuestionFormAnswers']['Answer']['QuestionIdentifier']: xml_doc['QuestionFormAnswers']['Answer']['FreeText']}
            
            print(f"\nReviewing Assignment ID: {assignment_id}")
            for q_id, ans in answers.items():
                print(f"Question: {q_id}")
                print(f"Answer: {ans}")
            
            decision = input("Approve (A) / Reject (R): ").strip().lower()

            if decision == "a":
                mturk.approve_assignment(AssignmentId=assignment_id, RequesterFeedback="Good work!", OverrideRejection=False)
                print(f"✅ Approved assignment {assignment_id}")
                hit_ids.remove(hit_id)
            elif decision == "r":
                mturk.reject_assignment(AssignmentId=assignment_id, RequesterFeedback="Your answer did not meet our requirements.")
                print(f"❌ Rejected assignment {assignment_id}")

                hit_ids.remove(hit_id)
                # Republishing HIT
                new_hit_id = republish_hit(hit_id)
                hit_ids.append(new_hit_id)  # Add new HIT ID
                        # Save updated HIT list
        
        save_hit_ids(filename, hit_ids)
        print("Review completed for this HIT.\n")

if __name__ == "__main__":
    filename = "hit_ids.json"
    review_submissions(filename)
