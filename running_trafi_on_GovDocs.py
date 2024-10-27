from trafilatura.pi_detection import mask_pii
from trafilatura.core import *
import os

# Path to the GovDocs1 dataset root directory, which is downloaded on local machine
govdocs_dir = "./govdocs_testingdata"

# Function to identify and read HTML files from the dataset
def find_html_files(directory):
    html_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file has an HTML extension
            if file.endswith(".html") or file.endswith(".htm"):
                html_files.append(os.path.join(root, file))
    return html_files

# Find HTML files in the dataset
html_files = find_html_files(govdocs_dir)

# Function to read the content of an HTML file
def read_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

# Process the HTML content with Trafilatura's extract() function
def process_html(html_content, chunk_size=512):
    text = extract(html_content, favor_recall=True)
    if text:
        redacted_text = ""
        instances = 0
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]
            redacted_chunk, chunk_instances = mask_pii(chunk, aggregate_redaction=False)
            redacted_text += redacted_chunk
            instances += chunk_instances
        return redacted_text, instances
    else:
        return None

# for each of the HTML files, use Trafilatura to extract content, then remove PII from that content, and write outputs to files
if html_files:
    i = 0
    total_instances = 0
    chunk_size = 512
    for file in html_files:
        html_content = read_html_file(file)
        redacted_content, instances = process_html(html_content)
        total_instances += instances
        if redacted_content:
            try:
                with open(f'./PIIranha_filtered_content/test{i}.txt', 'w', encoding='utf-8') as fp:
                    fp.write(redacted_content)
                i += 1
            except Exception as e:
                print(f"Error writing to file: {e}")
        else:
            print(f'Failed to extract text from {file}.')
    print("Total instances of PI detected in GovDocs subset: " + str(total_instances))



# RECORDS:
# total instances detected with spacy: 24,536
# total instances detected with distilBERT: 622
# total instances detecting with piiranha: 6,574