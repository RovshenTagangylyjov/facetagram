document.addEventListener('DOMContentLoaded', () => {
    friendRequest = (event) => {
        let value = 0;
        if (event.target.classList.contains('add')){
            value = 'add';
            event.target.classList.remove('add', 'btn-primary', 'fa-user-plus');
            event.target.classList.add('cancel', 'btn-warning', 'fa-user-minus');
        } else if(event.target.classList.contains('remove')){
            value = 'remove';
            event.target.classList.remove('remove', 'btn-danger', 'fa-user-minus');
            event.target.classList.add('add', 'btn-primary', 'fa-user-plus');
            document.querySelector('#link' + event.target.id).remove();
        } else{
            value = 'cancel';
            event.target.classList.remove('cancel', 'btn-warning', 'fa-user-minus');
            event.target.classList.add('add', 'btn-primary', 'fa-user-plus');
        };
        let xhr = new XMLHttpRequest();
        xhr.open('POST', friendRequestPath, true);
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({ profile_id: event.target.id, value: value }));
    };
    document.querySelectorAll('.request').forEach(btn => btn.addEventListener('click', friendRequest));
});