# News Podcast Maker  

An AI-powered news podcast generator inspired by *CNN 5 Things*, featuring automated news retrieval, scriptwriting, and high-quality text-to-speech synthesis. The podcast is enhanced with seamless background music, intro/outro jingles, and customizable AI hosts.  

---

## 🚀 Features  

✅ **Automated News Compilation** – Fetches top headlines from a news API.  
✅ **AI-Generated Scripts** – Uses OpenAI’s Chat Completions API to write structured news scripts.  
✅ **Realistic AI Hosts** – Randomly selects a host with a unique voice and customizable personality.  
✅ **High-Quality Speech Synthesis** – Converts the script into audio using an advanced TTS model.  
✅ **Seamless Background Music & SFX** – Fades in/out and loops smoothly.  
✅ **Time & Date Integration** – Announces the current date and time in the introduction.  
✅ **Customizable Studio Branding** – Set your own podcast studio name.  
✅ **Automatic Directory Management** – Creates necessary folders and cleans up temporary files.  
✅ **AI-Generated Episode Titles** – Generates clear and engaging episode names.  
✅ **Multilingual Support** – Optionally translates the podcast script into any language.  
✅ **User-Friendly CLI** – A sleek command-line interface with easy configuration options.  

---

## 📌 How It Works  

1. **Fetch Latest News** – Retrieves top headlines from an API.  
2. **Generate Script** – Uses AI to create a structured, engaging script.  
3. **Convert Script to Speech** – Splits and processes text for TTS output.  
4. **Merge Audio Components** – Combines spoken clips with background music and sound effects.  

---

## 🔮 Future Enhancements  

### 🔴 High Priority
- ⚠️ **AI Disclaimer** – Add an automated disclaimer about AI-generated content.
- ⚡ **Sequential Processing** – Generate and process audio in chunks for faster output.

### 🟡 Medium Priority
- 🌦 **Weather Reports** – Integrate real-time weather updates.
- 🌐 **Web-Based UI** – Create an interactive frontend for easier control.

### 🟢 Long-term Goals
- 🌍 **Project Website** – Create a dedicated website for project showcase and documentation.
- 🎙 **Multi-Host Conversations** – Simulate dialogue between AI hosts.
- 👤 **Personalized Experience** – Hosts can address users by name and provide tailored updates.
- 🔄 **Duplicate Prevention** – Implement news tracking to avoid repeated stories.
- 🎵 **Advanced Audio Processing** – Implement reliable audio splitting methods.

---

## 🛠 Installation  

### Prerequisites  
Ensure you have the following installed:  
- **Python 3.x**  
- **pip** (Python package manager)  
- An **OpenAI API key**  
- A **NewsAPI key** (e.g., [NewsAPI](https://newsapi.org/))  

### Setup  

1. Clone this repository:  
    ```bash
    git clone <repo-url>

    cd news-podcast-maker
    ```

2.	Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. (Optional but highly recommended) Set up a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```


4.	Set up API keys (in .env or a configuration file):

    ```
    OPENAI_API_KEY=your-openai-api-key
    NEWS_API_KEY=your-news-api-key
    ```


5.	Run the program:

    ```bash
    python main.py
    ```


## 🎵 Credits

Sound effects & music sourced from [Pixabay](https://pixabay.com/).

## 📄 License

See the [LICENSE](LICENSE) file for licensing information.

## 🤝 Contributing

Contributions are welcome! To contribute:

1.	Fork the repository
2.	Create a feature branch (`git checkout -b feature-name`)
3.	Commit your changes (`git commit -m "Added new feature"`)
4.	Push to your branch (`git push origin feature-name`)
5.	Submit a pull request

## 📬 Contact

For questions or suggestions, feel free to reach out via GitHub Issues.

🔥 Enjoy your personalized AI-generated news podcast!
