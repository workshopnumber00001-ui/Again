from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

FORCE_JOIN_BUTTON = InlineKeyboardMarkup([[InlineKeyboardButton("Join Channel", url="https://t.me/Stormy_thor")]])
FREE_BUTTON = InlineKeyboardMarkup([[InlineKeyboardButton("💎 Features", callback_data="feat_command"), InlineKeyboardButton("🎫 Bot plans", callback_data="upgrade_command")]])
HELP_BUTTON = InlineKeyboardMarkup([[InlineKeyboardButton("Help", callback_data="help_command")]])

ID_BUTTON = InlineKeyboardMarkup(
  [
    [
      InlineKeyboardButton(
        text="Send Here",
        url="https://t.me/Stormy_thor"
      )
    ]
  ]
)

OwnerButton = InlineKeyboardMarkup([
        [InlineKeyboardButton("👥 Global Auth Users", callback_data="show$AuthUsers")],
        [InlineKeyboardButton("🪵 User Logs", callback_data="show$UserLogs")],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]
])


PLAN_BUTTON = InlineKeyboardMarkup(
  [
    [InlineKeyboardButton("💚 NORMAL 💚", callback_data="plan1_"), InlineKeyboardButton("💙 PRO 💙", callback_data="plan2_")],
    [InlineKeyboardButton("💜 CONQUEROR 💜", callback_data="plan3_"), InlineKeyboardButton("🧡 LEGEND 🧡", callback_data="plan4_")],
    [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]
  ]
)


TOOL_BUTTON = InlineKeyboardMarkup(
  [
    [InlineKeyboardButton("🗃️ View Group With Topics", callback_data="ViewTopics")],
    [InlineKeyboardButton("💎 Features", callback_data="feat_command"), InlineKeyboardButton("🌟 『 𝐓𝐇𝐎𝐑 』™", callback_data="https://t.me/Stormy_thor")],
    [InlineKeyboardButton("🌟 Subscription Info", callback_data="subs_info_command")],
    [InlineKeyboardButton("🛑 Stop Bot", callback_data="sstop_command"), InlineKeyboardButton("🎫 Bot Plans", callback_data="upgrade_command")],
    [InlineKeyboardButton("⚙️ Settings", callback_data="set_command")]
  ]
)

HTML_BUTTON = InlineKeyboardMarkup(
  [
    [InlineKeyboardButton("Normal HTML", callback_data="n_html")],
    [InlineKeyboardButton("Subject Wise HTML", callback_data="s_html")],
    [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]
  ]
)


FT_BUTTON = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("📂 2GB+ File Supported", callback_data="2gb_command")],
        [InlineKeyboardButton("📝 TXT Maker/Editor Command", callback_data="editor_command")],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]
    ]
)

ST_BUTTON = InlineKeyboardMarkup(
    [
      [InlineKeyboardButton("📝 Default Name", callback_data="df_command"), InlineKeyboardButton("📎 Name Before Extension", callback_data="extension")],
      [InlineKeyboardButton("🎨 Caption Styling", callback_data="cap_style")],
      [InlineKeyboardButton("📺 Quality", callback_data="quality"), InlineKeyboardButton("🖼️ Thumbnail Setting", callback_data="thumb_st")],
      [InlineKeyboardButton("🛠 Text Overlay Pannel", callback_data="text_settings_")],
      [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]
    ]
)

BACK_MENU = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back to Main Menu", callback_data="back_to_main_menu")]])
