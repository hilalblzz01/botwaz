import requests
import json
import re

class RobloxBirthdateUpdater:
    def __init__(self, cookies):
        self.session = requests.Session()
        self.session.cookies.update(cookies)
        self.session.headers.update({
            "user-agent": "Mozilla/5.0 (Linux; Android 16; 2412DPC0AG Build/BP2A.250605.031.A3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.7632.79 Mobile Safari/537.36",
            "accept": "application/json, text/plain, */*",
            "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://www.roblox.com",
            "referer": "https://www.roblox.com/",
            "sec-ch-ua": '"Not:A-Brand";v="99", "Android WebView";v="145", "Chromium";v="145"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "x-requested-with": "mark.via.gp"
        })
    
    def get_csrf_token(self):
        """Mendapatkan token CSRF yang valid dengan melakukan request ke homepage"""
        try:
            # Request ke homepage untuk mendapatkan token CSRF baru
            response = self.session.get(
                "https://www.roblox.com/home",
                timeout=30
            )
            
            # Cari token CSRF dari response headers atau cookies
            if 'x-csrf-token' in response.headers:
                return response.headers['x-csrf-token']
            
            # Alternatif: coba ambil dari cookies
            for cookie in self.session.cookies:
                if cookie.name == 'XSRF-TOKEN' or cookie.name == 'csrf':
                    return cookie.value
            
            # Jika tidak ditemukan, coba parse dari response text
            match = re.search(r'csrf-token[^>]+content="([^"]+)"', response.text)
            if match:
                return match.group(1)
                
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting CSRF token: {e}")
            return None
    
    def update_birthdate(self, birth_month, birth_day, birth_year):
        """Mengupdate birthdate dengan token CSRF yang valid"""
        
        # Dapatkan token CSRF baru
        csrf_token = self.get_csrf_token()
        
        if not csrf_token:
            print("Gagal mendapatkan CSRF token")
            return None
        
        print(f"CSRF Token didapatkan: {csrf_token}")
        
        # Update headers dengan token CSRF baru
        headers = {
            "x-csrf-token": csrf_token,
            "rblx-challenge-metadata": "eyJ2ZXJpZmljYXRpb25Ub2tlbiI6Ik1yYmozUDRObTBxclE4U19PWWk3akEiLCJyZW1lbWJlckRldmljZSI6ZmFsc2UsImNoYWxsZW5nZUlkIjoiMWQ3MmFhNDItN2Q3Mi00NDZhLTkzODYtZjkwNjhkZTI1ZGViIiwiYWN0aW9uVHlwZSI6IkdlbmVyaWMifQ==",
            "rblx-challenge-id": "us-central-0550cd9b-3c58-4899-b791-422500e4cd38",
            "rblx-challenge-type": "chef",
            "traceparent": "00-bc192ae481844256b334d7c6d23d6c19-bdca90a1151c88ff-00",
            "x-bound-auth-token": "v1|Gkf0T3xvtAodfRAlhfsonieBzKTg6lLkA5ejZS6j0S4=|1772097036|iXZtsKBFc/PmiviHLF6qh6SRhcNHAO79kcuKzN8nQYYYjCiNYS0y1m/gJC+qd9RJTjKkV+ytlowu0ETGo9U0vA==|yH+2c4rtHFDt8icLh3OrZpwwCP8ndRZZyPl2XqyKQYiMLDjWDCq8Hb/LA2quqFWDlQmoUkW+WHtRSgD1rXuqjA==",
            "x-retry-attempt": "1",
            "priority": "u=1, i"
        }
        
        # Data payload
        payload = {
            "birthMonth": birth_month,
            "birthDay": birth_day,
            "birthYear": birth_year
        }
        
        # Update session headers
        self.session.headers.update(headers)
        
        # Kirim request
        try:
            print("Mengirim request ke /v1/birthdate...")
            response = self.session.post(
                "https://users.roblox.com/v1/birthdate",
                json=payload,
                timeout=30
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Body: {response.text}")
            
            # Handle kasus token invalid lagi
            if response.status_code == 403 and "XSRF token invalid" in response.text:
                print("Token CSRF masih invalid, mencoba mendapatkan token baru...")
                # Coba dapatkan token dari response headers
                if 'x-csrf-token' in response.headers:
                    new_token = response.headers['x-csrf-token']
                    print(f"Mendapatkan token baru dari response: {new_token}")
                    self.session.headers['x-csrf-token'] = new_token
                    # Ulangi request
                    response = self.session.post(
                        "https://users.roblox.com/v1/birthdate",
                        json=payload,
                        timeout=30
                    )
                    print(f"Status Code (percobaan ke-2): {response.status_code}")
                    print(f"Response Body (percobaan ke-2): {response.text}")
            
            return response
            
        except requests.exceptions.RequestException as e:
            print(f"Error saat mengirim request: {e}")
            return None

# Cookies baru dari data Anda
cookies = {
    "RBXEventTrackerV2": "CreateDate=02/23/2026 01:10:14&rbxid=10565915090&browserid=1771750821662001",
    "RBXPaymentsFlowContext": "c9cd0553-6e2b-4842-a9e1-45bd98ba643a,WebRobuxPurchase",
    "rbx-ip2": "1",
    "__stripe_mid": "da50b8ac-bafc-470b-abb1-a3ee215555ed172f62",
    "__utma": "200924205.158695342.1771830583.1771830583.1772094804.2",
    "__utmb": "200924205.0.10.1772094804",
    "__utmc": "200924205",
    "RBXSource": "rbx_acquisition_time=02/23/2026 07:09:40&rbx_acquisition_referrer=https://www.google.com/&rbx_medium=Social&rbx_source=www.google.com&rbx_campaign=&rbx_adgroup=&rbx_keyword=&rbx_matchtype=&rbx_send_info=0",
    "GuestData": "UserID=-74410054",
    "_ga": "GA1.1.94059792.1771830646",
    ".ROBLOSECURITY": "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhADIhsKBGR1aWQSEzQ1OTU5Njk2NjkxNTY2NTQ1NDMoAw.twaYSJe6aMVltQa6da0BFmnNjVegCjB-Y3DPdu4ZzRodFBEYoOxaZ1RQXPQHs3ujremJ-sbU3YRLbxrMeree1NuOrqyu_ZgjTtzHLdOATYAeWk949ZcHi-5szQM0gn4J-02iLAuz09nQmkLFCT6nCiCUbqUxj2VOoo6wvDJ20d81b9yPWKZz0f8a18KtQA26DZ5pntd5A7BMnCYB4sKTV25bifuebk87_g8PWlVaKrBqjKr-uyFwOjYg444IHOxtyMLJi4RraZIxExKxHuH0qKJHTBwuXEuL_mLdvb3DniNuMaObsz849BT3aIxF_FCWlK0nzf0zuLBA0cWQP_JNDj7FZTir2z7MTeeayATKjF1p9CdqOjIqjgCaRrx3gH07l1_PXSjFiOQUHqLLPDk_r7JPAmXWKmhxri2_pbpmxkz8iELKktSXnn96h9xhK6s434vjJh6ZDv1l6RN2FSPN930btsAtrgEJD7q6pjoQTNCSWxLVo9IBFpPGZBGl7B5ARIfC2-puXakxakWgoTZzTy45PsF9dL8QofZQxmnvljP3vUz0Cx1jf12yvWTErmChWqgfxCJtrG1Hc_kRt0D-p93wwbcgf1nlpmnpD_hy2igndxo2XP2D3CUM-4t5Ztp5dYcJ6uYX1yTx88q1YdENS_EpQW8Wf8Q0X4E5BvE5KTJLGCdjVIqxg4BkdAzY68aRJhh6Q1UD7bpyvgFJqzEXR6xjetxPmWwiy9_7f94pKjQG_78IpjA5g9Cw6hvAmNhbjKhAo8kzz96AXvqdbka5dKKsKE4_LDLjr3GvIAOD2O-rX-LO",
    "__stripe_sid": "e1ec4fbd-393c-4fe7-aeef-f1547915c8b5d766f0",
    "__utmz": "200924205.1771830583.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)",
    "_ga_F8VP9T1NT3": "GS2.1.s1771830645$o1$g0$t1771830652$j53$l0$h0",
    "RBXcb": "RBXViralAcquisition%3Dtrue%26RBXSource%3Dtrue%26GoogleAnalytics%3Dtrue",
    "RBXSessionTracker": "sessionid=0d9fb98e-43e5-4b1d-b65e-aa7d4066bfeb"
}

# Contoh penggunaan
if __name__ == "__main__":
    # Inisialisasi class
    roblox = RobloxBirthdateUpdater(cookies)
    
    # Update birthdate (gunakan data dari request Anda)
    # birthMonth: 3 (Maret), birthDay: 4, birthYear: 2015
    response = roblox.update_birthdate(
        birth_month=3,
        birth_day=4,
        birth_year=2015
    )
    
    if response and response.status_code == 200:
        print("✅ Birthdate berhasil diupdate!")
    else:
        print("❌ Gagal mengupdate birthdate")