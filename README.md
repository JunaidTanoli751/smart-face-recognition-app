# smart-face-recognition-app
# 🔐 Streamlit Face Recognition System

A real-time **Face Recognition & Verification System** built using **Python**, **Streamlit**, and the `face_recognition` library.  
This application allows users to **register**, **verify**, and **manage** users using facial biometrics via a webcam.

---

## ✨ Features

- 📸 Face registration using webcam
- 🔍 Face verification with confidence score
- 👤 User management (view & delete users)
- 💾 Persistent face database using Pickle
- 🧠 Accurate face matching with tolerance control
- 🌐 Interactive web UI powered by Streamlit

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **OpenCV**
- **face_recognition**
- **NumPy**
- **Pillow**

---
## 📂 Project Structure
├── app.py
├── face_database.pkl
├── README.md
├── .gitignore

Create virtual environment
python -m venv env
env\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the app
streamlit run app.py

🧪 How It Works
➕ Register User

Enter user details

Capture face using webcam

Face encoding stored securely
🔍 Verify User

Capture face

System compares with registered users

Displays match confidence & user info

👥 Manage Users

View all registered users

Delete users from database

⚠️ Notes

Ensure good lighting for better accuracy

Only one face should be visible during capture

Webcam access is required

🚀 Future Improvements

Database integration (MongoDB / MySQL)

Admin authentication

Liveness detection

Deployment on Streamlit Cloud

👨‍💻 Author

Junaid Tanoli
BS Computer Science | AI & Data Science
GitHub: https://github.com/JunaidTanoli751
























├── requirements.txt## 📂 Project Structure

