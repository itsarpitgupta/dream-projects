class Job:
    job_name = ""
    job_description = ""
    created_by = ""
    created_date_time = ""
    modified_by = ""
    modified_date_time = ""
    img_source = ""
    display = "ON"
    tools = []

    def __init__(self, job_name, job_description, created_by, created_date_time,
                 modified_by, modified_date_time, img_source, display, tools):
        self.job_name = job_name
        self.job_description = job_description
        self.created_by = created_by
        self.created_date_time = created_date_time
        self.modified_by = modified_by
        self.modified_date_time = modified_date_time
        self.img_source = img_source
        self.display = display
        self.tools = tools
