import json


class Job:

    def __init__(self, job_name, job_description, created_by, created_date_time, modified_by, modified_date_time,
                 tools, display):
        self.job_name = job_name
        self.job_description = job_description
        self.created_by = created_by
        self.created_date_time = created_date_time
        self.modified_by = modified_by
        self.modified_date_time = modified_date_time
        self.tools = tools
        self.display = display

    def toJSON(self):
        file_path = "D://github-repos//dream-projects//deepvision-py//com//deepvision//job//json//job16.json"
        try:
            json_data = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
            with open(file_path, 'w') as f:
                f.write(json_data)
        except FileNotFoundError:
            print(file_path + " not found.")
