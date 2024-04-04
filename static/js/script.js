// script.js
$(document).ready(function() {
    $('#openPythonTerminalButton').on('click', function() {
        $.ajax({
            url: '/get_user_code/',
            method: 'GET',
            dataType: 'json',
            success: function(data) {
                // Redirect to the Python terminal page with code as a URL parameter
                window.location.href = '/python_terminal/?code=' + encodeURIComponent(data.code);
            },
            error: function() {
                alert('No code found or error retrieving code.');
            }
        });
    });
});
