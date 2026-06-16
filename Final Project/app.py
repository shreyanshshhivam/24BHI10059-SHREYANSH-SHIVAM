import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Stock Management System", layout="wide")

API_URL = "http://127.0.0.1:8000/products/"

st.title("Stock Management Dashboard")

def fetch_products():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json().get("inventory", [])
        return []
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the backend API. Please ensure FastAPI is running.")
        return []

tab1, tab2, tab3 = st.tabs(["Inventory Dashboard", "Add New Product", "Manage Stock"])

with tab1:
    st.header("Current Inventory")
    products = fetch_products()
    
    if products:
        df = pd.DataFrame(products)
        df = df[["sku", "name", "category", "price", "quantity", "last_updated"]]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No products found or database is empty.")

with tab2:
    st.header("Add a New Product")
    
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            sku = st.text_input("SKU (e.g., LAP-001)")
            name = st.text_input("Product Name")
            category = st.text_input("Category")
        with col2:
            price = st.number_input("Price ($)", min_value=0.0, format="%.2f")
            quantity = st.number_input("Initial Quantity", min_value=0, step=1)
        
        submitted = st.form_submit_button("Save Product")
        
        if submitted:
            payload = {
                "sku": sku,
                "name": name,
                "category": category,
                "price": price,
                "quantity": quantity
            }
            res = requests.post(API_URL, json=payload)
            if res.status_code == 201:
                st.success(f"Product '{name}' added successfully! Go to the Dashboard to see it.")
            else:
                st.error(f"Error: {res.json().get('detail', 'Unknown error')}")

with tab3:
    st.header("Update or Delete Items")
    products = fetch_products()
    
    if products:
        sku_list = [p["sku"] for p in products]
        selected_sku = st.selectbox("Select Product by SKU", sku_list)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Update Stock Quantity")
            qty_change = st.number_input("Quantity Change (+ to add, - to remove)", step=1, value=0)
            
            if st.button("Update Stock"):
                if qty_change != 0:
                    res = requests.patch(f"{API_URL}{selected_sku}/stock", json={"quantity_change": qty_change})
                    if res.status_code == 200:
                        st.success("Stock updated successfully!")
                    else:
                        st.error(f"Error: {res.json().get('detail')}")
                else:
                    st.warning("Quantity change must be a number other than 0.")
        
        with col2:
            st.subheader("Delete Product")
            st.warning("Warning: This action permanently deletes the item from the database.")
            
            if st.button("Delete Item", type="primary"):
                res = requests.delete(f"{API_URL}{selected_sku}")
                if res.status_code == 200:
                    st.success("Product deleted successfully!")
                else:
                    st.error("Failed to delete product.")
    else:
        st.info("No products available to manage.")