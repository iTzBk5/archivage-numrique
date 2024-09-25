document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    if (username === 'bk' && password === '123') {
        // Correctly remove the blur
        document.getElementById('mainOverlay').classList.remove('blurred');
        document.getElementById('loginModal').style.display = 'none';
        document.getElementById('uploadForm').style.display = 'block'; // Show upload form after successful login
        enableInteractions();  // Enable all interactions after successful login
    } else {
        alert('Incorrect Username or Password!');
    }
});

function disableInteractions() {

    // Prevent default on all anchor tags
    document.querySelectorAll("a").forEach(function(link) {
        link.onclick = function(e) {
            e.preventDefault();
            alert('Please login to navigate.');
        };
    });

    // Disable hamburger menu initially
    document.getElementById("hamburger-btn").onclick = function(e) {
        e.preventDefault();
    };
}

function enableInteractions() {
    // Enable form submission
    document.getElementById("uploadForm").onsubmit = function() { return true; };

    // Enable all anchor tags
    document.querySelectorAll("a").forEach(function(link) {
        link.onclick = function() { return true; };
    });

    // Enable hamburger menu
    const hamburgerBtn = document.getElementById("hamburger-btn");
    hamburgerBtn.onclick = function() {
        document.querySelector("header").classList.toggle("show-mobile-menu");
    };
}

// Initially disable interactions
disableInteractions();