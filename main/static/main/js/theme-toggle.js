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

function toggleThemeStyles() {
    let theme = localStorage.getItem('theme');
    const oldThemeStyle = document.getElementById('theme-style');
    if (oldThemeStyle) {
        oldThemeStyle.remove();
    }

    if (theme === 'light') {
        const lightThemeLink = document.createElement('link');
        lightThemeLink.rel = 'stylesheet';
        lightThemeLink.type = 'text/css';
        lightThemeLink.href = '/static/main/css/styles-light.css';
        lightThemeLink.id = 'theme-style';
        document.head.appendChild(lightThemeLink);
    } else {
        const darkThemeLink = document.createElement('link');
        darkThemeLink.rel = 'stylesheet';
        darkThemeLink.type = 'text/css';
        darkThemeLink.href = '/static/main/css/styles.css';
        darkThemeLink.id = 'theme-style';
        document.head.appendChild(darkThemeLink);
    }
}

toggleThemeStyles();

const themeButton = document.getElementById('theme-button');
if (themeButton) {
    themeButton.addEventListener('click', function() {
        toggleTheme();
        toggleThemeStyles();
    });
}
