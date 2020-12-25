$(document).ready(function()
{
    // check Password difficulty
    $('#pwd').keyup(function()
    {
        var strength = 1;

        /*length 5 characters or more*/
        if (this.value.length > 7) strength++

        /*contains lowercase characters*/
        if(this.value.match(/[a-z]+/)) strength++

        /*contains uppercase characters*/
        if(this.value.match(/[A-Z]+/)) strength++

        /*contains digits*/
        if(this.value.match(/[0-9]+/)) strength++

        /*contains symbols*/
        if(this.value.match(/([!,%,&,@,#,$,^,*,?,_,~])/))  strength++

        /*contains Double symbols*/
        if(this.value.match(/(.*[!,%,&,@,#,$,^,*,?,_,~].*[!,%,&,@,#,$,^,*,?,_,~])/)) strength++


        $('#pb_pwd').attr('aria-valuenow', strength).css('width', (strength*100/7)+'%');

    });

    // check Confirm Password
    $('#cpwd').keyup(function()
    {

        if($(this).val() == $('#pwd').val())
        {
            $(this).removeClass("is-invalid");
            $(this).css({ 'background-color' : ''});
            $("#sub").removeAttr('disabled');

        }
        else
        {
            $(this).addClass("is-invalid");
            $(this).css({ 'background-color' : '#dc354547'});
            $("#sub").attr('disabled', 'disabled');
        }
    });



    //
    // Script For control and sell stocks
    //
    $(".table-row").click(function() {

        // Reset amount value
        $("#amount").val(0);

        // Get data from Table
        var symbol = $(this).find(".sy").text();
        var amount = $(this).find(".am").text();

        // Write data
        $("#symbol_sell").attr('value', symbol);
        $("#assets_sell").attr('value', amount);
        $("#amount").attr('max', amount);
        $("#sell_btn").removeAttr('disabled');
        $("#amount").removeAttr('disabled');
    });

})

// After loading page
$(window).on("load", function () {

});