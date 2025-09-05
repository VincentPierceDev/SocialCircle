function Start() {

    const mobileControls = new MobileDashboardControls();

    ServerListHoverEffects();

    //dashboard.css side panel breakpoint
    if(window.screen.width <= 1275){
        mobileControls.SideMenuControl();
        ServerListMobileClicks(mobileControls);
    }
        
}


class MobileDashboardControls {
    DASHBOARD_SERVER_INFO_OPEN = false;
    DASHBOARD_SETTINGS_INFO_OPEN = false;
    controlContainer = undefined;
    infoPanel = undefined;
    settingsPanel = undefined;
    quickAccessPanel = undefined;
    serverPanel = undefined;

    constructor() {
        this.controlContainer = document.getElementById('mobile-controls-wrapper');
        this.infoPanel = document.getElementById('info-panel');
        this.settingsPanel = document.getElementById('control-panel');
        this.quickAccessPanel = document.getElementById('quick-access-panel');
        this.serverPanel = document.getElementById('server-panel');
    }

    SideMenuControl() {
        this.controlContainer.addEventListener('click', (event) => {
            const button = event.target;
            if(button.id == "right-control") {

                if(this.DASHBOARD_SETTINGS_INFO_OPEN) {
                    this.CloseSettingsInfo();
                }

                if(this.DASHBOARD_SERVER_INFO_OPEN)
                    this.CloseServerInfo();
                else
                    this.OpenServerInfo();

            } else if(button.id == "left-control") {

                if(this.DASHBOARD_SERVER_INFO_OPEN) {
                    this.CloseServerInfo();
                }

                if(this.DASHBOARD_SETTINGS_INFO_OPEN)
                    this.CloseSettingsInfo();
                else
                    this.OpenSettingsInfo();
            }
        })
    }

    OpenServerInfo() {
        this.infoPanel.classList.add('open-info');
        this.DASHBOARD_SERVER_INFO_OPEN = true;
        
        this.quickAccessPanel.classList.add('open-right');
        this.serverPanel.classList.add('open-right');
    }

    CloseServerInfo() {
        this.infoPanel.classList.remove('open-info');
        this.DASHBOARD_SERVER_INFO_OPEN = false;

        this.quickAccessPanel.classList.remove('open-right');
        this.serverPanel.classList.remove('open-right');
    }

    OpenSettingsInfo() {
        this.settingsPanel.classList.add('open-settings');
        this.DASHBOARD_SETTINGS_INFO_OPEN = true;
     
        this.quickAccessPanel.classList.add('open-left');
        this.serverPanel.classList.add('open-left');
    }

    CloseSettingsInfo() {
        this.settingsPanel.classList.remove('open-settings');
        this.DASHBOARD_SETTINGS_INFO_OPEN = false;

        this.quickAccessPanel.classList.remove('open-left');
        this.serverPanel.classList.remove('open-left');
    }
}


function ServerListHoverEffects() {
    const serverList = document.getElementById("full-server-list");
    let currentCard;
    serverList.addEventListener('mouseover', (event) => {
        let button = event.target;
        if(button.className == "server-button" && !currentCard) {
            const card = button?.parentElement; //server card (list item)
            currentCard = card;
            card.classList.add('hovered-card');
        } else if(currentCard) {
            //ensure card is valid before removing class
            currentCard.classList.remove('hovered-card');
            currentCard = undefined;
        }
    })
}

function ServerListMobileClicks(mobileControls) {
    const serverList = document.getElementById("full-server-list");
    serverList.addEventListener('click', (event) => {
        let button = event.target;
        if(button.className == "server-button") {
            mobileControls.OpenServerInfo();
        }
    })
}

Start();