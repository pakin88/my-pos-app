import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_option_menu import option_menu
income_file = "income.csv"
expense_file = "expense.csv"
stock_file = "stock.csv"
st.set_page_config(
    page_title="POS รายรับรายจ่าย",   # ชื่อที่จะแสดงในแท็บเบราว์เซอร์
    page_icon="💵",                     # อีโมจิแท็บเว็บ
    layout="centered"                  # หรือ "wide"
)

# โหลดไฟล์ CSV หรือสร้างใหม่ถ้าไม่มี

def load_stock(file):
    try:
        return pd.read_csv(file, encoding='utf-8-sig')
    except FileNotFoundError:
        return pd.DataFrame(columns=[ "item", "price"])    


def load_data(file):
    try:
        return pd.read_csv(file, encoding='utf-8-sig')
    except FileNotFoundError:
        return pd.DataFrame(columns=["date", "item", "amount"])


# บันทึกข้อมูลลง CSV
def save_data(file, df):
    df.to_csv(file, index=False, encoding='utf-8-sig')


col1, col2 = st.columns([5, 10])

with col1:
    st.title("ระบบบันทึกรายรับรายจ่าย")
    menu = st.sidebar = option_menu(
            "เมนูหลัก", 
            ["แดชบอร์ด", "เพิ่มรายการสินค้า", "รายรับ", "รายจ่าย"],
            icons=["speedometer", "plus", "cash-stack", "credit-card"],
            menu_icon="cast", default_index=0
        
    )
with col2:

    if menu == "เพิ่มรายการสินค้า":
        st.subheader("เพิ่มรายการสินค้า")
        item = st.text_input("ชื่อรายการ",key = "input_item")
        price = st.number_input("ราคา", min_value=0,key = "input_price")
        if st.button("บันทึกรายสินค้า"):
            df = load_stock(stock_file)
            df.loc[len(df)] = [item, price]
            save_data(stock_file, df)
            st.success("✅ บันทึกสินค้าแล้ว")

    if menu == "รายรับ":
        st.subheader("บันทึกรายรับจากการขายสินค้า")

        stock_df = load_stock(stock_file)
        item_names = stock_df["item"].tolist()

        selected_item = st.selectbox("เลือกสินค้า", item_names)
        qty = st.number_input("จำนวนที่ขาย", min_value=1, key="sell_qty")

        if st.button("บันทึกรายรับ"):
            price = stock_df.loc[stock_df["item"] == selected_item, "price"].values[0]
            total = price * qty

            df = load_data(income_file)
            df = df.reset_index(drop=True)
            df.index += 1
            df.index.name = "ลำดับ"
            df.loc[len(df)] = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), selected_item, total]
            save_data(income_file, df)

            st.success(f"✅ บันทึกรายรับ {selected_item} x {qty} = {total} บาทแล้ว")


    if menu == "รายจ่าย":
        st.subheader("บันทึกรายจ่ายจากการซื้อสินค้า")

        stock_df = load_stock(stock_file)
        item_names = stock_df["item"].tolist()

        selected_item = st.selectbox("เลือกสินค้า", item_names, key="expense_item")
        qty = st.number_input("จำนวนที่ซื้อ", min_value=1, key="buy_qty")

        if st.button("บันทึกรายจ่าย"):
            price = stock_df.loc[stock_df["item"] == selected_item, "price"].values[0]
            total = price * qty

            df = load_data(expense_file)

            df.loc[len(df)] = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), selected_item, total]
            save_data(expense_file, df)

            st.success(f"✅ บันทึกรายจ่าย {selected_item} x {qty} = {total} บาทแล้ว")

    if menu == "ดูสรุปยอด":
        st.subheader("📊 สรุปรายรับรายจ่าย")


        income_df = load_data(income_file)
        expense_df = load_data(expense_file)

        total_income = income_df["amount"].sum()
        total_expense = expense_df["amount"].sum()

        st.metric("รายรับรวม", f"{total_income:,.2f} บาท")
        st.metric("รายจ่ายรวม", f"{total_expense:,.2f} บาท")
        st.metric("คงเหลือ", f"{total_income - total_expense:,.2f} บาท")

        st.markdown("### 📝 รายการรายรับ")
        income_df = income_df.reset_index(drop=True)
        income_df.index += 1
        income_df.index.name = "ลำดับ"
        st.dataframe(income_df)

        st.markdown("### 📝 รายการรายจ่าย")
        expense_df = expense_df.reset_index(drop=True)
        expense_df.index += 1
        expense_df.index.name = "ลำดับ"
        st.dataframe(expense_df)

    if menu == "แดชบอร์ด":
        st.subheader("📊 ภาพรวมระบบ POS")
        
        income_df = load_data(income_file)
        expense_df = load_data(expense_file)
        stock_df = load_stock(stock_file)

        total_income = income_df["amount"].sum()
        total_expense = expense_df["amount"].sum()
        net_profit = total_income - total_expense

        col1, col2, col3 = st.columns(3)
        col1.metric("💰 รายรับทั้งหมด", f"{total_income:,.2f} บาท")
        col2.metric("💸 รายจ่ายทั้งหมด", f"{total_expense:,.2f} บาท")
        col3.metric("📈 กำไรสุทธิ", f"{net_profit:,.2f} บาท", delta=f"{net_profit:,.2f}")

        st.markdown("### 🛍️ จำนวนรายการสินค้าในคลัง")
        st.write(f"รวม {len(stock_df)} รายการ")

        st.markdown("### 📆 รายรับ-รายจ่ายรายวัน")
        # รวมข้อมูลรายวัน
        income_df["date"] = pd.to_datetime(income_df["date"]).dt.date
        expense_df["date"] = pd.to_datetime(expense_df["date"]).dt.date

        income_daily = income_df.groupby("date")["amount"].sum()
        expense_daily = expense_df.groupby("date")["amount"].sum()

        daily_df = pd.DataFrame({
            "รายรับ": income_daily,
            "รายจ่าย": expense_daily
        }).fillna(0)

        st.line_chart(daily_df)

        st.markdown("### 🧾 รายการล่าสุด")
        st.write("**รายรับล่าสุด:**")
        st.dataframe(income_df.tail(5).reset_index(drop=True))

        st.write("**รายจ่ายล่าสุด:**")
        st.dataframe(expense_df.tail(5).reset_index(drop=True))
