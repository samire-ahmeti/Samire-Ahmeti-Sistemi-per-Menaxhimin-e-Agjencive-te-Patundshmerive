
document.addEventListener("DOMContentLoaded", () => {
    const dialog = document.getElementById("se-register-dialog");
    const openButton = document.getElementById("se-open-register");
    const closeButton = document.getElementById("se-register-close");
    const form = document.getElementById("se-register-form");
    const feedback = document.getElementById("se-register-feedback");
    const submitButton = document.getElementById("se-register-submit");

    if (!dialog || !openButton || !form) {
        return;
    }

    openButton.addEventListener("click", (event) => {
        event.preventDefault();
        dialog.showModal();
        form.querySelector("input[name='username']").focus();
    });

    closeButton.addEventListener("click", () => {
        dialog.close();
    });

    dialog.addEventListener("click", (event) => {
        if (event.target === dialog) {
            dialog.close();
        }
    });

    function clearErrors() {
        form.querySelectorAll("[data-error-for]").forEach((element) => {
            element.textContent = "";
        });

        form.querySelectorAll("[aria-invalid]").forEach((element) => {
            element.removeAttribute("aria-invalid");
        });
    }

    function showFeedback(message, success = false) {
        feedback.hidden = false;
        feedback.textContent = message;
        feedback.classList.toggle("success", success);
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        clearErrors();
        feedback.hidden = true;
        submitButton.disabled = true;
        submitButton.textContent = "Duke regjistruar...";

        try {
            const response = await fetch(form.action, {
                method: "POST",
                body: new FormData(form),
                credentials: "same-origin",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            const contentType = response.headers.get("content-type") || "";

            if (!contentType.includes("application/json")) {
                throw new Error("Përgjigje e papritur nga serveri.");
            }

            const data = await response.json();

            if (response.ok && data.ok) {
                form.reset();
                form.classList.add("se-register-hidden");

                showFeedback(data.message, true);
                return;
            }

            const errors = data.errors || {};

            Object.entries(errors).forEach(([field, messages]) => {
                const errorElement = Array.from(
                    form.querySelectorAll("[data-error-for]")
                ).find((element) => element.dataset.errorFor === field);

                const input = Array.from(form.elements).find(
                    (element) => element.name === field
                );

                if (errorElement) {
                    errorElement.textContent = messages.join(" ");
                }

                if (input) {
                    input.setAttribute("aria-invalid", "true");
                }
            });

            showFeedback(
                data.message || "Kontrollo të dhënat e formularit."
            );

        } catch (error) {
            showFeedback(
                "Regjistrimi nuk u përfundua. Kontrollo lidhjen dhe provo përsëri."
            );
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = "Krijo llogarinë";
        }
    });
});
