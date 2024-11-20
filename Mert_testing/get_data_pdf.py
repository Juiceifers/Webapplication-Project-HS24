import fitz  # pip install PyMuPDF
from transformers import pipeline
from huggingface_hub import login
from tqdm import tqdm

with open("/Users/merterol/Desktop/huggingface_token.txt", "r") as f:
    token = f.readline().strip()

login(token=token)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ''
    for page in doc:
        text += page.get_text()
    return text

# Function to split the text into manageable chunks
def chunk_text(text, max_tokens=1024):
    words = text.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(' '.join(current_chunk)) > max_tokens:
            chunks.append(' '.join(current_chunk[:-1]))
            current_chunk = [word]
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

# Function to summarize text using Hugging Face
def summarize_text_with_huggingface(text, model_name="facebook/bart-large-cnn"):
    summarizer = pipeline("summarization", model=model_name, device=-1)
    
    input_length = len(text.split())  # Calculate the number of tokens/words in the input
    max_length = min(input_length, 150)  # Set max_length to the smaller of input length or 150
    
    summary = summarizer(text, max_length=max_length, min_length=50, do_sample=False)
    return summary[0]['summary_text']


# Main function to process the PDF, chunk the text, and summarize it
def process_pdf(pdf_path):
    # Step 1: Extract text from the PDF
    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    
#    # Step 2: Split the text into chunks
#    print("Splitting text into chunks...")
#    chunks = chunk_text(text)
#    
#    # Step 3: Summarize each chunk with progress bar
#    print("Summarizing chunks...")
#    summaries = []
#    
#    # Use tqdm to show progress for chunk processing
#    for chunk in tqdm(chunks, desc="Processing Chunks", unit="chunk"):
#        summary = summarize_text_with_huggingface(chunk)
#        summaries.append(summary)
#    
#    # Step 4: Combine the summaries from each chunk into one final summary
#    final_summary = ' '.join(summaries)
    
    return final_summary

if __name__ == "__main__":
    pdf_path = "/Users/merterol/Desktop/da3.pdf"
    summary = process_pdf(pdf_path)

    with open("Mert_testing/summary.txt", "w") as f:
        f.write(summary)
