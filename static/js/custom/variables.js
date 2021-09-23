const csrfToken = document.cookie.split(';').map(c => c.trim()).filter(c => c.startsWith('csrftoken='))[0].split('=')[1];
const ratePostPath = '/posts/rate/';
const rateCommentPath = '/posts/comment/rate/';
const deletePostPath = '/posts/delete/';
const friendRequestPath = '/profiles/friend_request/';
const createFriendshipPath = '/profiles/create_friendship/';
const endFriendshipPath = '/profiles/end_friendship/';
const searchPath = '/profiles/search/';
const getNotificationsPath = '/profiles/get_notifications/';