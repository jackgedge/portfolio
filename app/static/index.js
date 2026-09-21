// Get all h1 elements with the class "hover-heading"
var h2Elements = document.querySelectorAll('.hover-heading');

// Loop through each h1 element
h2Elements.forEach(function(h2Element) {
    // Add mouseover event listener
    h2Element.addEventListener('mouseover', function() {
        // Make text bold
        this.style.fontWeight = 'bold';
        // Make text italic
        this.style.fontStyle = 'italic';
    });

    // Add mouseout event listener
    h2Element.addEventListener('mouseout', function() {
        // Remove bold style
        this.style.fontWeight = 'normal';
        // Reset rotation
        this.style.fontStyle = 'normal';
    });
});

var topnavElements = document.querySelectorAll('.topnav a')

topnavElements.forEach(function(topnavElement) {
    // Add mouseover event listener
    topnavElement.addEventListener('mouseover', function() {
            // Make text bold
            this.style.fontWeight = 'bold';
            // Make text italic
            this.style.fontStyle = 'italic';
        });
    // Add mouseout event listener
    topnavElement.addEventListener('mouseout', function() {
        // Remove bold style
        this.style.fontWeight = 'normal';
        // Reset rotation
        this.style.fontStyle = 'normal';
    });
});


var dropbtnElements = document.querySelectorAll('.dropbtn')

dropbtnElements.forEach(function(dropbtnElement) {
    // Add mouseover event listener
    dropbtnElement.addEventListener('mouseover', function() {
            // Make text bold
            this.style.fontWeight = 'bold';
            // Make text italic
            this.style.fontStyle = 'italic';
        });
    // Add mouseout event listener
    dropbtnElement.addEventListener('mouseout', function() {
        // Remove bold style
        this.style.fontWeight = 'normal';
        // Reset rotation
        this.style.fontStyle = 'normal';
    });
});


/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

// Refresh page when user scrolls to bottom on mobile devices (Index page infinite scroll)
var indexGallery = document.getElementById('index-gallery');

if (indexGallery) {
    // Reset scroll restoration so reloading starts at the top
    if ('scrollRestoration' in history) {
        history.scrollRestoration = 'manual';
    }

    var isRefreshing = false;

    window.addEventListener('scroll', function() {
        // Only run on mobile devices (screens 768px or narrower)
        var isMobile = window.innerWidth <= 768;

        if (isMobile && !isRefreshing) {
            // Check if user has scrolled near the bottom of the page
            var scrolledToBottom = (window.innerHeight + window.scrollY) >= (document.documentElement.scrollHeight - 20);

            if (scrolledToBottom) {
                isRefreshing = true;
                window.scrollTo(0, 0);
                window.location.reload();
            }
        }
    });
}
 