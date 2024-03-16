function toggleTheme() {
    let theme = localStorage.getItem('theme');
    if (theme === 'light') {
        document.body.classList.remove('light-theme');
        localStorage.setItem('theme', 'dark');
        const oldThemeStyle = document.getElementById('theme-style');
        if (oldThemeStyle) {
            oldThemeStyle.remove();
        }
        const darkThemeLink = document.createElement('link');
        darkThemeLink.rel = 'stylesheet';
        darkThemeLink.type = 'text/css';
        darkThemeLink.href = '/static/main/css/styles.css';
        darkThemeLink.id = 'theme-style';
        document.head.appendChild(darkThemeLink);
    } else {
        document.body.classList.add('light-theme');
        localStorage.setItem('theme', 'light');
        const oldThemeStyle = document.getElementById('theme-style');
        if (oldThemeStyle) {
            oldThemeStyle.remove();
        }
        const lightThemeLink = document.createElement('link');
        lightThemeLink.rel = 'stylesheet';
        lightThemeLink.type = 'text/css';
        lightThemeLink.href = '/static/main/css/styles-light.css';
        lightThemeLink.id = 'theme-style';
        document.head.appendChild(lightThemeLink);
    }
}
