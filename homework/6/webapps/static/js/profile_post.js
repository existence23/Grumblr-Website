var commentURL = "get-comments/";
var addcommentURL = "create-comment/";

function deletePost(post_id) {
    $.post("delete-post/"+post_id)
        .done(function () {
            $("#post-" + post_id).remove();
        })
}

function follow(post_id) {
    $.post("follow/"+post_id);
}

function unfollow(post_id) {
    $.post("unfollow/"+post_id);
}

$(document).ready(function () {
    var user_id = document.getElementById('testScript').getAttribute('data');
    var getURL = "posts/" + user_id;

    populatePostList(getURL, commentURL);
    $("#post-list").click(function (e) {
        var content = $(e.target).context.innerText;
        var id = $(e.target).parent().parent().attr("id");
        var post_id = parseInt(id.substring(5));
        if(content == "Delete"){
            deletePost(post_id);
        }else if(content == "Follow"){
            follow(post_id);
        }else if(content == "Unfollow"){
            unfollow(post_id);
        }else if(content == "Comment"){
            addCommment(post_id, addcommentURL);
        }
    });

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
});
