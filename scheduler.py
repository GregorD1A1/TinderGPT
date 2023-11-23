import schedule
import time
import random
import requests

BASE_URL = 'http://localhost:8080'
# configure here your sessions
SESSION_CONFIG = {
    'session1': {
        'time_range': (18, 19),
        'endpoints': ['/start_tnd', '/respond_all', '/opener', '/opener', '/opener', '/close'],
    },
    'session2': {
        'time_range': (20, 21),
        'endpoints': ['/start_tnd', '/respond_all', '/rise', '/close'],
    },
}

# Dictionary to store jobs
scheduled_jobs = {}


def run_session(session_name):
    config = SESSION_CONFIG[session_name]
    print(f"Running {session_name}")

    for endpoint in config['endpoints']:
        requests.get(BASE_URL + endpoint)

    # After job is run, clear the specific job and set a new one for next day
    schedule.cancel_job(scheduled_jobs[session_name])
    schedule_randomly(session_name)


def schedule_randomly(session_name):
    # Generate a random minute between 0 and 59
    minute = str(random.randint(0, 59)).zfill(2)
    # Create a time string with random minute within the session's hour range
    time_range = SESSION_CONFIG[session_name]['time_range']
    for hour in range(time_range[0], time_range[1]):
        session_time = f"{hour}:{minute}"
        print(f"{session_name} scheduled for {session_time}")
        # Schedule the session for this random time
        job = schedule.every().day.at(session_time).do(run_session, session_name)
        # Store the job to scheduled_jobs dictionary
        scheduled_jobs[session_name] = job


for session in SESSION_CONFIG:
    schedule_randomly(session)

while True:
    # Check whether a scheduled task is pending to run or not
    schedule.run_pending()
    time.sleep(60)
