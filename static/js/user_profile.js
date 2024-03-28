const editButton = document.getElementById("editButton");
        const readOnlyContainer = document.getElementById("readOnlyContainer");
        const editableContainer = document.getElementById("editableContainer");

        editButton.addEventListener("click", () => {
            readOnlyContainer.style.display = "none";
            editableContainer.style.display = "block";
        });

        const editForm = document.getElementById("editForm");
        editForm.addEventListener("submit", (e) => {
            e.preventDefault();
            // Handle form submission (e.g., send data to server)
            // For demonstration purposes, we just toggle back to the read-only view
            readOnlyContainer.style.display = "block";
            editableContainer.style.display = "none";
        });

        const profilePhotoInput = document.getElementById("profilePhoto");
        const fileNameSpan = document.getElementById("fileName");

        profilePhotoInput.addEventListener("change", () => {
            const files = profilePhotoInput.files;
            if (files.length > 0) {
                fileNameSpan.textContent = files[0].name;
            } else {
                fileNameSpan.textContent = "No file chosen";
            }
        });