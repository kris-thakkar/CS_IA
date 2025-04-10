```markdown
# Interactive Chess Web Application

Welcome to the **Interactive Chess Web Application** – a captivating and dynamic chess experience built with Python and Flask! This project combines the timeless challenge of chess with modern web technologies and real-time engine analysis using Stockfish. Whether you're a casual player or a serious chess enthusiast, you'll find this application engaging and powerful.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Getting the Stockfish Binary](#getting-the-stockfish-binary)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux](#linux)
- [Running the Application](#running-the-application)
- [How to Play](#how-to-play)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Interactive Chess Board:**  
  Enjoy a responsive, beautifully rendered chess board with Unicode pieces.

- **Real-Time Engine Analysis:**  
  Toggle engine mode to receive move suggestions and win probability evaluations powered by Stockfish.

- **Pawn Promotion Handling:**  
  Automatic prompts for choosing a promotion piece when a pawn reaches the back rank.

- **Opening Recognition:**  
  Detect and display chess openings using a comprehensive openings dataset (`openings.txt`).

- **Move Management:**  
  Make moves, undo/redo actions, and view a detailed move list with game statistics.

- **Live Game Stats:**  
  Track moves, captured pieces, material balance, and more in real-time.

- **Live Win Probability Chart:**  
  Visualize engine evaluations with a live-updating chart.

- **Dark Mode Toggle:**  
  Switch to dark mode for a modern, sleek look.

---

## Prerequisites

- **Python 3.7+** – Ensure you have Python installed.
- **pip** – Python’s package installer.
- **Stockfish Engine:**  
  Stockfish is used for chess engine analysis. See the section below for instructions on obtaining and configuring Stockfish.

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://your-repo-url.git
   cd your-repo-directory
   ```

2. **Create a Virtual Environment:**

   ```bash
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment:**

   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## Getting the Stockfish Binary

The chess engine used for analysis is Stockfish. Follow the instructions below to obtain and configure Stockfish for your operating system.

### Windows

1. **Download Stockfish:**
   - Visit the [Stockfish download page](https://stockfishchess.org/download/).
   - Select the appropriate Windows version (typically a ZIP file).

2. **Install Stockfish:**
   - Extract the ZIP file to a folder of your choice.
   - Locate the `stockfish.exe` binary in the extracted folder.

3. **Configure the Environment Variable:**
   - Set the `STOCKFISH_PATH` environment variable to the full path of `stockfish.exe`.
   - Example (Command Prompt):
     ```cmd
     set STOCKFISH_PATH=C:\path\to\stockfish.exe
     ```

### macOS

1. **Install via Homebrew (Recommended):**

   If you have Homebrew installed, run:
   ```bash
   brew install stockfish
   ```
   Homebrew will install Stockfish to `/usr/local/bin/stockfish` or `/opt/homebrew/bin/stockfish` on Apple Silicon Macs.

2. **Alternatively, Download Manually:**
   - Visit the [Stockfish download page](https://stockfishchess.org/download/).
   - Download the macOS version and extract the binary.

3. **Configure the Environment Variable:**
   - Set the `STOCKFISH_PATH` environment variable to the path of the Stockfish binary.
   - Example (Bash):
     ```bash
     export STOCKFISH_PATH="/usr/local/bin/stockfish"
     ```

### Linux

1. **Install via Package Manager (Debian/Ubuntu):**

   ```bash
   sudo apt update
   sudo apt install stockfish
   ```

2. **Alternatively, Download Manually:**
   - Visit the [Stockfish download page](https://stockfishchess.org/download/).
   - Download the Linux version, extract it, and locate the binary.

3. **Configure the Environment Variable:**
   - Set the `STOCKFISH_PATH` environment variable to the full path of the Stockfish binary.
   - Example (Bash):
     ```bash
     export STOCKFISH_PATH="/usr/bin/stockfish"
     ```

---

## Running the Application

1. **Ensure Stockfish is Configured:**

   Make sure the `STOCKFISH_PATH` environment variable is set according to your operating system as described above.

2. **Start the Flask Application:**

   ```bash
   python app.py
   ```

3. **Access the Application:**

   Open your browser and navigate to:  
   [http://localhost:5000](http://localhost:5000)

---

## How to Play

- **Move Pieces:**  
  Click on a piece to see its legal moves or drag and drop to make a move.

- **Engine Analysis:**  
  Toggle engine mode using the provided checkbox to get move suggestions and win probability evaluations.

- **Undo/Redo Moves:**  
  Use the "Undo" and "Redo" buttons to navigate through your move history.

- **Reset the Game:**  
  Click the "Reset Game" button to start a new match.

- **Pawn Promotion:**  
  When a pawn reaches the back rank, a prompt will appear to choose a promotion piece (Queen, Rook, Bishop, or Knight).

- **View Game Stats:**  
  The sidebar displays live updates on move count, captured pieces, material balance, and engine evaluation.

---

## Troubleshooting

- **Stockfish Not Found:**  
  Verify that Stockfish is installed and that the `STOCKFISH_PATH` environment variable is correctly set.

- **Dependency Issues:**  
  If you encounter issues during dependency installation, try upgrading pip:
  
  ```bash
  pip install --upgrade pip
  ```

- **Port Conflicts:**  
  If port 5000 is in use, update the port in the `app.run()` command in `app.py`.

---
## License

This project is open source and available under the [MIT License](LICENSE).

---

Enjoy your game and happy coding! If you have any questions or need further assistance, feel free to reach out.
```