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

from fastapi.responses import HTMLResponse




# Handle request for "Feeling" intent (from main1.py)
@router.post("/feeling")
async def handle_feeling_request(request: Request):
    payload = await request.json()

    # Accessing the intent and parameters
    intent = payload['queryResult']['intent']['displayName']  # Get the intent name
    parameters = payload['queryResult']['parameters']  # Get the parameters

    # Check if the intent is "Feeling"
    if intent == "Feeling":
        feeling = parameters.get("feeling")  # Extract feeling from parameters
        
        # Check if feeling is a list or a single value
        if isinstance(feeling, list):
            # Insert each feeling into the database
            insert_successful = True
            for f in feeling:
                try:
                    if not insert_diagnosis(f):
                        insert_successful = False
                        logging.error(f"Failed to insert feeling: {f}")
                except Exception as e:
                    insert_successful = False
                    logging.error(f"Error while inserting feeling '{f}': {e}")
            if insert_successful:
                return JSONResponse(content={
                    "fulfillmentText": "Feelings successfully recorded."
                })
            else:
                return JSONResponse(content={
                    "fulfillmentText": "Failed to insert feelings."
                })
        elif feeling:  # If it's a single value
            try:
                if insert_diagnosis(feeling):
                    return JSONResponse(content={
                        "fulfillmentText": "Feeling successfully recorded."
                    })
                else:
                    return JSONResponse(content={
                        "fulfillmentText": "Failed to insert feeling."
                    })
            except Exception as e:
                logging.error(f"Error while inserting feeling '{feeling}': {e}")
                return JSONResponse(content={
                    "fulfillmentText": f"Error: {e}"
                })

    # Return the original response from the chatbot if the intent is not "Feeling"
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

# Handle request for "Track" and "Feeling" (Combined functions)
@app.post("/")
async def handle_request(request: Request):
    payload = await request.json()

    # Correct the keys for accessing intent and parameters
    intent = payload['queryResult']['intent']['displayName']  # Note the uppercase 'N' in 'displayName'
    parameters = payload['queryResult']['parameters']  # Corrected 'queryresult' to 'queryResult'
    username = parameters.get("username")  # Extract username from parameters

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

    # Handle "Feeling" intent
    if intent == "Feeling":
        feeling = parameters.get("feeling")  # Extract feeling from parameters
        
        # Check if feeling is a list or a single value
        if isinstance(feeling, list):
            # Insert each feeling into the database
            insert_successful = True
            for f in feeling:
                try:
                    if not insert_diagnosis(f):
                        insert_successful = False
                        logging.error(f"Failed to insert feeling: {f}")
                except Exception as e:
                    insert_successful = False
                    logging.error(f"Error while inserting feeling '{f}': {e}")
            if insert_successful:
                return JSONResponse(content={
                    "fulfillmentText": "Feelings successfully recorded."
                })
            else:
                return JSONResponse(content={
                    "fulfillmentText": "Failed to insert feelings."
                })
        elif feeling:  # If it's a single value
            try:
                if insert_diagnosis(feeling):
                    return JSONResponse(content={
                        "fulfillmentText": "Feeling successfully recorded."
                    })
                else:
                    return JSONResponse(content={
                        "fulfillmentText": "Failed to insert feeling."
                    })
            except Exception as e:
                logging.error(f"Error while inserting feeling '{feeling}': {e}")
                return JSONResponse(content={
                    "fulfillmentText": f"Error: {e}"
                })

    # Default response for other intents
    return JSONResponse(content={
        "fulfillmentText": "This intent is not handled yet."
    })

# Include the router in the app
app.include_router(router)

