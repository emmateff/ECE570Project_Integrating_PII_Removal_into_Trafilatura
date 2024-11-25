# ECE570Project_Integrating_PII_Removal_into_Trafilatura
Trafilatura is an open-source generic extraction tool for extracting content from html, developed to build web corpora for training machine learning models. It is crucial to keep specific real PII out of corpora, so the piiranha model for PII detection is used to redact PII from trafilatura's extractions before returning the extracted content. Piiranha was selected as the best performer after evaluating a total of three models (see the three notebooks beginning with 'Testing...').

After selecting Piiranha, its integration into Trafilatura's workflow was achieved via 'Trafilatura_with_PI_protection.ipynb' or 'running_trafi_on_url.py' for examples with a simple user interaction of providing a url for Trafilatura to scrape, process, and return (with PII redacted). Additionally, I provided the file 'pi_detection.py' for inclusion into the real Trafilatura repository (https://github.com/adbar/trafilatura) in the /trafilatura/ directory, which is where other feature related files are location. This file will allow PII removal to be included in Trafilatura. All that needs to be additionally changed is a call to its provided mask_pii() function in the core trafilatura worker.

Steps for running code:
1. Unzip the govdocssubset files and save them to your google drive.
2. Download the Testing_ files and run them to witness the evaluation of the models.
3. The final implementation can be seen in Trafilatura_with_PII_Protection.
