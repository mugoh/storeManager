var slide_count = 0;

start_slide();

var max_slide_number;

var slides = document.getElementByClassName('slides-gonna-start-now');
var slide_mark = document.getElementByClassName('slides-gonna-start-now');

for (max_slide_number=0; max_slide_number < slides.length; max_slide_number++)
{
	slide_mark[max_slide_number].style.display = "none";
}

slide_count++;

if (slide_count > slides.length) {slide_count = 1}
for (max_slide_number = 0; max_slide_number < slide_mark.length; max_slide_number++) {
		slide_mark[max_slide_number].className = slide_mark[max_slide_number].className.replace("active", "");
}

slides[slide_count-1].style.display = "block";
slide_mark[slide_count-1].className += " active";
setTimeout(start_slide, 3000);
