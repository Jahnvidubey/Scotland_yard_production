import streamlit as st
import pandas as pd

# Function to display client information
def display_client_info(client_data):
    st.write(f"**Client Name:** {client_data['First Name']} {client_data['Last Name']}")
    st.write(f"**Contact Number:** {client_data['Contact Number']}")
    st.write(f"**Wedding Date:** {client_data['Wedding Date']}")
    st.write(f"**Wedding Venue:** {client_data['Wedding Vanue']}")
    st.write(f"**Function Number of Days:** {client_data['Function Number of days']}")
    st.write(f"**Functions:** {client_data['Functions']}")
    st.write(f"**Photography Services:** {client_data['Photography Services']}")
    st.write(f"**Special Request:** {client_data['Any Special Request or notes (optional)']}")

# Function to generate the message
def generate_message(client_data, prices):
    first_name = client_data['First Name']
    last_name = client_data['Last Name']
    wedding_date = client_data['Wedding Date']
    venue = client_data['Wedding Vanue']
    days = client_data['Function Number of days']
    services = client_data['Photography Services'].split(', ')

    final_price = prices['total_price'] * days

    message = f"""
    Cinematic Wedding Package

    Dear {first_name} {last_name},

    Your {days} days wedding photography package will be ₹{final_price}/- INR Only!

    This is full wedding photography coverage for {days} days at {venue} with a team of 4-5 members.

    Note -

    1. Client has to take care of food and accommodation.
    2. Our travel charges for your wedding are included in the package!
    3. There will be 4-5 team members.

    This includes -

    {', '.join(services)}

    Deliverables -

    1. All raw data will be provided. There's no photo limit for raw data. ️
    2. Professional editing (colour correction and colour grading) on all selected pictures for Photobook. ️
    3. Cinematic wedding highlight video of 4-5 minutes + 1 teaser of 30 sec - 1 minute. (Timeline depends on video data). ️️
    4. Full HD traditional video of 2-3 hours. (Timeline depends on video data). ️️
    5. 1 Premium luxury photobook of 45-50 (12×36 inch big size) sheets with leather printed cover and box.
    6. 1 WhatsApp wedding invitation video. ️

    Note - Client satisfaction is a must for us and we are very particular with our words!

    T&C Apply

    https://www.instagram.com/indoreweddingphotographer?igsh=Y25nbGR0NzE5a204
    """
    return message

# Streamlit App
st.title("Scotland Yard Productions Client Manager")

# Upload Excel file
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file:
    data = pd.read_excel(uploaded_file)
    st.success("File uploaded successfully!")
    
    # Normalize contact numbers by converting them to strings and stripping whitespace
    data['Contact Number'] = data['Contact Number'].astype(str).str.strip()
    
    # Display all client data
    st.write("## All Clients")
    st.dataframe(data)

    # Input to find client by phone number
    phone_number = st.text_input("Enter client's contact number to search:").strip()
    if phone_number:
        # Normalize the input phone number
        phone_number = phone_number.strip()
        
        client_data = data[data['Contact Number'] == phone_number]
        if client_data.empty:
            st.error("Client not found.")
        else:
            client_data = client_data.iloc[0]  # Assuming unique phone numbers
            display_client_info(client_data)

            # Get prices from user input
            st.write("### Enter Service Prices")
            prices = {}
            prices['candid_photography'] = st.number_input("Candid Photography Price:", min_value=0, value=0)
            prices['cinematography'] = st.number_input("Cinematography Price:", min_value=0, value=0)
            prices['traditional_photography'] = st.number_input("Traditional Photography Price:", min_value=0, value=0)
            prices['traditional_videography'] = st.number_input("Traditional Videography Price:", min_value=0, value=0)
            prices['drone_shooting'] = st.number_input("Drone Shooting Price:", min_value=0, value=0)

            prices['total_price'] = sum(prices.values())

            if st.button("Generate Wedding Package Message"):
                message = generate_message(client_data, prices)
                st.text_area("Generated Message", message, height=400)

                # Option to download the message as a text file
                file_name = f"{client_data['First Name'].replace(' ', '_')}_{client_data['Last Name'].replace(' ', '_')}_{client_data['Wedding Date'].strftime('%Y-%m-%d')}_wedding_package.txt"
                st.download_button(
                    label="Download Message as Text File",
                    data=message,
                    file_name=file_name,
                    mime="text/plain"
                )
