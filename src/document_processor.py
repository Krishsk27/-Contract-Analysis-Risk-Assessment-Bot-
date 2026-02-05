import io
import PyPDF2
from docx import Document

class DocumentProcessor:
    @staticmethod
    def extract_text(uploaded_file):
        """
        Extracts text from PDF, DOCX, or TXT files.
        Returns: (text_content, error_message)
        """
        text = ""
        try:
            # Handle PDF
            if uploaded_file.name.lower().endswith('.pdf'):
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                num_pages = len(pdf_reader.pages)
                
                # Safety check for massive files (token limits)
                if num_pages > 50:
                    return None, f"File too large ({num_pages} pages). Please upload a contract under 50 pages."
                
                for page in pdf_reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
            
            # Handle DOCX
            elif uploaded_file.name.lower().endswith('.docx'):
                doc = Document(uploaded_file)
                for para in doc.paragraphs:
                    text += para.text + "\n"
            
            # Handle TXT
            elif uploaded_file.name.lower().endswith('.txt'):
                text = uploaded_file.read().decode("utf-8")
            
            else:
                return None, "Unsupported file format. Please upload PDF, DOCX, or TXT."

            # Post-processing: Remove empty lines/noise
            clean_text = "\n".join([line for line in text.split('\n') if line.strip()])
            
            if len(clean_text) < 50:
                return None, "Could not extract sufficient text. The file might be a scanned image (OCR required)."

            return clean_text, None

        except Exception as e:
            return None, f"Error processing file: {str(e)}"