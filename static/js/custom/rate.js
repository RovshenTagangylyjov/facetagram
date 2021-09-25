document.addEventListener('DOMContentLoaded', () => {
    sendRate = (event) => {
        let xhr = new XMLHttpRequest();
        let path = ratePostPath;
        let thumbs = document.querySelectorAll('.p' + event.target.id);
        if (event.target.classList.contains('comment-rate')){
            path = rateCommentPath;
            thumbs = document.querySelectorAll('.c' + event.target.id);
        }
        xhr.open('POST', path, true);
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
        xhr.setRequestHeader('Content-Type', 'application/json');
        if (event.target.classList.contains('like')) {
            if (event.target.classList.contains('fas')) {
                event.target.classList.remove('fas', 'text-primary');
                event.target.classList.add('far');
                value = 0;
            } else {
                event.target.classList.add('fas', 'text-primary');
                value = 1;
                if (thumbs[1].classList.contains('fas')) {
                    thumbs[1].classList.remove('fas', 'text-danger');
                }
            }
        } else {
            if (event.target.classList.contains('fas')) {
                event.target.classList.remove('fas', 'text-danger');
                event.target.classList.add('far');
                value = 0;
            } else {
                event.target.classList.add('fas', 'text-danger');
                value = -1;
                if (thumbs[0].classList.contains('fas')) {
                    thumbs[0].classList.remove('fas', 'text-primary');
                }
            }
        }
        xhr.send(JSON.stringify({ id: event.target.id, value: value }));
        xhr.onreadystatechange = () => {
            if (xhr.readyState != 4) return;
            if (xhr.status == 200) {
                const data = JSON.parse(xhr.responseText);
                thumbs[0].textContent = data['likes'];
                thumbs[1].textContent = data['dislikes'];
            }
        };
    };
    document.querySelectorAll('.rate').forEach((rate) => {
        rate.addEventListener('click',  sendRate);
    });
});