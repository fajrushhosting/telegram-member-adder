#!/usr/bin/env python3
"""
Quick Test Script - Coba dulu dengan 1 member
"""

import asyncio
from telethon.sync import TelegramClient

# GANTI DENGAN DATA KAMU
API_ID = 1234567
API_HASH = 'abcdef1234567890abcdef'
PHONE = '+6281234567890'

async def test_add_member():
    """Test tambah 1 member"""
    print("🧪 TESTING: Add Single Member")
    
    # Connect
    client = TelegramClient('test_session', API_ID, API_HASH)
    await client.start(PHONE)
    
    print("✅ Connected to Telegram")
    
    # Input data
    group = input("Group username (@groupname): ").strip()
    member = input("Member username (@username): ").strip()
    
    if not group or not member:
        print("❌ Input cannot be empty!")
        return
    
    try:
        # Get group
        print(f"\n🔍 Getting group: {group}")
        group_entity = await client.get_entity(group)
        print(f"✅ Group: {getattr(group_entity, 'title', 'N/A')}")
        
        # Get member
        print(f"🔍 Getting member: {member}")
        if member.startswith('@'):
            member = member[1:]
        user = await client.get_input_entity(member)
        print(f"✅ User found")
        
        # Try to add
        print(f"\n🚀 Trying to add {member} to group...")
        
        try:
            # Try method 1 (channel/supergroup)
            await client(InviteToChannelRequest(
                channel=group_entity,
                users=[user]
            ))
            print(f"🎉 SUCCESS! Invitation sent")
            
        except Exception as e:
            # Try method 2 (regular group)
            try:
                await client(AddChatUserRequest(
                    chat_id=group_entity,
                    user_id=user,
                    fwd_limit=0
                ))
                print(f"🎉 SUCCESS! Added to group")
                
            except Exception as e2:
                error_msg = str(e2)
                print(f"❌ FAILED: {error_msg}")
                
                # Common errors
                if "USER_ALREADY_PARTICIPANT" in error_msg:
                    print("💡 User already in group")
                elif "USER_NOT_MUTUAL_CONTACT" in error_msg:
                    print("💡 You need to be mutual contact")
                elif "USER_PRIVACY_RESTRICTED" in error_msg:
                    print("💡 User has privacy restrictions")
                elif "CHAT_ADMIN_REQUIRED" in error_msg:
                    print("💡 You need to be admin")
                elif "FLOOD" in error_msg:
                    print("💡 Flood wait - Try again later")
    
    except Exception as e:
        print(f"💥 Error: {e}")
    
    finally:
        await client.disconnect()
        print("\n👋 Disconnected")

if __name__ == "__main__":
    # Validasi
    if API_ID == 1234567:
        print("❌ Please edit API credentials in the script!")
        print("📱 Get from: https://my.telegram.org")
    else:
        asyncio.run(test_add_member())
