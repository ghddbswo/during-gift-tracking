import streamlit as st
import pandas as pd
from urllib.parse import quote

st.set_page_config(page_title="듀링 설선물 배송조회", page_icon="🎁")

st.title("🎁 듀링 설선물 배송조회")

df = pd.read_excel("gift_tracking_db.xlsx")
df.columns = [str(c).strip() for c in df.columns]

name = st.text_input("이름을 입력하세요")
phone4 = st.text_input("휴대폰 뒤 4자리를 입력하세요", max_chars=4)


def build_tracking_link(carrier, invoice):
    carrier = str(carrier).strip()
    invoice = str(invoice).strip()

    if "우체국" in carrier:
        return f"https://service.epost.go.kr/trace.RetrieveDomRigiTraceList.comm?sid1={quote(invoice)}"

    if "롯데" in carrier:
        return "https://www.lotteglogis.com/home/reservation/tracking/index"

    if "CJ" in carrier or "대한통운" in carrier:
        return "https://www.cjlogistics.com/ko/tool/parcel/tracking"

    if "한진" in carrier:
        return "https://www.hanjin.com/kor/CMS/DeliveryMgr/WaybillSch.do"

    return None


if st.button("배송조회"):

    df["휴대폰"] = df["휴대폰"].astype(str).str.strip()

    result = df[
        (df["이름"].astype(str).str.strip() == name.strip()) &
        (df["휴대폰"].str[-4:] == phone4.strip())
    ]

    if len(result) == 0:
        st.error("일치하는 정보가 없습니다.")
    else:
        for _, row in result.iterrows():

            item = row["품목"]
            carrier = row["택배사"]
            invoice = row["송장번호"]

            st.success(f"{item} 조회 결과")
            st.write(f"택배사: {carrier}")
            st.write(f"송장번호: {invoice}")

            link = build_tracking_link(carrier, invoice)

            if link:
                st.link_button("🚚 배송조회 바로가기", link)
                st.caption("링크를 눌러 송장번호로 배송 상태를 확인하세요.")


