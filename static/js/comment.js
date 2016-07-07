/* Handles real time comment generation and post submission */
$(function() {
    // Stop propagation and default behaviour on form submit
    tinymce.init({
        selector: "textarea",
        statusbar: false,
        setup: function (editor) {
            editor.on('change', function () {
                editor.save();
            });
        }
    });

    $("#comment-form").submit(function(e) {
        return false;
    });

    $("#submit-comment-btn").click(function() {
        var commentValue = $("textarea").val();
        var dataString = 'content=' + commentValue;

        // Form is empty
        if(commentValue ==='') {
            // Add error class and messages
            $("#comment-body-error").show();
            $("#comment-form-textarea").addClass("has-error");
            console.log("MEOW");
        }

        // Form is valid
        else {
            // Remove possible error messages
            $("#comment-body-error").hide();
            $("#comment-form-textarea").removeClass("has-error");

            // Show loading animation
            $("#flash").show();
            $("#flash").fadeIn(400).html('<img src="/static/img/load.gif"' +
            'align="absmiddle"><span class="loading"> Loading Comment...</span>');

        }
        return false;
    });
});
