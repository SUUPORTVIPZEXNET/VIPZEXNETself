from rubpy import Client
import re
import asyncio

bot = Client("ultimate_bot")

# متن تبلیغاتی جدید
ADVERTISEMENT_TEXT = "اینجا متن تبلیغاتی که میخواهین ربات در گروه خا بفرسته رو بزارین"

# متغیر برای ذخیره GUID مدیر
admin_guid = None

@bot.on_message_updates()
async def handle_all_messages(message):
    """پردازش تمام پیام‌های دریافتی"""
    global admin_guid
    
    try:
        # اگر مدیر شناسایی نشده، اولین کاربر را مدیر کن
        if admin_guid is None:
            admin_guid = message.author_guid
            print(f"✅ مدیر شناسایی شد: {admin_guid}")
            await bot.send_message(admin_guid, "🤖 ربات راه اندازی شد! لینک‌های گروه را ارسال کنید.")
            return
        
        # فقط پیام‌های مدیر را پردازش کن
        if message.author_guid != admin_guid:
            print(f"⛔ پیام از کاربر غیرمجاز: {message.author_guid}")
            return
        
        if not message.text:
            return
        
        print(f"📩 پیام از مدیر: {message.text}")
        
        # پیدا کردن لینک‌ها
        links = re.findall(r'https?://\S+', message.text)
        
        if not links:
            await bot.send_message(admin_guid, "❌ هیچ لینکی در پیام پیدا نشد.")
            return
        
        await bot.send_message(admin_guid, f"🔗 دریافت {len(links)} لینک. در حال پردازش...")
        
        # پردازش هر لینک
        for i, link in enumerate(links, 1):
            try:
                await bot.send_message(admin_guid, f"⏳ پردازش لینک {i}/{len(links)}...")
                
                # پیوستن به گروه
                join_result = await bot.join_chat(link)
                
                if join_result and hasattr(join_result, 'group'):
                    group_guid = join_result.group.group_guid
                    group_title = getattr(join_result.group, 'title', 'گروه ناشناس')
                    
                    await bot.send_message(admin_guid, f"✅ به گروه پیوستم: {group_title}")
                    
                    # انتظار و ارسال پیام
                    await asyncio.sleep(5)
                    await bot.send_message(group_guid, ADVERTISEMENT_TEXT)
                    await bot.send_message(admin_guid, f"📨 پیام ارسال شد به: {group_title}")
                    
                    # انتظار و خروج
                    await asyncio.sleep(30)
                    await bot.leave_group(group_guid)
                    await bot.send_message(admin_guid, f"🚪 از گروه خارج شدم: {group_title}")
                    
                else:
                    await bot.send_message(admin_guid, f"❌ نتوانستم به لینک پیوستن کنم: {link}")
                    
            except Exception as e:
                error_msg = f"⚠️ خطا در لینک {link}: {str(e)}"
                await bot.send_message(admin_guid, error_msg)
                print(error_msg)
                continue
                
    except Exception as e:
        error_msg = f"❌ خطای کلی: {str(e)}"
        print(error_msg)
        if admin_guid:
            await bot.send_message(admin_guid, error_msg)

# اجرای ربات
if __name__ == "__main__":
    print("🎯 ربات تبلیغاتی روبیکا")
    print("➖➖➖➖➖➖➖➖➖➖")
    print("📩 پس از لاگین، یک پیام به ربات بفرستید")
    
    # اجرای ربات
    bot.run()