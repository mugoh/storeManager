

var slide_count = 0;
start_slides();

function start_slides() {

    var slides = document.getElementsByClassName("slides-gonna");
    var slide_mark = document.getElementsByClassName("dot");
    var slide_index;
    for (slide_index = 0; slide_index < slides.length; slide_index++) {
       slides[slide_index].style.display = "none";  
       
    }

    slide_count++;

    if (slide_count > slides.length) {slide_count = 1}    

    for (slide_index = 0; slide_index < slide_mark.length; slide_index++) {

        slide_mark[slide_index].className = slide_mark[slide_index].className.replace(" active", "");
    }

    slides[slide_count-1].style.display = "block";  
    slide_mark[slide_count-1].className += " active";
    setTimeout(start_slides, 10000); // Change image every 2 seconds
}