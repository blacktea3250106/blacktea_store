// Function to switch to the next slide
function switchToNextSlide() {
    const slides = document.querySelectorAll('.slide');
    const controls = document.querySelectorAll('[name="control"]');
    const activeControl = document.querySelector('[name="control"]:checked');
    const activeSlideIndex = Array.from(controls).indexOf(activeControl);
    const nextSlideIndex = (activeSlideIndex + 1) % slides.length;

    controls[nextSlideIndex].checked = true;
}

// Set an interval to switch to the next slide every 2.5 second (2500ms)
setInterval(switchToNextSlide, 2500);