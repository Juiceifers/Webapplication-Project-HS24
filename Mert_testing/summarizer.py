import pdfplumber
from transformers import BartTokenizer, BartForConditionalGeneration
import re

# Path to the PDF file
PATH = r"/Users/merterol/Desktop/WebApps_Project/webapps_project/Mert_testing/Summarizer/callaway.pdf"

# Function to clean up the extracted text
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces/newlines with a single space
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters (if necessary)
    text = text.strip()  # Remove whitespace
    return text

# Function to split text into chunks that do not exceed the model's token limit
def chunk_text(text, tokenizer, max_tokens=1024):
    tokens = tokenizer.encode(text)
    chunks = [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [tokenizer.decode(chunk, skip_special_tokens=True) for chunk in chunks]

# Main function to summarize the PDF
def summarize_pdf(PATH):
    # Open, extract and clean text from the PDF
    with pdfplumber.open(PATH) as pdf:
        all_text = ""
        for page in pdf.pages:
            extracted_text = page.extract_text()
            cleaned_text = clean_text(extracted_text)  # Clean the text
            all_text += cleaned_text

    # Load the model and tokenizer
    model = BartForConditionalGeneration.from_pretrained("sshleifer/distilbart-cnn-12-6")
    tokenizer = BartTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")

    # Split the entire document into smaller chunks
    chunks = chunk_text(all_text, tokenizer)

    summarized_chunks = []

    # Generate a summary for each chunk
    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, max_length=1024)

        # Generate the summary
        summary_ids = model.generate(
            inputs["input_ids"],
            num_beams=6, # quality --> higher (the higher the slower)
            early_stopping=True,
            min_length=100,
            max_length=850,
            top_p=0.9,  # quality --> higher
            temperature=0.5  # quality --> lower
        )

        summarized_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

        summarized_text = re.sub(r'([a-zA-Z]+)(?=[A-Z])', r'\1 ', summarized_text)  # Insert space between concatenated words
        summarized_text = re.sub(r'\s+', ' ', summarized_text)  # Remove excessive spaces

        summarized_chunks.append(summarized_text)

    final_summary = '\n\n'.join(summarized_chunks)

    with open("data/summary_summarizer.txt", "w") as f:
        f.write(final_summary)

def main():
    #summarize_pdf(PATH)
    summarize_pdf("topic_mods/callaway.pdf")

if __name__ == "__main__":
    main()