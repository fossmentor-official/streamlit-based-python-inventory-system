import streamlit as st
from inventory_system import InventorySystem
from user import User

def login_screen():
    st.title("Login")
    user_manager = User()  # Assuming User class handles login verification

    # Login form with automatic submission on Enter
    with st.form(key="login_form"):
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        login_button = st.form_submit_button("Login")  # Submit button for form

        if login_button:
            role = user_manager.verify_login(username, password)
            if role:
                # Set session state and query parameters on successful login
                st.session_state.logged_in = True
                st.session_state.role = role
                
                # Update query param and refresh page to apply session state
                st.query_params = {"logged_in": "true"}  # Update query param for reload
                st.success(f"Welcome, {username}!")
                st.rerun()  # Rerun to apply changes and refresh page with session state

            else:
                st.error("Invalid credentials")

def check_session_status():
    # Check query params on initial page load if 'logged_in' session state is not set
    if "logged_in" in st.query_params and st.query_params["logged_in"] == "true":
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = True
            st.session_state.role = st.session_state.get("role", "user")
    else:
        st.session_state.logged_in = False

def display_sidebar(role):
    st.sidebar.title("Inventory System")
    # Button to Home
    if st.sidebar.button("Home"):
        st.session_state.page = "home"

    if role == "admin":
        #st.sidebar.write("Admin Options:")

        # Button to Manage Products
        if st.sidebar.button("Manage Products"):
            st.session_state.page = "product_management"

        # Button to Manage Users
        if st.sidebar.button("Manage Users"):
            st.session_state.page = "user_management"

        # Button to Manage Role & Permissions
        if st.sidebar.button("Role Permissions"):
            st.session_state.page = "role_permission_management"
    else:
        if st.sidebar.button("View Products"):
            st.session_state.page = "product_management"

def display_modules():
    
    if 'page' not in st.session_state:
        st.session_state.page = "home" 

    # Initialize the inventory system
    inventory_system = InventorySystem()

    if st.session_state.page == "home":
        inventory_system.display_home()  # Display the Dashboard Page
    elif st.session_state.page == "view_product":
        inventory_system.display_product_management()  # Display the Product List
    elif st.session_state.page == "add_product":
        inventory_system.display_add_product_form()  # Display the Add Product form
    elif st.session_state.page == "update_product":
        inventory_system.display_update_product_form()  # Display the Update Product form
    elif st.session_state.page == "product_management":
        inventory_system.display_product_management()  # Display Product List
    elif st.session_state.page == "add_user":
        inventory_system.display_add_user_form()  # Display Add User form
    elif st.session_state.page == "update_user":
        inventory_system.display_update_user_form()  # Display Update User form
    elif st.session_state.page == "user_management":
        inventory_system.display_user_management()  # Display User List
    elif st.session_state.page == "role_permission_management":
        inventory_system.display_role_permission_management()  # Display Role & Permission Management
    elif st.session_state.page == "add_role":
        inventory_system.display_add_role_form()
    elif st.session_state.page == "update_role":
        inventory_system.display_update_role_form()
        
def main():

    # Run the display based on the current page
    if "logged_in" not in st.session_state:
        check_session_status()  # Initialize session state based on query params

    if st.session_state.logged_in:
        role = st.session_state.get("role", "user")
        # Show menus sidebar
        display_sidebar(role)

        # Optional logout button to clear session and reset query params
        if st.button("Logout"):
            st.session_state.clear()  # Clear session state on logout
            st.query_params = {}  # Clear query parameters
            st.rerun()
        
        # Display modules based on condition
        display_modules()
        
    else:
        login_screen()

# Main execution start here...        
main()