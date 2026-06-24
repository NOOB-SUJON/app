import streamlit as st
import yt_dlp
import requests

# ১. পেজ কনফিগারেশন
st.set_page_config(
    page_title="DownPro.net - Free Online Video Downloader",
    page_icon="📥",
    layout="centered"
)

# ২. মূল লোগো ও হেডার
st.markdown("<h1 style='text-align:center; font-family:Arial; color:#333333;'>Free Online Video Downloader</h1>", unsafe_allow_html=True)

# ৩. ইনপুট ও সার্চ মেকানিজম
col_input, col_search_btn = st.columns([3.5, 1])

with col_input:
    url_input = st.text_input("", placeholder="Paste your video link here", label_visibility="collapsed")

with col_search_btn:
    search_triggered = st.button("Download")

# পলিসি ও রিভিউ টেক্সট
st.markdown("<p style='text-align:center; font-size:12px; color:#666666; margin-top:8px;'>By using our service you accept our <a href='#'>Terms of Service</a> and <a href='#'>Privacy Policy</a></p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:14px; margin-top:10px;'><a href='#' style='color:#0066cc; text-decoration:none;'>▶ How to download? Watch the tutorial</a></p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:14px; color:#333333; margin-top:15px;'>Scanned by <span style='color:#7cd320; font-weight:bold;'>✓</span> <b>Norton</b> Safe Web</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:14px; color:#444444; margin-top:15px; text-align:center;'><span style='color:#ffbc00;'>★★★★★</span> <b>4.8</b> /5 — 54,989 reviews</p>", unsafe_allow_html=True)

st.write("---")

# ৪. সোশ্যাল মিডিয়া বাটন সেকশন (সহজ ও নিরাপদ পদ্ধতি)
st.write("### Supported Platforms:")
c1, c2, c3, c4 = st.columns(4)
c1.info("📘 facebook.com")
c2.error("📸 instagram.com")
c3.success("🔴 youtube.com")
c4.warning("🎵 tiktok.com")

st.write("---")

# ৫. মেইন ডাউনলোড লজিক
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
                st.write("### Video Details:")
                col_thumb, col_details = st.columns([1, 1.5])
                with col_thumb:
                    if video_thumbnail:
                        st.image(video_thumbnail, use_container_width=True)
                with col_details:
                    st.write(f"**Title:** {video_title[:60]}...")
                    st.write(f"⏱️ **Duration:** {duration_str}")
                
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
                    st.write("---")
                    col_select, col_dl_btn = st.columns([1, 1.3])
                    
                    with col_select:
                        selected_format = st.selectbox("Choose Quality:", list(download_options.keys()), label_visibility="collapsed")
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
                                    use_container_width=True
                                )
                        except Exception:
                            # নিরাপদ ব্যাকআপ বাটন লিংক
                            st.write(f"[🚀 Click Here to Download Video]({final_download_url})")
                else:
                    st.warning("⚠️ No download links found for this video.")
                    
        except Exception as e:
            st.error("❌ Error processing link. Please make sure the URL is correct.")

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

# ৭. সম্পূর্ণ গাইডলাইন সেকশন (নিরাপদ পদ্ধতিতে সাজানো)
st.write("### 📖 Complete Guide to Downloading High-Quality MP4 Videos Online")

st.write("**1. Begin by copying the video URL**")
st.write("Navigate to your preferred video platform, copy the link of the video you want to download from the address bar or share button.")

st.write("**2. Paste the link into the field**")
st.write("Go back to DownPro page and insert the copied link into the designated input field at the top of the page.")

st.write("**3. Select format and Download**")
st.write("Select 'Download' or hit 'Enter' to launch the video conversion. Once processed, select your preferred quality option.")

st.write("---")

# ফুটার
st.markdown("<p style='text-align:center; color:#888888; font-size:13px;'>© 2026 DownPro Online Service — Premium Video Downloader Layout</p>", unsafe_allow_html=True)
