//bank account created alert
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('button').addEventListener('click', function() {
        alert('Bank account created successfully!');
        e.preventDefault();
        window.location.reload();
    });
});