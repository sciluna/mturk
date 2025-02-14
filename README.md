# mturk
This repository contains a sample code to see how MTurk API works.

## Installation
```
pip install virtualenv
git clone https://github.com/sciluna/mturk.git
cd mturk
virtualenv .
source bin/activate
pip install boto3
pip install xmltodict
```
## Usage
```create_tasks.py``` is for creating tasks in a batch. It uses questions.xml as the template layout (you can modify this file to change the UI of your hit). It reads the csv file provided (in this case sbgn_data.csv) and loops through it to generate and publish different hits based on the data provided in csv file. This file also writes generated hit IDs to a file named hit_id.json.

```get_results.py``` is for getting submissons done to the hits. It reads hit_id.json, loops through it and prints the current results to the console. This script also writes the info about hits that have submissions to a file named hit_results.json.

```review_submissions.py``` is for accepting or rejecting the hits based on hit ID. This script requires you to enter hit ID and then shows the submission for that hit and asks to accept/reject the hit in an interactive way. 

## Notes
- This demo uses sandbox feature of MTurk. To publish in real MTurk environment, the links in the code should be adjusted accordingly.
- This demo is mainly based on the tutorial [here](https://blog.mturk.com/tutorial-a-beginners-guide-to-crowdsourcing-ml-training-data-with-python-and-mturk-d8df4bdf2977). It also contains information about setting AWS and MTurk accounts and connecting them. 
