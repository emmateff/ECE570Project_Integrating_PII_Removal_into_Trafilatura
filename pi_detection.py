'''
To improve trafilatura by implementing PII detection and removal in the text processing phase,
this file should be included in the trafilatura directory within Trafilatura's repository:
https://github.com/adbar/trafilatura

This file provides functions for PII detection and removal using the piiranha model.
https://huggingface.co/iiiorg/piiranha-v1-detect-personal-information

The processed text and a count of the number of instances of PII detected are returned.
'''

import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification
import os

# Load PIIranha model
tokenizer = AutoTokenizer.from_pretrained("iiiorg/piiranha-v1-detect-personal-information")
model = AutoModelForTokenClassification.from_pretrained("iiiorg/piiranha-v1-detect-personal-information")

# Use PIIranha to detect and redact PII
# if the parameter aggregate_redaction is true, PII is replaced with "[redacted]"
# if aggregate_redaction is false, PII is replaced with more detailed tags such as "[I-EMAIL]", "[I-SURNAME]", etc.
def mask_pii(text, aggregate_redaction=True):
    # Tokenize input text
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Get the model predictions
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the predicted labels
    predictions = torch.argmax(outputs.logits, dim=-1)

    # Convert token predictions to word predictions
    encoded_inputs = tokenizer.encode_plus(text, return_offsets_mapping=True, add_special_tokens=True)
    offset_mapping = encoded_inputs['offset_mapping']

    masked_text = list(text)
    is_redacting = False
    redaction_start = 0
    current_pii_type = ''
    count = 0

    for i, (start, end) in enumerate(offset_mapping):
        if start == end:  # Special token
            continue

        label = predictions[0][i].item()
        if label != model.config.label2id['O']:  # Non-O label
            pii_type = model.config.id2label[label]
            if not is_redacting:
                is_redacting = True
                redaction_start = start
                current_pii_type = pii_type
            elif not aggregate_redaction and pii_type != current_pii_type:
                # End current redaction and start a new one
                apply_redaction(masked_text, redaction_start, start, current_pii_type, aggregate_redaction)
                redaction_start = start
                current_pii_type = pii_type
                count += 1
        else:
            if is_redacting:
                apply_redaction(masked_text, redaction_start, end, current_pii_type, aggregate_redaction)
                is_redacting = False
                count += 1

    # Handle case where PII is at the end of the text
    if is_redacting:
        apply_redaction(masked_text, redaction_start, len(masked_text), current_pii_type, aggregate_redaction)
        count += 1

    return ''.join(masked_text), count

# helper function for replacing the detected PII with tags
def apply_redaction(masked_text, start, end, pii_type, aggregate_redaction):
    for j in range(start, end):
        masked_text[j] = ''
    if aggregate_redaction:
        masked_text[start] = '[redacted]'
    else:
        masked_text[start] = f'[{pii_type}]'