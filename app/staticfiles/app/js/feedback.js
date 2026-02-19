document.addEventListener("DOMContentLoaded", () => {
  document.querySelector('input[name="js_enabled"]').value = 1;
});


document.addEventListener("DOMContentLoaded", function() {
    const startTime = Date.now();

    document.querySelector("form").addEventListener("submit", function () {
        const seconds = Math.floor((Date.now() - startTime) / 1000);
        document.getElementById("time_on_page").value = seconds;
    });
});