var getURL = "/grumblr/get-posts";
var changeURL = "grumblr/get-changes/";
var commentURL = "grumblr/get-comments/";
var addcommentURL = "grumblr/create-comment/";

function addPost(){
    var post = $("#post-field");
    $.post("grumblr/add-post", {"post": post.val()})
        .done(function () {
        getUpdates();
        post.val("");
    });
}

function deletePost(post_id) {
    $.post("grumblr/delete-post/"+post_id)
        .done(function () {
            getUpdates();
        })
}

function follow(post_id) {
    $.post("grumblr/follow/"+post_id);
}

function unfollow(post_id) {
    $.post("grumblr/unfollow/"+post_id);
}

$(document).ready(function () {

    $('#add-btn').click(addPost);
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
    window.setInterval(getUpdates, 5000);

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

function getUpdates(){
    var list = $("#post-list");
    var max_time = list.data("max-time");
    $.get(changeURL + max_time)
        .done(function (data) {
            list.data('max-time', data['max-time']);
            for(var i = 0; i < data.posts.length; i++){
                var post = data.posts[i];
                var post_id = data.posts[i].id;
                if(post.deleted){
                    $("#post-" + post.id).remove();
                }else{
                    var new_post = $(generatePost(data.posts[i], data.current_user));
                    list.prepend(new_post);
                }
            }
        })
}