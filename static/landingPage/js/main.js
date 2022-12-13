$(function(){
    $("#form-total").steps({
        headerTag: "h2",
        bodyTag: "section",
        transitionEffect: "fade",
        enableAllSteps: true,
        autoFocus: true,
        transitionEffectSpeed: 500,
        titleTemplate : '<div class="title">#title#</div>',
        labels: {
            previous : 'Back',
            next : 'Next',
            finish : 'Confirm',
            current : ''
        },
        onStepChanging: function (event, currentIndex, newIndex) { 
            var fullname = $('#id_name').val();
            var room = $('#id_gender').val();
            var day = $('#day').val();
            var time = $('#id_phone').val();

            $('#id_name-val').text(fullname);
            $('#id_gender-val').text(room);
            $('#day-val').text(day);
            $('#id_phone-val').text(time);

            return true;
        }
    });
    $("#day").datepicker({
        dateFormat: "MM - DD - yy",
        showOn: "both",
        buttonText : '<i class="zmdi zmdi-chevron-down"></i>',
    });
});

let input = document.querySelectorAll('input')
for (let i = 0; i < input.length; i++) {
    input[i].removeAttribute('placeholder')
}
