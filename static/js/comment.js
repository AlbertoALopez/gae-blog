/* Handles real time comment generation, post submission, post edits and likes */
$(function() {
    // Tinymce init options
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

    // AJAX handler for new comments
    $("#submit-comment-btn").click(function() {
        var commentBody = $("textarea").val();
        var parent = $("#parent").val();
        var commentSubmitter = $("#comment-submitter").val();
        var lastComment = $(".comment").last();

        // Template string for live comment generation
        var liveComment =
            '<div class="media comment">' +
            '<a class="pull-left" href="#"><img class="media-object" src="http://placehold.it/64x64" alt=""></a>' +
            '<div class="media-body">' +
            '<h4 class="media-heading">' + commentSubmitter + ' <small> at ' + Date.now() + '</small></h4>' +
            commentBody +
            '<span class="number-of-likes pull-right" id="likes"> 0 <span class="glyphicon glyphicon-heart"></span>' +
            '</span></span></div>' +
            '<button type="button" class="btn btn-primary">Edit</button>' +
            '<button type="button" class="btn btn-danger">Delete</button>' +
            '</div>';

        if (commentBody === '') {
            // Add error class and messages
            $("#comment-body-error").show();
            $("#comment-form-textarea").addClass("has-error");
        }

        else {
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
                    $("#loading").hide();
                    lastComment.after(liveComment);
                }
            });
        }

        return false;
    }); // End POST for comment

    // AJAX handler to update comment likes
    $(".like-comment-btn").click(function(event) {
        event.stopPropagation();
        var commentId = $(this).data('value');
        var likeAmount = $(this).data('likes');
        var commentLiker = $(this).data('user');
        var commentHtml = likeAmount + " <span class='glyphicon glyphicon-heart'></span>";
        var prev = $(this).prev().find(".number-of-likes");

        // If there are no likes yet, set to 1
        if (likeAmount === "None") {
            likeAmount = 1 ;
        }
        else {
            likeAmount++;
        }

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

    // AJAX handler to update post likes
    $(".like-post-btn").click(function(event) {
        event.stopPropagation();
        var postId = $(this).data('value');
        var likeAmount = $(this).data('likes');
        var postLiker = $(this).data('user');
        var postHtml = likeAmount + " <span class='glyphicon glyphicon-heart'></span>";
        var prev = $(this).prev().find(".number-of-likes");

        if (likeAmount === "None") {
            likeAmount = 1 ;
        }
        else {
            likeAmount++;
        }

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
            }
        });
    }); // End PUT for post likes
});
