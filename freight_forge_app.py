import streamlit as st
import random
import string
import datetime
import pandas as pd
import os
import csv
import ast  # For safely evaluating the string representation of a dictionary
import json

# File paths for CSV storage
USERS_CSV = "data\\users.csv"
PENDING_USERS_CSV = "data\\pending_users.csv"
SHIPMENTS_CSV = "data\\shipments.csv"
WAYBILLS_CSV = "data\\waybills.csv"

# Function to load data from CSV or initialize if not exists
def load_data_from_csv(file_path, default_dict=None):
    if default_dict is None:
        default_dict = {}

    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            # Convert DataFrame to dictionary
            result_dict = {}
            for _, row in df.iterrows():
                key = row['username']  # Assuming 'username' is the key
                # Convert row to dict and remove the key column
                row_dict = row.to_dict()
                # Handle document bytes (stored as string in CSV)
                if 'doc' in row_dict:
                    row_dict['doc'] = row_dict['doc'].encode() if isinstance(row_dict['doc'], str) else b''
                result_dict[key] = row_dict
            return result_dict
        except Exception as e:
            st.error(f"Error loading {file_path}: {e}")
            return default_dict
    else:
        return default_dict

# Function to save data to CSV
def save_data_to_csv(data_dict, file_path):
    try:
        # Convert dictionary to DataFrame
        if data_dict:
            # Create list of dictionaries for DataFrame
            rows = []
            for key, value in data_dict.items():
                row = value.copy()
                # Handle document bytes (convert to string for CSV)
                if 'doc' in row:
                    row['doc'] = str(row['doc'])
                rows.append(row)

            df = pd.DataFrame(rows)
            df.to_csv(file_path, index=False)
    except Exception as e:
        st.error(f"Error saving to {file_path}: {e}")

# Load data from CSV files
USERS = load_data_from_csv(USERS_CSV)
PENDING_USERS = load_data_from_csv(PENDING_USERS_CSV)
SHIPMENTS = load_data_from_csv(SHIPMENTS_CSV, {})
WAYBILLS = load_data_from_csv(WAYBILLS_CSV, {})

# Initialize default admin if not exists
if 'admin' not in USERS:
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
    # Save updated users to CSV
    save_data_to_csv(USERS, USERS_CSV)

# Initialize default customers if not in pending users
if 'Customer1' not in PENDING_USERS and 'Customer1' not in USERS:
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
    # Save updated pending users to CSV
    save_data_to_csv(PENDING_USERS, PENDING_USERS_CSV)

if 'Customer2' not in PENDING_USERS and 'Customer2' not in USERS:
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
    # Save updated pending users to CSV
    save_data_to_csv(PENDING_USERS, PENDING_USERS_CSV)

# Function to create a default waybill
def create_default_waybill(username, goods_type, qty, origin, destination, option, charge, days_ago=2):
    booking_date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
    eta = booking_date + datetime.timedelta(hours=20)

    # Create a unique reference
    ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    # Create booking details
    booking_details = {
        "username": username,
        "goods_type": goods_type,
        "qty": qty,
        "origin": origin,
        "destination": destination,
        "dispatch_date": str(booking_date.date()),
        "option": option,
        "charge": charge,
        "status": "In Transit",
        "booked_on": str(booking_date)
    }

    # Create waybill
    waybill = {
        "username": booking_details["username"],
        "waybill_ref": ref,
        "details": booking_details,
        "tracking": [
            {"status": "Booking Confirmed", "time": booking_date},
            {"status": "In Transit", "time": booking_date + datetime.timedelta(hours=4)},
            {"status": "Arriving", "time": eta}
        ],
        "status": "In Transit",
        "eta": eta
    }

    return ref, booking_details, waybill

# Add default shipments and waybills if they don't exist yet
if len(SHIPMENTS) == 0 and len(WAYBILLS) == 0:
    # For Customer1 - Create two shipments
    # Shipment 1 - In Transit
    ref1, booking1, waybill1 = create_default_waybill(
        username="Customer1",
        goods_type="Wheat",
        qty=450,
        origin="Quebec, QC",
        destination="Windsor, ON",
        option="Train A (Covered Hopper x25, departs 09:00)",
        charge=4455.0,
        days_ago=2
    )
    SHIPMENTS[ref1] = booking1
    WAYBILLS[ref1] = waybill1

    # Shipment 2 - Delivered
    ref2, booking2, waybill2 = create_default_waybill(
        username="Customer1",
        goods_type="Corn",
        qty=300,
        origin="Montreal, QC",
        destination="Toronto, ON",
        option="Train B (Boxcar x22, departs 14:00)",
        charge=2970.0,
        days_ago=5
    )
    # Mark as delivered
    booking2["status"] = "Delivered"
    waybill2["status"] = "Delivered"
    waybill2["tracking"].append({
        "status": "Delivered", 
        "time": datetime.datetime.now() - datetime.timedelta(days=3)
    })
    SHIPMENTS[ref2] = booking2
    WAYBILLS[ref2] = waybill2

    # For Customer2 - Create one shipment
    ref3, booking3, waybill3 = create_default_waybill(
        username="Customer2",
        goods_type="Soybean",
        qty=550,
        origin="Ottawa, ON",
        destination="Hamilton, ON",
        option="Train C (Bulk Grain Car x30, departs 19:00)",
        charge=3850.0,
        days_ago=1
    )
    SHIPMENTS[ref3] = booking3
    WAYBILLS[ref3] = waybill3

    # Save to CSV files
    save_data_to_csv(SHIPMENTS, SHIPMENTS_CSV)
    save_data_to_csv(WAYBILLS, WAYBILLS_CSV)

    # Print the waybill references for demo purposes
    print(f"Created default waybills with references: {ref1}, {ref2}, {ref3}")

    
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
                    # Save to CSV
                    save_data_to_csv(PENDING_USERS, PENDING_USERS_CSV)
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
                            # Save changes to CSV files
                            save_data_to_csv(USERS, USERS_CSV)
                            save_data_to_csv(PENDING_USERS, PENDING_USERS_CSV)
                            st.success(f"User {uname} approved and can now log in.")
                            # Force a rerun to update the UI
                            st.rerun()

                    with col2:
                        if st.button(f"Reject {uname}", key=f"reject_{uname}"):
                            # Remove from PENDING_USERS
                            del PENDING_USERS[uname]
                            # Save changes to CSV
                            save_data_to_csv(PENDING_USERS, PENDING_USERS_CSV)
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

        # Show user's existing shipments
        st.subheader("Your Recent Shipments")
        user_shipments = {ref: ship for ref, ship in SHIPMENTS.items() if ship['username'] == user['username']}

        if user_shipments:
            for ref, shipment in user_shipments.items():
                waybill = WAYBILLS.get(ref)
                status = waybill['status'] if waybill else shipment['status']
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.write(f"**{shipment['goods_type']}** ({shipment['qty']} MT)")
                with col2:
                    st.write(f"{shipment['origin']} → {shipment['destination']}")
                with col3:
                    st.write(f"Status: {status}")
                with col4:
                    st.write(f"Waybill: `{ref}`")
        else:
            st.info("You have no existing shipments. Book your first shipment below!")

        st.markdown("---")
        st.write("Book new wheat shipment from Origin City to Destination City")
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

# Function to find shipment by waybill reference
def find_shipment(waybill_ref):
    try:
        with open(WAYBILLS_CSV, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['waybill_ref'] == waybill_ref:
                    # Debug: Print the raw details string
                    st.write("Raw details string:", row['details'])

                    # Try to parse the details string into a dictionary
                    details = {}
                    try:
                        # First try ast.literal_eval
                        details = ast.literal_eval(row['details'])
                    except (SyntaxError, ValueError) as e:
                        st.warning(f"Could not parse details with ast: {e}")
                        try:
                            # Fall back to json.loads
                            details = json.loads(row['details'])
                        except json.JSONDecodeError as e:
                            st.error(f"Could not parse details with json: {e}")
                            # As a last resort, try to extract key information using string manipulation
                            details_str = row['details']
                            # Extract origin and destination using simple string parsing
                            origin = "Unknown"
                            destination = "Unknown"
                            goods_type = "Unknown"
                            qty = "Unknown"

                            # Simple extraction from string (very basic)
                            if "'origin':" in details_str:
                                origin = details_str.split("'origin':")[1].split(",")[0].strip().strip("'\"")
                            if "'destination':" in details_str:
                                destination = details_str.split("'destination':")[1].split(",")[0].strip().strip("'\"")
                            if "'goods_type':" in details_str:
                                goods_type = details_str.split("'goods_type':")[1].split(",")[0].strip().strip("'\"")
                            if "'qty':" in details_str:
                                qty = details_str.split("'qty':")[1].split(",")[0].strip().strip("'\"")

                            details = {
                                'origin': origin,
                                'destination': destination,
                                'goods_type': goods_type,
                                'qty': qty
                            }

                    # Parse tracking data if available
                    tracking = []
                    if 'tracking' in row:
                        try:
                            tracking = ast.literal_eval(row['tracking'])
                        except:
                            try:
                                tracking = json.loads(row['tracking'])
                            except:
                                tracking = []

                    return {
                        'waybill_ref': row['waybill_ref'],
                        'status': row.get('status', 'Unknown'),
                        'details': details,
                        'tracking': tracking,
                        'eta': row.get('eta', 'Unknown'),
                        'origin': details.get('origin', 'Unknown'),
                        'destination': details.get('destination', 'Unknown'),
                        'goods_type': details.get('goods_type', 'Unknown'),
                        'qty': details.get('qty', 'Unknown')
                    }
    except Exception as e:
        st.error(f"Error finding shipment: {e}")
        import traceback
        st.error(traceback.format_exc())
    return None

# 4. Track Shipment
if menu == "Track Shipment (Waybill)":
    st.header("Track Shipment by Waybill Reference")

    # Display a few sample waybill references to help users
    if WAYBILLS:
        # Get actual waybill references from the dictionary values
        sample_refs = []
        count = 0
        for key, waybill in WAYBILLS.items():
            if 'waybill_ref' in waybill:
                sample_refs.append(waybill['waybill_ref'])
                count += 1
                if count >= 4:  # Limit to 3 samples
                    break

        if sample_refs:
            st.info(f"Sample waybill references for testing: {', '.join(sample_refs)}")
        else:
            st.info("No sample waybill references available.")
        
    ref = st.text_input("Enter Waybill Reference")
    if st.button("Track Now"):
        # Use the find_shipment function to get shipment details
        waybill = find_shipment(ref)

        if waybill:
            st.success("Shipment Found!")
            st.write(f"**Status:** {waybill['status']}")
            st.write(f"**Origin:** {waybill['origin']}  \n**Destination:** {waybill['destination']}")
            st.write(f"**Goods:** {waybill['goods_type']} ({waybill['qty']} MT)")

            # Handle ETA display - convert string to datetime if needed
            eta = waybill['eta']
            if isinstance(eta, str):
                try:
                    eta = datetime.datetime.fromisoformat(eta)
                except:
                    # If parsing fails, just use the string
                    pass
            st.write(f"**ETA:** {eta}")

            st.write("### Tracking History")
            tracking = waybill.get('tracking', [])
            if not tracking:
                st.write("No tracking information available.")
            else:
                for t in tracking:
                    # Handle time display - convert string to datetime if needed
                    time = t.get('time', 'Unknown')
                    status = t.get('status', 'Unknown')

                    if isinstance(time, str):
                        try:
                            time = datetime.datetime.fromisoformat(time)
                        except:
                            # If parsing fails, just use the string
                            pass
                    st.write(f"- {time} — {status}")

            # Update shipment status if not delivered
            if waybill['status'] != "Delivered" and st.button("Simulate Delivery"):
                # Get the original waybill from WAYBILLS dictionary
                original_waybill = WAYBILLS.get(ref)
                if original_waybill:
                    original_waybill['status'] = "Delivered"
                    delivery_time = datetime.datetime.now()

                    # Ensure tracking is a list
                    if not isinstance(original_waybill.get('tracking'), list):
                        original_waybill['tracking'] = []

                    original_waybill['tracking'].append({"status": "Delivered", "time": delivery_time})

                    # Also update the corresponding shipment
                    if ref in SHIPMENTS:
                        SHIPMENTS[ref]['status'] = "Delivered"

                    # Save changes to CSV files
                    save_data_to_csv(WAYBILLS, WAYBILLS_CSV)
                    save_data_to_csv(SHIPMENTS, SHIPMENTS_CSV)

                    st.success("Delivery status updated and saved!")
                    st.balloons()

                    # Force refresh to show updated status
                    st.rerun()
                else:
                    st.error("Could not update waybill in database.")
        else:
            st.error("Waybill not found!")