import streamlit as st
import pandas as pd

st.set_page_config(page_title="듀링 설선물 배송조회", page_icon="🎁")

st.title("🎁 듀링 설선물 배송조회")

name = st.text_input("이름을 입력하세요")
phone4 = st.text_input("휴대폰 뒤 4자리를 입력하세요")

if st.button("배송조회"):
    df = pd.read_excel("gift_tracking_db.xlsx")

    result = df[
        (df["이름"] == name) &
        (df["휴대폰"].astype(str).str[-4:] == phone4)
    ]

    if len(result) == 0:
        st.error("일치하는 정보가 없습니다. 다시 확인해주세요.")
    else:
        for _, row in result.iterrows():
            st.success(f"{row['품목']} 조회 결과")
            st.write(f"택배사: {row['택배사']}")
            st.write(f"송장번호: {row['송장번호']}")

            if row["택배사"] == "우체국":
                url = f"https://service.epost.go.kr/trace.RetrieveDomRigiTraceList.comm?displayHeader=N&sid1={row['송장번호']}"
            elif row["택배사"] == "한진":
                url = f"https://www.hanjin.com/kor/CMS/DeliveryMgr/WaybillResult.do?mCode=MN038&schLang=KR&wblnumText2={row['송장번호']}"
            elif row["택배사"] == "CJ":
                url = f"https://trace.cjlogistics.com/next/tracking.html?wblNo={row['송장번호']}"
            elif row["택배사"] == "롯데":
                url = f"https://www.lotteglogis.com/home/reservation/tracking/linkView?InvNo={row['송장번호']}"
            else:
                url = ""

            if url:
                st.link_button("🚚 배송조회 바로가기", url)

