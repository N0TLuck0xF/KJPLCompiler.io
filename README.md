# KJPLCompiler.io
KJPL Compiler with Vercel Serverless Functions
This project demonstrates how to build a KJPL Compiler using Vercel Serverless Functions. The compiler takes KJPL code as input and generates C code as output. The backend is hosted on Vercel, while the frontend can be deployed on GitHub Pages.

Features
KJPL to C Compilation: Convert KJPL code into C code using a serverless function.

Serverless Backend: Hosted on Vercel for automatic scaling and cost efficiency.

Frontend Integration: Easily integrate the compiler with a static frontend (e.g., GitHub Pages).

Easy Deployment: Deploy the backend with a single command using the Vercel CLI.

How It Works
Frontend: Users input KJPL code in a web interface.

Backend: The code is sent to a Vercel Serverless Function for compilation.

Compiler: The serverless function processes the KJPL code and generates C code.

Frontend: The generated C code is displayed to the user.

Setup Instructions
Prerequisites
Node.js and npm installed.

Vercel CLI installed (npm install -g vercel).

A Vercel account (sign up at vercel.com).

Step 1: Clone the Repository
bash
Copy
git clone https://github.com/<your-username>/kjpl-compiler.git
cd kjpl-compiler
Step 2: Set Up the Backend
Install Dependencies:

bash
Copy
npm init -y
npm install express
Create the Serverless Function:

Create an /api directory:

bash
Copy
mkdir api
Add a file for the compiler function, e.g., api/compile.js:

javascript
Copy
// api/compile.js
export default async function handler(req, res) {
    if (req.method === "POST") {
        const { code } = req.body;

        if (!code) {
            return res.status(400).json({ error: "No code provided" });
        }

        try {
            // Simulate compilation (replace with your actual compiler logic)
            const c_code = `#include <stdio.h>\nint main() {\n    printf("${code}");\n    return 0;\n}`;
            return res.status(200).json({ c_code });
        } catch (error) {
            return res.status(500).json({ error: error.message });
        }
    } else {
        return res.status(405).json({ error: "Method not allowed" });
    }
}
Test Locally:

Run the Vercel development server:

bash
Copy
vercel dev
Test the function using curl or Postman:

bash
Copy
curl -X POST http://localhost:3000/api/compile \
     -H "Content-Type: application/json" \
     -d '{"code": "Hello, World!"}'
Response:

json
Copy
{
    "c_code": "#include <stdio.h>\nint main() {\n    printf(\"Hello, World!\");\n    return 0;\n}"
}
Deploy to Vercel:

Deploy your project:

bash
Copy
vercel
Follow the prompts to link your project to Vercel.

Once deployed, your function will be available at:

Copy
https://<your-project>.vercel.app/api/compile
Step 3: Set Up the Frontend
Create a Static Frontend:

Add an index.html file to your project:

html
Copy
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KJPL Compiler</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        textarea, pre { width: 100%; height: 200px; font-family: monospace; }
        button { margin-top: 10px; padding: 10px 20px; font-size: 16px; }
    </style>
</head>
<body>
    <h1>KJPL Compiler</h1>
    <textarea id="inputCode" placeholder="Enter your KJPL code here..."></textarea>
    <button onclick="compileCode()">Compile</button>
    <h2>Generated C Code:</h2>
    <pre id="outputCode"></pre>

    <script>
        async function compileCode() {
            const inputCode = document.getElementById("inputCode").value;
            const outputCode = document.getElementById("outputCode");

            try {
                const response = await fetch("https://<your-project>.vercel.app/api/compile", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ code: inputCode }),
                });

                if (!response.ok) {
                    throw new Error("Compilation failed");
                }

                const result = await response.json();
                outputCode.textContent = result.c_code || result.error;
            } catch (error) {
                outputCode.textContent = `Error: ${error.message}`;
            }
        }
    </script>
</body>
</html>
Run HTML
Deploy to GitHub Pages:

Push your project to GitHub.

Go to your repository's Settings > Pages.

Enable GitHub Pages and select the main branch.

Example Workflow
Frontend: User enters KJPL code in the browser.

Backend: The code is sent to the Vercel Serverless Function.

Compiler: The function processes the code and generates C code.

Frontend: The generated C code is displayed to the user.

Advantages of Using Vercel Serverless Functions
Easy to Deploy: No need to manage servers or infrastructure.

Scalable: Functions automatically scale with traffic.

Cost-Effective: You only pay for what you use.

Fast Development: Focus on writing code, not managing servers.

Limitations
Execution Time: Functions have a maximum execution time (e.g., 10 seconds on the free tier).

Cold Starts: Functions may experience a delay (cold start) if they haven't been used recently.

Stateless: Functions are stateless, so you need to use external storage (e.g., databases) for persistent data.

Contributing
Contributions are welcome! Please open an issue or submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Let me know if you need further assistance!
