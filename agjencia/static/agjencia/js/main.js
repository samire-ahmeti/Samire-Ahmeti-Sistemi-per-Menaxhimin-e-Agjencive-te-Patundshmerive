
document.addEventListener("DOMContentLoaded", function () {
    const menuButton = document.querySelector(".mobile-menu-button");
    const navigation = document.querySelector(".main-navigation");
    const navigationLinks = document.querySelectorAll(".nav-link");

    if (menuButton && navigation) {
        function closeMenu() {
            navigation.classList.remove("is-open");
            menuButton.setAttribute("aria-expanded", "false");
            menuButton.setAttribute("aria-label", "Hap menynë");
        }

        menuButton.addEventListener("click", function () {
            const isOpen = navigation.classList.toggle("is-open");

            menuButton.setAttribute("aria-expanded", String(isOpen));
            menuButton.setAttribute(
                "aria-label",
                isOpen ? "Mbyll menynë" : "Hap menynë"
            );
        });

        navigationLinks.forEach(function (link) {
            link.addEventListener("click", closeMenu);
        });

        document.addEventListener("click", function (event) {
            if (
                !navigation.contains(event.target) &&
                !menuButton.contains(event.target)
            ) {
                closeMenu();
            }
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                closeMenu();
            }
        });

        window.addEventListener("resize", function () {
            if (window.innerWidth > 850) {
                closeMenu();
            }
        });
    }

    const currentPath = window.location.pathname;

    navigationLinks.forEach(function (link) {
        const linkPath = new URL(link.href).pathname;

        if (linkPath === currentPath) {
            link.classList.add("active");
            link.setAttribute("aria-current", "page");
        } else {
            link.classList.remove("active");
            link.removeAttribute("aria-current");
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const mainImage = document.getElementById("main-property-image");
    const thumbnails = document.querySelectorAll(".gallery-thumbnail");

    if (!mainImage || thumbnails.length === 0) {
        return;
    }

    thumbnails.forEach(function (thumbnail) {
        thumbnail.addEventListener("click", function () {
            const imageUrl = thumbnail.dataset.galleryImage;
            const imageAlt = thumbnail.dataset.galleryAlt;

            if (!imageUrl) {
                return;
            }

            mainImage.src = imageUrl;
            mainImage.alt = imageAlt || "Fotografia e pronës";

            thumbnails.forEach(function (item) {
                item.classList.remove("active");
                item.setAttribute("aria-pressed", "false");
            });

            thumbnail.classList.add("active");
            thumbnail.setAttribute("aria-pressed", "true");
        });
    });
});
