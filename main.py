import streamlit as st

def main():
    st.set_page_config(page_title="Smart Bin Validator", page_icon=":package:")
    st.title(":package: Smart Bin Validator")

    if "item_index" not in st.session_state:
        st.session_state["item_index"] = 0

    if "items" not in st.session_state:
        st.session_state["items"] = []

    main_col1, main_col2 = st.columns(
        [4, 5], 
        gap="large", 
        vertical_alignment="top"
    )

    with main_col1:
            bin_img = st.file_uploader("1 . Upload Bin Image", type=["jpg"])
            if bin_img:
                st.image(bin_img, caption="Uploaded Bin Image")
                if st.button("Process Bin"):
                    st.success("Bin validated successfully!")
            
            st.divider()

            n_items = st.number_input(
                "2 . Number of Unique Items in Bin",
                min_value=1,
                max_value=20,
                value=1,
                key="total_items"
            )
    
    with main_col2:
        i = st.session_state["item_index"]
        st.write(f"3 . Metadata for Item {i + 1} of {n_items}")

        asin = st.text_input("ASIN", key=f"asin_{i}", help="Amazon Standard Identification Number")
        height = st.number_input("Height (in Inches)", min_value=0.0, key=f"height_{i}")
        length = st.number_input("Length (in Inches)", min_value=0.0, key=f"length_{i}")
        width = st.number_input("Width (in Inches)", min_value=0.0, key=f"width_{i}")
        weight = st.number_input("Weight (in Pounds)", min_value=0.0, key=f"weight_{i}")
        quantity = st.number_input("Quantity of this Item in Bin", min_value=1, max_value=100, value=1, key=f"qty_{i}")

        col1, col2 = st.columns(2)
        with col1:
            save_next = st.button("💾 Save & Next", use_container_width=True)

        with col2:
            reset_form = st.button("🔁 Reset Form", use_container_width=True)

        if save_next:
            item_data = {
                "item_number": i + 1,
                "asin": asin,
                "height": height,
                "length": length,
                "width": width,
                "weight": weight,
                "quantity": quantity
            }

            st.session_state["items"].append(item_data)

            # Move to next item or finish
            if st.session_state["item_index"] + 1 < n_items:
                st.session_state["item_index"] += 1
                st.rerun()
            else:
                st.success("✅ All items submitted!")
                st.write("### Collected Metadata:")
                st.json(st.session_state["items"])

        if reset_form:
            st.session_state["item_index"] = 0
            st.session_state["items"] = []
            st.rerun()

if __name__ == "__main__":
    main()
