import os

# Define the structure
folders = [
    "portfolio_templates/neo",
    "portfolio_templates/glass",
    "generated_sites"
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"✓ Created folder: {folder}")

# Create the Neo-Brutalism files
with open("portfolio_templates/neo/index.html", "w") as f:
    f.write("<!DOCTYPE html><html><head><link rel='stylesheet' href='style.css'></head><body><div class='container'><header><h1>{{NAME}}</h1><p>{{BIO}}</p></header><div class='skills'></div></div></body></html>")

with open("portfolio_templates/neo/style.css", "w") as f:
    f.write("body { background: #FFF017; font-family: sans-serif; padding: 50px; } .container { background: white; border: 5px solid black; padding: 20px; box-shadow: 10px 10px 0px black; } .pill { display: inline-block; background: {{COLOR}}; border: 2px solid black; padding: 5px 10px; margin: 5px; }")

# Create the Glassmorphism files
with open("portfolio_templates/glass/index.html", "w") as f:
    f.write("<!DOCTYPE html><html><head><link rel='stylesheet' href='style.css'></head><body><div class='glass'><h1>{{NAME}}</h1><p>{{BIO}}</p><div class='skills'></div></div></body></html>")

with open("portfolio_templates/glass/style.css", "w") as f:
    f.write("body { background: linear-gradient(45deg, #0f172a, #1e293b); min-height: 100vh; color: white; display: flex; align-items: center; justify-content: center; font-family: sans-serif; } .glass { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); padding: 40px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.2); } .skill-chip { display: inline-block; background: {{COLOR}}44; border: 1px solid {{COLOR}}; padding: 5px 15px; border-radius: 50px; margin: 5px; }")

print("\n🚀 Project initialized! You can now run 'python main.py'")