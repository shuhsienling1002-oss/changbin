import streamlit as st
import random
import urllib.parse
from datetime import datetime, date

# ==========================================
# 1. 系統設定 (Code-CRF v9.0 架構)
# ==========================================
st.set_page_config(
    page_title="2026 長濱鄉雙浪(海浪與稻浪)漫遊系統",
    page_icon="🌊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CSS 美學 (太平洋海岸視覺重構)
# ==========================================
st.markdown("""
    <style>
    /* 1. 強制全站背景為淺海藍色，字體為深色 */
    .stApp {
        background-color: #F0F8FF;
        font-family: "Microsoft JhengHei", sans-serif;
        color: #1A365D !important;
    }
    
    /* 2. 強制輸入框與選單在深色模式下維持白底黑字 */
    div[data-baseweb="select"] > div, 
    div[data-baseweb="input"] > div, 
    div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
        border: 1px solid #90CDF4 !important;
        color: #2D3748 !important;
    }
    input, div[data-baseweb="select"] span, li[data-baseweb="option"] { color: #2D3748 !important; }
    ul[data-baseweb="menu"] { background-color: #ffffff !important; }
    svg { fill: #2B6CB0 !important; color: #2B6CB0 !important; }

    /* 3. 日期選單高亮 (視覺熱點區 CTA) */
    div[data-testid="stDateInput"] > label {
        color: #2C5282 !important; 
        font-size: 20px !important; 
        font-weight: 900 !important;
        margin-bottom: 10px !important;
        display: block;
    }
    div[data-testid="stDateInput"] div[data-baseweb="input"] {
        border: 3px solid #3182CE !important; 
        background-color: #EBF8FF !important;
        border-radius: 10px !important;
        box-shadow: 0 0 10px rgba(49, 130, 206, 0.2); 
    }

    /* 隱藏官方元件 */
    header {visibility: hidden;}
    footer {display: none !important;}
    
    /* 標題區 (湛藍與金黃漸層) */
    .header-box {
        background: linear-gradient(135deg, #2B6CB0 0%, #4FD1C5 100%);
        padding: 30px 20px;
        border-radius: 0 0 30px 30px;
        color: white !important;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(43, 108, 176, 0.4);
        margin-top: -60px;
    }
    .header-box h1, .header-box div, .header-box span { color: white !important; }
    .header-title { font-size: 28px; font-weight: bold; text-shadow: 1px 1px 3px rgba(0,0,0,0.3); }
    
    /* 輸入卡片 */
    .input-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }
    
    /* 按鈕 (高轉換率 CTA) */
    .stButton>button {
        width: 100%;
        background-color: #DD6B20; /* 稻浪橘 */
        color: white !important;
        border-radius: 50px;
        border: none;
        padding: 12px 0;
        font-weight: bold;
        transition: 0.3s;
        font-size: 18px;
        box-shadow: 0 4px 10px rgba(221, 107, 32, 0.3);
    }
    .stButton>button:hover { background-color: #C05621; }
    
    /* 資訊看板 */
    .info-box {
        background-color: #FFFFF0;
        border-left: 5px solid #D69E2E;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    
    /* 時間軸 */
    .timeline-item {
        background: white;
        border-left: 4px solid #3182CE;
        padding: 15px 20px;
        margin-bottom: 20px;
        border-radius: 0 10px 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        position: relative;
    }
    .timeline-item::before {
        content: '🌊';
        position: absolute;
        left: -17px;
        top: 12px;
        background: #F0F8FF;
        border-radius: 50%;
    }
    .day-header {
        background: #EBF8FF;
        color: #2B6CB0 !important;
        padding: 5px 15px;
        border-radius: 15px;
        display: inline-block;
        margin-bottom: 15px;
        font-weight: bold;
    }
    .spot-title { font-weight: bold; color: #2C5282 !important; font-size: 18px; }
    .spot-tag { 
        font-size: 12px; background: #E2E8F0; color: #4A5568 !important; 
        padding: 2px 8px; border-radius: 10px; margin-right: 5px;
    }
    
    /* 連結樣式防禦 */
    a.nav-link {
        color: #2B6CB0 !important;
        text-decoration: none;
        font-weight: bold;
        background: #EBF8FF;
        padding: 2px 8px;
        border-radius: 5px;
        transition: 0.2s;
    }
    a.nav-link:hover { background: #BEE3F8; color: #2C5282 !important; }

    /* 住宿/餐廳卡片 */
    .hotel-card {
        background: white;
        border-left: 5px solid #38B2AC;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 核心資料庫 (加入電話與導航資訊)
# ==========================================
# 輔助函數：生成安全的 Google Maps 搜尋連結
def get_gmap_url(query):
    return f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(query)}"

all_spots_db = [
    # 網美/景觀 
    {"name": "金剛大道", "category": "必訪", "type": "景觀", "time": "上午/下午", "fee": "免門票", "phone": "無", "map": get_gmap_url("台東長濱金剛大道"), "desc": "山海交界的筆直大道，兩側為絕美梯田，隨季節呈現翠綠或金黃稻浪。"},
    {"name": "星龍之巔", "category": "網美", "type": "咖啡/景觀", "time": "下午", "fee": "低消/門票", "phone": "0983-695-378", "map": get_gmap_url("星龍之巔"), "desc": "位於海拔200公尺，有「長濱空中花園」之稱，可180度俯瞰太平洋。"},
    {"name": "烏石鼻漁港", "category": "秘境", "type": "自然", "time": "上午/下午", "fee": "免門票", "phone": "無", "map": get_gmap_url("烏石鼻漁港"), "desc": "全台最大柱狀火山岩體，潮間帶生態豐富，適合看海踏浪。"},
    
    # 歷史/文化
    {"name": "八仙洞遺址", "category": "必訪", "type": "歷史/健行", "time": "上午", "fee": "停車費", "phone": "089-881-418", "map": get_gmap_url("八仙洞遺址"), "desc": "台灣最古老的史前文化遺址，海蝕洞奇觀與絕佳的海景步道。"},
    {"name": "長濱天主堂 (吳神父腳底按摩)", "category": "文化", "type": "放鬆", "time": "下午", "fee": "按摩收費", "phone": "089-831-428", "map": get_gmap_url("長濱天主堂 吳神父腳底按摩"), "desc": "正宗吳神父腳底按摩發源地，走完行程後最佳的放鬆去處。"},
    {"name": "南竹湖部落", "category": "秘境", "type": "人文", "time": "上午/下午", "fee": "免門票", "phone": "089-832-139", "map": get_gmap_url("南竹湖部落"), "desc": "充滿阿美族風情的藝術部落，白螃蟹的故鄉。"},
    {"name": "樟原船型教堂", "category": "網美", "type": "建築", "time": "上午", "fee": "免門票", "phone": "089-881-007", "map": get_gmap_url("樟原船型教堂"), "desc": "外觀猶如一艘大船的諾亞方舟教堂，花東海岸線最北端的寧靜聚落。"},
    
    # 美食/名店 
    {"name": "邱爸爸海味", "category": "必訪", "type": "無菜單海鮮", "time": "午餐/晚餐", "fee": "依人頭計價", "phone": "089-831-439", "map": get_gmap_url("長濱邱爸爸海味"), "desc": "長濱極具代表性的預約制無菜單海產店，食材極度新鮮。(需提早預約)"},
    {"name": "巨大少年咖啡館", "category": "網美", "type": "咖啡", "time": "下午", "fee": "低消", "phone": "0919-923-121", "map": get_gmap_url("長濱巨大少年咖啡館"), "desc": "藏身在公路旁的質感咖啡店，年輕人最愛的打卡熱點。"},
    {"name": "齒草埔 - 野餐", "category": "秘境", "type": "質感料理", "time": "午餐/晚餐", "fee": "套餐制", "phone": "僅接受FB粉專預約", "map": get_gmap_url("長濱齒草埔"), "desc": "低調隱密的藝術感餐廳，提供精緻的在地食材創意料理。"},
]

hotels_db = [
    {"name": "畫日風尚 (Sinasera 24)", "tag": "頂級法餐", "price": 6000, "phone": "089-832-558", "map": get_gmap_url("畫日風尚 Sinasera 24"), "desc": "長濱最知名的法式餐廳與住宿，享受花東最頂級的舌尖體驗。"},
    {"name": "陽光佈居", "tag": "寧靜放鬆", "price": 3500, "phone": "0933-990-233", "map": get_gmap_url("長濱陽光佈居"), "desc": "隱身半山腰的清水模民宿，完全無電視，專注於與自然對話。"},
    {"name": "海明威民宿", "tag": "海景第一排", "price": 4000, "phone": "0928-227-389", "map": get_gmap_url("長濱海明威民宿"), "desc": "躺在床上就能看日出，海浪聲伴你入眠。"},
    {"name": "余水知歡", "tag": "公益/美景", "price": 3800, "phone": "0988-566-788", "map": get_gmap_url("長濱余水知歡"), "desc": "嚴長壽先生推動的公益民宿，背山面海，大草皮極佳。"},
    {"name": "聽風說故事", "tag": "質感木屋", "price": 3200, "phone": "0936-149-003", "map": get_gmap_url("長濱聽風說故事民宿"), "desc": "隱密性高，建築充滿巧思的度假首選。"}
]

# ==========================================
# 4. 邏輯核心：動態行程生成演算法
# ==========================================
def generate_dynamic_itinerary(days_str, group):
    if "一日" in days_str: day_count = 1
    elif "二日" in days_str: day_count = 2
    else: day_count = 3
    
    itinerary = {}
    
    # Day 1: 長濱經典 (以金剛大道、八仙洞為主)
    d1_spot1 = next(s for s in all_spots_db if s['name'] == "八仙洞遺址")
    d1_spot2 = next(s for s in all_spots_db if s['name'] == "邱爸爸海味")
    d1_spot3 = next(s for s in all_spots_db if s['name'] == "金剛大道")
    
    if group == "長輩同行":
        d1_spot4 = next(s for s in all_spots_db if s['name'] == "長濱天主堂 (吳神父腳底按摩)")
    else:
        d1_spot4 = next(s for s in all_spots_db if s['name'] == "星龍之巔")
        
    itinerary[1] = [d1_spot1, d1_spot2, d1_spot3, d1_spot4]
    
    # Day 2: 深度海岸與秘境
    if day_count >= 2:
        d2_spot1 = next(s for s in all_spots_db if s['name'] == "樟原船型教堂")
        d2_spot2 = next(s for s in all_spots_db if s['name'] == "烏石鼻漁港")
        d2_spot3 = next(s for s in all_spots_db if s['name'] == "巨大少年咖啡館")
        itinerary[2] = [d2_spot1, d2_spot2, d2_spot3]

    # Day 3: 部落人文與回程
    if day_count == 3:
        d3_spot1 = next(s for s in all_spots_db if s['name'] == "南竹湖部落")
        d3_spot2 = {"name": "成功漁港/三仙台", "category": "順遊", "type": "景點", "time": "下午", "fee": "免門票", "phone": "無", "map": get_gmap_url("台東三仙台"), "desc": "南下回程順遊，採買新鮮海產。"}
        itinerary[3] = [d3_spot1, d3_spot2]
        
    return "🌊 遠離喧囂的太平洋假期", itinerary

# ==========================================
# 5. 頁面內容與交互 (UI/UX 佈局)
# ==========================================
st.markdown("""
    <div class="header-box">
        <div class="header-title">🌊 2026 台東長濱雙浪漫遊</div>
        <div style="margin-top:5px; font-size:14px;">海浪的湛藍 × 稻浪的金黃</div>
    </div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        travel_date = st.date_input("📅 預計出發日", value=date(2026, 6, 15))
    with col2:
        days_str = st.selectbox("🕒 停留時間", ["一日遊 (快閃)", "二日遊 (慢活)", "三日遊 (深度)"])
        group = st.selectbox("👥 旅遊型態", ["情侶/夫妻", "親子家庭", "長輩同行", "熱血獨旅"])
    
    if st.button("🚀 產出長濱專屬行程"):
        st.session_state['generated'] = True
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.get('generated'):
    status_title, itinerary = generate_dynamic_itinerary(days_str, group)
    
    st.markdown(f"""
    <div class="info-box">
        <h4 style="margin-top:0;">{status_title}</h4>
        <p style="margin-bottom:0;">為您規劃 <b>{travel_date.strftime('%Y/%m/%d')}</b> 的 <b>{group}</b> 專屬路線。長濱沒有火車直達，建議租車慢遊！</p>
    </div>
    """, unsafe_allow_html=True)

    # --- 顯示行程 (加入電話與地圖連結) ---
    for day, spots in itinerary.items():
        st.markdown(f'<div class="day-header">Day {day}</div>', unsafe_allow_html=True)
        
        for i, spot in enumerate(spots):
            # 判斷上下午或用餐
            if "午餐" in spot['time'] or "晚餐" in spot['time']: time_label = "🍽️ 用餐"
            elif i < len(spots)/2: time_label = "☀️ 上午" 
            else: time_label = "🌤️ 下午"
            
            tags_html = f'<span class="spot-tag">{spot["type"]}</span>'
            if spot['category'] == "必訪": tags_html += '<span class="spot-tag" style="background:#FBD38D;color:#C05621!important;">⭐ 必訪</span>'
            
            st.markdown(f"""
            <div class="timeline-item">
                <div class="spot-title">{time_label}：{spot['name']}</div>
                <div style="margin: 5px 0;">{tags_html}</div>
                <div style="font-size: 14px; color: #4A5568; line-height: 1.8;">
                    <b>💰 收費：</b> {spot['fee']} <br>
                    <b>📞 電話：</b> {spot['phone']} <br>
                    <b>📍 地點：</b> <a href="{spot['map']}" target="_blank" class="nav-link">🗺️ 點我開啟 Google 導航</a> <br>
                    <b>📝 簡介：</b> {spot['desc']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- 住宿推薦 (加入電話與地圖連結) ---
    if "一日" not in days_str:
        st.markdown("### 🏨 在地質感住宿推薦")
        
        for h in random.sample(hotels_db, 3):
            st.markdown(f"""
            <div class="hotel-card">
                <div style="font-weight:bold; color:#2C5282; font-size: 18px;">
                    {h['name']} 
                    <span style="font-size:12px; background:#4FD1C5; color:white; padding:2px 8px; border-radius:10px; margin-left:5px; vertical-align: middle;">{h['tag']}</span>
                </div>
                <div style="font-size:14px; color:#4A5568; margin-top:8px; line-height: 1.8;">
                    <b>💲 預估：</b> {h['price']} 元起 / 晚 <br>
                    <b>📞 電話：</b> {h['phone']} <br>
                    <b>📍 地點：</b> <a href="{h['map']}" target="_blank" class="nav-link">🗺️ 點我開啟 Google 導航</a> <br>
                    <b>📝 簡介：</b> {h['desc']}
                </div>
            </div>
            """, unsafe_allow_html=True)
