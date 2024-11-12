from product import Product
from user import User
from role_permission import RolePermission
import streamlit as st
import pandas as pd

class InventorySystem:
    def __init__(self):
        self.product_manager = Product()
        self.user_manager = User()
        self.role_permission_manager = RolePermission()

    def validate_fields(self, fields):
        """
        Validates input fields and returns an error message if any field is invalid.
        Each field should be passed as a dictionary with field names as keys.
        
        Parameters:
            fields (dict): A dictionary with keys as field names and values as field values.
            
        Returns:
            str or None: An error message if validation fails; otherwise, None.
        """
        for field, value in fields.items():
            # Check required fields
            if value in [None, '']:  # Checks for None or empty string
                return f"{field.replace('_', ' ').capitalize()} is required."

            # Additional specific field validations
            if field == "price" and value <= 0:
                return "Price must be greater than 0."
            if field == "stock_quantity" and value < 0:
                return "Stock Quantity cannot be negative."
        
        return None  # No errors found

    def display_home(self):
        st.subheader("Welcome to Inventory Management System")

    def display_product_management(self):
        st.subheader("Product Management")

        with st.container():
            # Add Product button at the top-right
            col1, col2 = st.columns([4, 1])
            with col2:
                if st.session_state.get("role", "user") == "admin":
                    if st.button("Add Product", key="add_product_button_main"):
                        st.session_state.page = "add_product"  # Navigate to the add product form

            # Display Filters for Product Table
            filter_column, value_column = st.columns([2, 4])
            with filter_column:
                filter_option = st.selectbox("Search By", ["Product ID", "Product Name", "Category", "Stock Quantity"])
            with value_column:
                filter_value = st.text_input(f"Enter {filter_option}", "")

            filter_button = st.button("Filter Products", key="filter_products_button")
            filtered_data = self.product_manager.products

            if filter_button:
                # Apply filtering based on user input
                if filter_option == "Product ID":
                    filtered_data = [prod for prod in filtered_data if str(filter_value).lower() in str(prod["product_id"]).lower()]
                elif filter_option == "Product Name":
                    filtered_data = [prod for prod in filtered_data if str(filter_value).lower() in str(prod["name"]).lower()]
                elif filter_option == "Category":
                    filtered_data = [prod for prod in filtered_data if str(filter_value).lower() in str(prod["category"]).lower()]
                elif filter_option == "Stock Quantity":
                    try:
                        filter_value_int = int(filter_value)
                        filtered_data = [prod for prod in filtered_data if prod["stock_quantity"] == filter_value_int]
                    except ValueError:
                        st.error("Please enter a valid stock quantity number.")
                        filtered_data = []

            # Display the product list or no data message
            if len(filtered_data) == 0:
                st.write("No products found.")
            else:
                for product in filtered_data:
                    product_row = f"**{product['name']}** - {product['category']} - {product['price']} USD"
                    col1, col2, col3 = st.columns([4, 2, 2])
                    
                    with col1:
                        st.write(product_row)
                    with col2:
                        if st.session_state.get("role", "user") == "admin":
                            if st.button("Update", key=f"update_button_{product['product_id']}"):
                                st.session_state.product_id_to_update = product['product_id']
                                st.session_state.page = "update_product"  # Redirect to update page

                    with col3:
                        if st.session_state.get("role", "user") == "admin":
                            if st.button("Delete", key=f"delete_button_{product['product_id']}"):
                                st.session_state.page = "delete_product"  # Redirect to delete page
                                self.delete_product(product['product_id'])  # Trigger delete function

    def display_add_product_form(self):
        st.subheader("Add New Product")

        with st.form(key='add_product_form_unique'):
            product_id = st.text_input("Product ID", placeholder="Enter Product Id")
            name = st.text_input("Product Name", placeholder="Enter Product Name")
            category = st.text_input("Category", placeholder="Enter Product Category")
            price = st.number_input("Price", min_value=0.01, step=0.01, placeholder="Enter Product Price")
            stock_quantity = st.number_input("Stock Quantity", min_value=0, step=1, placeholder="Enter Product Stock Qty")
            # Add two submit buttons for "Add Product" and "Cancel"
            col1, col2 = st.columns(2)
            with col1:
                add_button = st.form_submit_button(label='Add Product')
            with col2:
                cancel_button = st.form_submit_button(label='Cancel')
                
            if add_button:
                validation_error = self.validate_fields({
                    "product_id": product_id,
                    "name": name,
                    "category": category,
                    "price": price,
                    "stock_quantity": stock_quantity
                })
                # Validate form fields before adding the product
                # validation_error = self.validate_product_fields(product_id, name, category, price, stock_quantity)
                
                if validation_error:
                    st.error(validation_error)
                else:
                    # Add the product to product manager
                    new_product = {
                        "product_id": product_id,
                        "name": name,
                        "category": category,
                        "price": price,
                        "stock_quantity": stock_quantity
                    }
                    self.product_manager.add_product(new_product)
                    st.success(f"Product '{name}' added successfully!")
                    
                    st.session_state.page = "product_management"  # Redirect back to product management
                    st.rerun()  # Triggers the rerun
            elif cancel_button:
                # If "Cancel" button is clicked, go back to the main listing page
                st.session_state.page = "product_management"
                st.rerun()        

    def display_update_product_form(self):
        if st.session_state.product_id_to_update:
            product_id = st.session_state.product_id_to_update
            product = self.product_manager.get_product_by_id(product_id)

            if product:
                st.subheader("Update Product")
                with st.form(key="update_product_form"):
                    name = st.text_input("Product Name", value=product["name"], placeholder="Enter Product Name")
                    category = st.text_input("Category", value=product["category"], placeholder="Enter Product Category")
                    price = st.number_input("Price", min_value=0.01, step=0.01, value=product["price"], placeholder="Enter Product Price")
                    stock_quantity = st.number_input("Stock Quantity", min_value=0, step=1, value=product["stock_quantity"], placeholder="Enter Product Stock Qty")
                    # Add two submit buttons for "Add Product" and "Cancel"
                    col1, col2 = st.columns(2)
                    with col1:
                        update_button = st.form_submit_button(label='Update Product')
                    with col2:
                        cancel_button = st.form_submit_button(label='Cancel')

                    if update_button:
                        validation_error = self.validate_fields({
                            "name": name,
                            "category": category,
                            "price": price,
                            "stock_quantity": stock_quantity
                        })
                        # Validate form fields before adding the product
                        # validation_error = self.validate_product_fields(product_id, name, category, price, stock_quantity)
                        
                        if validation_error:
                            st.error(validation_error)
                        else:

                            if validation_error:
                                st.error(validation_error)
                            else:
                                updated_product = {
                                    "product_id": product_id,
                                    "name": name,
                                    "category": category,
                                    "price": price,
                                    "stock_quantity": stock_quantity
                                }
                                self.product_manager.update_product(product_id, updated_product)
                                st.success(f"Product '{name}' updated successfully!")
                                st.session_state.page = "product_management"  # Redirect back to product management
                                st.rerun()  # Triggers the rerun
                    elif cancel_button:
                        # If "Cancel" button is clicked, go back to the main listing page
                        st.session_state.page = "product_management"
                        st.rerun()  

    def delete_product(self, product_id):
        # This function will show the delete confirmation
        product = self.product_manager.get_product_by_id(product_id)

        if product:
            st.warning(f"Are you sure you want to delete '{product['name']}'?")
            confirm_delete = st.button("Confirm Deletion", key=f"confirm_delete_button_{product_id}")

            # In the delete_product method
            if confirm_delete:
                self.product_manager.delete_product(product_id)
                st.success(f"Product '{product['name']}' deleted successfully!")
                st.session_state.page = "product_management"
                st.rerun()

    def display_user_management(self):
        st.subheader("User Management")

        with st.container():
            # Add User button with a unique key
            col1, col2 = st.columns([4, 1])
            with col2:
                if st.session_state.get("role", "user") == "admin":
                    if st.button("Add User", key="unique_add_user_button"):  # Ensure unique key
                        st.session_state.page = "add_user"  # Navigate to the add user form

            # Display Filters for User Table
            filter_column, value_column = st.columns([2, 4])
            with filter_column:
                filter_option = st.selectbox("Search By", ["User ID", "Username", "Role"])
            with value_column:
                filter_value = st.text_input(f"Enter {filter_option}", "")

            filter_button = st.button("Filter Users", key="filter_users_button")  # Ensure unique key
            filtered_data = self.user_manager.users

            if filter_button:
                # Apply filtering based on user input
                if filter_option == "User ID":
                    filtered_data = [usr for usr in filtered_data if "user_id" in usr and str(filter_value).lower() in str(usr["user_id"]).lower()]
                elif filter_option == "Username":
                    filtered_data = [usr for usr in filtered_data if "username" in usr and str(filter_value).lower() in str(usr["username"]).lower()]
                elif filter_option == "Role":
                    filtered_data = [usr for usr in filtered_data if "role" in usr and str(filter_value).lower() in str(usr["role"]).lower()]

            # Display the user list or no data message
            if len(filtered_data) == 0:
                st.write("No users found.")
            else:
                for idx, user in enumerate(filtered_data):
                    # Check for 'user_id' key to avoid KeyError
                    if "user_id" in user:
                        user_row = f"**{user.get('username', 'Unknown User')}** - {user.get('role', 'No Role')}"
                        col1, col2, col3 = st.columns([4, 2, 2])
                        
                        with col1:
                            st.write(user_row)
                        with col2:
                            if st.session_state.get("role", "user") == "admin":
                                # Ensure unique key for each button in the loop
                                if st.button("Update", key=f"update_user_{user['user_id']}_{idx}"):
                                    st.session_state.user_id_to_update = user['user_id']
                                    st.session_state.page = "update_user"  # Redirect to update page
                        with col3:
                            if st.session_state.get("role", "user") == "admin":
                                # Ensure unique key for each button in the loop
                                if st.button("Delete", key=f"delete_user_{user['user_id']}_{idx}"):
                                    self.delete_user(user['user_id'])
                    else:
                        st.error("User data is missing a 'user_id' field. Please check data consistency.")

    def display_add_user_form(self):
        st.subheader("Add New User")

        with st.form(key='add_user_form'):
            user_id = st.text_input("User ID")
            username = st.text_input("Username")
            role = st.text_input("Role")
            # submit_button = st.form_submit_button(label='Add User')
            # Add two submit buttons for "Add Product" and "Cancel"
            col1, col2 = st.columns(2)
            with col1:
                add_button = st.form_submit_button(label='Add User')
            with col2:
                cancel_button = st.form_submit_button(label='Cancel')

            if add_button:
                # Add the user to user manager
                new_user = {
                    "user_id": user_id,
                    "username": username,
                    "role": role
                }
                self.user_manager.add_user(new_user)
                st.success(f"User '{username}' added successfully!")

                st.session_state.page = "user_management"  # Redirect back to product management
                st.rerun()  # Triggers the rerun
            elif cancel_button:
                # If "Cancel" button is clicked, go back to the main listing page
                st.session_state.page = "product_management"
                st.rerun()

    def display_update_user_form(self):
        if 'user_id_to_update' in st.session_state:
            user_id = st.session_state.user_id_to_update
            user = self.user_manager.get_user_by_id(user_id)

            if user:
                st.subheader("Update User")
                with st.form(key="update_user_form"):
                    username = st.text_input("Username", value=user["username"])
                    role = st.text_input("Role", value=user["role"])
                    submit_button = st.form_submit_button(label="Update User")

                    if submit_button:
                        updated_user = {
                            "user_id": user_id,
                            "username": username,
                            "role": role
                        }
                        self.user_manager.update_user(user_id, updated_user)
                        st.success(f"User '{username}' updated successfully!")
                        st.session_state.page = "user_management"
                        st.rerun()

    def delete_user(self, user_id):
        user = self.user_manager.get_user_by_id(user_id)

        if user:
            st.warning(f"Are you sure you want to delete '{user['username']}'?")
            confirm_delete = st.button("Confirm Deletion", key=f"confirm_delete_user_{user_id}")

            if confirm_delete:
                self.user_manager.delete_user(user_id)
                st.success(f"User '{user['username']}' deleted successfully!")
                st.session_state.page = "user_management"
                #st.rerun()

    def display_role_permission_management(self):
        st.subheader("Role & Permission Management")

        with st.container():
            # Add Role button with a unique key
            col1, col2 = st.columns([4, 1])
            with col2:
                if st.button("Add Role", key="unique_add_role_button"):
                    st.session_state.page = "add_role"  # Navigate to add role form

            # Display Filters for Role Table
            filter_column, value_column = st.columns([2, 4])
            with filter_column:
                filter_option = st.selectbox("Search By", ["Role ID", "Role Name", "Permission Level"])
            with value_column:
                filter_value = st.text_input(f"Enter {filter_option}", "")

            filter_button = st.button("Filter Roles", key="filter_roles_button")
            filtered_data = self.role_permission_manager.roles

            if filter_button:
                # Apply filtering based on user input
                if filter_option == "Role ID":
                    filtered_data = [role for role in filtered_data if "role_id" in role and str(filter_value).lower() in str(role["role_id"]).lower()]
                elif filter_option == "Role Name":
                    filtered_data = [role for role in filtered_data if "name" in role and str(filter_value).lower() in str(role["name"]).lower()]
                elif filter_option == "Permission Level":
                    filtered_data = [role for role in filtered_data if "permission_level" in role and str(filter_value).lower() in str(role["permission_level"]).lower()]

            # Display the role list or no data message
            if len(filtered_data) == 0:
                st.write("No roles found.")
            else:
                for idx, role in enumerate(filtered_data):
                    if "role_id" in role:
                        role_row = f"**{role.get('role_id', 'Unknown ID')}** - {role.get('name', 'Unknown Name')}"
                        col1, col2, col3 = st.columns([4, 2, 2])
                        
                        with col1:
                            st.write(role_row)
                        with col2:
                            if st.button("Update", key=f"update_role_{role['role_id']}_{idx}"):
                                st.session_state.role_id_to_update = role['role_id']
                                st.session_state.page = "update_role"
                        with col3:
                            if st.button("Delete", key=f"delete_role_{role['role_id']}_{idx}"):
                                self.delete_role(role['role_id'])
                    else:
                        st.error("Role data is missing a 'role_id' field. Please check data consistency.")

    def display_add_role_form(self):
        st.subheader("Add New Role")

        with st.form(key='add_role_form'):
            role_id = st.text_input("Role ID")
            name = st.text_input("Role Name")
            permission_level = st.text_input("Permission Level")
            submit_button = st.form_submit_button(label='Add Role')

            if submit_button:
                new_role = {
                    "role_id": role_id,
                    "name": name,
                    "permission_level": permission_level
                }
                self.role_permission_manager.add_role(new_role)
                st.success(f"Role '{name}' added successfully!")

                st.session_state.page = "role_permission_management"
                st.rerun()

    def display_update_role_form(self):
        if 'role_id_to_update' in st.session_state:
            role_id = st.session_state.role_id_to_update
            role = self.role_permission_manager.get_role_by_id(role_id)

            if role:
                st.subheader("Update Role")
                with st.form(key="update_role_form"):
                    name = st.text_input("Role Name", value=role["name"])
                    permission_level = st.text_input("Permission Level", value=role["permission_level"])
                    submit_button = st.form_submit_button(label="Update Role")

                    if submit_button:
                        updated_role = {
                            "role_id": role_id,
                            "name": name,
                            "permission_level": permission_level
                        }
                        self.role_permission_manager.update_role(role_id, updated_role)
                        st.success(f"Role '{name}' updated successfully!")
                        st.session_state.page = "role_permission_management"
                        st.rerun()

    def delete_role(self, role_id):
        role = self.role_permission_manager.get_role_by_id(role_id)

        if role:
            st.warning(f"Are you sure you want to delete '{role['name']}'?")
            confirm_delete = st.button("Confirm Deletion", key=f"confirm_delete_role_{role_id}")

            if confirm_delete:
                self.role_permission_manager.delete_role(role_id)
                st.success(f"Role '{role['name']}' deleted successfully!")
                st.session_state.page = "role_permission_management"
                st.rerun()
        # st.write("Contents of my_list:", st.session_state)
