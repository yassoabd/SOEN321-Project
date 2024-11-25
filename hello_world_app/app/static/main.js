document.addEventListener('DOMContentLoaded', function() {
    // When the button is clicked, send an AJAX request
    $('#helloButton').on('click', function() {
        $.ajax({
            url: 'http://127.0.0.1:5000/hello',  // Endpoint in the Flask app
            type: 'POST',
            success: function(response) {
                // Display the "Hello World" message in the #result div
                $('#result').text(response.message);
            },
            error: function(error) {
                console.error('Error:', error);
                $('#result').text('Failed to retrieve the message.');
            }
        });
    });
});
