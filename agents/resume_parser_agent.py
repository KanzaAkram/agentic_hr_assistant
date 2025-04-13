# resume_parser_agent.py
import PyPDF2
import re

class ResumeParserAgent:
    def __init__(self):
        pass
    
    def extract_text_from_pdf(self, pdf_file):
        """Extract text content from a PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def extract_email(self, text):
        """Extract email address from text using regex"""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None
    
    def extract_phone(self, text):
        """Extract phone number from text using regex"""
        # This pattern catches most US/international phone formats
        phone_pattern = r'(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        return phones[0] if phones else None
    
    def extract_name(self, text, fallback_filename=""):
        """Attempt to extract candidate name from the beginning of the resume"""
        # Usually names appear at the top, often on their own line
        lines = text.split('\n')
        # Check first few non-empty lines for potential names (simple heuristic)
        for line in lines[:5]:
            line = line.strip()
            if line and len(line.split()) <= 4 and not any(char.isdigit() for char in line):
                return line
                
        # If we can't find a name, use the filename without extension as fallback
        if fallback_filename:
            return fallback_filename.split('.')[0].replace('_', ' ').title()
        
        return "Unknown Candidate"