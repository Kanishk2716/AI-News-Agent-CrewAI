import streamlit as st
import os
from dotenv import load_dotenv
import time
import streamlit.components.v1 as components

# Import the necessary modules from your project
from crewai import Crew, Process
from crewai_tools import SerperDevTool
from agents import news_researcher, news_writer
from tasks import research_task, write_task

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="AI News Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for improved styling with a tech theme
st.markdown("""
<style>
    /* Global Styles */
    body {
        color: #E0E0E0;
        background-color: #1E1E1E;
    }
    .stApp {
        background: linear-gradient(to right, #1E1E1E, #2C3E50);
    }
    
    /* Typography */
    h1, h2, h3 {
        color: #00BFFF;
    }
    .big-font {
        font-size: 24px !important;
        color: #00BFFF;
        font-weight: bold;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #2C3E50;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #00BFFF;
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        transition: all 0.3s ease-in-out;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0080FF;
        transform: scale(1.05);
        box-shadow: 0 0 15px #00BFFF;
    }
    
    /* Text Areas */
    .stTextArea>div>div>textarea {
        background-color: #2C3E50;
        color: #E0E0E0;
        border: 2px solid #00BFFF;
        border-radius: 8px;
        padding: 10px;
        font-size: 16px;
    }
    
    /* Info boxes */
    .stAlert {
        background-color: #2C3E50;
        color: #E0E0E0;
        border: 1px solid #00BFFF;
        border-radius: 8px;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background-color: #00BFFF;
    }
    
    /* Animations */
    @keyframes pulse {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
        100% {
            transform: scale(1);
        }
    }
    .pulse {
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.title("🤖 AI Trend News Generator")
st.markdown('<p class="big-font pulse">Discover the Future of Tech with AI-Powered Insights</p>', unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    st.header("🔧 Configuration")
    
    # Topic input
    if 'topic' not in st.session_state:
        st.session_state.topic = ""

    topic = st.text_input(
        "Enter Technology Topic", 
        value=st.session_state.topic,
        placeholder="e.g., AI in Healthcare, Quantum Computing",
        help="Choose a specific technology or trend you want to explore",
        key="topic_input"
    )
    
    # # Advanced options (collapsible)
    # with st.expander("Advanced Options"):
    #     article_length = st.slider("Article Length", min_value=300, max_value=1500, value=800, step=100)
    #     include_sources = st.checkbox("Include Sources", value=True)
    
    # Generate button
    generate_clicked = st.button("Generate Article", type="primary")

# Main content area
if generate_clicked:
    if not topic.strip():
        st.error("❗ Please enter a valid technology topic to proceed.")
    else:
        # Animated progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(101):
            progress_bar.progress(i)
            if i < 50:
                status_text.text(f"🔍 Researching: {topic}...")
            else:
                status_text.text("✍️ Crafting your article...")
            time.sleep(0.1)
        
        try:
            # Configure the crew
            crew = Crew(
                agents=[news_researcher, news_writer],
                tasks=[research_task, write_task],
                process=Process.sequential
            )

            # Generate the article
            result = crew.kickoff(inputs={'topic': topic})

            # Check if `result` is a CrewOutput object and extract the content
            if hasattr(result, 'output') and isinstance(result.output, dict):
                article_content = result.output.get("final_output", "No content generated.")
            else:
                article_content = str(result)  # Fallback to string conversion

            status_text.success("🎉 Article generation complete!")

            # Display the generated article
            st.markdown("## 📝 Generated Article")
            st.markdown(article_content)

            # Option to save the article
            st.download_button(
                label="📥 Download Article",
                data=article_content,
                file_name=f"{topic.replace(' ', '_')}_article.md",
                mime="text/markdown"
            )
            
            # Feedback section
            st.markdown("### 📊 Article Feedback")
            
            # Use custom React component for star rating
            components.html(
                """
                <div id="star-rating"></div>
                <script src="https://unpkg.com/react@17/umd/react.development.js"></script>
                <script src="https://unpkg.com/react-dom@17/umd/react-dom.development.js"></script>
                <script src="https://unpkg.com/babel-standalone@6/babel.min.js"></script>
                <script type="text/babel">
                    function StarRating({ onRate }) {
                        const [rating, setRating] = React.useState(0);
                        const [hover, setHover] = React.useState(0);

                        return (
                            <div style={{ display: 'flex', alignItems: 'center' }}>
                                {[1, 2, 3, 4, 5].map((star) => (
                                    <button
                                        key={star}
                                        style={{
                                            background: 'none',
                                            border: 'none',
                                            cursor: 'pointer',
                                            fontSize: '24px',
                                            color: (hover || rating) >= star ? '#FFD700' : '#C0C0C0'
                                        }}
                                        onMouseEnter={() => setHover(star)}
                                        onMouseLeave={() => setHover(0)}
                                        onClick={() => {
                                            setRating(star);
                                            onRate(star);
                                        }}
                                    >
                                        ★
                                    </button>
                                ))}
                            </div>
                        );
                    }

                    function App() {
                        const handleRate = (rating) => {
                            Streamlit.setComponentValue(rating);
                        };

                        return <StarRating onRate={handleRate} />;
                    }

                    ReactDOM.render(<App />, document.getElementById('star-rating'));
                </script>
                """,
                height=100,
            )

            # Get the rating from the custom component
            user_rating = st.empty()
            if st.session_state.get('rating'):
                user_rating.success(f"Thank you for your feedback! You rated the article {st.session_state.rating}/5 stars.")

            # Add this custom component to prevent automatic reloads
            components.html(
                """
                <script>
                const doc = window.parent.document;
                doc.querySelector('.stButton button').onclick = function(){
                    setTimeout(function(){
                        window.parent.location.reload();
                    }, 3000);
                }
                </script>
                """,
                height=0,
            )
        
        except Exception as e:
            st.error(f"❗ An error occurred: {str(e)}. Please try again.")
else:
    # Interactive placeholder content
    st.info("👈 Enter a topic in the sidebar and click 'Generate Article'")
    
    # Feature highlights with icons and animations
    st.markdown("""
    <div class="pulse">
        <h3>🚀 How It Works</h3>
        <ol>
            <li>🎯 <strong>Choose a Topic:</strong> Select any cutting-edge technology trend</li>
            <li>🔍 <strong>AI Research:</strong> Our intelligent agents analyze vast amounts of data</li>
            <li>✍️ <strong>Crafted Article:</strong> Receive a tailored, insightful tech report</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample topics carousel
    st.markdown("### 💡 Need inspiration? Try these hot topics:")
    topics = ["Artificial General Intelligence", "5G Revolution", "Blockchain in Supply Chain", "Edge Computing", "Autonomous Vehicles"]
    selected_topic = st.selectbox("Select a trending topic", topics, key="topic_select")
    if selected_topic != st.session_state.topic:
        st.session_state.topic = selected_topic
        st.session_state.topic_changed = True

    # Update the sidebar topic input if a new topic was selected
    if 'topic_changed' in st.session_state and st.session_state.topic_changed:
        topic = st.session_state.topic
        st.session_state.topic_changed = False

# Footer
st.markdown("---")
st.markdown("Powered by CrewAI & Streamlit | © 2024 AI News Generator")

