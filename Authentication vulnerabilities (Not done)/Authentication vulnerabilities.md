# Authentication vulnerabilities
## Khái niệm
**Authentication**, hay **Xác thực**, là quá trình kiểm tra xem user đăng nhập vào có đúng là chính chủ tài khoản hay không. Khái niệm đơn giản nhất cho việc xác thực chính là mật khẩu, sau đó là các hình thức khác như 2FA, passkey,... Tuy nhiên, kẻ tấn công vẫn có thể xâm nhập vào tài khoản dù không biết chính xác mật khẩu.
## Lab
### Lab: Username enumeration via different responses
Lab này giả định kẻ tấn công có 1 danh sách tài khoản và mật khẩu, giờ cần kiểm tra xem tài khoản nào hợp lệ và mật khẩu nào cho tài khoản đó. Ta sẽ sử dụng Burp Intruder để bruteforce lab này.
![image-1](images/image-1.png)

Đối với tài khoản nào không hợp lệ, hệ thống báo `Invalid username`

![image-2](images/image-2.png)

Còn với tài khoản hợp lệ, hệ thống báo `Incorrect Password`

![image-3](images/image-3.png)

Sau khi tìm được username, ta chuyển sang bruteforce mật khẩu

![image-4](images/image-4.png)

Mật khẩu đúng sẽ có status 302. Lấy tài khoản và mật khẩu đăng nhập để hoàn thành lab.

![image-5](images/image-5.png)

### Lab: Username enumeration via subtly different responses
Cũng cách thức tương tự như trên, tuy nhiên khi bruteforce danh sách tài khoản ta nhận thấy độ dài của các request chỉ chênh lệch từ 3-12 kí tự:

![image-6](images/image-6.png)

Điều đó là do ở trong các dòng HTML của page xuất hiện dòng `fetch('/analytics?id=***')`

![image-7](images/image-7.png)

Mục đích chính của dòng trên chỉ mang tính chất gây nhiễu để ta không thể check request bằng độ dài. 

Khi kiểm tra thông báo của các request sai, ta thấy đều là `Invalid username or password.`
![image-8](images/image-8.png)

Vậy nếu ta thử filter lọc đi những request chứa câu đó thì sao?

![image-9](images/image-9.png)

Bước còn lại là bruteforce để tìm mật khẩu.

![image-10](images/image-10.png)

![image-11](images/image-11.png)
