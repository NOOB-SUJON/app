import streamlit as st
import yt_dlp
import requests

# ১. পেজ কনফিগারেশন
st.set_page_config(
    page_title="DownPro.net - Premium Video Downloader",
    page_icon="📥",
    layout="centered"
)

# ২. অ্যাডভান্সড সিএসএস ডিজাইন (লোগো এবং গাইডের সম্পূর্ণ কাস্টমাইজেশন)
st.markdown("""
    <style>
    /* পুরো ওয়েবসাইটের ব্যাকগ্রাউন্ড হালকা এবং ক্লিন রাখা */
    .stApp { background-color: #fcfcfc !important; }
    h1 { font-family: 'Arial', sans-serif; font-weight: bold; color: #1e1e1e; text-align: center; margin-bottom: 0px; }
    
    /* ডাউনলোড ইন্ট্রো সেকশন ডিজাইন */
    .intro-box {
        background: linear-gradient(135deg, #10b981, #059669); 
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 35px;
        box-shadow: 0 4px 15px rgba(16,185,129,0.2);
    }
    .intro-box h2 { color: white !important; margin-top: 0; font-size: 24px; }
    .intro-box p { color: #ecfdf5; margin-bottom: 0; font-size: 15px; }
    
    /* হোয়াইট সার্চ বক্স ডিজাইন */
    div.stTextInput > div > div > input {
        border: 2px solid #10b981 !important;
        border-radius: 6px !important;
        padding: 14px 15px !important;
        font-size: 16px !important;
        background-color: #ffffff !important;
        color: #222222 !important;
    }
    
    /* বাটন স্টাইল */
    div.stButton > button {
        background-color: #10b981 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 12px 20px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        width: 100%;
    }
    
    /* রেজাল্ট কার্ড ডিজাইন */
    .savefrom-card {
        background-color: #ffffff; padding: 20px; border-radius: 8px;
        border: 1px solid #e1e8ed; margin-top: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    
    /* সোশ্যাল মিডিয়া লোগো গ্রিড ডিজাইন */
    .supported-platforms { text-align: center; margin-top: 50px; margin-bottom: 20px; }
    .platform-grid { display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; margin-top: 15px; }
    .platform-card {
        background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px;
        padding: 10px 20px; font-weight: bold; color: #16a34a; font-size: 14px;
        display: flex; align-items: center; gap: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    /* গাইডলাইন সেকশন ডিজাইন */
    .guide-section { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 30px; margin-top: 60px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
    .guide-title { color: #1e1e1e; font-weight: 700; font-size: 22px; text-align: center; margin-bottom: 25px; }
    .guide-step { margin-bottom: 20px; padding-left: 15px; border-left: 4px solid #10b981; }
    .guide-step h4 { margin: 0 0 5px 0; color: #0f172a; font-size: 16px; }
    .guide-step p { margin: 0; color: #475569; font-size: 14px; }
    
    .footer { text-align: center; margin-top: 60px; color: #888888; font-size: 13px; border-top: 1px solid #e2e8f0; padding-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# ৩. লোগো সেকশন
st.markdown("<h1 style='font-size: 45px; text-align:center;'><span style='color:#1e1e1e;'>downpro</span><span style='color:#10b981;'>.net</span></h1>", unsafe_allow_html=True)
st.write("---")

# ৪. ডাউনপ্রো ইন্ট্রো সেকশন
st.markdown("""
    <div class='intro-box'>
        <h2>🚀 DownPro সুপারফাস্ট অনলাইন ভিডিও ডাউনলোডার</h2>
        <p>কোনো রকম সফটওয়্যার ছাড়াই ইউটিউব, ফেসবুক, ইনস্টাগ্রাম এবং টিকটকের যেকোনো ভিডিও ফুল এইচডি (Full HD) কোয়ালিটিতে সরাসরি আপনার ডিভাইসে সেভ করুন সম্পূর্ণ ফ্রিতে।</p>
    </div>
""", unsafe_allow_html=True)

# ৫. ইনপুট ও সার্চ মেকানিজম
col_input, col_search_btn = st.columns([3, 1])

with col_input:
    url_input = st.text_input("", placeholder="এখানে ভিডিওর লিংকটি পেস্ট করুন...", label_visibility="collapsed")

with col_search_btn:
    search_triggered = st.button("ভিডিও খুঁজুন 🔍")

# মেইন ডাউনলোড লজিক
if url_input or search_triggered:
    if not url_input:
        st.warning("⚠️ দয়া করে আগে একটি ভিডিও লিংক পেস্ট করুন।")
    else:
        try:
            with st.spinner("🔍 ভিডিওর সোর্স ফাইল খোঁজা হচ্ছে... অনুগ্রহ করে অপেক্ষা করুন।"):
                ydl_opts = {'extract_flat': False, 'skip_download': True}
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url_input, download=False)
                    
                    video_title = info_dict.get('title', 'Downloaded_Video')
                    video_thumbnail = info_dict.get('thumbnail', '')
                    duration = info_dict.get('duration', 0)
                    formats = info_dict.get('formats', [])
                    
                    mins, secs = divmod(duration, 60)
                    duration_str = f"{mins}:{secs:02d}"

                # ভিডিওর তথ্য প্রদর্শন
                st.markdown("<div class='savefrom-card'>", unsafe_allow_html=True)
                c1, c2 = st.columns([1, 1.4])
                
                with c1:
                    if video_thumbnail:
                        st.image(video_thumbnail, use_container_width=True)
                
                with c2:
                    st.markdown(f"<h4 style='color:#222222; margin-top:0;'>{video_title[:60]}...</h4>", unsafe_allow_html=True)
                    st.markdown(f"<p style='color:#555555;'>⏱️ <b>ডিউরেশন:</b> {duration_str}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # কোয়ালিটি ফরম্যাট ফিল্টারিং
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
                    download_options["MP4 (সাধারণ কোয়ালিটি)"] = info_dict['url']

                # কোয়ালিটি ড্রপডাউন এবং ফাইনাল ডাউনলোড বাটন
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
                                        background-color: #10b981; color: white; width: 100%; font-size: 16px; 
                                        font-weight: bold; border-radius: 6px; padding: 12px; border: none; cursor: pointer;
                                    ">📥 Download Now</button>
                                </a>
                            ''', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ দুঃখিত, কোনো ডাউনলোড লিংক পাওয়া যায়নি।")
                    
        except Exception as e:
            st.error("❌ দুঃখিত! ভিডিওর লিংকটি প্রсеস করা সম্ভব হয়নি। দয়া করে সঠিক লিংক দিন।")

# ৬. সাপোর্টেড প্ল্যাটফর্ম সেকশন (আপনার স্ক্রিনশট ১-এর মতো লোগো গ্রিড)
st.markdown("""
    <div class='supported-platforms'>
        <h3 style='color:#334155; font-size:18px;'>🎯 সমর্থিত জনপ্রিয় প্ল্যাটফর্মসমূহ:</h3>
        <div class='platform-grid'>
            <div class='platform-card'>🔵 facebook.com</div>
            <div class='platform-card'>📸 instagram.com</div>
            <div class='platform-card'>🔴 youtube.com</div>
            <div class='platform-card'>🎵 tiktok.com</div>
            <div class='platform-card'>🐦 twitter.com</div>
            <div class='platform-card'>🎬 vimeo.com</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ৭. সম্পূর্ণ গাইডলাইন সেকশন (Your Screenshot 2 - Step by Step Guide)
st.markdown("""
    <div class='guide-section'>
        <div class='guide-title'>📖 কীভাবে হাই-কোয়ালিটি ভিডিও ডাউনলোড করবেন?</div>
        
        <div class='guide-step'>
            <h4>১. ভিডিওর লিংকটি কপি করুন (Copy the URL)</h4>
            <p>আপনার পছন্দের প্ল্যাটফর্ম (যেমন: Facebook বা YouTube) থেকে যে ভিডিওটি ডাউনলোড করতে চান, সেটির শেয়ার বাটনে ক্লিক করে লিংকটি কপি করে নিন।</p>
        </div>
        
        <div class='guide-step'>
