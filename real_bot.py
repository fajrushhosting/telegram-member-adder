#!/usr/bin/env python3
"""
TELEGRAM MEMBER ADDER - REAL WORKING SCRIPT
Tested and Working - Member benar-benar masuk grup
"""

import asyncio
import csv
import random
import time
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.types import InputPeerUser, InputPeerChannel
import os

# ============================================
# CONFIGURASI - EDIT BAGIAN INI!
# ============================================

API_ID = 1234567  # GANTI dengan API ID dari my.telegram.org
API_HASH = 'abcdef1234567890abcdef'  # GANTI dengan API Hash
PHONE = '+6281234567890'  # GANTI dengan nomor kamu

# ============================================
# JANGAN EDIT DI BAWAH INI KECUALI PAHAM
# ============================================

class TelegramMemberAdder:
    def __init__(self, api_id, api_hash, phone):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.client = None
        
    async def connect(self):
        """Connect ke Telegram"""
        print("🔗 Connecting to Telegram...")
        self.client = TelegramClient('session_work', self.api_id, self.api_hash)
        await self.client.start(phone=self.phone)
        
        # Cek login
        me = await self.client.get_me()
        print(f"✅ Login successful as: {me.first_name}")
        print(f"📱 Phone: {me.phone}")
        print(f"🆔 User ID: {me.id}")
        return True
    
    async def add_single_member(self, group_entity, username):
        """Tambah satu member ke grup"""
        try:
            print(f"👤 Processing: {username}")
            
            # Bersihkan username
            if username.startswith('@'):
                username = username[1:]
            
            # 1. Cari user
            print(f"   🔍 Searching user...")
            try:
                user = await self.client.get_input_entity(username)
                print(f"   ✅ User found")
            except Exception as e:
                print(f"   ❌ User not found: {e}")
                return False, "User not found"
            
            # 2. Coba invite ke channel/grup
            try:
                # Method 1: Untuk channel/supergroup
                await self.client(InviteToChannelRequest(
                    channel=group_entity,
                    users=[user]
                ))
                print(f"   ✅ Invitation sent!")
                return True, "Invitation sent"
                
            except Exception as e:
                # Method 2: Untuk grup biasa
                try:
                    await self.client(AddChatUserRequest(
                        chat_id=group_entity,
                        user_id=user,
                        fwd_limit=0
                    ))
                    print(f"   ✅ Added to group!")
                    return True, "Added to group"
                    
                except Exception as e2:
                    error_msg = str(e2)
                    print(f"   ❌ Failed: {error_msg}")
                    
                    # Analisis error
                    if "USER_ALREADY_PARTICIPANT" in error_msg:
                        return False, "Already in group"
                    elif "USER_NOT_MUTUAL_CONTACT" in error_msg:
                        return False, "Not mutual contact"
                    elif "USER_PRIVACY_RESTRICTED" in error_msg:
                        return False, "Privacy restricted"
                    elif "FLOOD" in error_msg:
                        return False, "Flood wait"
                    else:
                        return False, error_msg
        
        except Exception as e:
            print(f"   💥 Unexpected error: {e}")
            return False, str(e)
    
    async def add_members_from_file(self, group_username, filename="members.csv", delay=30):
        """Tambah member dari file CSV"""
        print(f"\n📋 Reading members from {filename}")
        
        # Baca file
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                members = [row[0].strip() for row in reader if row and row[0].strip()]
        except FileNotFoundError:
            print(f"❌ File {filename} not found!")
            return
        
        if not members:
            print("❌ No members found in file!")
            return
        
        print(f"✅ Found {len(members)} members")
        
        # Dapatkan entity grup
        try:
            print(f"\n🎯 Getting group: {group_username}")
            group_entity = await self.client.get_entity(group_username)
            group_title = getattr(group_entity, 'title', 'Unknown Group')
            print(f"✅ Target: {group_title}")
        except Exception as e:
            print(f"❌ Error getting group: {e}")
            return
        
        # Konfirmasi
        print(f"\n⚠️  CONFIRMATION")
        print(f"Group: {group_title}")
        print(f"Members: {len(members)}")
        print(f"Delay: {delay} seconds between adds")
        
        confirm = input("\nContinue? (y/n): ").lower()
        if confirm != 'y':
            print("❌ Cancelled")
            return
        
        # Proses penambahan
        print("\n🚀 STARTING...")
        print("="*50)
        
        results = {
            'success': 0,
            'failed': 0,
            'skipped': 0,
            'errors': []
        }
        
        for i, member in enumerate(members, 1):
            try:
                print(f"\n[{i}/{len(members)}]")
                
                # Skip komentar
                if member.startswith('#'):
                    print(f"   ⏭️ Skipped (comment)")
                    results['skipped'] += 1
                    continue
                
                # Tambah member
                success, message = await self.add_single_member(group_entity, member)
                
                if success:
                    results['success'] += 1
                    print(f"   ✅ SUCCESS: {message}")
                else:
                    results['failed'] += 1
                    results['errors'].append(f"{member}: {message}")
                    print(f"   ❌ FAILED: {message}")
                
                # Delay antar penambahan (kecuali member terakhir)
                if i < len(members):
                    print(f"   ⏳ Waiting {delay} seconds...")
                    await asyncio.sleep(delay)
                
            except KeyboardInterrupt:
                print("\n\n⚠️ Process interrupted by user")
                break
            except Exception as e:
                print(f"   💥 Error: {e}")
                results['failed'] += 1
                results['errors'].append(f"{member}: {e}")
                await asyncio.sleep(5)
        
        # Tampilkan hasil
        print("\n" + "="*50)
        print("📊 FINAL RESULTS")
        print("="*50)
        print(f"✅ Success: {results['success']}")
        print(f"❌ Failed: {results['failed']}")
        print(f"⏭️ Skipped: {results['skipped']}")
        print(f"📊 Total: {len(members)}")
        
        # Simpan log
        self.save_results(results, group_title)
        
        # Tampilkan error jika ada
        if results['errors']:
            print(f"\n📝 Errors ({len(results['errors'])}):")
            for error in results['errors'][:5]:  # Tampilkan 5 error pertama
                print(f"   • {error}")
            if len(results['errors']) > 5:
                print(f"   ... and {len(results['errors']) - 5} more")
    
    def save_results(self, results, group_title):
        """Simpan hasil ke file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Telegram Member Adder - Results\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Group: {group_title}\n")
            f.write(f"Success: {results['success']}\n")
            f.write(f"Failed: {results['failed']}\n")
            f.write(f"Skipped: {results['skipped']}\n")
            f.write(f"Total: {results['success'] + results['failed'] + results['skipped']}\n\n")
            
            if results['errors']:
                f.write("Errors:\n")
                for error in results['errors']:
                    f.write(f"- {error}\n")
        
        print(f"\n📁 Results saved to: {filename}")
    
    async def check_group_info(self, group_username):
        """Cek info grup"""
        try:
            group = await self.client.get_entity(group_username)
            
            print(f"\n📊 GROUP INFORMATION")
            print(f"Name: {getattr(group, 'title', 'N/A')}")
            print(f"Username: @{getattr(group, 'username', 'N/A')}")
            print(f"ID: {getattr(group, 'id', 'N/A')}")
            
            # Cek participant count
            try:
                participants = await self.client.get_participants(group)
                print(f"Members: {len(participants)}")
            except:
                print(f"Members: Cannot fetch (need admin)")
            
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect dari Telegram"""
        if self.client:
            await self.client.disconnect()
            print("\n👋 Disconnected from Telegram")

async def main():
    """Main function"""
    print("\n" + "="*60)
    print("🤖 TELEGRAM MEMBER ADDER - REAL WORKING SCRIPT")
    print("="*60)
    
    # Validasi config
    if API_ID == 1234567 or "abcdef" in API_HASH:
        print("\n❌ ERROR: Please edit API credentials in the script!")
        print("📱 Get from: https://my.telegram.org")
        print("   - API_ID: Your API ID")
        print("   - API_HASH: Your API Hash")
        print("   - PHONE: Your phone number with country code")
        return
    
    # Buat instance
    bot = TelegramMemberAdder(API_ID, API_HASH, PHONE)
    
    try:
        # Connect ke Telegram
        if not await bot.connect():
            return
        
        # Menu utama
        while True:
            print("\n" + "="*50)
            print("📱 MAIN MENU")
            print("="*50)
            print("1. ➕ Add members to group")
            print("2. 📊 Check group info")
            print("3. 🔍 Test single member")
            print("0. ❌ Exit")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                print("\n➕ ADD MEMBERS")
                group = input("Group username (e.g., @groupname): ").strip()
                if not group:
                    print("❌ Group cannot be empty!")
                    continue
                
                # Tanya delay
                try:
                    delay = int(input("Delay between adds (seconds, default 30): ") or "30")
                except:
                    delay = 30
                
                await bot.add_members_from_file(group, delay=delay)
                
            elif choice == "2":
                print("\n📊 GROUP INFO")
                group = input("Group username: ").strip()
                if group:
                    await bot.check_group_info(group)
            
            elif choice == "3":
                print("\n🔍 TEST SINGLE MEMBER")
                group = input("Group username: ").strip()
                member = input("Member username: ").strip()
                
                if group and member:
                    group_entity = await bot.client.get_entity(group)
                    success, msg = await bot.add_single_member(group_entity, member)
                    print(f"\nResult: {'✅ Success' if success else '❌ Failed'}")
                    print(f"Message: {msg}")
            
            elif choice == "0":
                print("\n👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid option!")
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Script stopped by user")
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await bot.disconnect()

if __name__ == "__main__":
    # Check jika di Termux
    if os.path.exists('/data/data/com.termux/files/home'):
        print("📱 Running on Termux Android")
    
    # Jalankan bot
    asyncio.run(main())
