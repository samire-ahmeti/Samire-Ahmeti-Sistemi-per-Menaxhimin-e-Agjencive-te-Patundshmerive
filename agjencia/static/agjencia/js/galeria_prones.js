
document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("se-photo-modal");
    const fotoButtons = Array.from(
        document.querySelectorAll("[data-photo-src]")
    );

    if (!modal || fotoButtons.length === 0) {
        return;
    }

    const modalImage = document.getElementById("se-photo-modal-image");
    const closeButton = document.getElementById("se-photo-close");
    const prevButton = document.getElementById("se-photo-prev");
    const nextButton = document.getElementById("se-photo-next");
    const counter = document.getElementById("se-photo-counter");

    let currentIndex = 0;

    function showPhoto(index) {
        currentIndex = (
            index + fotoButtons.length
        ) % fotoButtons.length;

        const selectedPhoto = fotoButtons[currentIndex];

        modalImage.src = selectedPhoto.dataset.photoSrc;
        modalImage.alt = selectedPhoto.dataset.photoAlt || "Fotografi e pronës";

        counter.textContent = (
            currentIndex + 1
        ) + " / " + fotoButtons.length;

        const hasMultiplePhotos = fotoButtons.length > 1;

        prevButton.hidden = !hasMultiplePhotos;
        nextButton.hidden = !hasMultiplePhotos;
    }

    fotoButtons.forEach(function (button, index) {
        button.addEventListener("click", function () {
            showPhoto(index);

            if (!modal.open) {
                modal.showModal();
            }
        });
    });

    closeButton.addEventListener("click", function () {
        modal.close();
    });

    prevButton.addEventListener("click", function () {
        showPhoto(currentIndex - 1);
    });

    nextButton.addEventListener("click", function () {
        showPhoto(currentIndex + 1);
    });

    document.addEventListener("keydown", function (event) {
        if (!modal.open) {
            return;
        }

        if (event.key === "ArrowLeft") {
            event.preventDefault();
            showPhoto(currentIndex - 1);
        }

        if (event.key === "ArrowRight") {
            event.preventDefault();
            showPhoto(currentIndex + 1);
        }
    });

    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.close();
        }
    });

    modal.addEventListener("close", function () {
        modalImage.removeAttribute("src");
    });
});
