**📊 Complaint Management System**

A web-based Complaint Management System built using Flask, where students can submit complaints and admins can manage, track, and resolve them through a dashboard.

**🚀 Features**

**  📝 Student Side**
  
  Submit complaints with title, category, and description
  
  Track the status of submitted complaints

  **🔑 Admin Side**
  
  Login-secured dashboard
  
  View all complaints in a clean tabular format
  
  Collapsible complaint descriptions
  
  Update complaint status (Pending / In Progress / Resolved)
  
  Logout functionality
  
  **🎨 UI**
  
  Responsive design (works on desktop & mobile)
  
  Smooth animations & modern styling
  
  Loading spinner before content display

**🛠️ Tech Stack**

  Frontend: HTML, CSS, JavaScript
  
  Backend: Python (Flask)
  
  Database: SQLite (default)
  
  Version Control: Git & GitHub

**📂 Project Structure**

  project-folder/
  │── static/ → CSS, JS, images
  │── templates/ → HTML files (Flask templates)
  │── app.py → Flask app entry point
  │── requirements.txt → Dependencies
  │── README.md → Project documentation

**Setup Instructions**

  **Clone the repository**
  
  git clone https://github.com/your-username/complaint-system.git
  cd complaint-system


**Create virtual environment (optional but recommended)**

  python -m venv venv
  source venv/bin/activate   # For Linux/Mac
  venv\Scripts\activate      # For Windows


**Install dependencies**

pip install -r requirements.txt


**Run the application**

  python app.py


**Open in browser:**

  http://127.0.0.1:5000/
