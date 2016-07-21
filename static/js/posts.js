/**
 * AJAX functions for post edits, deletes and likes
 */

$(function() {

    // Open and close edit post area
    $("#open-edit-post-btn").click(function(event) {
        $(".post-edit-box").fadeIn("slow");
        return false;
    });

    $("#close-edit-post-btn").click(function(event) {
        $(".post-edit-box").hide("slow");
        return false;
    });

    // AJAX handler for post edits
    $("#submit-edit-btn").click(function() {
        var postId = $("#post-id").val();
        var postNewTitle = $("#post-title").val();
        var postNewBody = $("textarea#post-body").val();
        var postOriginalTitle = $(".blog-post-title");
        var postOriginalBody = $("#post-body");

        $.ajax({
            type: "PUT",
            url: "/blog/editpost",
            data: {
                'post-id': postId,
                'post-title': postNewTitle,
                'post-body': postNewBody
            },
            cache: false,
            success: function() {
                postOriginalTitle.html(postNewTitle);
                postOriginalBody.html(postNewBody);
                $(".post-edit-box").hide("slow");
            }
        });

        return false;
    }); // End PUT for body

    // AJAX handler to update post likes
    $(".like-post-btn").click(function(event) {
        var postId = $(this).data('value');
        var likeAmount = $(this).data('likes');
        var postLiker = $(this).data('user');
        var likesHtml = "";
        var likeAmountElement = $(this).prev().find(".number-of-likes");

        if (likeAmount === "None") {
            likeAmount = 1 ;
        }
        else {
            likeAmount++;
        }

        likeHtml = likeAmount + " <span class='glyphicon glyphicon-heart'></span>";

        // Disable like button so user cannot like more than once
        $(this).prop("disabled", true);

        $.ajax({
            type: "PUT",
            url: "/blog/likepost",
            data: {
                'post-id': postId,
                'post-liker': postLiker
            },
            cache: false,
            success: function(response) {
                likeAmountElement.html(likesHtml);
            }
        });

        return false;
    }); // End PUT for likes

    // AJAX handler for post deletion
    $("#delete-post-btn").click(function(event) {
        var postId = $(this).data("id");

        $.ajax({
            type: "PUT",
            url: "/blog/deletepost",
            data: {
                'post-id': postId
            },
            cache: false,
            success: function(response) {
                 window.location.href = "/blog/welcome";
            }
        });

        return false;
    });
});
