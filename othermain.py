from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# HTML form to submit user input
html_form = """
<!DOCTYPE html>
<html>
<head>
    <title>User Input Form</title>
</head>
<body>
    <h1>Enter Your Text</h1>
    <form method="post" action="/submit">
        <label for="user_input">Enter Text:</label>
        <input type="text" id="user_input" name="user_input" required>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return html_form


@app.post("/submit")
async def handle_form_submission(user_input: str = Form(...)):
    # Perform an action here with the user's input.
    # In this example, we print the user's input to the server's console.
    print("User input:", user_input)
    with open('dump.txt', 'a') as file:
        file.write(user_input + '\n')
    # You can add your own logic or actions here.

    return {"message": "User input submitted successfully"}
