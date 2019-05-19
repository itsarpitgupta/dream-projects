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
