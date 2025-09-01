
function Start() {
    UserMenuListener();
}

function UserMenuListener() {
    const userButton = document.getElementById("nav-user-button");
    const userMenu = document.getElementById("user-menu");
    let open = false;
    userButton.addEventListener('click', () => {
        open = !open;
        userButton.setAttribute('aria-expanded', open);
        userMenu.classList.toggle('open');
        userButton.classList.toggle('open');
    })
}

Start();