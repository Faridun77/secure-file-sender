# 💼 Corporate Secure File Sender

A modern, lightweight desktop application for instant file distribution via Email using a simple Drag-and-Drop interface. Designed for corporate environments.

## ✨ Features

- **Modern UI** - Built with CustomTkinter for sleek dark-themed interface
- **Drag-and-Drop** - Seamless file handling with tkinterdnd2
- **Smart Identification** - Auto-detects Windows username, includes in email
- **Always-on-Top** - Window stays above other apps for quick access
- **Multi-threaded** - File sending in background, UI never freezes
- **Visual Feedback** - Dynamic status labels and progress bars

## 🖥️ Tech Stack

- **Language:** Python 3.10+
- **GUI:** CustomTkinter
- **Email:** SMTPLib (SSL/TLS)
- **OS Integration:** GetPass, Threading
- **Drag-Drop:** tkinterdnd2

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- Windows OS (for best experience)
- Valid SMTP credentials

### Steps

1. Clone repository
```bash
git clone https://github.com/YOUR_USERNAME/secure-file-sender.git
cd secure-file-sender
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure SMTP settings
Open `secure_sender.py` and update:
```python
SMTP_SERVER = 'smtp.gmail.com'      # Your SMTP server
SMTP_PORT = 465                      # SSL port
SENDER_EMAIL = 'your-email@gmail.com'
SENDER_PASSWORD = 'your-app-password'
RECEIVER_EMAIL = 'receiver@mail.com'
```

4. Run the application
```bash
python secure_sender.py
```

## 🚀 How to Use

1. Run the application
2. Drag and drop a file into the app window
3. The file will be automatically sent via email
4. Watch the status updates in real-time

## 🔐 Security Notes

⚠️ **Important:**
- Never commit SMTP credentials to GitHub
- Use app passwords instead of main account passwords
- For Gmail: Generate app password from account settings
- Store credentials in environment variables in production

## 📝 Example Configuration

### Gmail Setup
1. Enable 2-Step Verification
2. Generate App Password for your account
3. Use app password in SENDER_PASSWORD

### Outlook Setup
```python
SMTP_SERVER = 'smtp-mail.outlook.com'
SMTP_PORT = 587  # or 465 for SSL
```

## 🔨 Building Executable

Create a standalone .exe file:
```bash
pip install pyinstaller

pyinstaller --noconsole --onefile \
  --collect-all tkinterdnd2 \
  --collect-all customtkinter \
  --icon="icon.ico" \
  --name "SecureSender" \
  secure_sender.py
```

Executable will be in `dist/` folder.

## 📋 Features Breakdown

### Drag-and-Drop
- Simply drag files into the application window
- Automatic validation of file paths
- Support for all file types

### Email Attachment
- Automatic file attachment to email
- Includes sender information in body
- Timestamp tracking

### Status Indicators
- **Blue:** Ready/Processing
- **Green:** Success
- **Orange:** Processing
- **Red:** Error

## 🐛 Troubleshooting

### "tkinterdnd2 module not found"
```bash
pip install tkinterdnd2
```

### "SMTP Connection Error"
- Verify SMTP credentials
- Check SMTP port (usually 465 or 587)
- Ensure firewall allows outgoing connections

### "App won't start"
- Update customtkinter: `pip install --upgrade customtkinter`
- Restart Python

## 📄 License

MIT License - Free to use and modify

## 👤 Author

Created with ❤️ for corporate environments

## 🤝 Contributing

Contributions welcome! Submit issues and pull requests.

---

**Made with Python and ❤️**
```

---

#### **Файл 4: .gitignore**

**Имя:** `.gitignore`

**Содержание:**
```
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.env
.venv
venv/
ENV/
env/
.idea/
.vscode/
*.swp
*.swo
*.log
*.sqlite
*.db
.DS_Store
