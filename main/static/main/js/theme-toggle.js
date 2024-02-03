function toggleTheme() {
    let theme = localStorage.getItem('theme');
    if (theme === 'light') {
        document.body.classList.remove('light-theme');
        localStorage.setItem('theme', 'dark');
    } else {
        document.body.classList.add('light-theme');
        localStorage.setItem('theme', 'light');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme === 'light') {
        document.body.classList.add('light-theme');
    } else {
        document.body.classList.remove('light-theme');
    }
});

document.getElementById('toggle-theme-btn').addEventListener('click', toggleTheme);
