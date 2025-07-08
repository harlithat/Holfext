
# 📡 Extensometer Dashboard – Holftontein Site

This is a real-time, cloud-hosted extensometer monitoring dashboard built with **Streamlit**. It visualizes and analyzes strain and temperature data transmitted over a GSM network, processed via a Virtual Machine (VM), and published online for public or project team access.

---

## 🚀 How the System Works

### 1. 📈 Data Generation & Transmission
- Extensometers that are buried underground collect strain data on-site. Temperature recordings are also made nearby but rather above ground and not at the actual Extensometers.
- The data is sent via **GSM network** to a **Virtual Machine (VM)**.

### 2. 🗃️ Local File Sync on VM
- A CSV file is maintained and updated on the VM.
- **Google Drive Backup & Sync** is set up on the VM to sync the CSV to Google Drive.

### 3. 🛠️ CSV Timestamp Update Script
- A small Python script is scheduled via **Windows Task Scheduler** to "touch" the CSV every 5 minutes to trigger sync.
- This ensures Google Drive always recognizes a file change and syncs it to the cloud.

### 4. ☁️ Cloud Hosting & Access
- The Google Drive CSV file is made accessible via a direct download URL

### 5. 📊 Streamlit Dashboard
- A Streamlit app is deployed on [Streamlit Cloud](https://streamlit.io/cloud).
- The app auto-fetches the CSV file from the link every **10 minutes** and:
  - Appends a constants row
  - Performs all engineering calculations
  - Displays:
    - A banner showing the last reading received
    - Interactive microstrain scatter chart
    - Temperature line chart
    - Two live pressure-style gauges (maximum compressive & tensile stresses recorded to date)
    - A scrolling credits marquee
- Hosted dashboard URL: `https://holfonteinextensometers.streamlit.app/`

---

## 📁 Files in This Repo

| File                | Purpose                                        |
|---------------------|------------------------------------------------|
| `app.py`            | Main Streamlit dashboard script                |
| `requirements.txt`  | Python dependencies for Streamlit Cloud        |
| `README.md`         | You are here! Setup instructions and overview |

---

## ✅ Technologies Used

- **Python**
- **Streamlit**
- **Plotly** (interactive charts + gauges)
- **Pandas**
- **Google Drive**
- **Windows Task Scheduler**
- **GSM Network**

---

## 🙌 Credits

- Back-End & Data Transmission: **Dennis Louw**
- Post-Processing & Dashboard: **Grant Harli (J&W)**
- Extensometer Hardware & Installation: **Dr. Irvin Luker**

---

## 📞 Support / Questions

Reach out via project channels or directly via GitHub issues if you have questions about deploying or modifying the dashboard.

