import os, sys, requests, cloudscraper, logging, subprocess, asyncio, pytz, glob, mmap, gc, base64, shutil, re, fitz, aiohttp
from config import my_hrk_api, my_auth_token, my_vercel_api
from pyrogram import Client
from pyrogram.types import Message
from PIL import Image, ImageDraw, ImageFont
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import datetime
from p_bar import *
from DbNew import *
from config import *
from Tools.AppxTestHtml import *
from Tools.OliveAddaTestHtml import *

# ========================= Time Zone ============================
def get_current_time_ist():
    ist = pytz.timezone("Asia/Kolkata")
    ist_time = datetime.now(ist)
    current_time = ist_time.strftime("%d-%m-%Y %I:%M:%S %p")
    return current_time

def my_encrypt_data(decoded_data):
    key = '%!$!%_$&!%M)&^_&'.encode("utf8")
    iv = '#*y*#2yJ*#$wJv*v'.encode("utf8")
    data_bytes = decoded_data.encode("utf8")
    padded_data = pad(data_bytes, AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(padded_data)
    return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')

def my_decrypt_data(encoded_data):
    key = '%!$!%_$&!%M)&^_&'.encode("utf8")
    iv = '#*y*#2yJ*#$wJv*v'.encode("utf8")
    decoded_data = base64.urlsafe_b64decode(encoded_data)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(decoded_data), AES.block_size)
    return decrypted_data.decode('utf-8')

async def decrypt_txt_file(input_file, file_name):
    results = ''
    output_file = 'decrypted_' + file_name.replace('EncMEGA_', 'MEGA_') + '.txt'
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read().split("\n")

        for line in content:
            if "https://megatron_encryption?link=" in line:
                name, enc_url = line.split('https://megatron_encryption?link=')
                if enc_url:
                    results += f'{name}{my_decrypt_data(enc_url)}\n'
            else:
                results += line.strip()
    
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(results.rstrip('\n'))
    return output_file


async def appx_dl(filename, key):
    with open(filename, "r+b") as f:
        num_bytes = min(28, os.path.getsize(filename))
        with mmap.mmap(f.fileno(), length=num_bytes, access=mmap.ACCESS_WRITE) as mmapped_file:
            for i in range(num_bytes):
                mmapped_file[i] ^= ord(key[i]) if i < len(key) else i
        logging.info(f"📁 {filename} has been Decrypted 🔓 Using Mmap..")
        return True

async def download_pdf(session: aiohttp.ClientSession, url: str, file_name, token=None):
    if os.path.exists(file_name): os.remove(file_name)
    
    # Clean URL: remove trailing '?' (but keep parameters if any)
    url = url.rstrip('?')
    
    for attempt in range(1, 4):
        try:
            # Case 1: Appx encrypted/signed PDF (with key in URL)
            if ("appx" in url or "?URLPrefix" in url) and ('--appx-pdf?key=' in url or '*' in url or "?key=" in url):
                url5 = url.replace('--appx-pdf?key=', '').replace('?key=', '*')
                d_url , key = url5.split("*")
                async with session.post(f"{my_vercel_api}/appxv2-pdf", json={'url': d_url, 'key': key}) as resp:
                    if resp.status == 200 and resp.headers.get('Content-Type') == 'application/pdf':
                        with open(file_name, 'wb') as fd:
                            async for chunk in resp.content.iter_chunked(8192):
                                if chunk:
                                    fd.write(chunk)
                        return file_name
                    else:
                        logging.warning(f"⚠️ Appx Signed PDF Download via API failed with {resp}!!")
                        d_url = d_url.replace("static-wsb.classx.co.in", "appx-wsb-gcp-mcdn.akamai.net.in").replace("static-wsb.appx.co.in", "appx-wsb-gcp-mcdn.akamai.net.in").replace("static-db.classx.co.in", "appxcontent.kaxa.in").replace("static-db.appx.co.in", "appxcontent.kaxa.in").replace("static-db-v2.classx.co.in", "appx-content-v2.classx.co.in").replace("static-db-v2.appx.co.in", "appx-content-v2.classx.co.in").strip()
                        os.system(f'yt-dlp -o "{file_name}" "{d_url}" --add-header "User-Agent:okhttp/5.0.0-alpha.2" --add-header "Accept-Encoding:gzip" --add-header "Referer:https://appx-play.akamai.net.in/" -R 25 --fragment-retries 25')
                        await appx_dl(file_name, key)
                        if os.path.exists(file_name):
                            return file_name
                        else:
                            raise FileNotFoundError(f"Appx Signed-PDF {file_name} not Found.")

            # Case 2: Appx signed PDF (with ?URLPrefix) – use yt-dlp WITHOUT domain replacement
            elif "?URLPrefix" in url:
                # Do NOT replace domain; use original signed URL
                os.system(f'yt-dlp -o "{file_name}" "{url}" --add-header "User-Agent:okhttp/5.0.0-alpha.2" --add-header "Accept-Encoding:gzip" --add-header "Referer:https://appx-play.akamai.net.in/" -R 25 --fragment-retries 25')
                if os.path.exists(file_name):
                    return file_name
                else:
                    raise ValueError("yt-dlp failed to download signed PDF")
            
            # Case 3: Other Appx domains (without ?URLPrefix) – replace domain and use yt-dlp
            elif ('classx.co.in' in url or 'appx.co.in' in url) and not "*" in url:
                url = url.replace("static-wsb.classx.co.in", "appx-wsb-gcp-mcdn.akamai.net.in").replace("static-wsb.appx.co.in", "appx-wsb-gcp-mcdn.akamai.net.in").replace("static-db.classx.co.in", "appxcontent.kaxa.in").replace("static-db.appx.co.in", "appxcontent.kaxa.in").replace("static-db-v2.classx.co.in", "appx-content-v2.classx.co.in").replace("static-db-v2.appx.co.in", "appx-content-v2.classx.co.in").strip()
                os.system(f'yt-dlp -o "{file_name}" "{url}" --add-header "User-Agent:okhttp/5.0.0-alpha.2" --add-header "Accept-Encoding:gzip" --add-header "Referer:https://appx-play.akamai.net.in/" -R 25 --fragment-retries 25')
                if os.path.exists(file_name):
                    return file_name
            
            # Case 4: CW PDF
            elif "cwmediabkt99" in url:
                scraper = cloudscraper.create_scraper()
                response = scraper.get(url)
                if response.status_code != 200:
                    raise ValueError(f"CW PDF : {response.status_code} - {response.text}")
                with open(file_name, 'wb') as file:
                    file.write(response.content)
                return file_name

            # Case 5: DOC files (convert via API)
            elif ".doc" in url.lower():
                url = f'{my_hrk_api}/adda/pdf?url={url}&token={token}&authorization={my_auth_token}'
                os.system(f'yt-dlp -o "{file_name}" "{url}" -R 25 --fragment-retries 25')
                return file_name

            # ========== FIXED CASE 6: Direct PDF download with filename sanitization ==========
            elif url.lower().endswith('.pdf') or '.pdf?' in url:
                # 🔥 Sanitize filename: remove non-ASCII, emojis, extra spaces
                safe_name = re.sub(r'[^\w\s.-]', '', file_name)   # remove special chars
                safe_name = re.sub(r'\s+', '_', safe_name)        # spaces to underscore
                safe_name = safe_name[:100]                       # limit length
                if not safe_name:
                    safe_name = "downloaded"
                
                # Ensure .pdf extension
                if not safe_name.endswith('.pdf'):
                    safe_name += '.pdf'
                
                async with session.get(url, allow_redirects=True) as resp:
                    if resp.status == 200:
                        content_type = resp.headers.get('Content-Type', '').lower()
                        # Accept PDF or binary stream
                        if 'pdf' in content_type or 'octet-stream' in content_type or url.lower().endswith('.pdf'):
                            with open(safe_name, 'wb') as fd:
                                async for chunk in resp.content.iter_chunked(8192):
                                    fd.write(chunk)
                            return safe_name
                        else:
                            # Maybe HTML error page
                            sample = (await resp.read())[:200]
                            raise ValueError(f"Unexpected Content-Type: {content_type}, sample: {sample}")
                    else:
                        raise ValueError(f"Failed to download PDF, status: {resp.status}")
            
            # Default: fallback to yt-dlp
            else:
                os.system(f'yt-dlp -o "{file_name}" "{url}" -R 25 --fragment-retries 25')
                return file_name
                
        except Exception as e:
            if attempt < 3:
                logging.warning(f"⚠️ {file_name} Download Failed in ({attempt}. Attempt) due to : {e}")
                await asyncio.sleep(3)
            else:
                logging.error(f"❌ All Retry Attempts Failed for PDF Download.")
                return file_name
    
async def send_pdf(bot: Client, chatId, session: aiohttp.ClientSession, d_url: str, name, EX, cc1, Token=None, thumb2=None, thread_id=None):
    PdfFile = await download_pdf(session, d_url, f'{name}.pdf', Token)
    await asyncio.sleep(1)

    if os.path.exists('thumb2.jpg') and thumb2:
        SentPdf = await bot.send_document(chatId, PdfFile, file_name=f'{name}_{EX}.pdf', caption=cc1, thumb=thumb2, message_thread_id=thread_id)
    else:
            try:
                doc = fitz.open(PdfFile)
                page = doc.load_page(0)
                pix = page.get_pixmap()
                pix.save("Newthumb2.jpg")
            except Exception as exc:
                logging.warning(f"Could not generate PDF thumbnail for {PdfFile}: {exc}")
            finally:
                try: doc.close()
                except Exception: pass
            SentPdf = await bot.send_document(chatId, PdfFile, file_name=f'{name}_{EX}.pdf', caption=cc1, thumb="Newthumb2.jpg" if os.path.exists('Newthumb2.jpg') else None, message_thread_id=thread_id)
    return SentPdf


async def download_send_tests(bot: Client, m, session: aiohttp.ClientSession, name, url: str, cchtml, thumb2, thread_id):
    try:
        if "/appx/test/v3/" in url:
            async with session.get(url, headers={'authorization': my_auth_token}) as r:
                try:
                    resp = await r.json()
                except Exception:
                    resp = None
            if not resp or not isinstance(resp, dict):
                raise ValueError("Invalid response from Appx Test API")
            TestResp = requests.get(resp.get('url', '')).text
            HtmlFile = await generate_Mock_HTML(name, resp.get('time', 0), resp.get('marks', 0), resp.get('ques', 0), TestResp)
        
        elif "/appx/quiz/" in url:
            async with session.get(url, headers={'authorization': my_auth_token}) as r:
                try:
                    resp = await r.json()
                except Exception:
                    resp = None
            if not resp:
                raise ValueError("Invalid response from Appx Quiz API")
            HtmlFile = await make_APPX_quiz_HTML(name, resp)
            
        elif "https://www.testranking.in/?testId=" in url:
            try:
                resp = requests.get(f"https://www.testranking.in/admin/api/questions-solutions-mob/{url.split('testId=')[1]}/en" , headers={'authorization': my_auth_token}).json()
            except Exception:
                resp = None
                
            if not resp or not isinstance(resp, dict) or 'data' not in resp:
                raise ValueError("Invalid response from TestRanking API")
                
            NewData = []
            total_questions = 0
            for item in resp.get('data', []):
                if not item or not isinstance(item, dict): continue
                for idx, data in enumerate(item.get('all_questions', []), 1):
                    if not data or not isinstance(data, dict): continue
                    Ques = f"{data.get('question_en')}<br>{data.get('question_hi')}"
                    negative_marking = data.get('negative_score', '0')
                    NewData.append({"sr_no": idx, "question": Ques, "option_1": data.get('option_en_1'), "option_2": data.get('option_en_2'), "option_3": data.get('option_en_3'), "option_4": data.get('option_en_4'), "answer": data.get('answer_en'), "negative_marking": negative_marking, "positive_marking": data.get('marks'), "solution_heading": "Full Solution", "solution_text":data.get('solution_en')})
                    total_questions += 1
            HtmlFile = await generate_Mock_HTML(name, total_questions*1, total_questions*2, total_questions, NewData)
            
        elif "https://u1.oliveboard.in/exams/solution/" in url:
            HtmlFile = await generate_OliveBoard_Test(name, url)
            
        elif "adda247.com/" in url and url.endswith('.json'):
            HtmlFile = await generate_Adda247_Test(name, url)
            
        await asyncio.sleep(2)
        if os.path.exists(HtmlFile):
            SentHTML = await bot.send_document(m.chat.id, HtmlFile, caption=cchtml, thumb=thumb2, message_thread_id=thread_id)
            os.remove(HtmlFile)
            return SentHTML
    except Exception as e:
        logging.error(f"❌ Error in Making Test Html : {e}")
        if 'HtmlFile' in locals() and os.path.exists(HtmlFile): os.remove(HtmlFile)

async def pw_download_video(url, quality, name, keys):
    for attempt in range(1, 4):
        try:
            if not isinstance(keys, list):
                keys = [keys]
            #url = url.replace("master", f"master_{quality}")
            
            key_args = []
            for key in keys:
                key_args.extend(["--key", key])
            logging.info(f'🔓 Attempt {attempt} :: 🔗 Download Url : {url} ⪼ 🔑 PW KEY : {key_args}')
            
            mkv_file = f"{name}.mkv"
            if os.path.exists(mkv_file):
                os.remove(mkv_file)

            PwResult = subprocess.run([
                    "N_m3u8DL-RE", "--auto-select",
                    *key_args, url, "-M", "format=mkv",  
                    "--save-name", name, "--append-url-params", "-mt",
                    "--concurrent-download", "--thread-count", "64", "--no-log"
            ], check=True, capture_output=True)

            if PwResult.returncode != 0:
                raise subprocess.CalledProcessError(f"ReturnCode: {PwResult.returncode}, {PwResult.args}, {PwResult.stdout.decode()}, {PwResult.stderr.decode()}")
            if not os.path.exists(mkv_file):
                raise FileNotFoundError(f"Output file '{mkv_file}' not created. ReturnCode: {PwResult.returncode}")

            logging.info(f"✅ Decryption and download to {mkv_file} successful at {quality}p with key {keys}.")
            return mkv_file
        except Exception as e:
            if attempt < 3:
                logging.warning(f"❌ PW Download Failed in ({attempt}. Attempt) due to : {e}")
                await asyncio.sleep(3)
            else:
                logging.error(f"❌ All Retry Attempts Failed for PW.")
                return None

async def spayee_video(url, quality, name, keys):
    for attempt in range(1, 4):
        try:
            mkv_file = f"{name}.mkv"
            
            SpayeeResult = subprocess.run([
                "N_m3u8DL-RE",
                url,
                "-M", "format=mkv",
                "--save-name", name,
                "--auto-select", "--custom-hls-key", keys,
                "-mt", "--concurrent-download", "--thread-count", "64",
                "--no-log"
            ], check=True)

            if SpayeeResult.returncode != 0:
                raise subprocess.CalledProcessError(f"ReturnCode: {SpayeeResult.returncode}, {SpayeeResult.args}, {SpayeeResult.stdout}, {SpayeeResult.stderr}")
            if not os.path.exists(mkv_file):
                raise FileNotFoundError(f"Output file '{mkv_file}' not created. ReturnCode: {SpayeeResult.returncode}")

            logging.info(f"✅ Decryption and download to {mkv_file} successful with key {keys}.")
            return mkv_file
        except Exception as e:
            if attempt < 3:
                logging.warning(f"⚠️Spayee/Graphy Download Failed in ({attempt}. Attempt) due to : {e}")
                await asyncio.sleep(5)
            else:
                logging.error(f"❌ All Retry Attempts Failed for Spayee/Graphy.")
                return None

async def cipher_procoder_video(url, quality, name, keys):
    for attempt in range(1, 4):
        try:
            mkv_file = f"{name}.mkv"
            
            if not isinstance(keys, list):
                keys = [keys]
            key_args = []
            for key in keys:
                key_args.extend(["--key", key]) 
            logging.info(f'🔗 Download Url : {url} ⪼ 🔑 DRM KEY : {keys}')

            CipherResult = subprocess.run([
                "N_m3u8DL-RE",
                url,
                "-M", "format=mkv", "--save-name", name,
                "--auto-select", *key_args,
                "-mt", "--concurrent-download", "--thread-count", "64",
                "--no-log"
            ], check=True)

            if CipherResult.returncode != 0:
                raise subprocess.CalledProcessError(f"ReturnCode: {CipherResult.returncode}", CipherResult.args, CipherResult.stdout, CipherResult.stderr)
            if not os.path.exists(mkv_file):
                raise FileNotFoundError(f"Output file '{mkv_file}' not created. ReturnCode: {CipherResult.returncode}")

            logging.info(f"✅ Decryption and download to {mkv_file} successful with key {keys}.")
            return mkv_file
        except Exception as e:
            logging.warning(f"⚠️ Cipher DRM Download Failed in ({attempt}. Attempt) failed due to : {e}")
            if attempt < 3:
                await asyncio.sleep(3)
            else:
                logging.error(f"❌ All Retry Attempts Failed for Cipher DRM Download.")
                await check_and_clear_temp_files()
                return None

async def wait_for_drm_keys(session: aiohttp.ClientSession, url: str, my_auth_token: str):
    for attempt in range(1, 51):
        try:
            if "/drm" in url:
                async with session.get(f'{my_hrk_api}/classp?url={url}&authorization={my_auth_token}') as r:
                    try:
                        cp_resp = await r.json()
                    except Exception:
                        cp_resp = None
                        
                if cp_resp and isinstance(cp_resp, dict) and cp_resp.get("keys") and cp_resp.get('url'):
                    keys_arr = cp_resp['keys']
                    CpDrmUrl = cp_resp['url']
                    logging.info(f"[✔] Cp-DRM Keys Found {keys_arr}")
                    return CpDrmUrl, keys_arr
                else:
                    raise ValueError(f"Unable to fetch Drm-Keys : {cp_resp}")
            else:
                async with session.get(f'{my_hrk_api}/classp?url={url}&authorization={my_auth_token}') as r2:
                    try:
                        resp = await r2.json()
                    except Exception:
                        resp = None
                        
                if resp and isinstance(resp, dict) and resp.get("url"):
                    SignedUrl = resp['url']
                    return SignedUrl, None
                else:
                    raise ValueError(f"Unable to fetch Signed-Url {r2.status} : {resp}")
        except Exception as e:
            if attempt < 50:
                logging.warning(f"⚠️ ClassPlus Download Failed ({attempt} Attempt) due to : {e}")
                await asyncio.sleep(5)
            else:
                logging.error(f"❌ All Retry Attempts Failed for ClassPlus Download.")
                return url, None

async def drm_download_video(url, quality, name, keys):
    for attempt in range(1, 4):
        try:
            qual = f"bestvideo[height<={quality}]"
            
            if not isinstance(keys, list):
                keys = [keys]
            key_args = " ".join([f"--key {key}" for key in keys])
            decrypted_video_path = f"{name}_decrypted_video.mp4"
            decrypted_audio_path = f"{name}_decrypted_audio.m4a"
            merged_file = f"{name}.mp4"
            
            video_download = subprocess.run(
                f'yt-dlp -k --allow-unplayable-formats -f "{qual}" --fixup never "{url}" '
                f'--external-downloader aria2c --downloader-args "aria2c: -x 16 -j 32" -o "{name}_encrypted_video.mp4"',
                shell=True, capture_output=True, text=True)
        
            audio_download = subprocess.run(
                f'yt-dlp -k --allow-unplayable-formats -f ba --fixup never "{url}" '
                f'--external-downloader aria2c --downloader-args "aria2c: -x 16 -j 32" -o "{name}_encrypted_audio.m4a"',
                shell=True, capture_output=True, text=True)

            if video_download.returncode != 0:
                raise ValueError(f"Video dl Error with ReturnCode : {video_download.returncode}")
            if audio_download.returncode != 0:
                raise ValueError(f"Audio dl Error with ReturnCode : {audio_download.returncode}")

            video_decrypt = subprocess.run(f'mp4decrypt --show-progress {key_args} "{name}_encrypted_video.mp4" "{decrypted_video_path}"', shell=True, capture_output=True, text=True)
            audio_decrypt = subprocess.run(f'mp4decrypt --show-progress {key_args} "{name}_encrypted_audio.m4a" "{decrypted_audio_path}"', shell=True, capture_output=True, text=True)
            
            if video_decrypt.returncode != 0:
                raise ValueError(f"🔴 Video decrypt error\n{video_decrypt.stderr.decode()}")
            if audio_decrypt.returncode != 0:
                raise ValueError(f"🔴 Audio decrypt error\n{audio_decrypt.stderr.decode()}")
            
            merge_process = subprocess.run(f'ffmpeg -i "{decrypted_video_path}" -i "{decrypted_audio_path}" -c copy "{merged_file}"', shell=True, capture_output=True, text=True)

            if merge_process.returncode != 0: raise ValueError(f"🔴 Merge error: {merge_process.returncode}")
            if not os.path.exists(merged_file): raise FileNotFoundError(f"{merged_file} Not Found")

            for f in [f"{name}_encrypted_video.mp4", f"{name}_encrypted_audio.m4a", decrypted_video_path, decrypted_audio_path]:
                try:
                    if os.path.exists(f): os.remove(f)
                except Exception as e: logging.exception(f"[✘] Unable to remove {f} due to : {e}")
            return merged_file
        except Exception as e:
            if attempt < 3:
                logging.warning(f"⚠️ DRM Video download Failed in ({attempt} Attempt) due to : {e}")
                await asyncio.sleep(5)
            else:
                logging.error(f"❌ All Retry Attempts Failed.")
                return name + ".mp4"



def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"

def time_name():
    date = datetime.date.today()
    now = datetime.now()
    current_time = now.strftime("%H%M%S")
    return f"{date} {current_time}.mp4"

# ============== USING IN DL CMD ================
async def duration(filename):
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
        "default=noprint_wrappers=1:nokey=1", filename],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT)
    return float(result.stdout)

async def download_yt_video(name, video_url=None, audio_url=None):
    if video_url and audio_url:
        result = subprocess.run(['ffmpeg', '-y', '-i', video_url, '-i', audio_url, '-c', 'copy', f'{name}.mp4'], shell=True)
        if result.returncode != 0:
            raise ValueError(f"{result.returncode}\n{result.stderr.decode('utf-8', errors='replace')}")
    elif not audio_url and video_url:
        result = subprocess.run(f'yt-dlp --no-warning "{video_url}" -o "{name}.mp4"', shell=True)
        if result.returncode != 0:
            raise ValueError(f"ReturnCode : {result.returncode}")
    return f"{name}.mp4"
      
async def download_video(d_url, cmd, name):
    FileVariants = [f"{name}", f"{name}.webm", f"{name}.mp4", f"{name}.mp4.webm", f"{name}.mkv"]
    for file in FileVariants:
        if os.path.exists(file):
            os.remove(file)
    
    for attempt in range(1, 4):
        try:
            download_cmd = f'{cmd} --newline --progress -R 25 --fragment-retries 25 --socket-timeout 50 --external-downloader aria2c --downloader-args "aria2c:-x 16 -j 32 -s 16 -k 1M --file-allocation=none --optimize-concurrent-downloads=true"'
            logging.info(f"⚙️ Attempt {attempt} : {download_cmd}")

            process = await asyncio.create_subprocess_shell(download_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if process.stdout:
                while True:
                    line_bytes = await process.stdout.readline()
                    if not line_bytes:
                        break
                    line = line_bytes.decode('utf-8', errors="replace").strip()
                    if line:
                        logging.info(line)
            await process.wait()
            if process.returncode != 0:
                raise ValueError(f"ReturnCode : {process.returncode}")
 
            for file in FileVariants:
                if os.path.isfile(file):
                    return file
                
        except Exception as e:
            if attempt < 3:
                logging.warning(f"⚠️ Download failed ({attempt} Attempt) due to : {e}.")
                await asyncio.sleep(5)
            else:
                logging.error(f"❌ All Download Attempts Failed..")
                await check_and_clear_temp_files()
                return name + ".mp4"
            

def extract_first_bracket(name):
    opening = {'(': ')', '[': ']', '{': '}'}
    stack = []
    
    for i, char in enumerate(name):
        if not stack and char in opening:
            stack.append(opening[char])
            start = i + 1
        elif stack:
            if char in opening:
                stack.append(opening[char])
            elif char == stack[-1]:
                stack.pop()
                if not stack:
                    return name[start:i], name[i+1:].strip()
    return None, name  # no match found


async def get_or_create_topic(bot: Client, m: Message, name1, b_name, user_id):
    """Get or create a topic in the group, using only MongoDB for persistence"""
    if name1.startswith(("(", "[", "{")):
        t_name, v_name = extract_first_bracket(name1)

        # Try MongoDB cache
        topic_id = None
        result0 = ActiveUsersCollection.find_one({"userId": user_id, "bot": bot.me.username})
        if result0 and result0.get('TopicsData'):
            for data in result0["TopicsData"]:
                ChatId = data['chat_id']
                for topic in data['topics']:
                    if ChatId == m.chat.id and topic.get("topic_name") == t_name.upper():
                        topic_id = topic.get("topic_id")
                        break
        if topic_id: return topic_id

        # Create a new topic (always uppercase)
        topic = await bot.create_forum_topic(m.chat.id, t_name.upper())
        
        # Step 1: Try to push the topic if chat_id already exists in TopicsData
        result = ActiveUsersCollection.update_one(
            {"userId": user_id, "bot": bot.me.username, "TopicsData.chat_id": m.chat.id},
            {"$push": {"TopicsData.$.topics": {"topic_id": topic.id, "topic_name": t_name.upper()}}}
        )

        # Step 2: If chat_id doesn't exist, create a new entry with the chat_id and the topic
        if result.matched_count == 0:
            ActiveUsersCollection.update_one(
                {"userId": user_id, "bot": bot.me.username},
                {"$push": {"TopicsData": {"chat_id": m.chat.id, "topics": [{"topic_id": topic.id, "topic_name": t_name.upper()}]}}},
                upsert=True
            )

        pin_msg = await bot.send_message(m.chat.id, f"<blockquote><b>🏷 Topic Name :</b> {t_name.upper()}\n\n<b>📚 Course Name :</b> {b_name}</blockquote>", message_thread_id=topic.id)
        await bot.pin_chat_message(m.chat.id, pin_msg.id)
        return topic.id
    else:
        return m.message_thread_id


# ==================== ADVANCED WATERMARK FUNCTIONS ====================

# Color name to RGB mapping
def get_color_rgb(color_name: str):
    colors = {
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "red": (255, 0, 0),
        "blue": (0, 0, 255),
        "green": (0, 255, 0),
        "golden": (255, 215, 0),
        "yellow": (255, 255, 0),
        "orange": (255, 165, 0),
        "purple": (128, 0, 128),
        "pink": (255, 192, 203),
        "magenta": (255, 0, 255),
        "teal": (0, 128, 128),
        "sky blue": (135, 206, 235),
        "beige": (245, 245, 220),
        "mint": (189, 252, 201),
        "coral": (255, 127, 80),
        "sea green": (46, 139, 87),
        "khaki": (240, 230, 140),
        "brown": (165, 42, 42),
        "lime": (0, 255, 0),
        "maroon": (128, 0, 0),
        "turquoise": (64, 224, 208),
        "peach": (255, 218, 185),
        "crimson": (220, 20, 60),
        "rose": (255, 0, 127),
        "slate blue": (106, 90, 205),
        "gray": (128, 128, 128),
        "cyan": (0, 255, 255),
        "navy": (0, 0, 128),
        "olive": (128, 128, 0),
        "indigo": (75, 0, 130),
        "lavender": (230, 230, 250),
        "salmon": (250, 128, 114),
        "periwinkle": (204, 204, 255),
        "ivory": (255, 255, 240),
        "chartreuse": (127, 255, 0),
    }
    return colors.get(color_name.lower(), (255, 255, 255))


# Font mapping: display name -> file path (INCLUDING NOTO SANS)
FONT_MAPPING = {
    "Comic Sans BD": "Modules/Fonts/comicbd.ttf",
    "Comic Sans I": "Modules/Fonts/comici.ttf",
    "DejaVu Sans": "Modules/Fonts/DejaVuSans.ttf",
    "Gabriola": "Modules/Fonts/Gabriola.ttf",
    "Himalaya": "Modules/Fonts/himalaya.ttf",
    "Impact": "Modules/Fonts/impact.ttf",
    "Inkfree": "Modules/Fonts/Inkfree.ttf",
    "Monotype Corsiva": "Modules/Fonts/MTCORSVA.TTF",
    "MT Extra": "Modules/Fonts/MTEXTRA.TTF",
    "Segoe Script Bold": "Modules/Fonts/segoescb.ttf",
    "Symbol": "Modules/Fonts/symbol.ttf",
    "Webdings": "Modules/Fonts/webdings.ttf",
    "Wingdings": "Modules/Fonts/wingding.ttf",
    "Wingdings 2": "Modules/Fonts/WINGDNG2.TTF",
    "Wingdings 3": "Modules/Fonts/WINGDNG3.TTF",
    "Arial": "Modules/Fonts/arial.ttf",
    "Bookshelf Symbol 7": "Modules/Fonts/BSSYM7.TTF",
    "Calibri": "Modules/Fonts/calibrii.ttf",
    "Noto Sans": "Modules/Fonts/NotoSans-Regular.ttf",
}

FONT_LIST = list(FONT_MAPPING.keys())

def get_font_path(font_name: str) -> str:
    """Return file path for given font name, fallback to Noto Sans."""
    return FONT_MAPPING.get(font_name, "Modules/Fonts/NotoSans-Regular.ttf")


async def generate_watermark_preview(text, font_name, color_name, font_size_str, opacity_str):
    """Create a preview image with watermark settings"""
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    img = Image.new('RGB', (600, 400), color='black')
    draw = ImageDraw.Draw(img)
    
    font_path = get_font_path(font_name)
    font_size = int(font_size_str)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()
    
    opacity = int(float(opacity_str) * 255)
    color_rgb = get_color_rgb(color_name)
    
    txt_img = Image.new('RGBA', img.size, (0,0,0,0))
    txt_draw = ImageDraw.Draw(txt_img)
    
    bbox = txt_draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (600 - text_width) // 2
    y = (400 - text_height) // 2
    
    txt_draw.text((x, y), text, font=font, fill=(*color_rgb, opacity))
    
    img = img.convert('RGBA')
    combined = Image.alpha_composite(img, txt_img)
    
    preview_path = f"preview_{font_name.replace(' ', '_')}.png"
    combined.save(preview_path)
    return preview_path


async def apply_advanced_watermark(input_thumb, text, font_name, color_name, font_size, opacity):
    """Apply watermark with custom font, size, opacity to thumbnail"""
    from PIL import Image, ImageDraw, ImageFont
    
    img = Image.open(input_thumb).convert("RGBA")
    txt_layer = Image.new('RGBA', img.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt_layer)
    
    font_path = get_font_path(font_name)
    try:
        font = ImageFont.truetype(font_path, int(font_size))
    except:
        font = ImageFont.load_default()
    
    color_rgb = get_color_rgb(color_name)
    alpha = int(float(opacity) * 255)
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (img.width - text_width) // 2
    y = (img.height - text_height) // 2
    
    draw.text((x, y), text, font=font, fill=(*color_rgb, alpha))
    
    out = Image.alpha_composite(img, txt_layer)
    output_path = f"{input_thumb}_wm.jpg"
    out.convert('RGB').save(output_path)
    return output_path


async def send_vid(bot: Client, m: Message, cc, filename, thumb, name, DumpThreadId, thread_id, WatermarkText, WatermarkColor, CreditName, user_id):
    from DbNew import get_user_status
    loop = asyncio.get_event_loop()
    
    subprocess.run(f'ffmpeg -i "{filename}" -ss 00:00:02 -vframes 1 -q:v 2 -y "{filename}.jpg"', shell=True)
    base_thumb = thumb if thumb != "no" and os.path.exists(thumb) else f"{filename}.jpg"
    
    # Fetch user watermark settings
    user = get_user_status(user_id, bot.me.username)
    data = user.get('data', {})
    
    if data.get('watermarkEnabled', 'yes') == 'no':
        WatermarkText = None  # Skip watermark
    
    # Apply advanced watermark if enabled
    if WatermarkText and WatermarkText.lower() != 'no':
        font_name = data.get('fontStyle', 'Noto Sans')
        font_size = data.get('fontSize', '80')
        opacity = data.get('opacity', '0.8')
        color_name = data.get('watermarkColor', WatermarkColor)
        
        try:
            thumbnail = await apply_advanced_watermark(base_thumb, WatermarkText, font_name, color_name, font_size, opacity)
        except Exception as e:
            logging.warning(f"Advanced watermark failed: {e}, using simple watermark")
            # Fallback to simple watermark
            thumbnail = base_thumb
            try:
                img = Image.open(thumbnail)
                draw = ImageDraw.Draw(img)
                width, height = img.size
                font_size_simple = int(width // 12)
                font = ImageFont.truetype("Modules/Tools/waltographUI.ttf", font_size_simple)
                bbox = draw.textbbox((0, 0), WatermarkText.strip(), font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                x = (width - text_width) / 2
                y = (height - text_height) / 2
                draw.text((x, y), WatermarkText.strip(), font=font, fill=WatermarkColor)
                thumbnail = f"{filename}_watermarked.jpg"
                img.save(thumbnail)
            except:
                thumbnail = base_thumb
    else:
        thumbnail = base_thumb
    
    dur = int(await duration(filename))
    file_size = os.path.getsize(filename)
    max_size = 1.85 * 1024 * 1024 * 1024  # 1.85 GB in bytes
    gb_size = 1 * 1024 * 1024 * 1024
    mb_size = 1 * 1024 * 1024
    f_size = f"{file_size / gb_size:.2f} GB" if file_size > gb_size else f"{file_size / mb_size:.2f} MB"

    start_time = time.time()
    SentMessage = FirstMessage = None

    output_dir = name
    if file_size > max_size:
        splitting_msg = await bot.send_message(m.chat.id,
            f"<blockquote>🔧 <b>Video Splitting In Progress...</b></blockquote>\n\n"
            f"╭━━━━━━━━━━━━━━━━━➣\n"
            f"┣⪼ 🪄 <b>Status :</b> <i>Breaking video into smaller parts...</i>\n"
            f"┣⪼ 📂 <b>Action :</b> <i>Processing & Splitting</i>\n"
            f"┣⪼ 🔄 <b>Please Wait :</b> <i>This might take a some times.</i>\n"
            f"╰━━━━━━━━━━━━━━━━━➣\n\n"
            f"💡 <b>𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘 :</b> {CreditName}",
            message_thread_id=thread_id
        )

        os.makedirs(output_dir, exist_ok=True)
        output_pattern = os.path.join(output_dir, "part_%03d.mkv")
        try:
            split_size_mb = 1850  # Size in MB
            subprocess.run(["mkvmerge", "-o", output_pattern, "--split", f"size:{split_size_mb}M", filename], check=True)
        except subprocess.CalledProcessError as e:
            await bot.send_message(m.chat.id, f"❌ Splitting failed: {e}", message_thread_id=thread_id)
            return 0
        
        # Get and sort segment files numerically
        video_parts = sorted(glob.glob(os.path.join(output_dir, "*.mkv")) + glob.glob(os.path.join(output_dir, "*.mp4")), key=lambda x: int(''.join(filter(str.isdigit, os.path.basename(x)))))

        if len(video_parts) == 0:
            await bot.send_message(m.chat.id, "❌ No segments found. Splitting may have failed.", message_thread_id=thread_id)
            return 0

        for i, parted_file in enumerate(video_parts, 1):
            part_dur = int(await duration(parted_file))
            try:
                part_caption = f"⋅ ⋅ ─ ─ <b><i>Part {i:02d} of {len(video_parts):02d}</i></b> ─ ─ ⋅ ⋅ \n{cc}"
                SentMessage = await bot.send_video(m.chat.id, parted_file, caption=part_caption, supports_streaming=True, height=720, width=1280, thumb=thumbnail, duration=part_dur, message_thread_id=thread_id, progress=progress_bar, progress_args=(splitting_msg, start_time, CreditName))
            except Exception as e:
                logging.error(f"⚠️ Error uploading part {i:02d}: {e} -- Trying to send as document instead...")
                SentMessage = await bot.send_document(m.chat.id, parted_file, caption=part_caption, message_thread_id=thread_id)
            
            if not FirstMessage: # 🟢 Store Only first Part
                FirstMessage = SentMessage
            if os.path.exists(parted_file): os.remove(parted_file)
        await splitting_msg.delete()

    else:
            reply = await bot.send_message(m.chat.id,
                f"<blockquote>📤 **𝐔𝐏𝐋𝐎𝐀𝐃𝐈𝐍𝐆 𝐕𝐈𝐃𝐄𝐎** 📤</blockquote>\n\n🗃️ **File Size :**  {f_size}\n📂 **File Name :** {name}\n\n"
                f"╔══════════════════════════╗\n"
                f"╠  ✨ **𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘: {CreditName}** \n"
                f"╚══════════════════════════╝",  message_thread_id=thread_id) 
            try:
                SentMessage = await loop.run_in_executor(None, lambda: bot.send_video(m.chat.id, filename, caption=cc, supports_streaming=True, height=720, width=1280, thumb=thumbnail, duration=dur, message_thread_id=thread_id, progress=progress_bar, progress_args=(reply, start_time, CreditName)))
            except Exception as e:
                logging.error(f"⚠️ **Error uploading video:** {str(e)} -- Trying to send as document instead...")
                SentMessage = await bot.send_document(m.chat.id, filename, caption=cc, message_thread_id=thread_id)
            FirstMessage = SentMessage
            await reply.delete()
    for f in [f"{filename}.jpg", f"{filename}_watermarked.jpg", filename]:
        try:
            if f and os.path.exists(f): os.remove(f)
        except Exception as e: logging.exception(f"[✘] Unable to remove {f} : {e}")
    return FirstMessage


async def send_msg_in_dump(LogDumpGrp, SentMessage, DumpThreadId=None, filename="Message"):
    try:
        if DumpThreadId and DumpThreadId != 0 and DumpThreadId != '0' :
            await SentMessage.copy(LogDumpGrp, message_thread_id=DumpThreadId)
    except Exception as ex:
        pass


async def check_and_clear_temp_files():
    """Cleans up temporary files like .mp4, .mkv, .zip, .pdf in the current directory."""
    for dir in ["/app/somebody_noobs_extracted_zip", "somebody_noobs_extracted_zip"]:
        if os.path.exists(dir):
            shutil.rmtree(dir)
            logging.info(f"[✔] {dir} has been removed from os...")
    for temp_file in glob.glob(f'*.mp4')+ glob.glob('*.m4a') + glob.glob('*.mp4.*') + glob.glob('*.mkv') + glob.glob('*.mkv.*') + glob.glob('*.pdf') + glob.glob('*.ytdl') + glob.glob('*.jpg'):
        try:
            if os.path.exists(temp_file): os.remove(temp_file)
        except Exception as e: logging.exception(f"[✘] Unable to remove {temp_file} : {e}")



def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002500-\U00002BEF"  # chinese char
        "\U00002702-\U000027B0"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # dingbats
        "\u3030"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)
