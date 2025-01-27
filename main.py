import json
import os
from fastapi import FastAPI, HTTPException
import google.generativeai as genai

# Configure Gemini API using the provided API key
genai.configure(api_key="YOUR API KEY")

# Create FastAPI app
app = FastAPI()

@app.get("/")
async def health_check():
    return {"message": "API is up and running"}

@app.post("/analyze_quiz")
async def analyze_quiz():
    """Endpoint to analyze quiz data and generate insights"""
    try:
        # Load JSON data from the file
        if not os.path.exists("API_Endpoint.json"):
            raise FileNotFoundError("API_Endpoint.json file not found")
        
        with open("API_Endpoint.json", "r") as file:
            input_data = json.load(file)

        # Convert input data to a string
        data_str = json.dumps(input_data, indent=2)

        # Construct the prompt for Gemini Pro
        prompt = (
            f"Analyze the following quiz data:\n\n{data_str}\n\n"
            "Create Recommendations:\n"
            "- Propose actionable steps for the user to improve, such as suggested topics, question types, or difficulty levels to focus on.\n\n"
            "Bonus Points:\n"
            "- Analyze and define the student persona based on patterns in the data.\n"
            "- Highlight specific strengths and weaknesses with creative labels or insights."
        )

        # Use Gemini to generate analysis
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        # Verify and return the response
        if hasattr(response, "text"):
            return {
                "status": "success",
                "analysis": response.text
            }
        else:
            raise ValueError("Unexpected response format from Gemini API")

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
