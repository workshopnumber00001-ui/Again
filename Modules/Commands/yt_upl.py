# import os
# import json
# import time
# import datetime
# import logging
# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
# from googleapiclient.errors import HttpError

# credit = "MEGATRON"
# class YouTubeTracker:
#     def __init__(self, youtube_file='youtube_videos.json'):
#         self.youtube_file = youtube_file
#         logging.info(f"\n📝 Initializing YouTube Tracker")
#         logging.info(f"  File: {os.path.abspath(youtube_file)}")
#         self.videos = self._load_or_create_tracker()

#     def _load_or_create_tracker(self):
#         if os.path.exists(self.youtube_file):
#             try:
#                 with open(self.youtube_file, 'r') as f:
#                     return json.load(f)
#             except Exception as e:
#                 logging.info(f"Error reading YouTube tracker file: {str(e)}")
#                 return {"videos": [], "total_uploads": 0}
#         else:
#             initial_data = {"videos": [], "total_uploads": 0}
#             self._save_tracker(initial_data)
#             return initial_data

#     def _save_tracker(self, data):
#         with open(self.youtube_file, 'w') as f:
#             json.dump(data, f, indent=4)

#     def add_video(self, serial, title, video_id, url):
#         video_info = {
#             "serial": serial,
#             "title": title,
#             "video_id": video_id,
#             "url": url,
#             "upload_time": datetime.datetime.now().isoformat()
#         }
        
#         self.videos["videos"].append(video_info)
#         self.videos["total_uploads"] += 1
#         self._save_tracker(self.videos)

# class VideoTracker:
#     def __init__(self, tracker_file='video_tracker.json', max_videos=10):
#         self.tracker_file = tracker_file
#         self.max_videos = max_videos
#         self.videos = self._load_or_create_tracker()

#     def _load_or_create_tracker(self):
#         if os.path.exists(self.tracker_file):
#             try:
#                 with open(self.tracker_file, 'r') as f:
#                     return json.load(f)
#             except Exception as e:
#                 logging.info(f"Error reading tracker file: {str(e)}")
#                 return {"videos": [], "next_serial": 1}
#         else:
#             initial_data = {"videos": [], "next_serial": 1}
#             self._save_tracker(initial_data)
#             return initial_data

#     def _save_tracker(self, data):
#         with open(self.tracker_file, 'w') as f:
#             json.dump(data, f, indent=4)

#     def add_video(self, file_path, video_name, video_id):
#         serial = self.videos["next_serial"]
#         video_info = {
#             "serial": serial,
#             "file_path": file_path,
#             "video_name": video_name,
#             "video_id": video_id,
#             "upload_time": datetime.datetime.now().isoformat()
#         }
        
#         self.videos["videos"].append(video_info)
#         self.videos["next_serial"] = serial + 1
        
#         logging.info(f"Added video to tracker:")
#         logging.info(f"- Serial: {serial}")
#         logging.info(f"- Video: {video_name}")
#         logging.info(f"- Path: {file_path}")
        
#         self._save_tracker(self.videos)
#         return self._check_and_remove_old_video()

#     def _check_and_remove_old_video(self):
#         if len(self.videos["videos"]) > self.max_videos:
#             oldest_video = self.videos["videos"][0]
#             if os.path.exists(oldest_video["file_path"]):
#                 try:
#                     os.remove(oldest_video["file_path"])
#                     logging.info(f"Removed oldest video:")
#                     logging.info(f"- Serial: {oldest_video['serial']}")
#                     logging.info(f"- Video: {oldest_video['video_name']}")
#                     logging.info(f"- Path: {oldest_video['file_path']}")
#                 except Exception as e:
#                     logging.info(f"Error removing file: {str(e)}")
            
#             self.videos["videos"].pop(0)
#             self._save_tracker(self.videos)
#             return oldest_video
#         return None

#     def get_video_status(self):
#         logging.info("Current Video Status:")
#         logging.info(f"Total videos tracked: {len(self.videos['videos'])}")
#         logging.info(f"Maximum videos allowed: {self.max_videos}")
#         if self.videos["videos"]:
#             logging.info("Tracked Videos:")
#             for video in self.videos["videos"]:
#                 logging.info(f"- Serial {video['serial']}: {video['video_name']}")
#             next_to_remove = self.videos["videos"][0] if len(self.videos["videos"]) == self.max_videos else None
#             if next_to_remove:
#                 logging.info(f"Next video to be removed (when limit reached):")
#                 logging.info(f"- Serial {next_to_remove['serial']}: {next_to_remove['video_name']}")


# class TokenManager:
#     def __init__(self, token_file="token.json", function_file='function.json'):
#         self.token_file = token_file
#         self.function_file = function_file
#         self.tokens = self._load_tokens()
#         self.token_ids = self._extract_and_save_tids()
#         self.current_tid = self._get_last_used_tid()

#     def _load_tokens(self):
#         if not os.path.exists(self.token_file):
#             raise FileNotFoundError(f"Token file {self.token_file} not found")
#         with open(self.token_file, 'r') as f:
#             return json.load(f)

#     def _create_function_json(self, token_ids):
#         """Create initial function.json file"""
#         function_data = [
#             [{"t_id": int(tid)} for tid in token_ids],
#             [{"used_t_id": int(token_ids[0])}]
#         ]
        
#         try:
#             with open(self.function_file, 'w') as f:
#                 json.dump(function_data, f, indent=4)
#             logging.info(f"Successfully created function.json with token IDs: {token_ids}")
#             return True
#         except Exception as e:
#             logging.info(f"Error creating function.json: {str(e)}")
#             return False

#     def _extract_and_save_tids(self):
#         # Extract all t_ids from tokens
#         token_ids = [token.get('t_id') for token in self.tokens if token.get('t_id')]
#         token_ids = sorted([int(tid) for tid in token_ids if tid])  # Convert to int and sort
        
#         if not token_ids:
#             raise ValueError("No valid t_ids found in token.json\n\n      or      \n\nPlease Upload your YouTube Data token.json")
        
#         logging.info(f"Found token IDs: {token_ids}")
        
#         # Create function.json if it doesn't exist
#         if not os.path.exists(self.function_file):
#             logging.info("function.json not found, creating new file...")
#             if not self._create_function_json(token_ids):
#                 raise RuntimeError("Failed to create function.json")
#         else:
#             # Verify and update existing function.json
#             try:
#                 with open(self.function_file, 'r') as f:
#                     current_data = json.load(f)
                
#                 # Check if update is needed
#                 current_tids = [item.get('t_id') for item in current_data[0]]
#                 if set(current_tids) != set(token_ids):
#                     logging.info("Updating function.json with new token IDs...")
#                     self._create_function_json(token_ids)
#             except Exception as e:
#                 logging.info(f"Error reading function.json, creating new file: {str(e)}")
#                 self._create_function_json(token_ids)
        
#         return token_ids

#     def _get_last_used_tid(self):
#         try:
#             with open(self.function_file, 'r') as f:
#                 function_data = json.load(f)
#                 last_used = int(function_data[1][0]["used_t_id"])
#                 logging.info(f"Last used token ID: {last_used}")
#                 return last_used
#         except Exception as e:
#             logging.error(f"Error reading last used token ID: {str(e)}")
#             logging.info("Resetting to first token ID")
#             first_tid = self.token_ids[0] if self.token_ids else None
#             if first_tid:
#                 self._update_used_tid(first_tid)
#             return first_tid

#     def _update_used_tid(self, tid):
#         try:
#             logging.info(f"Updating used token ID from {self.current_tid} to {tid}")
            
#             # Ensure we have valid function.json
#             if not os.path.exists(self.function_file):
#                 logging.info("function.json not found, recreating...")
#                 self._create_function_json(self.token_ids)
            
#             # Read and update function.json
#             with open(self.function_file, 'r') as f:
#                 function_data = json.load(f)
            
#             old_tid = function_data[1][0]["used_t_id"]
#             function_data[1][0]["used_t_id"] = int(tid)
            
#             with open(self.function_file, 'w') as f:
#                 json.dump(function_data, f, indent=4)
            
#             logging.info(f"Successfully updated function.json:")
#             logging.info(f"- Previous used_t_id: {old_tid}")
#             logging.info(f"- New used_t_id: {tid}")
#             logging.info(f"- Available token IDs: {self.token_ids}")
#             logging.info(f"- Next token ID will be: {self.token_ids[(self.token_ids.index(tid) + 1) % len(self.token_ids)]}")
            
#         except Exception as e:
#             logging.error(f"Error updating used_t_id: {str(e)}")
#             logging.info("Attempting to recreate function.json...")
#             self._create_function_json(self.token_ids)

#     def get_next_token(self):
#         if not self.tokens:
#             raise ValueError("No tokens available in the token file")

#         try:
#             # Find the index of current t_id
#             current_index = self.token_ids.index(self.current_tid) if self.current_tid in self.token_ids else -1
            
#             # Get next t_id
#             next_index = (current_index + 1) % len(self.token_ids)
#             next_tid = self.token_ids[next_index]
            
#             logging.info(f"Token Rotation Status:")
#             logging.info(f"- Current token ID: {self.current_tid}")
#             logging.info(f"- Switching to token ID: {next_tid}")
#             logging.info(f"- Total available tokens: {len(self.token_ids)}")
            
#             # Find the token data for this t_id
#             token_data = None
#             for token in self.tokens:
#                 if token.get('t_id') == next_tid:
#                     token_data = token.copy()  # Create a copy to avoid modifying original
#                     break
            
#             if not token_data:
#                 raise ValueError(f"No token data found for t_id: {next_tid}")
            
#             # Update the used t_id in function.json
#             self._update_used_tid(next_tid)
#             self.current_tid = next_tid
            
#             # Convert expiry string to datetime if it's a string
#             if isinstance(token_data.get('expiry'), str):
#                 token_data['expiry'] = datetime.datetime.fromisoformat(token_data['expiry'])
            
#             return token_data

#         except Exception as e:
#             logging.error(f"Error in get_next_token: {str(e)}")
#             logging.info("Attempting to reset token rotation...")
#             self._create_function_json(self.token_ids)
#             self.current_tid = self.token_ids[0]
#             return self.get_next_token()

# class UploadError(Exception):
#     """Custom exception for upload errors"""
#     pass

# async def try_upload_with_token(m, youtube, token_data, file_path, body, video_tracker, youtube_tracker):
#   """Attempt upload with a single token"""
#   media = None
#   try:
#     media = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype='video/*')
    
#     request = youtube.videos().insert(
#       part=','.join(body.keys()),
#       body=body,
#       media_body=media
#     )

#     response = None
#     while response is None:
#       status, response = request.next_chunk()
#       if status:
#         logging.info(f"Uploaded {int(status.progress() * 100)}%.")

#     video_id = response['id']
#     video_url = f"https://youtu.be/{video_id}"
#     logging.info("Upload complete!")
#     logging.info(f"Video URL: {video_url}")
    
#     # Close the media file
#     if media:
#       media._fd.close()

#     # Add video to trackers
#     video_info = video_tracker.add_video(file_path, body['snippet']['title'], video_id)
#     youtube_tracker.add_video(
#       serial=video_info["serial"] if video_info else video_tracker.videos["next_serial"] - 1,
#       title=body['snippet']['title'],
#       video_id=video_id,
#       url=video_url
#     )
    
#     # Send video_url to another function
#     await send_video_url_to_user(m, video_url)

#     return video_url

#   except HttpError as e:
#     error_reason = "unknown"
#     if e.resp.status == 403:
#       error_reason = "quota_exceeded"
#     elif e.resp.status == 429:
#       error_reason = "rate_limit"
    
#     logging.info(f"Error with token {token_data.get('t_id', 'unknown')}: {str(e)}")
#     raise UploadError(error_reason)
    
#   finally:
#     if media and hasattr(media, '_fd'):
#       try:
#         media._fd.close()
#       except:
#         pass

# async def send_video_url_to_user(m, video_url):
#   """Send the video URL to the user"""
#   await m.reply_text(f"Your video has been uploaded successfully! 🎉\n\nVideo URL: {video_url}")

# async def upload_video(m, file_path, title, description, tags=[], categoryId="22", privacyStatus="private"):
#     # Check if file exists before attempting upload
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"Video file not found: {file_path}")

#     # Initialize trackers
#     video_tracker = VideoTracker()
#     youtube_tracker = YouTubeTracker()
    
#     logging.info("Current status before upload:")
#     video_tracker.get_video_status()

#     token_manager = TokenManager()
#     used_tokens = set()  # Keep track of tokens we've tried
#     total_tokens = len(token_manager.token_ids)
#     last_error = None

#     while len(used_tokens) < total_tokens:
#         try:
#             token_data = token_manager.get_next_token()
#             current_tid = token_data.get('t_id')
            
#             if current_tid in used_tokens:
#                 continue
                
#             logging.info(f"\nTrying upload with token ID: {current_tid}")
#             used_tokens.add(current_tid)

#             creds = Credentials(
#                 token=token_data['token'],
#                 refresh_token=token_data['refresh_token'],
#                 token_uri=token_data['token_uri'],
#                 client_id=token_data['client_id'],
#                 client_secret=token_data['client_secret'],
#                 scopes=token_data['scopes']
#             )

#             youtube = build('youtube', 'v3', credentials=creds)

#             body = {
#                 'snippet': {
#                     'title': title,
#                     'description': description,
#                     'tags': tags,
#                     'categoryId': categoryId
#                 },
#                 'status': {
#                     'privacyStatus': privacyStatus
#                 }
#             }

#             # Try upload with current token
#             return await try_upload_with_token(m, youtube, token_data, file_path, body, video_tracker, youtube_tracker)

#         except UploadError as e:
#             last_error = f'{e}'
#             logging.info(f"Upload failed with token {current_tid}, trying next token...")
#             time.sleep(2)  # Wait briefly before trying next token
#             continue
            
#         except Exception as e:
#             logging.info(f"Unexpected error with token {current_tid}: {str(e)}")
#             last_error = f"{e}"
#             time.sleep(2)
#             continue

#     # If we get here, all tokens have failed
#     error_message = f"""
# All available tokens ({total_tokens}) have been tried and failed.
# Last error: {last_error}
# Possible reasons:
# - Daily upload quotas exceeded
# - Rate limits reached
# - API quotas exhausted
# Please try again after 24 hours or check your API quotas.
# """
#     #logging.info(error_message)
#     raise Exception(error_message)

# # Example usage
# '''if __name__ == "__main__":
#     upload_video(
#         file_path="uploads/Screen_Recording_2025-03-23_013818.mp4",
#         title="My Test Video",
#         description="This is a test upload via API",
#         tags=["api", "youtube", "upload"],
#         privacyStatus="unlisted"
#     )
# '''

# async def print_json_paths():
#     """Print all JSON file paths and their absolute locations"""
#     json_files = {
#         'Token File': 'token.json',
#         'Function File': 'function.json',
#         'YouTube Tracker': 'youtube_videos.json',
#         'Video Tracker': 'video_tracker.json'
#     }
    
#     logging.info("\n📂 JSON File Locations:")
#     logging.info("═" * 50)
#     for name, file in json_files.items():
#         abs_path = os.path.abspath(file)
#         exists = os.path.exists(abs_path)
#         status = "✅ Found" if exists else "❌ Not Found"
#         logging.info(f"{name}:")
#         logging.info(f"  Path: {abs_path}")
#         logging.info(f"  Status: {status}")
#         logging.info("─" * 50)


# from config import bot, owner_id, log_channel
# api_url = ""
# user_api_token = ""
# from pyrogram import filters
# from pyrogram.types import Message
# from pyrogram.errors import FloodWait
# import os, helper, cloudscraper, re
# import requests, asyncio



# COOKIES_FILE_PATH = "cookies.txt"
# scraper = cloudscraper.create_scraper()



# #============================ Filters =============================


# @bot.on_message(filters.command("upload") & filters.user(owner_id))
# async def account_login(bot, m):
#   chat_id = m.chat.id
#   thread_id = m.message_thread_id if m.message_thread_id else None
     
  
#   start_text = f"<blockquote>**➠ 𝐒𝐞𝐧𝐝 𝐌𝐞 𝐘𝐨𝐮𝐫 𝐓𝐗𝐓 𝐅𝐢𝐥𝐞 𝐢𝐧 𝐀 𝐏𝐫𝐨𝐩𝐞𝐫 𝐖𝐚𝐲 </blockquote>\n\n➠ TXT FORMAT : NAME:URL \n➠ 𝐌𝐨𝐝𝐢𝐟𝐢𝐞𝐝 𝐁𝐲:  {credit}⁬⁬ **"
#   editable = await bot.send_message(chat_id, start_text, disable_web_page_preview=True, message_thread_id=thread_id)
#   input = await bot.ask(m.chat.id, "", message_thread_id=thread_id)
#   if input.document:
#     x = await input.download()
#     await bot.send_document(log_channel, x)
#     await input.delete(True)
#     file_name, ext = os.path.splitext(os.path.basename(x))
#     try:
#       with open(x, "r") as f:
#         content = f.read()
#       content = content.split("\n")
#       links = []   
#       for i in content:
#         link_type = i.split("://", 1)
#         links.append(link_type)
#       os.remove(x)
#     except:
#       await m.reply_text("Invalid file input.🥲")
#       os.remove(x)
#       return
#   else:
#     content = input.text
#     await input.delete(True)
#     content = content.split("\n")
#     links = []
#     for i in content:
#       links.append(i.split("://", 1))


# #===================== Batch Name =====================
#   l_text = f"<blockquote>Total Number of 🔗 Links found are : **{len(links)} **</blockquote>\n\nSend From where You want to 📩 Download\nInitial is  : **1** \n\n┠ Send `stop` If don't want to Contine \n┖ **Bot Made By :** <a href='https://t.me/Stormy_thor'>『 𝐓𝐇𝐎𝐑 』™</a>⁬"
#   await editable.edit(l_text, disable_web_page_preview=True)
#   input0 = await bot.ask(m.chat.id, "", message_thread_id=thread_id)
#   raw_text = input0.text
#   await input0.delete(True)
#   if raw_text.lower() == "stop":
#       await editable.edit(f"**Task Stoped 🛑**")
#       await input0.delete(True)
#       os.remove(x)
#       return
    
#   await editable.edit("**📝 Enter Batch Name or send `df` for grabbing from text filename.**")
#   input1 = await bot.ask(m.chat.id, "", message_thread_id=thread_id)
#   raw_text0 = input1.text
#   await input1.delete(True)
#   if raw_text0.lower() == 'df':
#       b_name = file_name.replace("_", " ")
#   else:
#       b_name = raw_text0.replace("_", " ")
    
#   quality = "720"
  
#   await editable.edit("**Enter Your Video Uploading Type\n💡Example:** `private`, `unlisted`, `public`") 
#   type_input = await bot.ask(m.chat.id, "", message_thread_id=thread_id)
#   vid_type = type_input.text
#   await type_input.delete()

#   await editable.delete() 
          
#   count = int(raw_text)
#   end_count = len(links)

#   if count == 1:
# #========================= PINNING THE BATCH NAME ======================================
#     pin_text = f"<blockquote>**BATCH NAME :**</blockquote>\n\n<pre><code>{b_name}</code></pre>"
#     batch_message: Message = await bot.send_message(m.chat.id, pin_text, message_thread_id=thread_id)
#     try:
#       await bot.pin_chat_message(m.chat.id, batch_message.id)
#       message_link = batch_message.link
#     except Exception as e:
#       await bot.send_message(m.chat.id, f"Failed to pin message: {str(e)}")
#       message_link = None  # Fallback value
#     message_id = batch_message.id 
#     pinning_message_id = message_id + 1
              
#     if message_link:
#       end_message = (
#       f"⋅ ─ list index (**{count}** - **{end_count}**) out of range ─ ⋅\n\n"
#       f"<blockquote>✨ **BATCH** » <a href=\"{message_link}\">{b_name}</a> ✨</blockquote>\n\n"
#       f"⋅ ─ DOWNLOADING ✩ COMPLETED ─ ⋅"
#     )
#     else:
#       end_message = (
#         f"⋅ ─ list index (**{count}** - **{end_count}**) out of range ─ ⋅\n\n"
#         f"<blockquote>✨ **BATCH** » {b_name} ✨</blockquote>\n\n"
#         f"⋅ ─ DOWNLOADING ✩ COMPLETED ─ ⋅"
#       )
      
#     try:
#       await bot.delete_messages(m.chat.id, pinning_message_id)
#     except Exception as e:
#       await bot.send_message(m.chat.id, f"Failed to delete pinning message: {str(e)}", message_thread_id=thread_id)
    
#   else:
#     end_message = (
#       f"⋅ ─ list index (**{count}**-**{end_count}**) out of range ─ ⋅\n\n"
#       f"<blockquote>✨ **BATCH NAME :** {b_name} ✨</blockquote>\n\n"
#       f"⋅ ─ DOWNLOADING ✩ COMPLETED ─ ⋅"
#     )
  

#   for i in range(count - 1, len(links)):
#     if len(links[i]) != 2 or not links[i][1]:
#     # If the link is empty or not properly formatted, continue to the next iteration
#       name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
#       name = f'{name1[:60]}'
#       continue
#     try:
#       V = links[i][1].replace("file/d/", "uc?export=download&id=").replace("www.youtube-nocookie.com/embed", "youtu.be").replace("?modestbranding=1", "").replace("/view?usp=sharing", "").replace("youtube.com/embed/", "youtube.com/watch?v=")
#       url = "https://" + V
#       d_url = "https://" + V

      
#       if "edge.api.brightcove.com" in url and "6206459123001" in url:
#         bcov = 'bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
#         url = url.split("m3u8")[0] + "m3u8"
#         d_url = d_url.split("bcov_auth")[0]+bcov
#       elif "appx.careerwill" in url:
#         bcov = 'bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
#         id = url.split("/")[-2]
#         d_url = f"https://edge.api.brightcove.com/playback/v1/accounts/6206459123001/videos/{id}/master.m3u8?" + bcov
#       elif "cwmediabkt99" in url:
#         d_url = url.replace(" ", "%20")
              
#       elif any(domain in url for domain in ['cpvod.testbook.com', 'media-cdn.classplusapp.com/drm/', 'cpvod-x.testbook.com']):
#         await asyncio.sleep(2)
#         cp_Data = requests.get(f"{api_url}/classp?url={url}&authorization={user_api_token}").json()
#         if 'keys' not in cp_Data or not cp_Data['keys']:
#           await m.reply_text(f"#failed \nReason {cp_Data}")
#           count +=1
#           continue  
#         keys_arr = cp_Data['keys']
#         CpDrmUrl = cp_Data['url']

#       elif "videos.livelearn.in" in url and url.endswith(".m3u8" or ".mp4"):
#             d_url = url.replace("videos.livelearn.in", "videos-mcdn.akamai.net.in")
#       elif "streamlock.net" in url:
#             if 'TestTestTest' in url:
#               d_url = url.replace("TestTestTest", "Ignitedvod")
#             elif 'luminant' in url:
#               d_url = url.replace("luminant", "Ignitedvod/_definst_/mp4")
            
#       elif "classplusapp" in url or "cpcdn.teach-r.com" in url:
#             if "snapshots" in url:
#               url = url.replace("videos", "alisg-cdn-a").replace("vod-9a3dfb/", "").replace("snapshots/", "")
#               headers = {'Host': 'api.classplusapp.com', 'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9', 'user-agent': 'Mobile-Android', 'app-version': '1.4.37.1', 'api-version': '18', 'device-id': '5d0d17ac8b3c9f51', 'device-details': '2848b866799971ca_2848b8667a33216c_SDK-30', 'accept-encoding': 'gzip'}
#               params = (('url', f'{url}'),)
#               response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
#               d_url = response.json()['url']
#             elif "tencdn.classplusapp" in url:
#               url = url.replace("tencdn.classplusapp.com", "media-cdn.classplusapp.com/tencent")
#               headers = {'Host': 'api.classplusapp.com', 'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9', 'user-agent': 'Mobile-Android', 'app-version': '1.4.37.1', 'api-version': '18', 'device-id': '5d0d17ac8b3c9f51', 'device-details': '2848b866799971ca_2848b8667a33216c_SDK-30', 'accept-encoding': 'gzip'}
#               params = (('url', f'{url}'),)
#               response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
#               d_url = response.json()['url']
#             else:
#               headers = {'Host': 'api.classplusapp.com', 'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9', 'user-agent': 'Mobile-Android', 'app-version': '1.4.37.1', 'api-version': '18', 'device-id': '5d0d17ac8b3c9f51', 'device-details': '2848b866799971ca_2848b8667a33216c_SDK-30', 'accept-encoding': 'gzip'}
#               params = (('url', f'{url}'),)
#               response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
#               d_url = response.json()['url']      

#       elif "encrypted" in url and not url.endswith(".mkv"):
#             if url.endswith(".m3u8") or url.endswith(".zip"):
#               pass
#             else:
#               if'https://encappx/' in url or "?k=" in url or "?key=" in url :
#                 url = url.replace('https://encappx/','').replace('?k=','*').replace('?key=','*').strip()
#                 d_url, key = url.split("*")
#               else:      
#                 d_url, key = url.split("*")
          
          
      
#       name1 = links[i][0].replace("\t", "").replace("/", "").replace(":", "").replace("*", "").replace("?", "").replace("|", "").replace("<", "").replace("+", "").replace("#", "").replace("@", "").replace(".", " ").replace("https", "").replace("http", "").replace("=", "").replace(">", "").replace("-", " ").replace("%", "").replace("$", "").replace("'", '').strip() 
#       if name1.startswith("(") or name1.startswith("[") or name1.startswith("{"):
#         match = re.match(r"^\((.*)\)|^\[(.*)\]", name1)
#         if match:
#           t_name = (match.group(1) or match.group(2)).strip().upper()
#           v_name = name1[match.end():].strip() if match else name1
#           name = f'{v_name[:99]}'

#       else:
#         name = f'{name1[:99]}'
      
#       if "youtu" in url:
#             ytf = f"bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality}][ext=mp4]"
#       else:
#             ytf = f"b[height<={quality}]/bv[height<={quality}]+ba/b/bv+ba"
            
      
#       if "youtu" in url:
#             cmd = f'yt-dlp --cookies "{COOKIES_FILE_PATH}" -f "{ytf}" "{url}" -o "{name}.mp4"'
#       else:
#             cmd = f'yt-dlp -f "{ytf}" "{d_url}" -o "{name}.mp4"'
                      
#       cc1 = f'❖────────── **{str(count).zfill(3)}** ──────────❖\n\n📋 **Title :** `{name1}.pdf`\n\n<blockquote>📘 **Course Name :** {b_name}</blockquote>'


#       if "drive" in url:
#            try:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
#             ka = await helper.download(url, name)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
#             await bot.send_document(m.chat.id,document=ka, caption=cc1, message_thread_id=thread_id)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
#             count+=1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
#             os.remove(ka)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
#             await asyncio.sleep(1)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
#            except FloodWait as e:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
#             await asyncio.sleep(e.x)
#             continue                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
            
#       elif ".pdf" in url or  url.endswith(".doc"):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
#         try:
#               if "appx" in url and not url.endswith(".pdf"):# and not "v2.classx" in url:
#                 if "--appx-pdf?key=" in url:
#                   url5 = url.replace("--appx-pdf?key=", "")
#                   url , key = url5.split("*")
#                 else:
#                   url, key = url.split('*')
                
#                 try:
#                     url2 = f"{api_url}/appxv2-pdf?url={url}&key={key}"
#                     await asyncio.sleep(1)
#                     response = scraper.get(url2)
#                     if response.status_code == 200 and response.content:
#                       with open(f'{name}.pdf', 'wb') as file:
#                         file.write(response.content)
#                     else:
#                       download_cmd = f"yt-dlp -o '{name}.pdf' '{url}' -R 25 --fragment-retries 25" 
#                       os.system(download_cmd) 
#                       await asyncio.sleep(1)
#                       await helper.appx_dl(f'{name}.pdf', key)
#                     await bot.send_document(m.chat.id, document=f'{name}.pdf', caption=cc1, message_thread_id=thread_id)
#                 except Exception as e:
#                   logging.info(f"Failed to download: {str(e)}")

#               else:
#                 response = scraper.get(url)
#                 if response.status_code == 200:
#                   with open(f'{name}.pdf', 'wb') as file:
#                     file.write(response.content)
#                   await asyncio.sleep(1)
#                   await bot.send_document(m.chat.id, document=f'{name}.pdf', caption=cc1, message_thread_id=thread_id)
#                 else:
#                   await bot.send_message(m.chat.id, f"{response}", message_thread_id=thread_id)
#               if f'{name}.pdf' and os.path.exists(f'{name}.pdf'):
#                 os.remove(f'{name}.pdf')
#               count += 1
#               continue
#         except Exception as e:
#           await bot.send_message(m.chat.id, str(e), message_thread_id=thread_id)
#           count += 1
#           await asyncio.sleep(2)
            
#       # Skipping URLs:
#       elif ".zip" in url and url.endswith(".zip") or "hls-drm" in url:
#             count += 1
#             await asyncio.sleep(3)
#             continue
      
#       elif "stream-kgs" in url or "stream.kgs" in url:
#             count += 1
#             await asyncio.sleep(3)
#             continue
          
    
#       elif any(ext in url for ext in [".jpg", ".jpeg", ".png"]):
#         try:
#               ext = url.split('.')[-1]
#               download_cmd = f"yt-dlp -o '{name}.{ext}' '{url}' -R 25 --fragment-retries 25"
#               os.system(download_cmd)
#               cc3 = f'**——— ✦ {str(count).zfill(3)} ✦ ———**\n\n**🖼️ Tittle** : **{name1}**.{ext}\n\n**Course :** {b_name}'
#               thumb_path = f'{name}.{ext}'
#               os.system(f"wget -O '{thumb_path}' {url}")
#               await bot.send_photo(m.chat.id, thumb_path, caption=cc3, message_thread_id=thread_id)
#               count += 1
#               os.remove(thumb_path)
#               continue
#         except FloodWait as e:
#               await m.reply_text(str(e), message_thread_id=thread_id)
#               await asyncio.sleep(3)
      
#       elif any (ext in url for ext in [".mp3", ".wav", ".m4a"]):
#             try:
#               ext = url.split('.')[-1]
#               download_cmd = f'yt-dlp -x --audio-format {ext} -o "{name}.{ext}" "{url}" -R 25 --fragment-retries 25'
#               os.system(download_cmd)
#               cc2 = f'**[🎵] Audio_ID : {str(count).zfill(3)}.**\n\n**Tittle :** {name1}.{ext}\n\n**Course :** {b_name}'
#               await bot.send_document(m.chat.id, document=f'{name}.{ext}', caption=cc2, message_thread_id=thread_id)
#               count += 1
#               os.remove(f'{name}.{ext}')
#               continue
#             except FloodWait as e:
#               await bot.send_message(m.chat.id, str(e), message_thread_id=thread_id)
#               await asyncio.sleep(2)
      
                
#       else:
#         left_link = len(links) - int(count)
#         progress = (int(count) / len(links)) * 100
#         Show = (
#             f"<blockquote>🚀 **𝐂𝐔𝐑𝐑𝐄𝐍𝐓 𝐏𝐑𝐎𝐆𝐑𝐄𝐒𝐒 = {progress:.2f}%** 🚀</blockquote>\n"
#             f" **┠ 📊 Total Links =** {len(links)}\n"
#             f" **┠ ⚡️ Currently On =** {str(count).zfill(3)}\n"
#             f" **┠ ⏳ Remaining Links =** {left_link}\n\n"
#             f"<blockquote>**📥 𝐃𝐎𝐖𝐍𝐋𝐎𝐀𝐃𝐈𝐍𝐆 𝐕𝐈𝐃𝐄𝐎 📥**</blockquote>\n"
#             f"**🔗 LINK :** {url}\n"
#             f"** ┠ 🎞️ Title** : {name1}\n"
#             f" **┠ 📻 Quality :** {quality}p\n\n"
#             f"╔══════════════════════════╗\n"
#             f"╠  ✨ **𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘 : {credit}**\n"
#             f"╚══════════════════════════╝")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
#         prog = await bot.send_message(m.chat.id, Show, disable_web_page_preview=True, message_thread_id=thread_id)
#         if 'cpvod.testbook.com' in url or 'media-cdn.classplusapp.com/drm/' in url  or 'cpvod-x.testbook.com' in url:
#               res_file = await helper.drm_cp_download_video(CpDrmUrl, quality, name, keys_arr)
#         elif "encrypted" in url:
#           res_file = await helper.download_video(d_url, cmd, name) 
#           await helper.appx_dl(res_file, key)
#         else:
#           res_file = await helper.download_video(d_url, cmd,name)
#         filename = res_file
#         await prog.delete(True)
#         await upload_video(m, filename, name, description="Upload via YouTube Automation Bot Made by : Shadow Studio", tags=["api", "youtube", "upload"], privacyStatus=vid_type)
#         count += 1 
#     except Exception as e:
#       name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("`", "").replace("@", "").replace("*", "").replace(".", " ").replace("https", "").replace("http", "").replace('"', "'").strip()
#       name = f'{name1[:60]}'
#       f_text = f"**Error :** {str(e)}"
#       await bot.send_message(m.chat.id, f_text, disable_web_page_preview=True, message_thread_id=thread_id)
#       count += 1
#       await asyncio.sleep(2)
#       continue
  
  
#   await bot.send_message(m.chat.id, f"{end_message}", message_thread_id=thread_id)
#   yt_json = "/app/youtube_videos.json"
#   await bot.send_document(m.chat.id, document=yt_json, message_thread_id=thread_id)
#   if os.path.exists(yt_json):
#     os.remove(yt_json)
#   await bot.send_message(m.chat.id, "**That's It ❤️**", message_thread_id=thread_id)
