function toggleInput(id) {
    var input = document.getElementById(id + "-input");
    if (document.getElementById(id + "-checkbox").checked) {
        input.style.display = "block";
    } else {
        input.style.display = "none";
    }
}

document.querySelectorAll('.form__field').forEach(function(input) {
    input.addEventListener('focus', function() {
        var label = this.parentNode.parentNode.querySelector('label');
        if (label) {
            label.style.color = 'transparent';
            label.style.backgroundImage = 'linear-gradient(to right, #11998e, #38ef7d)';
            label.style.webkitBackgroundClip = 'text';
            label.style.fontWeight = '700'; /* Make the text bold */
        }
    });
    input.addEventListener('blur', function() {
        var label = this.parentNode.parentNode.querySelector('label');
        if (label) {
            label.style.color = '#fff';
            label.style.backgroundImage = 'none';
            label.style.fontWeight = 'normal'; /* Make the text normal weight */
        }
    });
});