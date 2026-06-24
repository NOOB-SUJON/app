import streamlit as st
import yt_dlp
import requests

# ১. পেজ কনফিগারেশন
st.set_page_config(
    page_title="DownPro.net - Free Online Video Downloader",
    page_icon="📥",
    layout="centered"
)

# ২. অ্যাডভান্সড সিএসএস ডিজাইন (হুবহু ছবির মতো বাটন, রেটিং এবং অল রিসোর্স সেকশন)
st.markdown("""
    <style>
    /* পুরো ওয়েবসাইটের ব্যাকগ্রাউন্ড সাদা এবং টেক্সট ক্লিন রাখা */
    .stApp { background-color: #ffffff !important; }
    h1 { font-family: 'Arial', sans-serif; font-weight: bold; color: #333333; text-align: center; margin-bottom: 25px; }
    
    /* ১০০% হোয়াইট সার্চ বক্স ডিজাইন */
    div.stTextInput > div > div > input {
        border: 2px solid #7cd320 !important;
        border-radius: 4px !important;
        padding: 14px 15px !important;
        font-size: 16px !important;
        background-color: #ffffff !important;
        color: #222222 !important;
        box-shadow: none !important;
    }
    
    /* সার্চ/ডাউনলোড বাটন স্টাইল */
    div.stButton > button {
        background-color: #7cd320 !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 13px 20px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        width: 100%;
        transition: 0.2s ease;
    }
    div.stButton > button:hover { background-color: #69b519 !important; }
    
    /* টার্মস এবং রিভিউ সেকশন */
    .policy-text { text-align: center; font-size: 12px; color: #666666; margin-top: 8px; }
    .policy-text a { color: #0066cc; text-decoration: none; }
    .meta-info { text-align: center; font-size: 14px; color: #444444; margin-top: 15px; margin-bottom: 30px; }
    .stars { color: #ffbc00; font-size: 16px; }
    
    /* সোশ্যাল মিডিয়া বড় বাটন গ্রিড */
    .social-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 15px;
        margin-top: 20px;
        margin-bottom: 40px;
    }
    .social-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #eaf6dd;
        color: #333333;
        padding: 12px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 14px;
        font-family: Arial;
    }
    .social-btn img { width: 20px; margin-right: 8px; }

    /* অল রিসোর্স গ্রিড */
    .resource-title { text-align: center; font-weight: bold; color: #333333; margin-top: 20px; margin-bottom: 20px; font-size: 18px; }
    .resource-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-bottom: 40px;
    }
    .resource-item {
        display: flex;
        align-items: center;
        font-size: 14px;
        color: #444444;
        padding: 6px;
        font-family: Arial;
    }
    .resource-item span { margin-right: 8px; font-size: 16px; }
    
    /* গাইডলাইন সেকশন ডিজাইন */
    .guide-section { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 30px; margin-top: 40px; box-shadow: 0 4px 12px rgba(0,0,0,0.02); }
    .guide-title { color: #1e1e1e; font-weight: 700; font-size: 22px; text-align: center; margin-bottom: 25px; }
    .guide-step { margin-bottom: 20px; padding-left: 15px; border-left: 4px solid #7cd320; }
    .guide-step h4 { margin: 0 0 5px 0; color: #0f172a; font-size: 16px; }
    .guide-step p { margin: 0; color: #475569; font-size: 14px; }
    
    /* ভিডিও রেজাল্ট কার্ড */
    .savefrom-card {
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 8px;
        border: 1px solid #e1e8ed; 
        margin-top: 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .footer { text-align: center; margin-top: 60px; color: #888888; font-size: 13px; border-top: 1px solid #eeeeee; padding-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# ৩. লোগো ও হেডার
st.markdown("<h1 style='font-size: 36px; text-align:center; color:#333333;'>Free Online Video Downloader</h1>", unsafe_allow_html=True)

# ৪. ইনপুট ও সার্চ মেকানিজম
col_input, col_search_btn = st.columns([3.5, 1])

with col_input:
    url_input = st.text_input("", placeholder="Paste your video link here", label_visibility="collapsed")

with col_search_btn:
    search_triggered = st.button("Download")

# পলিসি, সিকিউরিটি ও রিভিউ টেক্সট (হুবহু ছবির মতো)
st.markdown("""
    <p class='policy-text'>By using our service you accept our <a href='#'>Terms of Service</a> and <a href='#'>Privacy Policy</a></p>
    <p style='text-align:center; font-size:14px; margin-top:10px;'><a href='#' style='color:#0066cc; text-decoration:none;'>▶ How to download? Watch the tutorial</a></p>
    <p style='text-align:center; font-size:14px; color:#333333; margin-top:15px;'>Scanned by <span style='color:#7cd320; font-weight:bold;'>✓</span> <b>Norton</b> Safe Web</p>
    <p class='meta-info'><span class='stars'>★★★★★</span> <b>4.8</b> /5 — 54,989 reviews</p>
""", unsafe_allow_html=True)

# ৫. সোশ্যাল মিডিয়া বড় বাটন সেকশন
st.markdown("""
    <div class='social-grid'>
        <div class='social-btn'><span style='color:#1877f2; font-size:18px; margin-right:8px;'>📘</span> facebook.com</div>
        <div class='social-btn'><span style='color:#e1306c; font-size:18px; margin-right:8px;'>📸</span> instagram.com</div>
        <div class='social-btn'><span style='color:#ff0000; font-size:18px; margin-right:8px;'>🔴</span> youtube.com</div>
        <div class='social-btn'><span style='color:#000000; font-size:18px; margin-right:8px;'>🎵</span> tiktok.com</div>
    </div>
""", unsafe_allow_html=True)

# মেইন ডাউনলোড লজিক পার্ট
if url_input or search_triggered:
    if not url_input:
        st.warning("⚠️ Please paste a video link first.")
    else:
        try:
            with st.spinner("🔍 Locating video source file... Please wait."):
                ydl_opts = {'extract_flat': False, 'skip_download': True}
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url_input, download=False)
                    
                    video_title = info_dict.get('title', 'Downloaded_Video')
                    video_thumbnail = info_dict.get('thumbnail', '')
                    duration = info_dict.get('duration', 0)
                    formats = info_dict.get('formats', [])
                    
                    mins, secs = divmod(duration, 60)
                    duration_str = f"{mins}:{secs:02d}"

                # ভিডিওর তথ্য প্রদর্শন কার্ড
                st.markdown("<div class='savefrom-card'>", unsafe_allow_html=True)
                c1, c2 = st.columns([1, 1.4])
                
                with c1:
                    if video_thumbnail:
                        st.image(video_thumbnail, use_container_width=True)
                
                with c2:
                    st.markdown(f"<h4 style='color:#222222; margin-top:0;'>{video_title[:60]}...</h4>", unsafe_allow_html=True)
                    st.markdown(f"<p style='color:#555555;'>⏱️ <b>Duration:</b> {duration_str}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # কোয়ালিটি লিংক ফিল্টারিং
                download_options = {}
                for f in formats:
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('url'):
                        ext = f.get('ext', 'mp4')
                        resolution = f.get('format_note', f.get('resolution', 'Unknown'))
                        label = f"MP4 {resolution}"
                        download_options[label] = f['url']
                        
                for f in formats:
                    if f.get('vcodec') == 'none' and f.get('acodec') != 'none' and f.get('url'):
                        label = f"Audio MP3"
                        download_options[label] = f['url']
                
                if not download_options and info_dict.get('url'):
                    download_options["MP4 (Normal Quality)"] = info_dict['url']

                # কোয়ালিটি সিলেক্টর এবং ডাউনলোড বাটন
                if download_options:
                    st.write("")
                    col_select, col_dl_btn = st.columns([1, 1.3])
                    
                    with col_select:
                        selected_format = st.selectbox("", list(download_options.keys()), label_visibility="collapsed", key="format_select")
                        final_download_url = download_options[selected_format]
                    
                    @st.cache_data(show_spinner=False)
                    def get_video_bytes(url):
                        return requests.get(url).content

                    with col_dl_btn:
                        try:
                            with st.spinner("⏳"):
                                video_bytes = get_video_bytes(final_download_url)
                                st.download_button(
                                    label="📥 Download Now",
                                    data=video_bytes,
                                    file_name=f"{video_title}.mp4",
                                    mime="video/mp4",
                                    use_container_width=True,
                                    key="actual_download_btn"
                                )
                        except Exception:
                            st.markdown(f'''
                                <a href="{final_download_url}" download="{video_title}.mp4" target="_self" style="text-decoration:none;">
                                    <button style="
                                        background-color: #7cd320; color: white; width: 100%; font-size: 16px; 
                                        font-weight: bold; border-radius: 4px; padding: 12px; border: none; cursor: pointer;
                                    ">📥 Download Now</button>
                                </a>
