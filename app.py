import streamlit as st
import os
from markitdown import MarkItDown
from pathlib import Path
from openai import OpenAI
import mimetypes
from datetime import datetime
import time

def setup_directories():
    """Create necessary directories if they don't exist"""
    directories = ['documents', 'converted']
    for dir_name in directories:
        os.makedirs(dir_name, exist_ok=True)
    return Path('documents'), Path('converted')

def get_file_icon(filename):
    """Return appropriate emoji icon based on file type"""
    if is_image_file(filename):
        return "🖼️"
    elif filename.endswith('.pdf'):
        return "📄"
    elif filename.endswith(('.doc', '.docx')):
        return "📝"
    elif filename.endswith(('.xls', '.xlsx')):
        return "📊"
    elif filename.endswith('.txt'):
        return "📋"
    else:
        return "📎"

def is_image_file(filename):
    """Check if the file is an image based on its mimetype"""
    mimetype, _ = mimetypes.guess_type(filename)
    return mimetype and mimetype.startswith('image/')

def save_uploaded_file(uploaded_file, save_dir):
    """Save uploaded file to the documents directory"""
    try:
        file_path = save_dir / uploaded_file.name
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None

def convert_to_markdown(file_path, output_dir, openai_client=None):
    """Convert file to markdown using MarkItDown"""
    try:
        if is_image_file(str(file_path)) and openai_client:
            md = MarkItDown(
                llm_client=openai_client,
                llm_model="gpt-4o"
            )
        else:
            md = MarkItDown()
        
        result = md.convert(str(file_path))
        output_path = output_dir / f"{file_path.stem}.md"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result.text_content)
        
        return output_path, result.text_content
    except Exception as e:
        st.error(f"Error converting file: {e}")
        return None, None

def initialize_session_state():
    """Initialize session state variables"""
    defaults = {
        'uploaded_files': [],
        'converted_files': [],
        'combined_markdown': "",
        'conversion_status': {},
        'show_welcome': True,
        'dark_mode': False,
        'conversion_started': False,
        'needs_reset': False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def create_sidebar():
    """Create and handle sidebar elements"""
    with st.sidebar:
        st.title("🛠️ Configuration")
        
        # Theme toggle
        st.session_state.dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
        if st.session_state.dark_mode:
            st.markdown("""
                <style>
                    .stApp {
                        background-color: #1E1E1E;
                        color: #FFFFFF;
                    }
                </style>
                """, unsafe_allow_html=True)
        
        # API Key input
        st.divider()
        openai_api_key = st.text_input(
            "🔑 OpenAI API Key",
            type="password",
            help="Required for image descriptions",
            placeholder="sk-..."
        )
        
        # File uploader
        st.divider()
        st.subheader("📁 Upload Files")
        uploaded_files = st.file_uploader(
            "Choose files to convert",
            accept_multiple_files=True,
            type=None
        )
        
        if uploaded_files:
            st.session_state.uploaded_files = uploaded_files
            st.success(f"✅ {len(uploaded_files)} files uploaded")
            
            for file in uploaded_files:
                icon = get_file_icon(file.name)
                st.info(f"{icon} {file.name}")
        
        # Convert button
        st.divider()
        if st.button("🚀 Convert Files", type="primary", disabled=not uploaded_files):
            st.session_state.conversion_started = True
            st.session_state.converted_files = []  # Reset converted files
            st.session_state.combined_markdown = ""  # Reset combined markdown
        
        # Help section
        with st.expander("ℹ️ Help"):
            st.markdown("""
            **Supported file types:**
            - 📄 PDF documents
            - 📝 Word documents
            - 📊 Excel spreadsheets
            - 🖼️ Images (requires API key)
            - 📋 Text files
            - 🌐 HTML files
            - 📎 ZIP files
            """)
    
    return openai_api_key

def show_welcome_screen():
    """Display welcome screen"""
    st.title("🎯 Document to Markdown Converter")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 👋 Welcome!
        
        This tool helps you convert various document formats to Markdown.
        Get started by:
        1. Adding your OpenAI API key (for image processing)
        2. Uploading your documents
        3. Clicking the Convert button
        """)
    
    with col2:
        st.markdown("""
        ### ✨ Features
        
        - 🔄 Convert multiple files at once
        - 🖼️ AI-powered image descriptions
        - 📥 Download individual or combined files
        - 🎨 Dark mode support
        - 📊 Progress tracking
        """)

def main():
    # Initialize session state and setup
    initialize_session_state()
    st.set_page_config(layout="wide", page_title="MarkItDown Converter")
    docs_dir, converted_dir = setup_directories()
    
    # Create sidebar and get API key
    openai_api_key = create_sidebar()
    
    # Show welcome screen if no conversion started
    if not st.session_state.conversion_started:
        show_welcome_screen()
        return
    
    # Main content area
    st.title("🔄 Converting Documents")
    
    # Process files only when conversion is started and not yet processed
    if st.session_state.conversion_started and not st.session_state.converted_files:
        openai_client = OpenAI(api_key=openai_api_key) if openai_api_key else None
        combined_content = []
        
        # Progress bar
        progress_bar = st.progress(0)
        status_container = st.empty()
        
        for idx, uploaded_file in enumerate(st.session_state.uploaded_files):
            progress = (idx + 1) / len(st.session_state.uploaded_files)
            progress_bar.progress(progress)
            
            # Update status
            status_container.info(f"Processing: {uploaded_file.name}")
            
            # Check for image files
            if is_image_file(uploaded_file.name) and not openai_api_key:
                st.warning(f"⚠️ Skipping {uploaded_file.name} - OpenAI API Key required")
                continue
            
            # Process file
            file_path = save_uploaded_file(uploaded_file, docs_dir)
            if not file_path:
                continue
            
            output_path, content = convert_to_markdown(file_path, converted_dir, openai_client)
            if not output_path:
                continue
            
            # Add to combined content
            combined_content.append(f"\n## {uploaded_file.name}\n")
            combined_content.append(content)
            
            # Store converted file
            st.session_state.converted_files.append({
                'name': uploaded_file.name,
                'path': output_path,
                'content': content,
                'is_image': is_image_file(uploaded_file.name)
            })
        
        # Clear progress indicators
        progress_bar.empty()
        status_container.empty()
        
        # Save combined markdown
        st.session_state.combined_markdown = "\n".join(combined_content)
        
        # Show results
        st.success("✅ Conversion Complete!")
        
        # Download buttons
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "📥 Download All as Single File",
                st.session_state.combined_markdown,
                file_name=f"combined_markdown_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                key="download_all"
            )
        
        # Display converted files
        st.subheader("📑 Converted Files")
        for file_info in st.session_state.converted_files:
            with st.expander(f"{get_file_icon(file_info['name'])} {file_info['name']}"):
                if file_info['is_image']:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.image(docs_dir / file_info['name'])
                    with col2:
                        st.markdown(file_info['content'])
                else:
                    st.markdown(file_info['content'])
                
                st.download_button(
                    f"📥 Download {file_info['name']}.md",
                    file_info['content'],
                    file_name=f"{file_info['name']}.md",
                    mime="text/markdown",
                    key=f"download_{file_info['name']}"
                )

if __name__ == "__main__":
    main()