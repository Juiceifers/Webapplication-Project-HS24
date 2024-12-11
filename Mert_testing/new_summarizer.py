import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
import re

# Download necessary NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file with multiple extraction methods.
    
    Args:
        pdf_path (str): Path to the PDF file
    
    Returns:
        str: Extracted text from the PDF
    """
    try:
        with open(pdf_path, 'rb') as file:
            # Try multiple extraction methods
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Extract text from all pages
            text = ''
            for page in pdf_reader.pages:
                # Try multiple text extraction methods
                page_text = page.extract_text() or ''
                text += page_text + '\n'
            
            return clean_text(text)
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def clean_text(text):
    """
    Clean and preprocess the extracted text.
    
    Args:
        text (str): Raw extracted text
    
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove headers, footers, and page numbers
    text = re.sub(r'\n[0-9]+\n', ' ', text)
    
    return text

def extractive_summarization(text, num_sentences=12):
    """
    Generate a summary using an extractive approach.
    
    Args:
        text (str): Input text to summarize
        num_sentences (int): Number of sentences to extract
    
    Returns:
        str: Summarized text
    """
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # If text is too short, return full text
    if len(sentences) <= num_sentences:
        return text
    
    # Remove stopwords and calculate word frequency
    stop_words = set(stopwords.words('english'))
    
    def sentence_score(sentence):
        # Score sentences based on word frequency
        words = sentence.lower().split()
        score = sum(1 for word in words if word not in stop_words)
        return score
    
    # Score and sort sentences
    sentence_scores = {sent: sentence_score(sent) for sent in sentences}
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    
    # Preserve original order
    summary_sentences = sorted(summary_sentences, key=sentences.index)
    
    return ' '.join(summary_sentences)

def abstractive_summarization(text, max_length=700):
    """
    Generate a summary using an abstractive approach.
    
    Args:
        text (str): Input text to summarize
        max_length (int): Maximum length of summary
    
    Returns:
        str: Summarized text
    """
    # Split text into words
    words = text.split()
    
    # If text is too short, return full text
    if len(words) <= max_length:
        return text
    
    # Truncate and add ellipsis
    truncated_text = ' '.join(words[:max_length]) + '...'
    
    return truncated_text

def summarize_pdf(pdf_path, method='hybrid'):
    """
    Summarize a PDF file using different methods.
    
    Args:
        pdf_path (str): Path to the PDF file
        method (str): Summarization method ('extractive', 'abstractive', 'hybrid')
    
    Returns:
        str: Summarized text
    """
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        return "Unable to extract text from the PDF. The file might be scanned, encrypted, or empty."
    
    # Choose summarization method
    if method == 'extractive':
        summary = extractive_summarization(text)
    elif method == 'abstractive':
        summary = abstractive_summarization(text)
    else:  # hybrid method
        # Try extractive first, if it's too short, fall back to abstractive
        extractive_summary = extractive_summarization(text)
        if len(extractive_summary.split()) < 50:
            summary = abstractive_summarization(text)
        else:
            summary = extractive_summary
    
    return summary

# Diagnostic function to help troubleshoot PDF processing
def diagnose_pdf(pdf_path):
    """
    Provide diagnostic information about PDF processing.
    
    Args:
        pdf_path (str): Path to the PDF file
    """
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            print(f"Number of pages: {len(pdf_reader.pages)}")
            
            for i, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                print(f"Page {i} text length: {len(text) if text else 0} characters")
                if not text or len(text) < 10:
                    print(f"Warning: Page {i} contains very little or no text")
    
    except Exception as e:
        print(f"Diagnostic error: {e}")

def main():
    pdf_path = "ptopic_mods/callaway.pdf"
    
    # First, run diagnostics
    print("Running PDF Diagnostics:")
    diagnose_pdf(pdf_path)
    
    # Try different summarization methods
    print("\nExtractive Summary:")
    extractive = summarize_pdf(pdf_path, method='extractive')
    with open("extractive.txt", "w") as f:
        f.write(extractive)
    
    print("\nAbstractive Summary:")
    abstractive = summarize_pdf(pdf_path, method='abstractive')
    with open("abstractive.txt", "w") as f:
        f.write(abstractive)
    
    print("\nHybrid Summary:")
    hybrid = summarize_pdf(pdf_path, method='hybrid')
    with open("hybrid.txt", "w") as f:
        f.write(hybrid)
        
def new_summarize_text(text):

    text = "".joine(text) if isinstance(text, list) else text

    extractive_summary = extractive_summarization(text)
    if len(extractive_summary.split()) < 50:
        summary = abstractive_summarization(text)
    else:
        summary = extractive_summary

    return summary
    


if __name__ == "__main__":
    main()