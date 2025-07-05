# 🎥 YouTube Summarizer Agent with Chrome Extension

An AI-powered YouTube video summarizer that extracts transcripts from YouTube videos and provides intelligent answers to user questions using LangChain and Ollama.

## 🌟 Features

- **AI-Powered Q&A**: Ask questions about any YouTube video content
- **Transcript Extraction**: Automatically fetches video transcripts using YouTube Transcript API
- **Semantic Chunking**: Intelligently splits content for better context understanding
- **Vector Database**: Uses ChromaDB for efficient content retrieval
- **Chrome Extension**: Browser extension for easy video ID extraction
- **Streamlit Interface**: Beautiful web interface for interaction
- **Multi-language Support**: Handles videos in different languages with fallback

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- Chrome browser (for extension)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/abhay-2108/YouTube-Summarizer-Agent-with-Chrome-Extension.git
   cd YouTube-Summarizer-Agent-with-Chrome-Extension
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv yt
   # On Windows
   yt\Scripts\activate
   # On macOS/Linux
   source yt/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Ollama and download model**
   ```bash
   # Install Ollama (follow instructions at https://ollama.ai/)
   # Download the required model
   ollama pull llama3.1:8b
   ```

5. **Install Chrome Extension**
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" and select the `chrome_extension/` folder

## 📖 Usage

### Web Interface

1. **Start the Streamlit app**
   ```bash
   streamlit run YT_ChatTalk.py
   ```

2. **Get YouTube Video ID**
   - Use the Chrome extension to extract video ID from any YouTube video
   - Or manually copy the ID from the URL (e.g., `s3p2EoAzhtE` from `https://www.youtube.com/watch?v=s3p2EoAzhtE`)

3. **Ask Questions**
   - Enter your question about the video content
   - Enter the YouTube video ID
   - Click submit and get AI-powered answers!

### Chrome Extension

1. **Navigate to any YouTube video**
2. **Click the extension icon** in your browser toolbar
3. **Copy the video ID** that appears in the popup
4. **Use the ID** in the Streamlit interface

## 🛠️ Project Structure

```
YouTube-Summarizer-Agent-with-Chrome-Extension/
├── YT_ChatTalk.py              # Main Streamlit application
├── yt_qa_core.py              # Core Q&A functionality
├── requirements.txt            # Python dependencies
├── chrome_extension/          # Chrome extension files
│   ├── manifest.json
│   ├── popup.html
│   └── popup.js
├── chroma_db/                 # Vector database (auto-generated)
└── README.md                  # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Optional: Custom Ollama model
OLLAMA_MODEL=llama3.1:8b

# Optional: Custom embeddings model
OLLAMA_EMBEDDINGS_MODEL=llama3.1:8b
```

### Model Configuration

The application uses Ollama for both LLM and embeddings. You can modify the model in `YT_ChatTalk.py`:

## 🎯 How It Works

1. **Transcript Extraction**: Uses YouTube Transcript API to fetch video transcripts
2. **Semantic Chunking**: Splits transcript into meaningful chunks using embeddings
3. **Vector Storage**: Stores chunks in ChromaDB for efficient retrieval
4. **Question Processing**: Retrieves relevant chunks based on user question
5. **AI Generation**: Uses Ollama LLM to generate contextual answers

## 🐛 Troubleshooting

### Common Issues

1. **"Error fetching transcript"**
   - Check if the video has available transcripts
   - Verify the video ID is correct
   - Try a different video

2. **"Failed to load Ollama model"**
   - Ensure Ollama is running: `ollama serve`
   - Verify the model is downloaded: `ollama list`
   - Download the model: `ollama pull llama3.1:8b`

3. **"No transcript found"**
   - Some videos have disabled transcripts
   - Try videos with auto-generated captions
   - Check if the video is publicly accessible


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ by [Abhay](https://github.com/abhay-2108)**

*Star this repository if you find it helpful! ⭐* 