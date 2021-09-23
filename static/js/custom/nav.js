document.addEventListener('DOMContentLoaded', () => {
    reduceCounter = () => {
        counter = document.querySelector('.notification-count');
        counter.textContent -= 1;
        if (counter.textContent == 0){
            counter.style.display = 'none';
        }
    }
    
    responseRequest = () =>{
        document.querySelectorAll('.accept').forEach(accept => accept.addEventListener('click', event => {
            toast = document.querySelector(".toast-container").querySelector(".toast" + event.target.id);
            let xhr = new XMLHttpRequest();
            xhr.open('POST', createFriendshipPath, true);
            xhr.setRequestHeader('X-CSRFToken', csrfToken);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify({ user: toast.querySelector('.user').id, notification: event.target.id}));
            toast.remove()
            reduceCounter();
            
        }))
        
        document.querySelectorAll('.deny').forEach(deny => deny.addEventListener('click', event => {
            toast = document.querySelector(".toast-container").querySelector(".toast" + event.target.id);
            let xhr = new XMLHttpRequest();
            xhr.open('POST', friendRequestPath, true);
            xhr.setRequestHeader('X-CSRFToken', csrfToken);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify({ profile_id: toast.querySelector('.user').id, value: 'deny'}));
            toast.remove()
            reduceCounter();
        }))
    }
    
    setInterval(() => {
        toastContainer = document.querySelector(".toast-container")
        lastNotification = toastContainer.querySelector(".toast");
        lastNotificationId = -1
        if (lastNotification != null) 
            lastNotificationId = lastNotification.id
        let xhr = new XMLHttpRequest();
        xhr.open('POST', getNotificationsPath, true);
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({last_notification_id: lastNotificationId}));
        xhr.onreadystatechange = () => {
            if (xhr.readyState != 4) return;
            if (xhr.status == 200) {
                const data = JSON.parse(xhr.responseText);
                if (Object.keys(data).length != 0){
                    for (i in data){
                        if (lastNotificationId == -1) toastContainer.innerHTML = "";
                        avatar = data[i].sender_avatar;
                        if (avatar == "") avatar = data[i].default_avatar
                        toastContainer.innerHTML = `<div class="toast show toast${data[i].id}" role="alert" aria-live="assertive" aria-atomic="true" id="${data[i].id}">
                            <div class="toast-header">
                                <a href="/profiles/detail/${data[i].sender_id}" class="user" id="${data[i].sender_id}">
                                    <img src="${avatar}" class="rounded me-2 avatar" alt="avatar">
                                </a>
                                <strong class="me-auto">${data[i].sender_username}</strong>
                                <small class="text-muted">${data[i].date_created}</small>
                            </div>
                            <div class="toast-body">
                                Friend request
                                <div class="mt-3 pt-3 border-top d-flex justify-content-evenly">
                                    <button class="btn btn-primary w-50 accept" id="${data[i].id}">Accept</button>
                                    <button class="btn btn-secondary w-50 ms-3 deny" id="${data[i].id}">Deny</button>
                                </div>
                            </div>
                        </div>` + toastContainer.innerHTML;
                        counter = document.querySelector('.notification-count');
                        counter.textContent++;
                        counter.classList.remove("d-none");
                    };
                    responseRequest();
                };
            };
        };
    }, 5000)
})