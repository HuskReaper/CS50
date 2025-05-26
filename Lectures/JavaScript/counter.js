if (!localStorage.getItem('counter')) {
    localStorage.setItem('counter', 0);
}

function count_up() {
    let counter = localStorage.getItem('counter');
    counter++;
    document.querySelector('p').innerHTML = counter;
    localStorage.setItem('counter', counter)
};

document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('p').innerHTML = localStorage.getItem('counter');
    document.querySelector('button').onclick = count_up
}); 