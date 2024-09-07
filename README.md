# 🎵 Samaruy Audio Separator and Stem Library

Welcome to the **Samaruy Audio Separator and Stem Library**! This application allows you to separate audio files into stems and search through an extensive sample library. 🎶

## Features ✨

- **Audio Separation**: Upload audio files and separate them into different stems.
- **Sample Library**: Browse and search through a vast collection of audio stems.
- **Audio Playback**: Play audio stems directly in the browser.
- **Download Stems**: Download separated stems for offline use.

## Installation 🛠️

Follow these steps to set up the project locally:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/bantoinese83/samaruy.git
    cd samaruy
    ```

2. **Backend Setup**:
    - Navigate to the `backend` directory:
        ```bash
        cd samaruy
        ```
    - Create a virtual environment and activate it:
        ```bash
        python -m venv venv
        source venv/bin/activate  # On Windows use `venv\Scripts\activate`
        ```
    - Install the required dependencies:
        ```bash
        pip install -r requirements.txt
        ```
    - Start the backend server:
        ```bash
        uvicorn main:app --reload
        ```

3. **Frontend Setup**:
    - Navigate to the `frontend-samaruy` directory:
        ```bash
        cd ../frontend-samaruy
        ```
    - Install the required dependencies:
        ```bash
        npm install
        ```
    - Start the frontend development server:
        ```bash
        npm start
        ```

## Usage 🚀

1. **Upload Audio**:
    - Navigate to the **Upload** page.
    - Drag and drop an audio file or click to select one.
    - Click the **Upload** button to separate the audio into stems.

2. **Search Stems**:
    - Navigate to the **Search** page.
    - Enter a search query to find specific stems.
    - Browse the search results and play or download stems.

3. **Sample Library**:
    - Navigate to the **Sample Library** page.
    - Browse through the available stems and play or download them.

## Contributing 🤝

We welcome contributions! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature/your-feature-name`).
6. Open a pull request.

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by [bantoinese83](https://github.com/bantoinese83)