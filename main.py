import streamlit as st
import cv2
import face_recognition
import numpy as np
import pickle
import os
from pathlib import Path
from PIL import Image

# Database file path
DB_FILE = "face_database.pkl"

# Initialize database
def load_database():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

def save_database(db):
    with open(DB_FILE, 'wb') as f:
        pickle.dump(db, f)

# Initialize session state
if 'database' not in st.session_state:
    st.session_state.database = load_database()

# Page configuration
st.set_page_config(page_title="Face Recognition System", page_icon="🔐", layout="wide")

# Title
st.title("🔐 Face Recognition System")
st.markdown("---")

# Sidebar for navigation
menu = st.sidebar.selectbox("Menu", ["Register User", "Verify User", "View Registered Users"])

# Register User Section
if menu == "Register User":
    st.header("📝 Register New User")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Basic Information")
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        address = st.text_area("Address")
    
    with col2:
        st.subheader("Capture Face")
        camera_input = st.camera_input("Take a photo")
        
        if camera_input is not None:
            # Display captured image
            image = Image.open(camera_input)
            st.image(image, caption="Captured Image", use_container_width=True)
    
    if st.button("Register User", type="primary"):
        if not name or not email or not camera_input:
            st.error("Please fill all required fields (Name, Email) and capture a photo!")
        elif email in st.session_state.database:
            st.error("User with this email already exists!")
        else:
            # Process the image
            image = Image.open(camera_input)
            image_np = np.array(image)
            
            # Convert RGB to BGR for face_recognition
            image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
            
            # Detect face encodings
            face_locations = face_recognition.face_locations(image_rgb)
            face_encodings = face_recognition.face_encodings(image_rgb, face_locations)
            
            if len(face_encodings) == 0:
                st.error("No face detected! Please capture a clear photo of your face.")
            elif len(face_encodings) > 1:
                st.error("Multiple faces detected! Please ensure only one face is visible.")
            else:
                # Save user data
                user_data = {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'address': address,
                    'face_encoding': face_encodings[0]
                }
                
                st.session_state.database[email] = user_data
                save_database(st.session_state.database)
                
                st.success(f"✅ User {name} registered successfully!")
                st.balloons()

# Verify User Section
elif menu == "Verify User":
    st.header("🔍 Verify User")
    
    if len(st.session_state.database) == 0:
        st.warning("No users registered yet. Please register first!")
    else:
        st.subheader("Capture Face for Verification")
        camera_input = st.camera_input("Take a photo to verify")
        
        if camera_input is not None:
            image = Image.open(camera_input)
            st.image(image, caption="Captured Image", use_container_width=True)
            
            if st.button("Verify Face", type="primary"):
                # Process the image
                image_np = np.array(image)
                image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
                
                # Detect face encodings
                face_locations = face_recognition.face_locations(image_rgb)
                face_encodings = face_recognition.face_encodings(image_rgb, face_locations)
                
                if len(face_encodings) == 0:
                    st.error("❌ No face detected! Please capture a clear photo.")
                elif len(face_encodings) > 1:
                    st.error("❌ Multiple faces detected! Please ensure only one face is visible.")
                else:
                    unknown_encoding = face_encodings[0]
                    
                    # Compare with all registered users
                    match_found = False
                    
                    for email, user_data in st.session_state.database.items():
                        registered_encoding = user_data['face_encoding']
                        
                        # Compare faces
                        matches = face_recognition.compare_faces([registered_encoding], unknown_encoding, tolerance=0.6)
                        face_distance = face_recognition.face_distance([registered_encoding], unknown_encoding)
                        
                        if matches[0]:
                            match_found = True
                            confidence = (1 - face_distance[0]) * 100
                            
                            st.success(f"✅ Face Matched!")
                            st.balloons()
                            
                            # Display user information
                            st.markdown("---")
                            st.subheader("User Information")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**Name:** {user_data['name']}")
                                st.write(f"**Email:** {user_data['email']}")
                            
                            with col2:
                                st.write(f"**Phone:** {user_data['phone']}")
                                st.write(f"**Address:** {user_data['address']}")
                            
                            st.info(f"Match Confidence: {confidence:.2f}%")
                            break
                    
                    if not match_found:
                        st.error("❌ Face Does Not Match! User not found in database.")

# View Registered Users Section
elif menu == "View Registered Users":
    st.header("👥 Registered Users")
    
    if len(st.session_state.database) == 0:
        st.info("No users registered yet.")
    else:
        st.write(f"Total Registered Users: {len(st.session_state.database)}")
        st.markdown("---")
        
        for i, (email, user_data) in enumerate(st.session_state.database.items(), 1):
            with st.expander(f"User {i}: {user_data['name']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Name:** {user_data['name']}")
                    st.write(f"**Email:** {user_data['email']}")
                
                with col2:
                    st.write(f"**Phone:** {user_data['phone']}")
                    st.write(f"**Address:** {user_data['address']}")
                
                if st.button(f"Delete {user_data['name']}", key=f"del_{email}"):
                    del st.session_state.database[email]
                    save_database(st.session_state.database)
                    st.success(f"User {user_data['name']} deleted successfully!")
                    st.rerun()

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and Face Recognition")