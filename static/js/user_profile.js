

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