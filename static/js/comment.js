/* AJAX functions for real time comment generation, likes, edits and deletes */

$(function() {
    // Tinymce init options
    tinymce.init({
        selector: "textarea",
        statusbar: false,
        plugins: [
            'advlist autolink lists link image charmap print preview anchor',
            'searchreplace visualblocks code fullscreen',
            'insertdatetime media table contextmenu paste code'
        ],
        toolbar: 'undo redo | styleselect | bold italic | alignleft aligncenter alignbright alignjustify | bullist numlist outdent indent | link image',
        setup: function (editor) {
            editor.on('change', function () {
                editor.save();
            });
        }
    });

    // Open and close edit comment area
    $(".open-edit-comment-btn").click(function(event) {
        $(this).parent().next().fadeIn("slow");
        return false;
    });

    $(".close-edit-comment-btn").click(function(event) {
        $(this).parent().parent().hide("slow");
        return false;
    });

    // Stop propagation and default behaviour on form submit
    $("#comment-form").submit(function(e) {
        return false;
    });

    // AJAX handler for new comments
    $("#submit-comment-btn").click(function() {
        var commentBody = $("textarea#comment-body").val();
        var commentParent = $("#parent").val();
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
                data: {
                    'parent': commentParent,
                    'comment-submitter': commentSubmitter,
                    'comment-body': commentBody
                },
                cache: false,
                success: function(response) {
                    $("#loading").hide("slow");
                    lastComment.after(liveComment);
                }
            });
        }

        return false;
    }); // End POST for new comment

    // AJAX handler for comment deletion
    $(".delete-comment-btn").click(function(event) {
        var commentId = $(this).data("id");
        var _this = this;

        $.ajax({
            type: "PUT",
            url: "/blog/deletecomment",
            data: {
                'comment-id': commentId
            },
            cache: false,
            success: function(response) {
                $(_this).parent().hide("slow");
            }
        });

        return false;
    });

    // AJAX handler to update comment likes
    $(".like-comment-btn").click(function(event) {
        event.stopPropagation();
        var commentId = $(this).data('value');
        var likeAmount = $(this).data('likes');
        var commentLiker = $(this).data('user');
        var commentHtml = likeAmount + " <span class='glyphicon glyphicon-heart'></span>";
        var likeBoxHtml = $(this).prev().find(".number-of-likes");

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
            url: "/blog/likecomment",
            data: {
                'comment-id': commentId,
                'comment-liker': commentLiker
            },
            cache: false,
            success: function(response) {
                likeBoxHtml.html(commentHtml);
            }
        });

    }); // End PUT for likes


    // AJAX handler for comment edits
    $(".submit-comment-edit-btn").click(function() {
        var commentId = $(this).parent().find("#comment-id").val();
        var commentEditBody = $(this).parent().find("textarea#comment-body").val();
        var originalCommentBody = $(this).parent().parent().prev().find("#comment-body");
        var commentEditBox = $(this).parent().parent();

        $.ajax({
            type: "PUT",
            url: "/blog/editcomment",
            data: {
                'comment-id': commentId,
                'comment-body': commentEditBody
            },
            cache: false,
            success: function(response) {
                originalCommentBody.html(commentEditBody);
                commentEditBox.hide("slow");
            }
        });

        return false;
    }); // End PUT for edits

});
