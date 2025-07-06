import json

# convert the json file to a json one line file
with open('/raws/student_job_hunt_berlin_cleaned.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('/raws/student_job_hunt_berlin_cleaned.jsonl', 'w', encoding='utf-8') as f:
    for item in data:
        f.write(json.dumps(item) + "\n")
