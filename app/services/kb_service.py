import os
from werkzeug.utils import secure_filename
from docx import Document
import io


# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'docx'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 MB in bytes


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_extension(filename):
    """Get file extension."""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''


def extract_text_from_txt(file_stream):
    """
    Extract text from a .txt file.
    
    Args:
        file_stream: File stream object
        
    Returns:
        str: Extracted text
    """
    try:
        # Read with UTF-8 encoding
        content = file_stream.read()
        
        # Try UTF-8 first
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            # Fallback to latin-1 if UTF-8 fails
            text = content.decode('latin-1')
        
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error reading text file: {str(e)}")


def extract_text_from_docx(file_stream):
    """
    Extract text from a .docx file.
    
    Args:
        file_stream: File stream object
        
    Returns:
        str: Extracted text
    """
    try:
        # Read the DOCX file
        document = Document(file_stream)
        
        # Extract all paragraphs
        paragraphs = [paragraph.text for paragraph in document.paragraphs]
        
        # Join paragraphs with newlines
        text = '\n'.join(paragraphs)
        
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error reading DOCX file: {str(e)}")


def process_uploaded_file(file):
    """
    Process uploaded file and extract text.
    
    Args:
        file: FileStorage object from Flask request
        
    Returns:
        dict: {
            'filename': str,
            'file_type': str,
            'file_size': int,
            'content': str
        }
        
    Raises:
        ValueError: If file is invalid or processing fails
    """
    # Validate filename
    if not file or not file.filename:
        raise ValueError("No file provided")
    
    filename = secure_filename(file.filename)
    
    # Validate file extension
    if not allowed_file(filename):
        raise ValueError(f"File type not allowed. Only .txt and .docx files are supported.")
    
    # Get file extension
    file_type = get_file_extension(filename)
    
    # Read file into memory to check size
    file_stream = io.BytesIO(file.read())
    file_size = len(file_stream.getvalue())
    
    # Validate file size
    if file_size > MAX_FILE_SIZE:
        raise ValueError(f"File too large. Maximum size is {MAX_FILE_SIZE / (1024*1024):.0f} MB")
    
    if file_size == 0:
        raise ValueError("File is empty")
    
    # Reset stream position for processing
    file_stream.seek(0)
    
    # Extract text based on file type
    if file_type == 'txt':
        content = extract_text_from_txt(file_stream)
    elif file_type == 'docx':
        content = extract_text_from_docx(file_stream)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    # Validate extracted content
    if not content or len(content.strip()) == 0:
        raise ValueError("No text content found in file")
    
    return {
        'filename': filename,
        'file_type': file_type,
        'file_size': file_size,
        'content': content
    }


def combine_knowledge_bases(knowledge_bases):
    """
    Combine multiple knowledge base documents into one text.
    
    Args:
        knowledge_bases: List of KnowledgeBase model instances
        
    Returns:
        str: Combined text from all knowledge bases
    """
    if not knowledge_bases:
        return ""
    
    combined_text = []
    
    for kb in knowledge_bases:
        combined_text.append(f"--- {kb.filename} ---")
        combined_text.append(kb.content)
        combined_text.append("")  # Empty line between documents
    
    return "\n".join(combined_text)
