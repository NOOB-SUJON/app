import streamlit as st
import yt_dlp
import requests

# ১. পেজ কনফিগারেশন এবং টাইটেল সেটআপ (SaveFrom এর মতো গ্রিন-ডার্ক মিক্স থিম)
st.set_page_config(
    page_title="Pro Video Downloader",
    page_icon="📥",
    layout="centered"
)

# ২. কাস্টম CSS ডিজাইন (সম্পূর্ণ SaveFrom.net ভাইব দেওয়ার জন্য)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #25d366; text-align: center; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; margin-bottom: 5px; }
    .subtitle { text-align: center; color: #a3a8b4; margin-bottom: 30px; font-size: 16px; }
    
    /* ইনপুট বক্স ডিজাইন */
    div.stTextInput > div > div > input {
        border: 2px solid #25d366 !important;
        border-radius: 30px !important;
        padding: 12px 20px !important;
        font-size: 16px !important;
        background-color: #1e222b !important;
        color: white !important;
    }
    
    /* ভিডিও কার্ড ডিজাইন */
    .video-card {
        background-color: #1e222b; padding: 20px; border-radius: 15px;
        border: 1px solid #2d3139; margin-top: 20px; margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
    }
    
    /* ড্রপডাউন ডিজাইন */
    div.stSelectbox > div > div {
        border: 1px solid #25d366 !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ৩. হেডার সেকশন
st.markdown("<h1>📥 DownPro Online Downloader</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>All website video just in one place </p>", unsafe_allow_html=True)

# ৪. লিংক ইনপুট বক্স
video_url = st.text_input("", placeholder="এখানে ভিডিওর লিংকটি পেস্ট করুন (যেমন: https://...)", label_visibility="collapsed")

# ৫. ভিডিও প্রসেসিং লজিক
if video_url:
    try:
        with st.spinner("🔍 ভিডিওর সোর্স ফাইল খোঁজা হচ্ছে... অনুগ্রহ করে অপেক্ষা করুন।"):
            ydl_opts = {'extract_flat': False, 'skip_download': True}
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=False)
                
                video_title = info_dict.get('title', 'Downloaded_Video')
                video_thumbnail = info_dict.get('thumbnail', '')
                duration = info_dict.get('duration', 0)
                formats = info_dict.get('formats', [])
                
                mins, secs = divmod(duration, 60)
                duration_str = f"{mins} মিনিট {secs} সেকেন্ড" if mins > 0 else f"{secs} সেকেন্ড"

            # ৬. ইউজার ইন্টারফেসে ভিডিওর তথ্য প্রদর্শন (SaveFrom এর মতো কার্ড)
            st.markdown("<div class='video-card'>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1.5])
            
            with col1:
                if video_thumbnail:
                    st.image(video_thumbnail, use_container_width=True)
            
            with col2:
                st.markdown(f"#### 🎬 {video_title[:60]}...")
                st.write(f"⏱️ **ডিউরেশন:** {duration_str}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # ৭. ফিল্টারিং করে কোয়ালিটি লিংক বের করা
            download_options = {}
            for f in formats:
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('url'):
                    ext = f.get('ext', 'mp4')
                    resolution = f.get('format_note', f.get('resolution', 'Unknown'))
                    label = f"ভিডিও - {resolution} ({ext.upper()})"
                    download_options[label] = f['url']
                    
            for f in formats:
                if f.get('vcodec') == 'none' and f.get('acodec') != 'none' and f.get('url'):
                    label = f"🎵 শুধুমাত্র অডিও/গান (MP3)"
                    download_options[label] = f['url']
            
            if not download_options and info_dict.get('url'):
                download_options["🎬 সাধারণ কোয়ালিটি (Direct Link)"] = info_dict['url']

            # ৮. নতুন প্রফেশনাল ডিরেক্ট ডাউনলোড বাটন (কোনো নতুন পেজ ওপেন হবে না)
            if download_options:
                selected_format = st.selectbox("ডাউনলোডের ফরম্যাট বেছে নিন:", list(download_options.keys()))
                final_download_url = download_options[selected_format]
                
                # ফাইল ডিরেক্ট ডাউনলোড করার জন্য ব্যাকএন্ড রিকোয়েস্ট ট্রিক
                @st.cache_data(show_spinner=False)
                def get_video_bytes(url):
                    # ভিডিওর ডাটা ব্যাকএন্ডে সাময়িক ডাউনলোড করে ব্রাউজারে পুশ করবে
                    return requests.get(url).content

                try:
                    with st.spinner("📥 ফাইলটি ডাউনলোডের জন্য রেডি হচ্ছে..."):
                        video_bytes = get_video_bytes(final_download_url)
                        
                        # স্ট্রিমলিটের অফিসিয়াল ডিরেক্ট ডাউনলোড বাটন
                        st.download_button(
                            label="🚀 সরাসরি ডাউনলোড করুন",
                            data=video_bytes,
                            file_name=f"{video_title}.mp4",
                            mime="video/mp4",
                            use_container_width=True
                        )
                except Exception:
                    # যদি ফাইলটি অনেক বড় হয়, তবে ব্যাকআপ হিসেবে ডিরেক্ট ফোর্স-ডাউনলোড লিংক শো করবে
                    st.markdown(f'''
                        <a href="{final_download_url}" download="{video_title}.mp4" target="_self" style="text-decoration:none;">
                            <button style="
                                background-color: #25d366; color: white; width: 100%; font-size: 20px; 
                                font-weight: bold; border-radius: 8px; padding: 12px; border: none; cursor: pointer;
                                margin-top: 15px; box-shadow: 0 4px 15px rgba(37,211,102,0.3);
                            ">🚀 ডিরেক্ট ডাউনলোড করুন (Alt)</button>
                        </a>
                    ''', unsafe_allow_html=True)
            else:
                st.warning("⚠️ কোনো ডাউনলোড লিংক পাওয়া যায়নি।")
                
    except Exception as e:
        st.error("❌ দুঃখিত! ভিডিওর সোর্স ফাইল বের করা যায়নি। অন্য লিংক ট্রাই করুন।")

           
           
