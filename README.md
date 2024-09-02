# Auric - Personalized AI-Powered Meditation App ✨

## 📖 Project Description

**Auric** is an AI-powered meditation app that delivers personalized experiences by generating custom meditation sessions based on user input. Created as part of Stanford's **TECH-16: Large Language Models for Business with Python** course, Auric combines AI-generated text, voice, and music to provide a unique and immersive meditation experience, helping users achieve mindfulness and relaxation in a fast-paced world.

## 🌟 Features

- **🧘 Personalized Meditation:** Auric generates custom meditations based on user input, utilizing the OpenAI API to create content that resonates with each individual.
- **🎙️ Text-to-Speech:** The app employs an AI-generated voice (powered by xtts) to read the personalized meditation, making the experience more immersive.
- **🎶 AI-Generated Music:** Auric enhances the meditation experience with relaxing background music created through AI technology from Suno.com, adding another layer of tranquility to the sessions.

## 🛠️ How to Use

1. **📥 Installation:** 
   - Clone this repository to your local machine.
   - Install the necessary software (refer to the scripts in the `setup` directory for macOS installation).
   - Set up a virtual environment and install the required Python packages (refer to the `prepare_once.sh` script in the `backend` directory).

2. **🚀 Running the App:**
   - Open `meditation.py` and insert your OpenAI API key in the `open_ai_key` section. For details on obtaining an API key, visit the [OpenAI API documentation](https://platform.openai.com/docs/api-reference/authentication).
   - Download the music and voice files from [Google Drive](https://drive.google.com/file/d/1GeryFwSEc8zgoyk0s3xvgufG_XgfM9ja/view?usp=share_link) and place them in the `backend/music` and `backend/voice` directories, respectively.
   - Run `start_backend.sh` from the `backend` directory.
   - Run `start_frontend.sh` from the `frontend` directory.
   - Open [http://localhost:8000/](http://localhost:8000/) in your web browser.

3. **🧘 Using the App:**
   - Input your preferences and choose your desired meditation settings, or select "Generate Random Meditation".
   - Generate a personalized meditation, delivered with AI-generated text, voice, and music.

## 💻 Technologies

- **🔮 OpenAI API:** Used for generating the meditation text based on user input.
- **🎤 xtts:** An AI-driven voice generation model that converts the meditation text into speech.
- **🎧 Suno.com:** Provides AI-generated music for a relaxing meditation background.
  - *Note:* At the time this project was built, Suno.com didn’t offer an API. Therefore, the AI-generated music was created separately and manually uploaded to the project.
- **🌐 Flask:** Backend framework.
- **💻 Vanilla JavaScript:** Handles the frontend.

## 👥 Collaborators

This project was developed by:

- **[Yulia Reva](https://github.com/juliareva)**
- **[Valeriy Leletko](https://github.com/lvaleriy)**

## 📜 License

This project is open for use under the terms of the MIT License. You are free to use, modify, and distribute the code, but it comes without any warranty. By using this project, you agree to these terms.
