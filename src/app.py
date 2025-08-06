"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    # Sports activities
    "Basketball Team": {
        "description": "Competitive basketball team with regular matches and training",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu", "lucas@mergington.edu"]
    },
    "Swimming Club": {
        "description": "Swimming lessons and competitive team training",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["lily@mergington.edu", "noah@mergington.edu"]
    },
    # Artistic activities
    "Art Studio": {
        "description": "Drawing, painting, and mixed media art creation",
        "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["isabella@mergington.edu", "ethan@mergington.edu"]
    },
    "Drama Club": {
        "description": "Theater productions and acting workshops",
        "schedule": "Mondays and Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    # Intellectual activities
    "Debate Team": {
        "description": "Practice logical argumentation and compete in debate tournaments",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 16,
        "participants": ["william@mergington.edu", "charlotte@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Prepare for and compete in science competitions across various disciplines",
        "schedule": "Tuesdays, 3:30 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["benjamin@mergington.edu", "amelia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Check if the student is already registered
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already registered for this activity")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Check if the student is registered
    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is not registered for this activity")

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
