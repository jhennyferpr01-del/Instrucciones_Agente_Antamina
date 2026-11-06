import docx
import re
import sys

def fill_template(template_path, data_dict, output_path):
    # Load the original document
    doc = docx.Document(template_path)

    # 1. Replace text in Paragraphs (Preserving runs and formatting)
    for p in doc.paragraphs:
        if "[Por definir]" in p.text:
            # We need to handle runs carefully to preserve formatting (bold, italic, etc.)
            # Iterating through runs to find the exact placeholder
            for run in p.runs:
                if "[Por definir]" in run.text:
                    # Replace with data from dict. If key not found, leave as is or fill generic.
                    for key, value in data_dict.items():
                        if key in run.text:
                            run.text = run.text.replace(key, value)

    # 2. Replace text in Tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        if "[Por definir]" in run.text:
                            for key, value in data_dict.items():
                                if key in run.text:
                                    run.text = run.text.replace(key, value)

    # 3. Replace text in Headers and Footers
    for section in doc.sections:
        # Header
        for header in section.header.paragraphs:
            for run in header.runs:
                if "[Por definir]" in run.text:
                    for key, value in data_dict.items():
                        if key in run.text:
                            run.text = run.text.replace(key, value)
        # Footer
        for footer in section.footer.paragraphs:
            for run in footer.runs:
                if "[Por definir]" in run.text:
                    for key, value in data_dict.items():
                        if key in run.text:
                            run.text = run.text.replace(key, value)

    # Save the document
    doc.save(output_path)
    print(f"Document saved successfully to {output_path}")

# --- USAGE EXAMPLE (For the Agent to fill) ---
# The agent will map the data from the TXT to these keys based on the specific project.
# Note: Since there are multiple [Por definir], the agent should use a unique ID mapping 
# or sequential replacement if you are doing a single project at a time.

# Example Data (The agent will populate this dynamically):
data_mapping = {
    "[Por definir]": "Information extracted from the TXT", 
    # In a real scenario, you might use regex or unique IDs if there are many.
    # Since your template has many [Por definir], the agent should replace them sequentially 
    # or generate specific content for each placeholder.
}

if __name__ == "__main__":
    # The agent should call this with actual paths
    fill_template("template.docx", data_mapping, "output_final.docx")
