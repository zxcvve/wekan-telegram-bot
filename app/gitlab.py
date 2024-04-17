import requests
import zipfile
import os


GITLAB_PRIVATE_TOKEN = os.environ["GITLAB_PRIVATE_TOKEN"]
GIT_URL = os.environ["GITLAB_URL"]
PROJECT_ID = 8
HEADERS = {"PRIVATE-TOKEN": GITLAB_PRIVATE_TOKEN}


def find_build_job_id(res_json):
    for x in res_json:
        if x["stage"] == "build":
            return x["id"]


def get_latest_successful_job():
    res = requests.get(
        f"{GIT_URL}/api/v4/projects/{PROJECT_ID}/jobs?scope[]=success", headers=HEADERS
    )
    res_json = res.json()
    latest_successful_build_job_id = find_build_job_id(res_json)
    return latest_successful_build_job_id


def download_artifacts_zip(job_id):
    url = f"{GIT_URL}/api/v4/projects/{PROJECT_ID}/jobs/{job_id}/artifacts"
    res = requests.get(url, headers=HEADERS)
    with open("artifacts.zip", "wb") as writer:
        writer.write(res.content)


def unzip_artifacts_zip(delete_zip_after_extraction=True):
    zip_files = []
    with zipfile.ZipFile("./artifacts.zip", "r") as zip_ref:
        zip_files += zip_ref.namelist()
        zip_ref.extractall("./")
    if delete_zip_after_extraction:
        os.remove("./artifacts.zip")
    return zip_files[0]


def get_latest_apk():
    job_id = get_latest_successful_job()
    download_artifacts_zip(job_id)
    apk_name = unzip_artifacts_zip()
    return apk_name
