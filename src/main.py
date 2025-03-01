from fastapi import FastAPI, APIRouter, Form, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
import logging
from db_helper import insert_user  # Import the insert_user function from db_helper
from db_helper1 import insert_diagnosis  # Import the insert_diagnosis function from db_helper1
from db_helper2 import get_diagnosis  # Import the get_diagnosis function from db_helper2

# Initialize FastAPI app and router
app = FastAPI()
router = APIRouter()

# Test the database connection at the start
import db_helper
db_helper.test_db_connection()

# Logging setup
logging.basicConfig(level=logging.INFO)

# Routes

# Signup endpoint to handle form submission
@router.post("/signup")
async def signup(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
):
    # Basic validation: check if passwords match
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    # Insert the new user into the database
    insert_user(username, password)
    
    # Redirect to a welcome or login page after successful signup
    return RedirectResponse(url="/welcome", status_code=303)

# Welcome endpoint
@router.get("/welcome")
async def welcome():
    return {"message": "Welcome to Calmconnect! You have successfully logged in. Please head back to the Home page."}

# Handle request for "Feeling" intent
@router.post("/feeling")
async def handle_feeling_request(request: Request):
    payload = await request.json()

    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']

    if intent == "Feeling":
        feeling = parameters.get("feeling")
        if isinstance(feeling, list):
            for f in feeling:
                try:
                    insert_diagnosis(f)
                except Exception as e:
                    logging.error(f"Error while inserting feeling '{f}': {e}")
        elif feeling:
            try:
                insert_diagnosis(feeling)
            except Exception as e:
                logging.error(f"Error while inserting feeling '{feeling}': {e}")

    return JSONResponse(content={
        "fulfillmentText": payload['queryResult']['fulfillmentText']
    })

# Handle request for "Track" intent (from main2.py)
@router.post("/track")
async def handle_track_request(request: Request):
    payload = await request.json()

    # Correct the keys for accessing intent and parameters
    intent = payload['queryResult']['intent']['displayName']  # Note the uppercase 'N' in 'displayName'
    parameters = payload['queryResult']['parameters']  # Corrected 'queryresult' to 'queryResult'
    username = parameters.get("username")  # Extract username from parameters

    # Check if the intent is "Track"
    if intent == "Track" and username:
        try:
            diagnosis = get_diagnosis(username)
            if diagnosis:
                return JSONResponse(content={
                    "fulfillmentText": f"Diagnosis for {username}: {diagnosis}"
                })
            else:
                return JSONResponse(content={
                    "fulfillmentText": f"No diagnosis found for {username}."
                })
        except Exception as e:
            logging.error(f"Error while retrieving diagnosis for {username}: {e}")
            return JSONResponse(content={
                "fulfillmentText": f"Error: {e}"
            })

    # Default response for other intents
    return JSONResponse(content={
        "fulfillmentText": "This intent is not handled yet."
    })

# Combined handler for "Track" and "Feeling" intents
@app.post("/")
async def handle_request(request: Request):
    payload = await request.json()

    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    username = parameters.get("username")

    # Handle "Track" intent
    if intent == "Track" and username:
        try:
            diagnosis = get_diagnosis(username)
            if diagnosis:
                return JSONResponse(content={
                    "fulfillmentText": f"Diagnosis for {username}: {diagnosis}"
                })
            else:
                return JSONResponse(content={
                    "fulfillmentText": f"No diagnosis found for {username}."
                })
        except Exception as e:
            logging.error(f"Error while retrieving diagnosis for {username}: {e}")
            return JSONResponse(content={
                "fulfillmentText": f"Error: {e}"
            })

    if intent == "Feeling":
        feeling = parameters.get("feeling")
        if isinstance(feeling, list):
            for f in feeling:
                try:
                    insert_diagnosis(f)
                except Exception as e:
                    logging.error(f"Error while inserting feeling '{f}': {e}")
        elif feeling:
            try:
                insert_diagnosis(feeling)
            except Exception as e:
                logging.error(f"Error while inserting feeling '{feeling}': {e}")

    return JSONResponse(content={
        "fulfillmentText": payload['queryResult']['fulfillmentText']
    })

# Include the router in the app
app.include_router(router)
