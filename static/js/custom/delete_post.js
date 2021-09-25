document.addEventListener('DOMContentLoaded', () => {
    deletePost = (event) => {
        if (!confirm("Are you sure you want to delete this post?")) return;
        let xhr = new XMLHttpRequest();
        xhr.open('POST', deletePostPath, true);
        xhr.setRequestHeader('X-CSRFToken', csrfToken);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.send(JSON.stringify({ id: event.target.id }));
        document.getElementById(event.target.id).remove();
    }
    document.querySelectorAll('.delete').forEach((btn) => {
        btn.addEventListener('click', deletePost);
    });
});