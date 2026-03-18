import streamlit as st
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "https://your-n8n-domain.com/webhook/finserve")
RESPONSES_DIR = "responses"

# Create responses directory if it doesn't exist
if not os.path.exists(RESPONSES_DIR):
    os.makedirs(RESPONSES_DIR)

st.set_page_config(page_title="FinServe Co-Pilot", layout="wide")

# --- SESSION STATE INITIALIZATION ---
if "ai_data" not in st.session_state:
    st.session_state.ai_data = None
if "current_ticket" not in st.session_state:
    st.session_state.current_ticket = None

# --- MOCK TICKETS ---
TICKETS = {
    "TCK-8091 (Lost Card)": {
        "customer": "Sarah Jenkins",
        "email": "I was on vacation in Spain and my purse was stolen along with my FinServe credit card! I'm panicking, please block it immediately. Will I be charged for a new one?"
    },
    "TCK-8092 (Loan Info)": {
        "customer": "Michael Scott",
        "email": "Hi, I have a small SME loan with you guys. Business has been good and I want to pay off the remaining balance early. Are there any hidden penalty fees for doing this?"
    },
    "TCK-8093 (Crypto Query)": {
        "customer": "David Chen",
        "email": "Hello, I am looking to secure a loan of $50,000 to invest in a new cryptocurrency portfolio. Do you offer specialized crypto-backed loans?"
    }
}

def save_response(ticket_id, customer, response_text, action):
    """Save response to a text file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{RESPONSES_DIR}/{ticket_id}_{action}_{timestamp}.txt"
    
    content = f"""FinServe Support Response Log
{'='*60}
Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Ticket ID: {ticket_id}
Customer: {customer}
Action: {action}
{'='*60}

RESPONSE TEXT:
{response_text}

{'='*60}
End of Response
"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return filename

# --- MAIN APP ---
st.title("Client Support Workspace")


# --- SPLIT SCREEN LAYOUT ---
left_col, right_col = st.columns([1, 1.5], gap="large")

# --- LEFT COLUMN: TICKET DETAILS ---
with left_col:
    st.subheader("Ticket Details")
    selected_ticket_id = st.selectbox("Select a ticket to resolve:", list(TICKETS.keys()))

    if st.session_state.current_ticket != selected_ticket_id:
        st.session_state.ai_data = None
        st.session_state.current_ticket = selected_ticket_id

    ticket_data = TICKETS[selected_ticket_id]

    st.markdown(f"**Customer:** {ticket_data['customer']}")
    st.markdown(f"**Ticket ID:** {selected_ticket_id}")
    st.info(f"\"{ticket_data['email']}\"")
    
    st.markdown("<br>", unsafe_allow_html=True) 
    
    if st.button("Generate Compliant Response", type="primary", use_container_width=True):
        with st.spinner("Connecting to n8n... Fetching policies and drafting response..."):
            payload = {
                "ticket_text": ticket_data['email'],
                "customer_name": ticket_data['customer']
            }
            
            try:
                response = requests.post(N8N_WEBHOOK_URL, json=payload)
                if response.status_code == 200:
                    st.session_state.ai_data = response.json()
                else:
                    st.error(f"Backend error: {response.status_code}. Make sure your n8n test webhook is active!")
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")

# --- RIGHT COLUMN: AI ANALYSIS & ACTION ---
with right_col:
    st.subheader("AI Analysis & Action")
    
    if st.session_state.ai_data:
        ai_data = st.session_state.ai_data
        
        c_cat, c_sent = st.columns(2)
        with c_cat:
            st.markdown(f"**Detected Category**: `{ai_data.get('category', 'N/A')}`")
        with c_sent:
            st.markdown(f"**Detected Sentiment**: `{ai_data.get('sentiment', 'N/A')}`")

       
        suggested_policy = ai_data.get('suggested_policy', '')
        
        if suggested_policy == "NO_POLICY_FOUND":
            st.error("**COMPLIANCE ALERT:** AI did not find a matching policy in the knowledge base! This draft is a generic placeholder. Please consult a manager or route to a specialist.")
        else:
            st.success("Response drafted successfully using verified FinServe knowledge base policies.")
            with st.expander("View Policy Used (RAG Source)"):
                st.write(suggested_policy)
        
        draft_response = st.text_area("Review & Edit Draft:", value=ai_data.get('draft_reply', ''), height=250, key="draft_text_input")
        
        c1, c2 = st.columns(2)
        
        with c1:
            if st.button("Approve & Send", key="approve_btn", use_container_width=True):
                filename = save_response(selected_ticket_id, ticket_data['customer'], draft_response, "APPROVED")
                st.success(f"Message sent! Log saved to `{filename}`.")
                
        with c2:
            if st.button("Escalate", key="escalate_btn", use_container_width=True):
                filename = save_response(selected_ticket_id, ticket_data['customer'], draft_response, "ESCALATED")
                st.warning(f"Ticket escalated. Log saved to `{filename}`.")
    else:
        st.info("Click **Generate Compliant Response** to trigger the AI Co-Pilot.")