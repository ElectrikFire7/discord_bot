# **Discord Bot - Interactive Chat & Reaction Handling**

A simple Discord bot that responds to messages, handles reactions, and supports interactive commands.

---

## **🚀 Features**
✅ Responds to user messages with predefined replies.  
✅ Supports **private and public messages**.  
✅ Adds **emoji reactions** to specific messages.  
✅ Detects and processes **user reactions**.  
✅ Uses an external **`.env` file** for token security.  

---

## **📂 Project Structure**
```
discord-bot/
│── media/                    # Stores GIFs and media files
│── directCommands/           # Handles specific commands
│── simpleResponse/           # Handles predefined responses
│── .env                      # Stores the bot token securely
│── .gitignore                # Ignores unnecessary files (e.g., __pycache__)
│── main.py                   # Main bot script
│── controller.py             # Routes messages to the appropriate functions
│── requirements.txt          # Dependencies for the project
│── README.md                 # Project documentation
```

---

## **🛠️ Setup Instructions**
### **1️⃣ Prerequisites**
- Install **Python 3.9+**
- Create a **Discord bot** and get its **TOKEN** from the [Discord Developer Portal](https://discord.com/developers/applications)

### **2️⃣ Clone the Repository**
```sh
git clone https://github.com/yourusername/discord-bot.git
cd discord-bot
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**
Create a `.env` file in the project root and add:
```
TOKEN=your_discord_bot_token_here
```

### **5️⃣ Run the Bot**
```sh
python main.py
```

---

## **📜 Bot Messages**
| Message | Description |
|---------|-------------|
| `hello` | Responds with `"Hello!"` |
| `hello there` | Replies with `"General Kenobi!"` |
| `hi` | Sends a fun message and a GIF |

## **📜 Bot Messages**
| Commands | Description |
|---------|-------------|
| `In Development` | Replies with `In Development` |
| `In Development` | Replies with `In Development` |

---

## **🤖 How the Bot Works**
1. **Message Handling**  
   - `main.py` receives messages and forwards them to `controller.py`.  
   - `controller.py` checks whether it's a command (`?command`) or a simple response.  
   - `simpleResponse.py` processes basic responses.

2. **Reactions Handling**  
   - The bot sends messages that allow reactions.  
   - It listens for `on_reaction_add()` to detect user reactions.  
   - It filters reactions **only to bot messages** using `message.author == client.user`.

---


## **🛑 Troubleshooting**
❌ **Bot doesn't respond?**  
✔️ Ensure the bot has **`MESSAGE CONTENT INTENT`** enabled in the Discord Developer Portal.  

❌ **Reactions not appearing?**  
✔️ Make sure the bot has the `"Add Reactions"` permission.  

❌ **`__pycache__` folder appearing?**  
✔️ This is normal. Add `__pycache__/` to `.gitignore` to exclude it from Git.  

---

## **📜 License**
This project is licensed under the **CHIGGA**.

---

## **💡 Contributing**
Want to improve this bot?  
1. Fork the repo  
2. Create a new branch (`feature-xyz`)  
3. Commit your changes  
4. Create a pull request  

---

## **📞 Contact**
For issues or suggestions, create an **Issue** on GitHub or reach out on Discord.  

---
### **🌟 Star this repo if you found it useful!**
