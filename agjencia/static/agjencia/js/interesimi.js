
document.addEventListener("DOMContentLoaded", function () {
    const dialog = document.getElementById("se-interest-dialog");
    const openButton = document.getElementById("se-interest-open");
    const closeButton = document.getElementById("se-interest-close");
    const cancelButton = document.getElementById("se-interest-cancel");

    if (!dialog || !openButton) {
        return;
    }

    function openDialog() {
        if (!dialog.open) {
            dialog.showModal();
        }
    }

    function closeDialog() {
        if (dialog.open) {
            dialog.close();
        }
    }

    openButton.addEventListener("click", openDialog);

    closeButton.addEventListener("click", closeDialog);

    cancelButton.addEventListener("click", closeDialog);

    dialog.addEventListener("click", function (event) {
        if (event.target === dialog) {
            closeDialog();
        }
    });

    if (dialog.dataset.reopen === "true") {
        openDialog();
    }
});
