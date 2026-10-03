from fpdf import FPDF
import os

# Find where your panels are
possible_folders = ["app/static/panels", "static/panels", "app/static/panels", "panels"]
panels_folder = None
for f in possible_folders:
    if os.path.exists(f) and len([x for x in os.listdir(f) if x.endswith('.png')]) >= 5:
        panels_folder = f
        break

if not panels_folder:
    panels_folder = "app/static/panels"

print(f"Using folder: {panels_folder}")

# Make sure exports exists
os.makedirs("app/static/exports", exist_ok=True)
os.makedirs("static/exports", exist_ok=True)

pdf = FPDF(format='A4')
pdf.set_auto_page_break(auto=False)

story = [
    "Panel 1: Alex arrives at the construction site at sunrise, ready for a new day.",
    "Panel 2: Building the foundation with the team - hard work begins.",
    "Panel 3: Working high on scaffolding during dramatic sunset.",
    "Panel 4: Tired but proud, Alex looks at the progress.",
    "Panel 5: The finished building - dream becomes reality!"
]

for i in range(1, 6):
    img_path = f"{panels_folder}/panel_{i}.png"
    # try other naming too
    if not os.path.exists(img_path):
        # check for any png with that number
        files = [f for f in os.listdir(panels_folder) if str(i) in f and f.endswith('.png')]
        if files:
            img_path = f"{panels_folder}/{files[0]}"

    if not os.path.exists(img_path):
        print(f"Missing {img_path} - skipping")
        continue

    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"ComicCraft - Panel {i}", ln=True, align='C')

    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, story[i-1], align='C')
    pdf.ln(5)

    # Center image
    pdf.image(img_path, x=10, y=35, w=190)

output_path = "app/static/exports/ComicCraft_Final.pdf"
pdf.output(output_path)
print(f"\nSUCCESS! PDF saved: {output_path}")
print(f"Open it with: explorer {output_path}")