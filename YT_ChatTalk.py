import streamlit as st
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, CouldNotRetrieveTranscript
from langchain_experimental.text_splitter import SemanticChunker
from langchain.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
import os
import shutil

# Set up page
st.set_page_config(page_title="🎥 Ask a Question about a YouTube Video", layout="centered")
st.title("AI-Powered YouTube Video Summarizer", )

# Step 1: Ask the user for a question
user_question = st.text_input("❓ What do you want to know from a YouTube video?", placeholder="e.g., What is this video about?")

# Step 2: Ask for YouTube video ID
video_id = st.text_input("🎬 Enter YouTube Video ID:", placeholder="e.g., s3p2EoAzhtE")

if user_question and video_id:
    with st.spinner("🔄 Processing..."):

        # Load LLM and embeddings
        try:
            llm = OllamaLLM(model="llama3.1:8b")
            embeddings = OllamaEmbeddings(model="llama3.1:8b")
        except Exception as e:
            st.error(f"❌ Failed to load Ollama model: {e}")
            st.stop()

        # Function to get transcript with fallback and error handling
        def get_transcript(vid):
            try:
                # List all available transcripts
                transcript_list = YouTubeTranscriptApi.list_transcripts(vid)
                # Try to get English transcript first
                try:
                    transcript = transcript_list.find_transcript(['en'])
                except NoTranscriptFound:
                    # Fallback: get first available transcript
                    transcript = next(iter(transcript_list))
                # Fetch the actual transcript
                transcript_chunks = transcript.fetch()
                return " ".join(chunk["text"] for chunk in transcript_chunks)
            except TranscriptsDisabled:
                st.error("❌ Transcript is disabled for this video.")
                return None
            except (NoTranscriptFound, CouldNotRetrieveTranscript):
                st.error("❌ No transcript found for this video.")
                return None
            except Exception as e:
                st.error(f"❌ Error fetching transcript: {e}")
                return None

        # Get transcript
        transcript = get_transcript(video_id)

        if transcript is None:
            st.warning("⚠️ Transcript not found or unavailable for this video. Please check video ID or try another video.")
        else:
            # Remove old DB
            persist_directory = "chroma_db"
            if os.path.exists(persist_directory):
                shutil.rmtree(persist_directory)

            # Split into semantic chunks
            splitter = SemanticChunker(embeddings=embeddings)
            docs = splitter.create_documents([transcript])

            # Create vector store
            vector_store = Chroma.from_documents(
                documents=docs,
                embedding=embeddings,
                persist_directory=persist_directory
            )

            retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

            # Prompt template
            prompt = PromptTemplate(
                template="""
You are a helpful assistant.
Answer ONLY from the provided transcript context.
If the context is insufficient, just say you don't know.

{context}
Question: {question}
""",
                input_variables=["context", "question"]
            )

            # Format documents
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)

            # Set up chain
            parallel_chain = RunnableParallel({
                "context": retriever | RunnableLambda(format_docs),
                "question": RunnablePassthrough()
            })

            parser = StrOutputParser()
            main_chain = parallel_chain | prompt | llm | parser

            # Run chain with user question
            try:
                answer = main_chain.invoke(user_question)
                st.subheader("📌 Answer")
                st.write(answer)
            except Exception as e:
                st.error(f"❌ Error during answering: {e}")
