import streamlit as st
import yt_dlp
import os

# ১. পেজ কনফিগারেশন এবং টাইটেল সেটআপ
st.set_page_config(
    page_title="Pro Video Downloader",
    page_icon="📥",
    layout="centered"
)

# ২. কাস্টম CSS ডিজাইন (অ্যাপটিকে প্রিমিয়াম এবং সুন্দর দেখানোর জন্য)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #ff4b4b; text-align: center; font-family: 'Helvetica Neue', sans-serif; font-weight: 700; }
    .subtitle { text-align: center; color: #a3a8b4; margin-bottom: 30px; }
    div.stButton > button:first-child {
        background-color: #ff4b4b; color: white; width: 100%; font-size: 18px; 
        font-weight: bold; border-radius: 8px; padding: 10px; border: none;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover { background-color: #ff3333; transform: scale(1.02); }
    .video-card {
        background-color: #1e222b; padding: 20px; border-radius: 12px;
        border: 1px solid #2d3139; margin-top: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# ৩. হেডার সেকশন
st.markdown("<h1>📥 অল-ইন-ওয়ান ভিডিও ডাউনলোডার</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>ইউটিউব, ফেসবুক, ইনস্টাগ্রাম, টিকটকসহ যেকোনো সাইটের ভিডিও লিংক পেস্ট করুন</p>", unsafe_allow_html=True)

# ৪. লিংক ইনপুট বক্স
video_url = st.text_input("", placeholder="এখানে ভিডিওর লিংকটি পেস্ট করুন (যেমন: https://...)", label_visibility="collapsed")

# ৫. ভিডিও প্রসেসিং লজিক
if video_url:
    try:
        with st.spinner("🔍 ভিডিওর সোর্স ফাইল খোঁজা হচ্ছে... অনুগ্রহ করে অপেক্ষা করুন।"):
            # ভিডিওর মেটাডেটা স্ক্র্যাপ করার জন্য yt-dlp এর কনফিগারেশন
            ydl_opts = {'extract_flat': False, 'skip_download': True}
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=False)
                
                # ভিডিওর প্রয়োজনীয় তথ্য সংগ্রহ
                video_title = info_dict.get('title', 'Unknown Title')
                video_thumbnail = info_dict.get('thumbnail', '')
                duration = info_dict.get('duration', 0)
                formats = info_dict.get('formats', [])
                
                # মিনিট ও সেকেন্ডে রূপান্তর
                mins, secs = divmod(duration, 60)
                duration_str = f"{mins} মিনিট {secs} সেকেন্ড" if mins > 0 else f"{secs} সেকেন্ড"

            # ৬. ইউজার ইন্টারফেসে ভিডিওর তথ্য প্রদর্শন করা
            st.markdown("<div class='video-card'>", unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1.5])
            
            with col1:
                if video_thumbnail:
                    st.image(video_thumbnail, use_container_width=True)
            
            with col2:
                st.subheader(video_title)
                st.write(f"⏱️ **ডিউরেশন:** {duration_str}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.write("---")
            st.write("### ⚙️ ডাউনলোডের কোয়ালিটি সিলেক্ট করুন:")
            
            # ৭. ফিল্টারিং করে ভালো মানের ডাউনলোড লিংক বের করা
            download_options = {}
            
            # সেরা মানের ভিডিও এবং অডিও কম্বাইন অপশন খোঁজা
            for f in formats:
                # যেসব লিংকে অডিও এবং ভিডিও দুটোই একসাথে বিল্ট-ইন আছে (Direct Download এর জন্য সহজ)
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('url'):
                    ext = f.get('ext', 'mp4')
                    resolution = f.get('format_note', f.get('resolution', 'Unknown'))
                    label = f"🎬 ভিডিও - {resolution} ({ext.upper()})"
                    download_options[label] = f['url']
                    
            # শুধুমাত্র MP3 অডিও অপশন যোগ করা
            for f in formats:
                if f.get('vcodec') == 'none' and f.get('acodec') != 'none' and f.get('url'):
                    label = f"🎵 শুধুমাত্র অডিও/গান (MP3/M4A)"
                    download_options[label] = f['url']
            
            # যদি কোনো ফিল্টার কাজ না করে তবে ডিফল্ট বেস্ট লিংক দেওয়া
            if not download_options and info_dict.get('url'):
                download_options["🎬 সাধারণ কোয়ালিটি (Direct Link)"] = info_dict['url']

            # ৮. ড্রপডাউন মেনু এবং ফাইনাল ডাউনলোড বাটন
            if download_options:
                selected_format = st.selectbox("ফরম্যাট বেছে নিন:", list(download_options.keys()))
                final_download_url = download_options[selected_format]
                
                # রেসপন্সিভ ডাউনলোড বাটন (ক্লিক করলে নতুন ট্যাবে ফাইল ওপেন/ডাউনলোড হবে)
                st.markdown(f'''
                    <a href="{final_download_url}" target="_blank" style="text-decoration:none;">
                        <button style="
                            background-color: #25d366; color: white; width: 100%; font-size: 20px; 
                            font-weight: bold; border-radius: 8px; padding: 12px; border: none; cursor: pointer;
                            margin-top: 15px; box-shadow: 0 4px 15px rgba(37,211,102,0.3);
                        ">🚀 এখনই ডাউনলোড শুরু করুন</button>
                    </a>
                ''', unsafe_allow_html=True)
            else:
                st.warning("⚠️ এই ভিডিওটির জন্য সরাসরি কোনো ডাউনলোড লিংক পাওয়া যায়নি।")
                
    except Exception as e:
        st.error("❌ দুঃখিত! লিংকটি প্রসেস করা যায়নি। লিংক সঠিক আছে কিনা পুনরায় চেক করুন বা অন্য লিংক ট্রাই করুন।")
