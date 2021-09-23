document.addEventListener('DOMContentLoaded', () => {  
    document.getElementById('post-input').addEventListener('change', (event) => {
        figure = document.getElementById('post-figure');
        figure.classList.remove('d-none');
        figure.classList.add('d-flex');
        img = figure.querySelector('#post-img');
        img.src = URL.createObjectURL(event.target.files[0]);
    });
})