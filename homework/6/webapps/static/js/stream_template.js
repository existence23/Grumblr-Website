function populatePostList(getURL, commentURL){
    $.get(getURL)
        .done(function (data) {
            var list = $("#post-list");
            list.data('max-time', data["max-time"]);
            for(var i = 0; i < data.posts.length; i++){
                var new_post = $(generatePost(data.posts[i], data.current_user));
                list.prepend(new_post);
                var post_id = data.posts[i]['id'];
                generateCommentList(post_id, commentURL);
            }
        })
}

// function to generate a post div for a given post
function generatePost(post, current_user){
    var post_id = post['id'];
    var user_id = post['user']['user_id'];
    var username = post['user']['username'];
    var firstname = post['user']['firstname'];
    var lastname = post['user']['lastname'];
    var text = post['text'];
    var time_str = post['time'];
    var img = post['image'];
    var imgStr = '<div class="postPhoto"><img src="' + img +
        '" alt="profile-photo" style="width: 100px; height: 100px"></div>';
    var follow;
    if(username.valueOf() != current_user.valueOf()){
        follow = '<a type="button" class="linkColor" href="javascript:void(0)" id="follow-' + post_id + '">Follow</a> ' +
            '<a type="button" class="linkColor" href="javascript:void(0)" id="unfollow-' + post_id + '">Unfollow</a>';
    }else{
        follow = '<a type="button" class="linkColor" href="#" id="delete-' + post_id + '">Delete</a>';
    }

    var comment = '<br><div id="addComment"><input class="comment" style="margin-top: 10px" id="comment-' + post_id + '" type="text" placeholder="Write your comment...">';
    var submit_comment = ' <button id="comment-button-' + post_id + '"type="button" class="loginButton" style="border-radius: 5px">Comment</button></div>';
    var comment_list = '<div id="comment-list-' + post_id + '"></div>';

    var html = '<div class="postBackground" id="post-' + post_id + '">' + '<div class="postText">' +
                    '<p class="userNameFont"><a class="linkColor" href="/grumblr/check-profile/'  + user_id + '">' +
                    firstname + ' ' + lastname + ' (' + username + ')</a></p>' +
                    '<p>' + text + '</p>' +
                    '<p>' + time_str + '</p>' + follow + '</div>' + imgStr +
                    comment + submit_comment + comment_list + '<div class="clearfloat"></div>' +'</div>';
    return html;
}

function generateSingleComment(comment) {
    var img = comment.image;
    var imgStr = '<img src="' + img + '"class="commentPic">';
    var commentHtml = '<div class="singleComment">' + imgStr +
        '<p class="commentText"><span class="commentUser">' + comment.user.firstname + ' ' + comment.user.lastname +
        '</span> ' + comment.text + ' ' + '<span class="commentTime">' + comment.time + '</span></p></div>';
    return commentHtml;
}

function generateCommentList(post_id, commentURL){
    $.get(commentURL+post_id.toString())
        .done(function (data) {
            for(var i = 0; i < data.comments.length; i++){
                var comment = data.comments[i];
                var commentHtml = generateSingleComment(comment);
                $("#comment-list-"+post_id).append(commentHtml);
            }
        })
}

function addCommment(post_id, addcommentURL){
    var comment = $("#comment-" + post_id);
    $.post(addcommentURL, {"comment":comment.val(), "post-id":post_id})
        .done(function (data){
            var commentHtml = generateSingleComment(data);
            $("#comment-list-"+post_id).append(commentHtml);
            comment.val("");
        });
}
