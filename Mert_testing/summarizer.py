import pdfplumber
from transformers import BartTokenizer, BartForConditionalGeneration
from tqdm import tqdm
import re

# Path to the PDF file
PATH = r"/Users/merterol/Desktop/WebApps Course Project/webapps_project/Mert_testing/1_DA_Exercises_Combined.pdf"

# Function to clean up the extracted text
def clean_text(text):
    #! chatgpt regex
    # Remove extra spaces, newlines, and any non-ASCII characters that might cause issues
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces/newlines with a single space
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters (if necessary)
    text = text.strip()  # Remove whitespace
    return text

# Function to split text into chunks that do not exceed the model's token limit
def chunk_text(text, max_tokens=1024):
    # Tokenize text to get the number of tokens
    tokens = tokenizer.encode(text)
    
    # Split the tokens into smaller chunks that do not exceed max_tokens
    chunks = [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]
    
    # Convert tokens back to text for each chunk
    return [tokenizer.decode(chunk, skip_special_tokens=True) for chunk in chunks]

# Open and extract text from the PDF, then clean it
with pdfplumber.open(PATH) as pdf:
    all_text = ""
    for page in pdf.pages:
        extracted_text = page.extract_text()
        cleaned_text = clean_text(extracted_text)  # Clean the text
        all_text += cleaned_text

model = BartForConditionalGeneration.from_pretrained("sshleifer/distilbart-cnn-12-6")
tokenizer = BartTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")

# Split the entire document into smaller chunks
chunks = chunk_text(all_text)

summarized_chunks = []

# Generate a summary for each chunk (we can remove the progessbar later)
for chunk in tqdm(chunks, desc="Summarizing", unit="chunk"):
    inputs = tokenizer(chunk, return_tensors="pt", truncation=True, max_length=1024)
    
    # Generate the summary
    summary_ids = model.generate(
        inputs["input_ids"],
        num_beams=4,
        early_stopping=True,
        min_length=100,  # Minimum summary length
        max_length=1500,  # Max summary length
        top_p=0.9,  # Use top-p sampling to improve output
        temperature=0.7  # Lower temperature for more deterministic output
    )
    
    summarized_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    
    #! chatgpt regex
    # Post-process the summarized text to fix concatenated words or strange formatting
    summarized_text = re.sub(r'([a-zA-Z]+)(?=[A-Z])', r'\1 ', summarized_text)  # Insert space between concatenated words
    summarized_text = re.sub(r'\s+', ' ', summarized_text)  # Remove excessive spaces
    
    summarized_chunks.append(summarized_text)

# Combine all the summarized chunks into a final summary (added double \n for readability)
final_summary = '\n\n'.join(summarized_chunks)

with open("Mert_testing/summary.txt", "w") as f:
    f.write(final_summary)


