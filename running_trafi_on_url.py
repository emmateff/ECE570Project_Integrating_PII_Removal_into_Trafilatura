from trafilatura.pi_detection import mask_pii
from trafilatura.core import extract
from trafilatura import fetch_url

if __name__ == "__main__":
    # Prompt the user for a URL
    print("\nTrafilatura w/ PII Protection!\n")
    url = input("Please enter a URL to extract content from: ")
    # Fetch the page content from the URL
    downloaded_html = fetch_url(url)

    if downloaded_html:
        # Extract main content from the downloaded HTML
        extracted_content = extract(downloaded_html, favor_recall=True)
        
        if extracted_content:
            filtered_content, pii_instance_count = mask_pii(extracted_content, aggregate_redaction=False)
            print(f"\nThere were a total of {pii_instance_count} redactions of PII made:\n")
            print(filtered_content)
        else:
            print("Content extraction failed.")
    else:
        print("Failed to fetch content from the URL.")