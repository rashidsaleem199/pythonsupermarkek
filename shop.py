import streamlit as st
from fpdf import FPDF
from datetime import datetime

# -------------------------------
# PAGE SETTINGS
# -------------------------------

st.set_page_config(page_title="Smart Buy Super Mart", layout="wide", page_icon="🛒")
st.markdown(
    """
    <h1 style='text-align: center; color:#5F9B8C'>🛒 Smart Buy Super Mart</h1>
    <h3 style='text-align: center; color: #A0C382'>www.SmartBuySuperMart.com</h3>
    """,
    unsafe_allow_html=True
)




st.markdown("<hr style='height:2px;border:none;color:#5F9B8C;background-color:#5F9B8C;' />", unsafe_allow_html=True)

# -------------------------------
# SESSION STATE
# -------------------------------
if "products" not in st.session_state:
    st.session_state.products = [
        {"name": "apple", "price": 100, "qty": 50, "image": None},
        {"name": "banana", "price": 50, "qty": 60, "image": None},
        {"name": "milk", "price": 80, "qty": 30, "image": None},
    ]
if "cart" not in st.session_state:
    st.session_state.cart = []
if "total" not in st.session_state:
    st.session_state.total = 0.0

# -------------------------------
# PDF INVOICE FUNCTION
# -------------------------------
def generate_invoice_pdf(cart, total, tax, grand_total):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Smart Buy Super Mart", ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(60, 10, "Product")
    pdf.cell(30, 10, "Qty")
    pdf.cell(40, 10, "Unit Price")
    pdf.cell(40, 10, "Total", ln=True)
    pdf.set_font("Arial", size=11)
    for item in cart:
        pdf.cell(60, 10, item["product"].title())
        pdf.cell(30, 10, str(item["quantity"]))
        pdf.cell(40, 10, str(item["unitprice"]))
        pdf.cell(40, 10, str(item["price"]), ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Total: {total:.2f}", ln=True)
    pdf.cell(0, 10, f"Tax: {tax:.2f}", ln=True)
    pdf.cell(0, 10, f"Grand Total: {grand_total:.2f}", ln=True)
    return pdf.output(dest="S").encode("latin-1")

# -------------------------------
# SIDEBAR NAVIGATION
# -------------------------------
st.sidebar.markdown("<h2 style='color: #A0C382;'>📌 Navigation</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio(
    "Select Section",
    ["🏠 Dashboard", "🛍 Shopping", "📄 Invoice", "🧹 Reset"]
)

# -------------------------------
# DASHBOARD / PRODUCT MANAGEMENT
# -------------------------------
if menu == "🏠 Dashboard":
    st.subheader("🏠 Product Management")
    action = st.radio(
        "Choose Action",
        ["➕ Add Product", "✏️ Update Product", "🗑 Delete Product"],
        horizontal=True
    )

    # ---------------------- ADD PRODUCT ----------------------
    if action == "➕ Add Product":
        col1, col2 = st.columns([0.5, 0.5]) 
        with col1:
          name = st.text_input("Product Name")
        with col1:
          qty = st.number_input("Quantity", min_value=0)
        with col1:
           price = st.number_input("Price", min_value=0.0)
        with col1:
          image = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

        if st.button("Add Product"):
            if name and price > 0 and qty > 0:
                st.session_state.products.append({
                    "name": name.lower(),
                    "price": price,
                    "qty": qty,
                    "image": image.read() if image else None
                })
                st.success(f"✅ '{name}' Added Successfully")
            else:
                st.warning("⚠ Fill all fields")

    # ---------------------- UPDATE PRODUCT ----------------------
    elif action == "✏️ Update Product":
        product_names = [p["name"] for p in st.session_state.products]
        if product_names:
            
            
            col1, col2 = st.columns([0.5, 0.5]) 
            with col1:
             selected = st.selectbox("Select Product to Update", product_names)
           
            with col1:
             prod = next(p for p in st.session_state.products if p["name"] == selected)

            # Separate input rows
            col1, col2 = st.columns([0.5, 0.5]) 
            with col1:
              new_name = st.text_input("New Name", prod["name"])
            with col1:
              new_qty = st.number_input("New Quantity", value=prod["qty"])
            with col1:
              new_price = st.number_input("New Price", value=prod["price"])
            with col1:
              new_image = st.file_uploader("Update Image", type=["jpg", "png", "jpeg"])
            with col1:
             if st.button("Update Product"):
                col1, col2 = st.columns([0.5, 0.5]) 
                with col1:
                 prod["name"] = new_name.lower()
                with col1:
                 prod["price"] = new_price
                 with col1:
                  prod["qty"] = new_qty
                if new_image:
                    prod["image"] = new_image.read()
                st.success(f"✏️ '{new_name}' Updated Successfully")
        else:
            st.info("No products available to update")

    # ---------------------- DELETE PRODUCT ----------------------
    elif action == "🗑 Delete Product":
        
        product_names = [p["name"] for p in st.session_state.products]
        if product_names:
             col1, col2 = st.columns([0.5, 0.5]) 
             with col1:
              delete_name = st.selectbox("Select Product to Delete", product_names)
              if st.button("Delete Product"):
              
                st.session_state.products = [
                    p for p in st.session_state.products if p["name"] != delete_name
                ]
                st.success(f"🗑 '{delete_name}' Deleted Successfully")
        else:
            st.info("No products available to delete")

    # ---------------------- DISPLAY PRODUCTS ----------------------
    st.markdown("---")
    st.subheader("📦 All Products")
    products = st.session_state.products

    # Show 3 products per row
    for i in range(0, len(products), 3):
        cols = st.columns(3)
        for j, product in enumerate(products[i:i+3]):
            with cols[j]:
                st.markdown(f"### {product['name'].title()}")
                st.markdown(f"**Price:** ₹{product['price']}")
                st.markdown(f"**Stock:** {product['qty']}")
                if product["image"]:
                    st.image(product["image"], width=150)


# -------------------------------
# SHOPPING DASHBOARD
# -------------------------------
elif menu == "🛍 Shopping":
    st.subheader("🛍 Shopping Dashboard")
    products = st.session_state.products

    # 3 products per row
    for i in range(0, len(products), 3):
        cols = st.columns(3)
        for j, product in enumerate(products[i:i+3]):
            with cols[j]:
                st.markdown(f"### {product['name'].title()}")
                st.markdown(f"**Price:** ₹{product['price']}")
                st.markdown(f"**Stock:** {product['qty']}")
                if product["image"]:
                    st.image(product["image"], width=150)
                qty = st.number_input(
                    f"Qty ({product['name']})", 
                    min_value=1, 
                    max_value=int(product['qty']), 
                    key=f"shop_qty_{product['name']}"
                )
                if st.button(f"Add to Cart ({product['name']})", key=f"shop_cart_{product['name']}"):
                    if qty <= product['qty']:
                        amount = product['price'] * qty
                        product['qty'] -= qty
                        st.session_state.total += amount
                        st.session_state.cart.append({
                            "product": product['name'],
                            "quantity": qty,
                            "unitprice": product['price'],
                            "price": amount
                        })
                        st.success(f"🟢 '{product['name']}' Added to Cart!")
                    else:
                        st.error("❌ Invalid quantity")

    st.markdown("---")
    st.subheader("🛒 Cart Summary")
    if not st.session_state.cart:
        st.info("Cart is empty")
    else:
        for item in st.session_state.cart:
            st.markdown(
                f"- **{item['product'].title()}** | Qty: {item['quantity']} | "
                f"Unit: ₹{item['unitprice']} | Total: ₹{item['price']}"
            )

# -------------------------------
# INVOICE PAGE
# -------------------------------
elif menu == "📄 Invoice":
    st.subheader("📄 Invoice")
    
    if not st.session_state.cart:
        st.info("Cart is empty")
    else:
        for item in st.session_state.cart:
            st.markdown(f"- **{item['product'].title()}** | Qty: {item['quantity']} | Unit: ₹{item['unitprice']} | Total: ₹{item['price']}")
        total = st.session_state.total
        tax = total * 0.20 if total >= 1000 else 0
        grand_total = total + tax
        st.markdown(f"### 💵 Total: ₹{total:.2f}")
        st.markdown(f"### 🧮 Tax : ₹{tax:.2f}")
        st.markdown(f"## 🟩 Grand Total: ₹{grand_total:.2f}")
        pdf_data = generate_invoice_pdf(st.session_state.cart, total, tax, grand_total)
        st.download_button("⬇️ Download Invoice (PDF)", data=pdf_data, file_name="invoice.pdf", mime="application/pdf")
        st.divider()
# -------------------------------
# RESET SYSTEM
# -------------------------------
elif menu == "🧹 Reset":
    if st.button("RESET SYSTEM"):
        st.session_state.cart = []
        st.session_state.total = 0.0
        st.success("🧹 System Reset Successfully")
