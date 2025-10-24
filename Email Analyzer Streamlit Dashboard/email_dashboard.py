import streamlit as st
import imapclient
import pyzmail
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
import ssl
import os

# configs
EMAIL_ACCOUNT = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"
IMAP_SERVER = "imap.gmail.com"
SHEET_NAME = "Email Analysis Data"
FETCH_LIMIT = 200
SERVICE_ACCOUNT_FILE = "path/to/your/service_account.json"


# google sheets setup
def init_google_sheets():
    try:
        if not os.path.exists(SERVICE_ACCOUNT_FILE):
            st.warning(
                "⚠️ Google Sheets credentials not found — using local logging instead."
            )
            return None

        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=scope
        )
        client = gspread.authorize(creds)

        try:
            sheet = client.open(SHEET_NAME).sheet1
        except gspread.SpreadsheetNotFound:
            sheet = client.create(SHEET_NAME).sheet1
            sheet.append_row(["Timestamp", "Total Emails", "Unread Emails"])

        st.success("✅ Connected to Google Sheets!")
        return sheet
    except Exception as e:
        st.warning(f"⚠️ Google Sheets unavailable: {e}")
        st.info("📁 Falling back to local CSV logging.")
        return None


# email connection setup
def init_email_connection():
    try:
        try:
            imap_obj = imapclient.IMAPClient(IMAP_SERVER, ssl=True)
        except ssl.SSLError:
            # Fix SSL issue on macOS
            st.warning(
                "⚠️ SSL verification failed. Using fallback SSL context (macOS fix)."
            )
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            imap_obj = imapclient.IMAPClient(
                IMAP_SERVER, ssl=True, ssl_context=ssl_context
            )

        imap_obj.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        imap_obj.select_folder("INBOX", readonly=True)
        st.success("✅ Email connection established!")
        return imap_obj
    except Exception as e:
        st.error(f"❌ Email connection failed: {e}")
        return None


# fetch emails
def fetch_emails(imap_obj, limit=FETCH_LIMIT):
    try:
        uids = imap_obj.search("ALL")
        uids = uids[-limit:] if len(uids) > limit else uids
        emails, senders = [], []

        for uid in uids:
            try:
                raw = imap_obj.fetch([uid], ["BODY[]", "FLAGS"])
                msg = pyzmail.PyzMessage.factory(raw[uid][b"BODY[]"])
                subject = msg.get_subject() or "No Subject"
                from_addrs = msg.get_addresses("from")
                from_email = from_addrs[0][1] if from_addrs else "Unknown"
                flags = raw[uid][b"FLAGS"]
                read_status = "Unread" if b"\\Seen" not in flags else "Read"
                emails.append(
                    {"subject": subject, "from": from_email, "status": read_status}
                )
                senders.append(from_email)
            except Exception as e:
                st.warning(f"⚠️ Skipped one email (UID {uid}): {e}")
                continue
        return emails, senders
    except Exception as e:
        st.error(f"❌ Failed to fetch emails: {e}")
        return [], []


# streamlit app
st.title("📧 Email Analyzer Dashboard")
st.write("Analyze your inbox, unread emails, and top senders.")

sheet = init_google_sheets()
imap_obj = init_email_connection()

if not imap_obj:
    st.stop()

# fetch button
if st.button("Fetch Latest Emails"):
    with st.spinner("Fetching emails..."):
        emails, senders = fetch_emails(imap_obj)
        if not emails:
            st.warning(
                "⚠️ No emails fetched. Please verify your credentials or IMAP access."
            )
        else:
            df = pd.DataFrame(emails)
            total, unread = len(df), len(df[df["status"] == "Unread"])

            col1, col2 = st.columns(2)
            col1.metric("Total Emails Fetched", total)
            col2.metric("Unread Emails", unread)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if sheet:
                try:
                    sheet.append_row([timestamp, total, unread])
                    st.success("✅ Logged to Google Sheets!")
                except Exception as e:
                    st.warning(f"⚠️ Failed to log to Google Sheets: {e}")
                    with open("email_log.csv", "a") as f:
                        f.write(f"{timestamp},{total},{unread}\n")
                    st.info("📁 Logged locally to email_log.csv.")
            else:
                # create CSV with header if it doesn't exist
                if not os.path.exists("email_log.csv"):
                    with open("email_log.csv", "w") as f:
                        f.write("Timestamp,Total Emails,Unread Emails\n")
                
                with open("email_log.csv", "a") as f:
                    f.write(f"{timestamp},{total},{unread}\n")
                st.info("📁 Logged locally to email_log.csv.")

            st.subheader("Recent Emails")
            st.dataframe(df)

            top_senders = Counter(senders).most_common(10)
            if top_senders:
                names, counts = zip(*top_senders)
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.barh(names, counts, color="skyblue")
                ax.set_xlabel("Number of Emails")
                ax.set_ylabel("Sender")
                ax.set_title("Top 10 Senders")
                plt.tight_layout()
                st.pyplot(fig)

# show history
if st.checkbox("Show Historical Logs"):
    if sheet:
        try:
            data = sheet.get_all_records()
            if data:
                st.subheader("📊 Historical Email Logs (Google Sheets)")
                st.dataframe(pd.DataFrame(data))
            else:
                st.info("ℹ️ No history found.")
        except Exception as e:
            st.warning(f"⚠️ Unable to fetch Google Sheets data: {e}")
    elif os.path.exists("email_log.csv"):
        try:
            df_local = pd.read_csv("email_log.csv")
            
            if len(df_local.columns) == 1 or 'Timestamp' not in df_local.columns:
                df_local = pd.read_csv(
                    "email_log.csv", names=["Timestamp", "Total Emails", "Unread Emails"]
                )
            st.subheader("📁 Historical Email Logs (Local CSV)")
            st.dataframe(df_local)
        except Exception as e:
            st.warning(f"⚠️ Error reading CSV file: {e}")
    else:
        st.info("ℹ️ No log data found yet.")

# logout
try:
    imap_obj.logout()
except:
    pass
