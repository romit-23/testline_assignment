# README for Analysis.ipynb

## Overview
This Jupyter Notebook, titled **Analysis.ipynb**, is designed to perform data analysis related to various topics in biology and health. It includes a dataset that captures quiz scores across different subjects, allowing for insights into performance trends and educational outcomes.

## Contents
The notebook contains the following key sections:

1. **Introduction**
   - Brief description of the dataset and its relevance.
   
2. **Data Loading**
   - Code to import necessary libraries and load the dataset.

3. **Data Exploration**
   - Initial exploration of the data structure, including:
     - Summary statistics
     - Data types
     - Missing values

4. **Data Visualization**
   - Visual representations of quiz scores by topic to identify patterns and trends.

5. **Statistical Analysis**
   - Application of statistical methods to analyze the performance across different subjects.

6. **Conclusion**
   - Summary of findings and potential implications for educational strategies.

## Dataset
The dataset includes the following columns:
- **quiz.topic**: The subject of the quiz (e.g., Body Fluids and Circulation, Human Reproduction).
- **score**: The score achieved by students in each quiz.
  - ![distribution of scores](score-vs-frequency.png)
  - ![score over time](score-over-time.png)
  -  ![topic&title.png](topic&title.png)
### Sample Data
| quiz.topic                               | score |
|------------------------------------------|-------|
| Body Fluids and Circulation              | 108   |
| Body Fluids and Circulation              | 92    |
| Body Fluids and Circulation              | 116   |
| Human Reproduction                       | 40    |
| Reproductive Health                      | 64    |

## Requirements
To run this notebook, ensure you have the following Python packages installed:
- Jupyter Notebook
- Pandas
- Matplotlib
- Seaborn
- NumPy

You can install these packages using pip:

```bash
pip install jupyter pandas matplotlib seaborn numpy
```

## Usage
1. Clone this repository or download the notebook file.
2. Open a terminal or command prompt.
3. Navigate to the directory containing the notebook.
4. Launch Jupyter Notebook:

```bash
jupyter notebook Analysis.ipynb
```

5. Follow the instructions within the notebook to execute the analysis.

API Guide
Docker Setup
To run the FastAPI application using Docker, follow these steps:
Create a Dockerfile: Use the following code in your Dockerfile:
text
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY API_Endpoint.json .
COPY main.py .

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]
Create main.py: Use the following code for your FastAPI application:
python
import json
import os
from fastapi import FastAPI, HTTPException
import google.generativeai as genai

# Configure Gemini API using the provided API key
genai.configure(api_key="AIzaSyBlNQsGCa4VjCUm8BB-HXvdOspO9j0W324")

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
Create requirements.txt: List all required Python packages needed for your FastAPI application:
text
fastapi==0.78.0
uvicorn==0.18.2
google-generativeai==x.x.x  # Replace with actual version if available.
Build and Run Docker Container:
Open a terminal in your project directory.
Build your Docker image:
bash
docker build -t fastapi-quiz-analyzer .
Run your Docker container:
bash
docker run -p 8000:8000 fastapi-quiz-analyzer
Accessing the API:
Once your container is running, you can access the API at http://localhost:8000.
Use tools like Postman or cURL to interact with your endpoints.
License
This project is licensed under the MIT License - see the LICENSE file for details.


## Acknowledgments
Thanks to all contributors who helped in developing this analysis framework.

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/50605726/363f2896-e22a-4c35-9ddf-160c4d446788/Analysis.ipynb
