// Add any custom JavaScript here

// Automatically close flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    // Get all flash messages
    var flashMessages = document.querySelectorAll('.alert');
    
    // For each flash message, set a timeout to remove it
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            // If Bootstrap is used, use the built-in close method
            var closeButton = message.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            } else {
                // Otherwise, fade out and remove manually
                message.style.opacity = '0';
                setTimeout(function() {
                    message.style.display = 'none';
                }, 500);
            }
        }, 5000);
    });
});

// Confirm deletion of items
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this item?');
}
