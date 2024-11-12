
### Project Title:

**Inventory Management System (IMS)**

### Objective:

A basci gui-based system that manages inventory for a small business. The system allow admins to create, update, view, and delete products in the inventory while keeping track of stock levels and handling multiple users with role-based permissions.

### Main Features:

1. **User Authentication and Role Management**

   - Support different roles like “Admin” and “User.”
   - Admins can add, edit, and delete products, whereas Users can only view inventory details.
   - Implement a basic login system with username and password validation.

2. **Product Management**

   - List of all products.
   - CRUD operations including filters based search.

3. **User Management**

   - List of all users.
   - CRUD operations including filters based search.

## Instructions
- This project is used `Docker` for `containarization` feature. So, these steps must follow:

<h2> Step-1: Download docker (Mac/Window/Linux) if you don't have before:  </h2>
<code> https://docs.docker.com/desktop/</code>

<h2> Step-2: Create a docker image:  </h2>
<code> docker build -t inventory-system</code>

<h2> Step-3: Run docker image in container: </h2>
<code> docker run -it inventory-system</code>

<h2> Step-4: Once, container is started successfully then move into the project directory and execute the following command:</h2>
<code> streamlit run main.py</code>

<p>A url like http://localhost:8501 show in your terminal. Just open it into your browser. </p>

<h2>Project Snapshots</h2>

<h3>Login Screen</h3>
<div align="center">

![Login Screen](/static/img/screenshots/Login-page.png)

</div>

<h3>Dashboard</h3>
<div align="center">

![Login Screen](/static/img/screenshots/Dashboard-page.png)
</div>

<h3>Product Management</h3>
<div align="center">

![Login Screen](/static/img/screenshots/Product-management.png)
</div>

<h3>Add Product</h3>
<div align="center">

![Login Screen](/static/img/screenshots/Add-product.png)
</div>

<h3>Update Product</h3>
<div align="center">

![Login Screen](/static/img/screenshots/update-product.png)
</div>

<h3>User Management</h3>
<div align="center">

![Login Screen](/static/img/screenshots/User-management.png)
</div>

<h3>Add User</h3>
<div align="center">

![Login Screen](/static/img/screenshots/Add-user.png)
</div>

<h3>Update User</h3>
<div align="center">

![Login Screen](/static/img/screenshots/Update-user.png)
</div>

<h3>Role & Permission</h3>
<div align="center">

![Login Screen](/static/img/screenshots/Roles-permission.png)
</div>