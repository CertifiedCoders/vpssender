# 📦 VPS Sender - Telegram File Uploader

**VPS Sender** is a Python-based CLI tool to upload and send files or entire folders (as zipped files) to a specified Telegram chat using a bot. It provides real-time upload progress and supports bulk sending via pattern matching (e.g., `*.txt`).

---

## 🚀 Features

- ✅ Send individual files or complete folders to Telegram
- 📦 Automatically zips folders before sending
- 📁 Bulk file sending using patterns like `*.zip`, `*.pdf`, etc.
- 📊 Real-time upload progress bar with speed and time remaining
- 💬 Interactive command-line interface with prompts and error handling

---

## 🛠️ Requirements

- Python 3.6+
- Telegram Bot Token & Chat ID (see [Get Started](#-get-started))

### Python Dependencies

Install the required packages using:

```bash
pip install -r requirements.txt
```

**Dependencies:**
- `requests`
- `rich`

---

## 📅 Installation

1. Clone the repository:
```bash
git clone https://github.com/CertifiedCoders/vpssender.git
cd vpssender
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🔧 Get Started

1. **Create a Telegram Bot:**
   - Go to [@BotFather](https://t.me/BotFather)
   - Use `/newbot` to create a bot and get the `BOT_TOKEN`.

2. **Find your Chat ID:**
   - Search for [@userinfobot](https://t.me/userinfobot) on Telegram
   - Start the bot to get your `chat_id`

3. **Run the Tool:**
```bash
python3 vpssender.py
```

---

## 🧑‍💻 Usage

Follow the CLI prompts:

- Enter your bot token and chat ID
- Enter a file path, folder name, or pattern like `*.pdf`
- The tool will:
  - Show file size
  - Display a real-time upload progress bar
  - Zip folders automatically and delete them after sending

---

## 📸 Example

```bash
Welcome to the Advanced Telegram File Sender

Enter your Telegram Bot Token: 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
Enter the Chat ID to send the file to: 987654321

Enter the file or folder name (use *.ext for bulk send): *.pdf
Found 3 file(s) to send: report1.pdf, doc2.pdf, notes.pdf
```

---

## 💡 Tips

- Use `*.ext` to send multiple files of the same type.
- Use the full folder name to zip and send it as a `.zip` file.
- Works well on both Windows and Unix-based systems.

---

## 📜 License

This project is open-source under the [MIT License](LICENSE).

---

## 🙌 Credits

Developed and maintained by [CertifiedCoders](https://github.com/CertifiedCoders)
