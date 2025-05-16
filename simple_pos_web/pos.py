import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_option_menu import option_menu
income_file = "income.csv"
expense_file = "expense.csv"
water_file = "water.csv"
waterpun_file = "waterpun.csv"
snack_file = "snack.csv"
burger_file = "burger.csv"
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


def clear_income_input(key1,key2):
    st.session_state[key1] = ""
    st.session_state[key2] = 0.0

menu = st.sidebar.selectbox("ตัวเลือก", ["รายรับ", "รายจ่าย","เพิ่มรายการสินค้า", "ดูสรุปยอด"])

if menu == "เพิ่มรายการสินค้า":
    st.subheader("เพิ่มรายการสินค้า")
    item = st.text_input("ชื่อรายการ",key = "input_item")
    price = st.number_input("ราคา", min_value=0,key = "input_price")
    source_type = st.selectbox("ของซื้อหรือของขาย", ["ของซื้อ", "ของขาย"])
    if source_type == "ของขาย":
        tpye_item = st.radio("เลือกหมวดหมู่",["น้ำ","น้ำปั่น","เบอร์เกอร์","ขนม"],horizontal=True,index=None)
        if tpye_item == "น้ำ":
            if st.button("บันทึกรายสินค้า"):
                df = load_stock(water_file)
                df.loc[len(df)] = [item, price]
                save_data(water_file, df)
                st.success("✅ บันทึกสินค้าแล้ว")
        if tpye_item == "น้ำปั่น":
            if st.button("บันทึกรายสินค้า"):
                df = load_stock(waterpun_file)
                df.loc[len(df)] = [item, price]
                save_data(waterpun_file, df)
                st.success("✅ บันทึกสินค้าแล้ว")
        if tpye_item == "เบอร์เกอร์":
            if st.button("บันทึกรายสินค้า"):
                df = load_stock(burger_file)
                df.loc[len(df)] = [item, price]
                save_data(burger_file, df)
                st.success("✅ บันทึกสินค้าแล้ว")
        if tpye_item == "ขนม":
            if st.button("บันทึกรายสินค้า"):
                df = load_stock(snack_file)
                df.loc[len(df)] = [item, price]
                save_data(snack_file, df)
                st.success("✅ บันทึกสินค้าแล้ว")
    if source_type == "ของซื้อ":
        if st.button("บันทึกรายสินค้า"):
            df = load_stock(stock_file)
            df.loc[len(df)] = [item, price]
            save_data(stock_file, df)
            st.success("✅ บันทึกสินค้าแล้ว")
if menu == "รายรับ":
    st.subheader("บันทึกรายรับจากการขายสินค้า")

    tpye_item = st.radio("เลือกหมวดหมู่",["น้ำ","น้ำปั่น","เบอร์เกอร์","ขนม"],horizontal=True)
    if tpye_item == "น้ำ":
        stock_df = load_stock(water_file)
        item_names = stock_df["item"].tolist()
        item = st.selectbox("รายการ",item_names, key="income_item")
        qty = st.number_input("จำนวนที่ซื้อ", min_value=1, key="buy_qty")
        if st.button("บันทึกรายจ่าย"):
            price = stock_df.loc[stock_df["item"] == item, "price"].values[0]
            total = price * qty
            df = load_data(income_file)
            df.loc[len(df)] = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), item, total]
            save_data(income_file, df)
            st.success(f"✅ บันทึกรายจ่าย {item} x {qty} = {total} บาทแล้ว")        
    if tpye_item == "น้ำปั่น":
        stock_df = load_stock(waterpun_file)
        item_names = stock_df["item"].tolist()
        item = st.selectbox("รายการ",item_names, key="income_item")
        qty = st.number_input("จำนวนที่ซื้อ", min_value=1, key="buy_qty")
        if st.button("บันทึกรายจ่าย"):
            price = stock_df.loc[stock_df["item"] == item, "price"].values[0]
            total = price * qty
            df = load_data(income_file)
            df.loc[len(df)] = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), item, total]
            save_data(income_file, df)
            st.success(f"✅ บันทึกรายจ่าย {item} x {qty} = {total} บาทแล้ว")        
    if tpye_item == "เบอร์เกอร์":
        stock_df = load_stock(burger_file)
        item_names = stock_df["item"].tolist()
        item = st.selectbox("รายการ",item_names, key="income_item")
        qty = st.number_input("จำนวนที่ซื้อ", min_value=1, key="buy_qty")
        if st.button("บันทึกรายจ่าย"):
            price = stock_df.loc[stock_df["item"] == item, "price"].values[0]
            total = price * qty
            df = load_data(income_file)
            df.loc[len(df)] = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), item, total]
            save_data(income_file, df)
            st.success(f"✅ บันทึกรายจ่าย {item} x {qty} = {total} บาทแล้ว")        
    if tpye_item == "ขนม":
        stock_df = load_stock(snack_file)
        item_names = stock_df["item"].tolist()
        item = st.selectbox("รายการ",item_names, key="income_item")
        qty = st.number_input("จำนวนที่ซื้อ", min_value=1, key="buy_qty")
        if st.button("บันทึกรายจ่าย"):
            price = stock_df.loc[stock_df["item"] == item, "price"].values[0]
            total = price * qty
            df = load_data(income_file)
            df.loc[len(df)] = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), item, total]
            save_data(income_file, df)
            st.success(f"✅ บันทึกรายจ่าย {item} x {qty} = {total} บาทแล้ว")        


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

    total_income = income_df["amount"].sum()
    total_expense = expense_df["amount"].sum()
    net_profit = total_income - total_expense

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 รายรับทั้งหมด", f"{total_income:,.2f} บาท")
    col2.metric("💸 รายจ่ายทั้งหมด", f"{total_expense:,.2f} บาท")
    col3.metric("📈 กำไรสุทธิ", f"{net_profit:,.2f} บาท", delta=f"{net_profit:,.2f}")



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
    income_df = income_df.reset_index(drop=True)
    income_df.index += 1
    income_df.index.name = "ลำดับ"
    st.write("**รายรับล่าสุด:**")
    st.dataframe(income_df.tail(5).reset_index(drop=True))

    st.write("**รายจ่ายล่าสุด:**")
    expense_df = expense_df.reset_index(drop=True)
    expense_df.index += 1
    expense_df.index.name = "ลำดับ"
    st.dataframe(expense_df.tail(5).reset_index(drop=True))
