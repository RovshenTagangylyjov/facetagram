document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('search').addEventListener('keyup', (event) => {
        value = event.target.value;
        if ([13, 38, 40].includes(event.keyCode)) return;
        friends = false;
        if (document.URL.endsWith('friends'))
            friends = true;
        let xhr = new XMLHttpRequest();
        xhr.open('POST', searchPath, true);
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({ search: value, friends: friends }));
        xhr.onreadystatechange = () => {
            if (xhr.readyState != 4) return;
            if (xhr.status == 200) {
                const profiles = JSON.parse(xhr.responseText);
                let a = [];
                for (i=0; i<profiles.length; i++){
                    a[i] = profiles[i]["username"];
                };
                autocomplete(a);
            };
        };
    });
});