// Função para alternar entre os modos escuro e claro
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

// Aplicar o tema salvo ao carregar a página
document.addEventListener('DOMContentLoaded', () => {
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme === 'light') {
        document.body.classList.add('light-theme');
    } else {
        document.body.classList.remove('light-theme');
    }
});

// Adicionar o listener de evento ao botão
document.getElementById('toggle-theme-btn').addEventListener('click', toggleTheme);
