import json, os

settings = json.load(open("setup.json", "r"))
username = settings["username"]

def crontab_init():

    # clear all crontab
    cron = CronTab(user=username)
    cron.remove_all()
    cron.write()

def process_setup_file():
    for app in settings["apps"]:
        print "----- Fetching {} -----".format(app["description"])
        if "repo" in app:
            clone_repo(app["repo"])
        if "cron" in app:
            add_cronjobs(app["description"], app["cronjobs"])

def clone_repo(repo):
    repo_name = repo.split("/")[-1]
    os.system("rm -rf " + repo_name)
    os.system("git clone " + repo)

def add_cronjobs(description, cronjobs):
    cron = CronTab(user=username)
    for cronjob in cronjobs:
        job  = cron.new(
            command=cronjob['command'],
            comment=description)
        job.setall(cronjob['schedule'])
        cron.write()

crontab_init()
process_setup_file()