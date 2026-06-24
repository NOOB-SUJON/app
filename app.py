import streamlit as st
import yt_dlp

# ১. পেজ কনফিগারেশন
st.set_page_config(
    page_title="DownPro.net - Free Online Video Downloader",
    page_icon="📥",
    layout="centered"
)

# ২. মূল লোগো ও হেডার
st.title("Free Online Video Downloader")

# ৩. ইনপুট ও সার্চ মেকানিজম
col_input, col_search_btn = st.columns([3.5, 1])

with col_input:
    url_input = st.text_input("Input URL", placeholder="Paste your video link here", label_visibility="collapsed")

with col_search_btn:
    search_triggered = st.button("Download")

# পলিসি ও রিভিউ টেক্সট 
st.write("By using our service you accept our Terms of Service and Privacy Policy")
st.write("▶ How to download? Watch the tutorial")
st.write("Scanned by ✓ Norton Safe Web")
st.write("★★★★★ 4.8 /5 — 54,989 reviews")

st.write("---")

# ৪. সোশ্যাল মিডিয়া বাটন সেকশন
st.write("### Supported Platforms:")
c1, c2, c3, c4 = st.columns(4)
c1.info("📘 facebook.com")
c2.error("📸 instagram.com")
c3.success("🔴 youtube.com")
c4.warning("🎵 tiktok.com")

st.write("---")

# ৫. মেইন লজিক (আপনার পছন্দের সুন্দর ইন্টারফেস)
if url_input or search_triggered:
    if not url_input:
        st.warning("Please paste a video link first.")
    else:
        try:
            with st.spinner("🔍 Gathering video details... Please wait."):
                # সার্ভার ব্লক এড়াতে বেসিক সেটিংস
                ydl_opts = {
                    'extract_flat': False, 
                    'skip_download': True,
                    'quiet': True,
                    'no_warnings': True
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url_input, download=False)
                    
                    video_title = info_dict.get('title', 'Downloaded_Video')
                    video_thumbnail = info_dict.get('thumbnail', '')
                    duration = info_dict.get('duration', 0)
                    formats = info_dict.get('formats', [])
                    
                    mins, secs = divmod(duration, 60)
                    duration_str = f"{mins}:{secs:02d}"

                # 🎬 ভিডিওর তথ্য প্রদর্শন (থাম্বনেইল ও টাইটেল দেখাবে)
                st.write("### 🎥 Video Found:")
                col_thumb, col_details = st.columns([1, 1.5])
                with col_thumb:
                    if video_thumbnail:
                        st.image(video_thumbnail, use_container_width=True)
                with col_details:
                    st.write(f"**Title:** {video_title[:80]}...")
                    st.write(f"⏱️ **Duration:** {duration_str}")
                
                # কোয়ালিটি লিংক ফিল্টারিং
                download_options = {}
                for f in formats:
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('url'):
                        ext = f.get('ext', 'mp4')
                        resolution = f.get('format_note', f.get('resolution', 'Unknown'))
                        label = f"MP4 {resolution}"
                        download_options[label] = f['url']
                
                if not download_options and info_dict.get('url'):
                    download_options["MP4 (Normal Quality)"] = info_dict['url']

                # ডাউনলোড বাটন তৈরি
                if download_options:
                    st.write("---")
                    selected_format = st.selectbox("Choose Quality:", list(download_options.keys()))
                    final_download_url = download_options[selected_format]
                    
                    st.write("👇 Click the button below to get your video:")
                    
                    # নিরাপদ এবং সচল ওপেন লিংক মেথড
                    st.page_link(final_download_url, label="🚀 Go to Video Stream (Right-Click & Save)", icon="📥")
                    st.caption("💡 Guide: When the link opens, if the video plays, right-click (or long press on mobile) and select 'Save Video As...' to download.")
                else:
                    st.warning("Could not safely extract direct download formats for this video.")
                    
        except Exception as e:
            st.error("Platform restrictions active for this link. Please try another public video link.")

st.write("---")

# ৬. অল রিসোর্স লিস্ট সেকশন
st.write("### All Resources:")
res_col1, res_col2 = st.columns(2)
with res_col1:
    st.write("🎥 dailymotion.com")
    st.write("🌐 vimeo.com")
    st.write("🔹 vk.com")
    st.write("🎵 tiktok.com")
with res_col2:
    st.write("🤖 reddit.com")
    st.write("🧵 threads.net")
    st.write("🇨🇳 xiaohongshu.com")
    st.write("🔄 MP4 Converter")

st.write("---")

# ৭. সম্পূর্ণ গাইডলাইন সেকশন
st.write("### 📖 Complete Guide to Downloading High-Quality MP4 Videos Online")
st.write("**1. Begin by copying the video URL**")
st.write("Navigate to your preferred video platform, copy the link of the video you want to download from the address bar or share button.")

st.write("**2. Paste the link into the field**")
st.write("Go back to DownPro page and insert the copied link into the designated input field at the top of the page.")

st.write("**3. Select format and Download**")
st.write("Select 'Download' or hit 'Enter' to launch the video conversion. Once processed, select your preferred quality option.")

st.write("---")

# ফুটার
st.write("© 2026 DownPro Online Service — Premium Video Downloader Layout")
