document.addEventListener("DOMContentLoaded", () => {

    const pages = {
        ".main-page": {
            links: ["debug-console", "test-panel", "logs"],
            source: "main"
        },
        ".neural-page": {
            links: ["admin", "admin-panel", "management"],
            source: "neural"
        },
        ".feedback-page": {
            links: ["config", "env", "system-config"],
            source: "feedback"
        },
        ".about-page": {
            links: ["backup", "db-backup", "data-dump"],
            source: "about"
        }
    };

    Object.keys(pages).forEach(selector => {
        const page = document.querySelector(selector);

        if (page) {
            const serviceBlock = page.querySelector(".service");
            addLinks(serviceBlock, pages[selector].links, pages[selector].source);
        }
    });

    function addLinks(container, links, source) {
        if (!container) return;

        for (let i = 0; i < links.length; i++) {
            const a = document.createElement("a");
            a.className = "link";
            a.href = "/" + links[i] + "/?name=" + links[i] + "&type=js" + "&source=" + source;
            container.appendChild(a);
        }
    }

});
