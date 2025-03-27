from fastapi import FastAPI, HTTPException  # Import FastAPI framework and HTTPException for error handling
from pydantic import BaseModel  # Import BaseModel from Pydantic for data validation
from typing import Dict, Optional, List  # Import typing utilities for type hints

# Create a FastAPI application instance
app = FastAPI()

# In-memory storage for users (dictionary with user ID as key and user details as value)
users_db: Dict[int, dict] = {}

# Define a Pydantic model for user data
class User(BaseModel):
    id: int  # Unique identifier for the user
    name: str  # User's name
    phone_no: str  # User's phone number
    address: str  # User's address

# Define a Pydantic model for updating user data (all fields are optional)
class UpdateUser(BaseModel):
    name: Optional[str] = None  # Optional name field
    phone_no: Optional[str] = None  # Optional phone number field
    address: Optional[str] = None  # Optional address field

# Route to create a new user
@app.post("/users/", status_code=201)  # HTTP POST request with a 201 (Created) status code
def create_user(user: User):
    if user.id in users_db:  # Check if user ID already exists
        raise HTTPException(status_code=400, detail="User ID already exists")  # Return 400 error if ID is duplicate
    users_db[user.id] = user.dict()  # Store user data in the in-memory database
    return {"message": "User created successfully"}  # Return success message

# Route to fetch all users
@app.get("/users/")
def get_all_users() -> List[dict]:
    return list(users_db.values())  # Return a list of all stored users

# ✅ Moved this route above `/users/{id}` to prevent path conflicts
@app.get("/users/search")
def search_users(name: str) -> List[dict]:
    """
    Search users by name.
    - GET /users/search?name={name}
    - Returns a list of users matching the provided name.
    """
    # Filter users by name (case-insensitive)
    result = [user for user in users_db.values() if user["name"].lower() == name.lower()]
    return result  # Return the matching users

# Route to fetch a single user by ID
@app.get("/users/{id}")
def get_user(id: int):
    if id in users_db:  # Check if user exists
        return users_db[id]  # Return user data
    raise HTTPException(status_code=404, detail="User not found")  # Return 404 if user not found

# Route to update user details
@app.put("/users/{id}")
def update_user(id: int, user_update: UpdateUser):
    if id not in users_db:  # Check if user exists
        raise HTTPException(status_code=404, detail="User not found")  # Return 404 if user is not found
    
    user = users_db[id]  # Retrieve existing user data
    if user_update.name is not None:  # Update name if provided
        user["name"] = user_update.name
    if user_update.phone_no is not None:  # Update phone number if provided
        user["phone_no"] = user_update.phone_no
    if user_update.address is not None:  # Update address if provided
        user["address"] = user_update.address
    
    return {"message": "User updated successfully"}  # Return success message

# Route to delete a user by ID
@app.delete("/users/{id}")
def delete_user(id: int):
    if id not in users_db:  # Check if user exists
        raise HTTPException(status_code=404, detail="User not found")  # Return 404 if user is not found
    
    del users_db[id]  # Remove user from the database
    return {"message": "User deleted successfully"}  # Return success message
