function toggleInput(id) {
    var input = document.getElementById(id + "-input");
    if (document.getElementById(id + "-checkbox").checked) {
        input.style.display = "block";
    } else {
        input.style.display = "none";
    }
}
