import streamlit as st
import random
import string
import datetime

# In-memory "databases"
USERS = {}
PENDING_USERS = {}
SHIPMENTS = {}
WAYBILLS = {}

# Directly initialize the admin user (always run this)
USERS['admin'] = {
    "username": "admin",
    "business_name": "FreightForge Administration",
    "contact_person": "System Administrator",
    "email": "admin@freightforge.com",
    "mobile": "555-ADMIN",
    "pan_gst": "ADMIN123456",
    "approved": "yes",
    "business_type": "Administration",
    "address": "FreightForge HQ",
    "password": "admin",
    "doc": b"admin_document"
}

# Add customers to pending users if they don't exist yet
if 'Customer1' not in PENDING_USERS:
    PENDING_USERS['Customer1'] = {
        "username": "Customer1",
        "business_name": "Grain Traders Inc.",
        "contact_person": "John Smith",
        "email": "john@graintraders.com",
        "mobile": "555-1234",
        "pan_gst": "GRAIN123456",
        "approved": "no",
        "business_type": "Agriculture",
        "address": "123 Farm Road, Rural County",
        "password": "Customer1",
        "doc": b"customer1_document"
    }

if 'Customer2' not in PENDING_USERS:
    PENDING_USERS['Customer2'] = {
        "username": "Customer2",
        "business_name": "Logistics Masters Ltd.",
        "contact_person": "Sarah Johnson",
        "email": "sarah@logisticsmasters.com",
        "mobile": "555-5678",
        "pan_gst": "LOGIS123456",
        "approved": "no",
        "business_type": "Logistics",
        "address": "456 Transport Avenue, Shipping City",
        "password": "Customer2",
        "doc": b"customer2_document"
    }
    
# Helper functions
def send_otp(email_or_phone):
    otp = ''.join(random.choices(string.digits, k=6))
    st.session_state['otp'] = otp
    st.session_state['otp_verified'] = False
    st.session_state['otp_contact'] = email_or_phone
    st.info(f"(Demo) OTP for {email_or_phone} is {otp}")

def generate_waybill(booking_info):
    ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    WAYBILLS[ref] = {
        "waybill_ref": ref,
        "details": booking_info,
        "tracking": [
            {"status":"Booking Confirmed", "time":datetime.datetime.now()},
            {"status":"In Transit", "time":datetime.datetime.now() + datetime.timedelta(hours=4)},
            {"status":"Arriving", "time":datetime.datetime.now() + datetime.timedelta(hours=16)},
        ],
        "status": "Booked",
        "eta": datetime.datetime.now() + datetime.timedelta(hours=20)
    }
    return ref

def check_user(username, password):
    # Debug info
    st.write(f"Checking user: {username}")
    st.write(f"Available users: {list(USERS.keys())}")

    u = USERS.get(username)
    if u and u['password'] == password and u.get('approved') == "yes":
        return u
    return None

def is_admin():
    # For this demo, first user is admin.
    return st.session_state.get('user') and st.session_state['user']['username'] == 'admin'


# Page selector
st.set_page_config(page_title="FreightForge - Railway Freight Portal", layout="wide")
menu = st.sidebar.radio(
    "Menu", 
    (
        "Welcome",
        "Register & Login",
        "Freight Inquiry & Booking",
        "Track Shipment (Waybill)"
    )
)

# 1. Welcome
if menu == "Welcome":
    st.title("🚞 FreightForge - Railway Freight Booking Portal Prototype")
    st.header("Bulk Grain Shipment Workflow")
    st.write("""
    - Register as a logistics manager to book freight for your business.
    - Inquire rates, book shipment, and generate waybills.
    - Track shipments and receive real-time updates.
    """)

    st.subheader("Demo Instructions")
    st.markdown("""
    This is a **demo Streamlit app** simulating the core user journeys:
    - Registration (with OTP & document upload)
    - Freight inquiry (rate calculator)
    - Shipment booking & waybill generation
    - Real-time tracking
    **(No real OTP/email sent; all data is in-memory!)**
    """)

# 2. Registration & Login
if menu == "Register & Login":
    tab1, tab2, tab3 = st.tabs(["Register", "Login", "Admin Approvals"])
    with tab1:
        st.subheader("New Logistics Manager Registration")
        with st.form("registration-form"):
            business_name = st.text_input("Business Name")
            contact_person = st.text_input("Contact Person")
            email = st.text_input("Email")
            mobile = st.text_input("Mobile Number")
            pan_gst = st.text_input("PAN/GST Number")
            business_type = st.selectbox("Business Type", ["Agriculture", "Logistics", "Other"])
            address = st.text_area("Business Address")
            username = st.text_input("Desired Username")
            password = st.text_input("Password", type="password")
            doc = st.file_uploader("Upload Business Registration/ID Proof (PDF, JPG)", type=['pdf', 'jpg','jpeg','png'])

            if st.form_submit_button("Send OTP for Verification"):
                if not all([business_name, contact_person, email, mobile, pan_gst, username, password, doc]):
                    st.warning("Please fill all fields and upload a document.")
                elif username in USERS or username in PENDING_USERS:
                    st.error("Username already exists!")
                else:
                    send_otp(email)
                    # Save pending registration in session
                    st.session_state['pending_reg'] = {
                        "username":username,
                        "business_name":business_name,
                        "contact_person":contact_person,
                        "email":email,
                        "mobile":mobile,
                        "pan_gst":pan_gst,
                        "business_type":business_type,
                        "address":address,
                        "password":password,
                        "doc":doc.getvalue()
                    }

        if st.session_state.get('otp'):
            st.text_input("Enter OTP sent to your email", key="user_otp")
            if st.button("Verify OTP"):
                if st.session_state['user_otp'] == st.session_state['otp']:
                    st.success("OTP Verified. Registration submitted for admin approval.")
                    PENDING_USERS[st.session_state['pending_reg']['username']] = st.session_state['pending_reg']
                    del st.session_state['pending_reg']
                    del st.session_state['otp']
                else:
                    st.error("Invalid OTP. Try again.")

    with tab2:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            # Debug info
            st.write(f"Available users: {list(USERS.keys())}")
            st.write(f"Trying to log in with username: {username}")

            u = check_user(username, password)
            if u:
                st.session_state['user'] = u
                st.success(f"Welcome {u['contact_person']} as {u['business_name']}")
            else:
                st.error("Invalid credentials or account not yet approved.")

    with tab3:
        st.subheader("Admin: Approve New Users")
        if not is_admin():
            st.info("Login as admin to access approvals. (First registered user is admin.)")
        else:
            if not PENDING_USERS:
                st.info("No pending registrations.")
            else:
                # Create a list of pending users to avoid modification during iteration
                pending_usernames = list(PENDING_USERS.keys())

                for uname in pending_usernames:
                    reg = PENDING_USERS[uname]
                    st.write(f"**{uname}** | {reg['business_name']} | {reg['email']} | Approval Status: {reg['approved']}")
                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button(f"Approve {uname}", key=f"approve_{uname}"):
                            # Set approved status to "yes"
                            reg["approved"] = "yes"
                            # Add to USERS dictionary
                            USERS[uname] = reg
                            # Remove from PENDING_USERS
                            del PENDING_USERS[uname]
                            st.success(f"User {uname} approved and can now log in.")
                            # Force a rerun to update the UI
                            st.rerun()

                    with col2:
                        if st.button(f"Reject {uname}", key=f"reject_{uname}"):
                            # Remove from PENDING_USERS
                            del PENDING_USERS[uname]
                            st.warning(f"User {uname} rejected.")
                            # Force a rerun to update the UI
                            st.rerun()
                        
                        
# 3. Freight Inquiry & Booking
if menu == "Freight Inquiry & Booking":
    user = st.session_state.get('user')
    if not user:
        st.warning("Please log in first.")
    else:
        st.header("🚚 Freight Inquiry and Booking")
        st.write("Book new wheat shipment from Quebec, QC to Windsor, ON.")
        with st.form("freight-inquiry"):
            st.write("### Freight Details")
            goods_type = st.selectbox("Goods Type", ["Wheat","Corn","Soybean"])
            qty = st.number_input("Quantity (metric tons)", min_value=1, max_value=1000, value=500)
            origin = st.text_input("Origin", value="Quebec, QC")
            destination = st.text_input("Destination", value="Windsor, ON")
            dispatch_date = st.date_input("Preferred Dispatch Date", min_value=datetime.date.today())
            submitted = st.form_submit_button("Check Rates & Wagon Options")

        if submitted:
            # Dummy rate calc
            dist_km = 900  # Approx Qc to Windsor
            rate_per_ton_km = 0.11  # Dummy value
            total_charge = qty * dist_km * rate_per_ton_km
            st.success(f"Estimated Freight Charge: **${total_charge:,.2f}**")
            st.write("### Available Wagons/Trains for Grain")
            option = st.radio("Select Option", [
                "Train A (Covered Hopper x25, departs 09:00)",
                "Train B (Boxcar x22, departs 14:00)",
                "Train C (Bulk Grain Car x30, departs 19:00)"
            ])
            if st.button("Book & Pay Now", key="booknow"):
                # Booking
                booking_details = {
                    "user": user['username'],
                    "goods_type":goods_type,
                    "qty":qty,
                    "origin":origin,
                    "destination":destination,
                    "dispatch_date":str(dispatch_date),
                    "option":option,
                    "charge":total_charge,
                    "status":"Booked",
                    "booked_on":str(datetime.datetime.now())
                }
                # Generate waybill
                waybill_ref = generate_waybill(booking_details)
                SHIPMENTS[waybill_ref] = booking_details
                st.session_state['just_booked'] = waybill_ref
                st.success(f"Booking Confirmed! Waybill reference: `{waybill_ref}`")
                st.balloons()

        # Show latest waybill if just booked
        if st.session_state.get('just_booked'):
            ref = st.session_state.get('just_booked')
            st.write("### Download Waybill")
            waybill = WAYBILLS[ref]
            txt = f"""
            WAYBILL REFERENCE: {ref}
            Shipper: {user['business_name']}
            Goods: {waybill['details']['goods_type']} ({waybill['details']['qty']} MT)
            Route: {waybill['details']['origin']} → {waybill['details']['destination']}
            Train: {waybill['details']['option']}
            Charges: ${waybill['details']['charge']:,.2f}
            ETA: {waybill['eta']}
            Tracking Link: Use reference {ref} in tracking tab.
            """
            st.download_button(
                label="Download PDF Waybill (demo .txt)",
                data=txt, 
                file_name=f"waybill_{ref}.txt"
            )
            st.info(f"Track your shipment using waybill reference `{ref}` in tracking tab.")

# 4. Track Shipment
if menu == "Track Shipment (Waybill)":
    st.header("Track Shipment by Waybill Reference")
    ref = st.text_input("Enter Waybill Reference")
    if st.button("Track Now"):
        waybill = WAYBILLS.get(ref)
        if waybill:
            st.success("Shipment Found!")
            st.write(f"**Status:** {waybill['status']}")
            st.write(f"**Origin:** {waybill['details']['origin']}  \n**Destination:** {waybill['details']['destination']}")
            st.write(f"**Goods:** {waybill['details']['goods_type']} ({waybill['details']['qty']} MT)")
            st.write(f"**ETA:** {waybill['eta']}")
            st.write("### Tracking History")
            for t in waybill['tracking']:
                st.write(f"- {t['time']} — {t['status']}")
            if waybill['status'] != "Delivered" and st.button("Simulate Delivery"):
                waybill['status'] = "Delivered"
                waybill['tracking'].append({"status":"Delivered", "time":datetime.datetime.now()})
                st.success("Delivery status updated!")
        else:
            st.error("Waybill not found!")
