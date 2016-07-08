/* Handles real time comment generation, post submission, post edits and likes */
$(function() {
    // Tinymce options
    tinymce.init({
        selector: "textarea",
        statusbar: false,
        setup: function (editor) {
            editor.on('change', function () {
                editor.save();
            });
        }
    });

    // Stop propagation and default behaviour on form submit
    $("#comment-form").submit(function(e) {
        return false;
    });
    // AJAX form handler
    $("#submit-comment-btn").click(function() {
        // Grab form values
        var commentBody = $("textarea").val();
        var parent = $("#parent").val();
        var commentSubmitter = $("#comment-submitter").val();

        // Form is empty
        if(commentBody === '') {
            // Add error class and messages
            $("#comment-body-error").show();
            $("#comment-form-textarea").addClass("has-error");
            console.log("MEOW");
        }

        // Form is valid
        else {
            //
            // Remove possible error messages
            $("#comment-body-error").hide();
            $("#comment-form-textarea").removeClass("has-error");

            // Show loading animation
            $("#loading").show();
            $("#loading").fadeIn(400).html('<img src="/static/img/load.gif"' +
            'align="absmiddle"><span class="loading"> Loading Comment...</span>');

            $.ajax({
                type: "POST",
                url: "/blog/newcomment",
                data: {'parent': parent,
                       'comment-submitter': commentSubmitter,
                       'comment-body': commentBody},
                cache: false,
                success: function(response) {
                    console.log(response);
                }
            });
        }

        return false;
    }); // End POST for comment

    // Handler to update comment likes
    $(".like-comment-btn").click(function(event) {
        event.stopPropagation();
        var commentId = $(this).data('value');
        var likeAmount = $(this).data('likes');
        var commentLiker = $(this).data('user');

        // If there are no likes yet, set to 1
        if (likeAmount === "None") {
            likeAmount = 1 ;
        }
        else {
            likeAmount++;
        }

        var commentHtml = likeAmount + " <span class='glyphicon glyphicon-heart'></span>";
        var prev = $(this).prev().find(".number-of-likes");

        // Disable like button so user cannot like more than once
        $(this).prop("disabled", true);

        $.ajax({
            type: "PUT",
            url: "/blog/commentliked",
            data: {
                'comment-id': commentId,
                'comment-liker': commentLiker
            },
            cache: false,
            success: function(response) {
                prev.html(commentHtml);
            }
        });
    }); // End PUT for comment likes

    // Handler to update post likes
    $(".like-post-btn").click(function(event) {
        event.stopPropagation();
        var postId = $(this).data('value');
        var likeAmount = $(this).data('likes');
        var postLiker = $(this).data('user');

        // If there are no likes yet, set to 1
        if (likeAmount === "None") {
            likeAmount = 1 ;
        }
        else {
            likeAmount++;
        }

        var postHtml = likeAmount + " <span class='glyphicon glyphicon-heart'></span>";
        var prev = $(this).prev().find(".number-of-likes");

        // Disable like button so user cannot like more than once
        $(this).prop("disabled", true);

        $.ajax({
            type: "PUT",
            url: "/blog/postliked",
            data: {
                'post-id': postId,
                'post-liker': postLiker
            },
            cache: false,
            success: function(response) {
                prev.html(postHtml);
                console.log(response)
            }
        });
    }); // End PUT for post likes
});
