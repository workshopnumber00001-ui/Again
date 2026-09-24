'''from pymongo.mongo_client import MongoClient
import hashlib
from pymongo.errors import OperationFailure


def get_collection(bot_name, mongo_uri):
    client = MongoClient(mongo_uri)
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except OperationFailure as e:
        raise ValueError(f"Failed to connect to MongoDB: {e}")

    # Generate a unique collection name using the bot token
    collection_name = hashlib.md5(bot_name.encode()).hexdigest()
    db = client['Megatron']
    return db[collection_name]


#===================== SAVING AND LOADING TEXT OVERLAY ===========================
def save_text_wtmark(collection, text_wtmark=""):
    with open("text_wtmark.txt", "w") as file:
        file.write(text_wtmark)

    existing_text_wtmark = collection.find_one({"type": "text_wtmark"})
    if existing_text_wtmark:
        collection.update_one({"type": "text_wtmark"}, {"$set": {"value": text_wtmark}})
    else:
        collection.insert_one({"type": "text_wtmark", "value": text_wtmark})

def load_text_wtmark(collection):
    try:
        with open("text_wtmark.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        pass
    
    # Load text_wtmark from MongoDB
    result = collection.find_one({"type": "text_wtmark"})
    if result:
        return result.get("value")  # Use get method to avoid KeyError
    else:
        return ""
    
# ======================== SAVE BOT SUPPORT TYPE ===========================
def save_allowed_support_types(collection, supports):
    with open("allowed_support_types.txt", "w") as file:
        for support in supports:
            if isinstance(support, (int, str)):  # Ensure integers and strings are written
                file.write(str(support) + "\n")
    
    existing_supports = collection.find_one({"type": "allowed_support_types"})
    if existing_supports:
        collection.update_one({"type": "allowed_support_types"}, {"$set": {"value": supports}})
    else:
        collection.insert_one({"type": "allowed_support_types", "value": supports})

def load_allowed_support_types(collection):
    try:
        with open("allowed_support_types.txt", "r") as file:
            return [int(support) if support.isdigit() else support for support in file.read().splitlines()]
    except (FileNotFoundError, ValueError):
        pass
    result = collection.find_one({"type": "allowed_support_types"})
    if result:
        return result.get("value", [])
    else:
        return []

# ======================== SAVE PW URL TYPE ===========================
def save_pwurltype(collection, pwurltype):
    with open("pwurltype.txt", "w") as file:
        file.write(pwurltype)
    
    existing_pwurltype = collection.find_one()
    if existing_pwurltype:
        collection.update_one({}, {"$set": {"pwurltype": pwurltype}})
    else:
        collection.insert_one({"pwurltype": pwurltype})

def load_pwurltype(collection):
    try:
        with open("pwurltype.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        pass  # If file not found, proceed to MongoDB
    
    result = collection.find_one()
    if result:
        return result.get("pwurltype")  # Use get method to avoid KeyError
    else:
        return None
#===================== SAVING AND LOADING YT COOKIES ===========================
def save_ytcookies(collection, ytcookies):
    # Save ytcookies to local file
    with open("ytcookies.txt", "w") as file:
        file.write(ytcookies)

    # Check if ytcookies already exists in MongoDB
    existing_ytcookies = collection.find_one({"type": "ytcookies"})
    if existing_ytcookies:
        # Update existing ytcookies in MongoDB
        collection.update_one({"type": "ytcookies"}, {"$set": {"value": ytcookies}})
    else:
        # Insert new ytcookies into MongoDB
        collection.insert_one({"type": "ytcookies", "value": ytcookies})

def load_ytcookies(collection):
    try:
        # Try to load pwtoken from local file
        with open("ytcookies.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        pass  # If file not found, proceed to MongoDB
    
    # Load ytcookies from MongoDB
    result = collection.find_one({"type": "ytcookies"})
    if result:
        return result.get("value")  # Use get method to avoid KeyError
    else:
        return None

# ============================== VID : THUMBNAIL ====================================
def save_vid_thumb(collection, vid_thumb="no"):
    with open(f"vid_thumb.txt", "w") as file:
        file.write(vid_thumb)
    existing_vid_thumb = collection.find_one({"type": "vid_thumb"})
    if existing_vid_thumb:
        collection.update_one({"type": "vid_thumb"}, {"$set": {"value": vid_thumb}})
    else:
        collection.insert_one({"type": "vid_thumb", "value": vid_thumb})

def load_vid_thumb(collection):
    try:
        with open(f"vid_thumb.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        pass

    result = collection.find_one({"type": "vid_thumb"})
    if result:
        return result.get("value")
    else:
        return "no"
    
# ============================== PDF : THUMBNAIL ====================================
def save_pdf_thumb(collection, pdf_thumb="no"):
    with open(f"pdf_thumb.txt", "w") as file:
        file.write(pdf_thumb)
    existing_pdf_thumb = collection.find_one({"type": "pdf_thumb"})
    if existing_pdf_thumb:
        collection.update_one({"type": "pdf_thumb"}, {"$set": {"value": pdf_thumb}})
    else:
        collection.insert_one({"type": "pdf_thumb", "value": pdf_thumb})

def load_pdf_thumb(collection):
    try:
        with open(f"pdf_thumb.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        pass

    result = collection.find_one({"type": "pdf_thumb"})
    if result:
        return result.get("value")
    else:
        return "no"


# ============================== JOIN DATE & TIME ====================================
def save_joindate(collection, joindate):
    with open(f"joindate.txt", "w") as file:
        file.write(joindate)
    existing_joindate = collection.find_one({"type": "joindate"})
    if existing_joindate:
        collection.update_one({"type": "joindate"}, {"$set": {"value": joindate}})
    else:
        collection.insert_one({"type": "joindate", "value": joindate})

def load_joindate(collection):
    try:
        with open(f"joindate.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        pass

    result = collection.find_one({"type": "joindate"})
    if result:
        return result.get("value")
    else:
        return None
    
# ============================== END DATE & TIME ====================================
def save_enddate(collection, enddate):
    with open(f"enddate.txt", "w") as file:
        file.write(enddate)
    existing_enddate = collection.find_one({"type": "enddate"})
    if existing_enddate:
        collection.update_one({"type": "enddate"}, {"$set": {"value": enddate}})
    else:
        collection.insert_one({"type": "enddate", "value": enddate})

def load_enddate(collection):
    try:
        with open(f"enddate.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        pass

    result = collection.find_one({"type": "enddate"})
    if result:
        return result.get("value")
    else:
        return None
#===================== SAVING AND LOADING PWTOKEN ===========================
def save_pwtoken(collection, pwtoken):
    with open("pwtoken.txt", "w") as file:
        file.write(pwtoken)

    existing_pwtoken = collection.find_one({"type": "pwtoken"})
    if existing_pwtoken:
        collection.update_one({"type": "pwtoken"}, {"$set": {"value": pwtoken}})
    else:
        collection.insert_one({"type": "pwtoken", "value": pwtoken})

def load_pwtoken(collection):
    try:
        with open("pwtoken.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        pass
    
    # Load pwtoken from MongoDB
    result = collection.find_one({"type": "pwtoken"})
    if result:
        return result.get("value")  # Use get method to avoid KeyError
    else:
        return None


# ===================== Extension NAME =========================
def save_exname(collection, exname):
    # Save EX_name to local file
    with open("exname.txt", "w") as file:
        file.write(exname)
    
    # Check if EX_name already exists in MongoDB
    existing_exname = collection.find_one()
    if existing_exname:
        # Update existing EX_name in MongoDB
        collection.update_one({}, {"$set": {"exname": exname}})
    else:
        # Insert new EX_name into MongoDB
        collection.insert_one({"exname": exname})

def load_exname(collection):
    try:
        # Try to load name from local file
        with open("exname.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        pass  # If file not found, proceed to MongoDB
    
    # Load EX_name from MongoDB
    result = collection.find_one()
    if result:
        return result.get("exname")  # Use get method to avoid KeyError
    else:
        return None

# ====================== Credit NAME ==========================
def save_crname(collection, crname):
    # Save CR_name to local file
    with open("crname.txt", "w") as file:
        file.write(crname)
    
    # Check if CR_name already exists in MongoDB
    existing_crname = collection.find_one()
    if existing_crname:
        # Update existing CR_name in MongoDB
        collection.update_one({}, {"$set": {"crname": crname}})
    else:
        # Insert new CR_name into MongoDB
        collection.insert_one({"crname": crname})

def load_crname(collection):
    try:
        # Try to load CR_name from local file
        with open("crname.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        pass  # If file not found, proceed to MongoDB
    
    # Load CR_name from MongoDB
    result = collection.find_one()
    if result:
        return result.get("crname")  # Use get method to avoid KeyError
    else:
        return None

# ====================== Authorized Users ==========================
def save_authorized_users(collection, authorized_users):
    # Save authorized users to local file
    with open("authorized_users.txt", "w") as file:
        for user_id in authorized_users:
            file.write(str(user_id) + "\n")
    
    # Check if authorized users already exist in MongoDB
    existing_users = collection.find_one({"type": "authorized_users"})
    if existing_users:
        # Update existing authorized users in MongoDB
        collection.update_one({"type": "authorized_users"}, {"$set": {"value": authorized_users}})
    else:
        # Insert new authorized users into MongoDB
        collection.insert_one({"type": "authorized_users", "value": authorized_users})
#fvc
    
def load_authorized_users(collection):
    try:
        # Try to load authorized users from local file
        with open("authorized_users.txt", "r") as file:
            return [int(user_id) for user_id in file.read().splitlines()]
    except (FileNotFoundError, ValueError):
        pass  # If file not found or contains invalid data, proceed to MongoDB
    
    # Load authorized users from MongoDB
    result = collection.find_one({"type": "authorized_users"})
    if result:
        return result.get("value", [])  # Use get method to avoid KeyError
    else:
        return []  # Default value if not found in MongoDB



def save_allowed_channel_ids(collection, allowed_channel_ids):
    # Save allowed channel IDs to local file
    with open("allowed_channel_ids.txt", "w") as file:
        for channel_id in allowed_channel_ids:
            file.write(str(channel_id) + "\n")
    
    # Check if allowed channel IDs already exist in MongoDB
    existing_channels = collection.find_one({"type": "allowed_channel_ids"})
    if existing_channels:
        # Update existing allowed channel IDs in MongoDB
        collection.update_one({"type": "allowed_channel_ids"}, {"$set": {"value": allowed_channel_ids}})
    else:
        # Insert new allowed channel IDs into MongoDB
        collection.insert_one({"type": "allowed_channel_ids", "value": allowed_channel_ids})

def load_allowed_channel_ids(collection):
    try:
        # Try to load allowed channel IDs from local file
        with open("allowed_channel_ids.txt", "r") as file:
            return [int(channel_id) for channel_id in file.read().splitlines()]
    except (FileNotFoundError, ValueError):
        pass  # If file not found or contains invalid data, proceed to MongoDB
    
    # Load allowed channel IDs from MongoDB
    result = collection.find_one({"type": "allowed_channel_ids"})
    if result:
        return result.get("value", [])  # Use get method to avoid KeyError
    else:
        return []  # Default value if not found in MongoDB
    

# ===================== POWERED NAME =========================
def save_poweredname(collection, poweredname="[『 𝐓𝐇𝐎𝐑 🧑‍💻 』™](t.me/Stormy_thor)"):
    with open("poweredname.txt", "w") as file:
        file.write(poweredname)
    
    existing_poweredname = collection.find_one({"type": "poweredname"})
    if existing_poweredname:
        collection.update_one({"type": "poweredname"}, {"$set": {"value": poweredname}})
    else:
        collection.insert_one({"type": "poweredname", "value": poweredname})

def load_poweredname(collection):
    try:
        with open("poweredname.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        pass
    
    result = collection.find_one({"type": "poweredname"})
    if result:
        return result.get("value")
    else:
        return "[『 𝐓𝐇𝐎𝐑 🧑‍💻 』™](t.me/Stormy_thor)"'''
