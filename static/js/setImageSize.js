document.addEventListener("DOMContentLoaded", function () {
    const portraits = document.querySelectorAll("img.portrait");

    portraits.forEach(img => {
        img.style.width = "500px";      // doubled width
        img.style.height = "400px";     // increased height
        img.style.objectFit = "cover";  // crop to fit without distortion
        img.style.borderRadius = "6px"; // optional: rounded corners
    });
});
