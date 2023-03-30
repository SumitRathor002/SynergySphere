
document.addEventListener('DOMContentLoaded', () => {
    let active = document.querySelector('.body').dataset.page;
    document.querySelector("#" + active).classList.add('active');
});

function drop_down(event) {
    let drop_down = event.target.parentElement.querySelector(".dropdown-menu");
    setTimeout(() => {
        drop_down.style.display = 'block';
        width = drop_down.offsetWidth;
        let btn_width = drop_down.parentElement.querySelector('button').offsetWidth;
        let left = width - btn_width;
        drop_down.style.left = '-' + left + 'px';
        document.addEventListener('keydown', event => {
            if (event.key === 'Escape') {
                drop_down.style.display = 'none';
            }
        });
    }, 100);
}

function remove_drop_down(event) {
    setTimeout(() => {
        event.target.parentElement.querySelector(".dropdown-menu").style.display = 'none';
    }, 250);
}

function createpost() {
    let popup = document.querySelector(".popup");
    popup.style.display = 'block';
    popup.querySelector('.large-popup').style.display = 'block'
    document.querySelector('.body').setAttribute('aria-hidden', 'true');
    document.querySelector('body').style.overflow = "hidden";
    document.querySelector('#insert-img').onchange = previewFile;
    popup.querySelector('.large-popup').querySelector('form').setAttribute('onsubmit', '');
    popup.querySelector('.large-popup').querySelector("#post-text").addEventListener('input', (event) => {
        if (event.target.value.trim().length > 0) {
            popup.querySelector('.submit-btn').disabled = false;
        }
        else if (event.target.parentElement.querySelector('#img-div').style.backgroundImage) {
            popup.querySelector('.submit-btn').disabled = false;
        }
        else {
            popup.querySelector('.submit-btn').disabled = true;
        }
    });
}

function confirm_delete(id) {
    let popup = document.querySelector('.popup');
    popup.style.display = 'block';
    let small_popup = popup.querySelector('.small-popup');
    small_popup.style.display = 'block';
    document.querySelector('.body').setAttribute('aria-hidden', 'true');
    document.querySelector('body').style.overflow = "hidden";
    small_popup.querySelector('#delete_post_btn').setAttribute('onclick', `delete_post(${id})`);
}

function delete_post(id) {
    remove_popup();
    setTimeout(() => {
        let post = 0;
        document.querySelectorAll('.post').forEach(eachpost => {
            if (eachpost.dataset.post_id == id) {
                post = eachpost;
            }
        });
        post.style.animationPlayState = 'running';
        post.addEventListener('animationend', () => {
            post.remove();
        });
        fetch('/n/post/' + parseInt(id) + '/delete', {
            method: 'PUT'
        });
    }, 200);
}

function edit_post(element) {
    let post = element.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
    let popup = document.querySelector('.large-popup');
    let promise = new Promise((resolve, reject) => {
        let post_text = post.querySelector('.post-content').innerText;
        let post_image = post.querySelector('.post-image').style.backgroundImage;

        popup.querySelector('#post-text').value = post_text;
        if (post_image) {
            popup.querySelector('#img-div').style.backgroundImage = post_image;
            document.querySelector('#del-img').addEventListener('click', del_image);
            popup.querySelector('#img-div').style.display = 'block';
        }
        else {
            popup.querySelector('#img-div').style.backgroundImage = '';
        }
        resolve(popup);
    });
    promise.then(() => {
        createpost();
        popup.querySelector('form').setAttribute('onsubmit', `return edit_post_submit(${post.dataset.post_id})`);
        popup.querySelector('.submit-btn').disabled = false;
    });
}
function edit_post_submit(post_id) {
    let popup = document.querySelector('.large-popup');
    let text = popup.querySelector('#post-text').value;
    let pic = popup.querySelector('#insert-img');
    let chg = popup.querySelector('#img-change');
    let formdata = new FormData();
    formdata.append('text', text);
    formdata.append('picture', pic.files[0]);
    formdata.append('img_change', chg.value);
    formdata.append('id', post_id);
    fetch('/n/post/' + parseInt(post_id) + '/edit', {
        method: 'POST',
        body: formdata
    })
        .then(response => response.json())
        .then(response => {
            if (response.success) {
                let posts = document.querySelectorAll('.post');
                posts.forEach(post => {
                    if (parseInt(post.dataset.post_id) === parseInt(post_id)) {
                        if (response.text) {
                            post.querySelector('.post-content').innerText = response.text;
                        }
                        else {
                            post.querySelector('.post-content').innerText = "";
                        }
                        if (response.picture) {
                            post.querySelector('.post-image').style.backgroundImage = `url(${response.picture})`;
                            post.querySelector('.post-image').style.display = 'block';
                        }
                        else {
                            post.querySelector('.post-image').style.backgroundImage = '';
                            post.querySelector('.post-image').style.display = 'none';
                        }
                    }
                });
                return false;
            }
            else {
                console.log('There was an error while editing the post.');
            }
        });
    remove_popup();
    return false;
}

function remove_popup() {
    let popup = document.querySelector('.popup');
    popup.style.display = 'none';
    document.querySelector('.body').style.marginRight = '0px';
    document.querySelector('.body').setAttribute('aria-hidden', 'false');
    document.querySelector('body').style.overflow = "auto";
    let small_popup = document.querySelector('.small-popup');
    let large_popup = document.querySelector('.large-popup');
    let login_popup = document.querySelector('.login-popup');
    small_popup.style.display = 'none';
    large_popup.style.display = 'none';
    login_popup.style.display = 'none';
    large_popup.querySelector('#post-text').value = '';
    large_popup.querySelector('#insert-img').value = '';
    large_popup.querySelector('#img-div').style.backgroundImage = '';
    large_popup.querySelector('#img-change').value = 'false';
    large_popup.querySelector('#img-div').style.display = 'none';
}

function login_popup(action) {
    let popup = document.querySelector('.popup');
    popup.style.display = 'block';
    popup.querySelector('.login-popup').style.display = 'block';
    document.querySelector('.body').setAttribute('aria-hidden', 'true');
    document.querySelector('body').style.overflow = "hidden";
    if (action === 'like') {
        document.querySelector('.icon-div').innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-hand-thumbs-up-fill" viewBox="0 0 16 16">
        <path d="M6.956 1.745C7.021.81 7.908.087 8.864.325l.261.066c.463.116.874.456 1.012.965.22.816.533 2.511.062 4.51a9.84 9.84 0 0 1 .443-.051c.713-.065 1.669-.072 2.516.21.518.173.994.681 1.2 1.273.184.532.16 1.162-.234 1.733.058.119.103.242.138.363.077.27.113.567.113.856 0 .289-.036.586-.113.856-.039.135-.09.273-.16.404.169.387.107.819-.003 1.148a3.163 3.163 0 0 1-.488.901c.054.152.076.312.076.465 0 .305-.089.625-.253.912C13.1 15.522 12.437 16 11.5 16H8c-.605 0-1.07-.081-1.466-.218a4.82 4.82 0 0 1-.97-.484l-.048-.03c-.504-.307-.999-.609-2.068-.722C2.682 14.464 2 13.846 2 13V9c0-.85.685-1.432 1.357-1.615.849-.232 1.574-.787 2.132-1.41.56-.627.914-1.28 1.039-1.639.199-.575.356-1.539.428-2.59z"/>
        </svg>`;
        document.querySelector('.main_text-div').querySelector('h2').innerText = 'Like a post to share the love';
    }
    else if (action === 'comment') {
        document.querySelector('.icon-div').innerHTML = `
        <svg width="2.5em" height="2.5em" viewBox="0 0 16 16" class="bi bi-chat-fill" fill="#1da1f2" xmlns="http://www.w3.org/2000/svg">
            <path d="M8 15c4.418 0 8-3.134 8-7s-3.582-7-8-7-8 3.134-8 7c0 1.76.743 3.37 1.97 4.6-.097 1.016-.417 2.13-.771 2.966-.079.186.074.394.273.362 2.256-.37 3.597-.938 4.18-1.234A9.06 9.06 0 0 0 8 15z"/>
        </svg>`;
        document.querySelector('.main_text-div').querySelector('h2').innerText = 'Comment to join the conversation';
    }
    else if (action === 'save') {
        document.querySelector('.icon-div').innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pin-fill" viewBox="0 0 16 16">
  <path d="M4.146.146A.5.5 0 0 1 4.5 0h7a.5.5 0 0 1 .5.5c0 .68-.342 1.174-.646 1.479-.126.125-.25.224-.354.298v4.431l.078.048c.203.127.476.314.751.555C12.36 7.775 13 8.527 13 9.5a.5.5 0 0 1-.5.5h-4v4.5c0 .276-.224 1.5-.5 1.5s-.5-1.224-.5-1.5V10h-4a.5.5 0 0 1-.5-.5c0-.973.64-1.725 1.17-2.189A5.921 5.921 0 0 1 5 6.708V2.277a2.77 2.77 0 0 1-.354-.298C4.342 1.674 4 1.179 4 .5a.5.5 0 0 1 .146-.354z"/>
</svg>`;
        document.querySelector('.main_text-div').querySelector('h2').innerText = 'Save a post to reference later';
    }
    else if (action === 'follow') {
        document.querySelector('.icon-div').innerHTML = `
        <svg width="2.5em" height="2.5em" viewBox="0 0 24 24" fill="#17bf63" class="r-1re7ezh r-4qtqp9 r-yyyyoo r-1q142lx r-1xvli5t r-19einr3 r-dnmrzs r-bnwqim r-1plcrui r-lrvibr">
            <g><path d="M23.152 3.483h-2.675V.81c0-.415-.336-.75-.75-.75s-.75.335-.75.75v2.674H16.3c-.413 0-.75.336-.75.75s.337.75.75.75h2.677V7.66c0 .413.336.75.75.75s.75-.337.75-.75V4.982h2.675c.414 0 .75-.336.75-.75s-.336-.75-.75-.75zM8.417 11.816c1.355 0 2.872-.15 3.84-1.256.813-.93 1.077-2.367.806-4.392-.38-2.826-2.116-4.513-4.646-4.513S4.15 3.342 3.77 6.168c-.27 2.025-.007 3.462.807 4.393.968 1.108 2.485 1.257 3.84 1.257zm-3.16-5.448c.16-1.2.786-3.212 3.16-3.212 2.373 0 2.998 2.013 3.16 3.212.207 1.55.056 2.627-.45 3.205-.455.52-1.266.743-2.71.743s-2.256-.223-2.71-.743c-.507-.578-.658-1.656-.45-3.205zm11.44 12.867c-.88-3.525-4.283-5.988-8.28-5.988-3.998 0-7.403 2.463-8.28 5.988-.172.693-.03 1.4.395 1.94.408.522 1.04.822 1.733.822H14.57c.69 0 1.323-.3 1.73-.82.425-.54.568-1.247.396-1.942zm-1.577 1.018c-.126.16-.316.245-.55.245H2.264c-.235 0-.426-.085-.552-.246-.137-.174-.18-.412-.12-.654.71-2.855 3.517-4.85 6.824-4.85s6.113 1.994 6.824 4.85c.06.24.017.48-.12.655z"></path></g>
        </svg>`;
        document.querySelector('.main_text-div').querySelector('h2').innerText = 'Follow people that inspires you';
    }
}


function previewFile() {
    document.querySelector('#img-div').style.display = 'block';
    document.querySelector('#spinner').style.display = 'block';
    document.querySelector('#del-img').style.display = 'none';
    document.querySelector('#del-img').addEventListener('click', del_image);
    var preview = document.querySelector('#img-div');
    var file = document.querySelector('input[type=file]').files[0];
    var reader = new FileReader();

    reader.onloadend = function () {
        preview.style.backgroundImage = `url(${reader.result})`;
        document.querySelector('.large-popup').querySelector('#img-change').value = 'true';
    }

    if (file) {
        //reader.addEventListener('progress', (event) => {
        //    document.querySelector('#spinner').style.display = 'block';
        //});
        document.querySelector('.form-action-btns').querySelector('input[type=submit]').disabled = false;
        var promise = new Promise(function (resolve, reject) {
            setTimeout(() => {
                var read = reader.readAsDataURL(file);
                resolve(read);
            }, 500);
        });
        promise
            .then(function () {
                document.querySelector('#spinner').style.display = 'none';
                document.querySelector('#del-img').style.display = 'block';
            })
            .catch(function () {
                console.log('Some error has occured');
            });

    }
    else {
        document.querySelector('#spinner').style.display = 'none';
        document.querySelector('#del-img').style.display = 'block';
    }
}

function del_image() {
    document.querySelector('input[type=file]').value = '';
    document.querySelector('#img-div').style.backgroundImage = '';
    document.querySelector('#img-div').style.display = 'none';
    document.querySelector('.large-popup').querySelector('#img-change').value = 'true';
    if (document.querySelector('.large-popup').querySelector('#post-text').value.trim().length <= 0) {
        document.querySelector('.large-popup').querySelector('.form-action-btns').querySelector('input[type=submit]').disabled = true;
    }
}

function like_post(element) {
    if (document.querySelector('#user_is_authenticated').value === 'False') {
        login_popup('like');
        return false;
    }
    let id = element.dataset.post_id;
    fetch('/n/post/' + parseInt(id) + '/like', {
        method: 'PUT'
    })
        .then(() => {
            let count = element.querySelector('.likes_count');
            let value = count.innerHTML;
            value++;
            count.innerHTML = value;
            element.querySelector('.svg-span').innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-hand-thumbs-up-fill" viewBox="0 0 16 16">
            <path d="M6.956 1.745C7.021.81 7.908.087 8.864.325l.261.066c.463.116.874.456 1.012.965.22.816.533 2.511.062 4.51a9.84 9.84 0 0 1 .443-.051c.713-.065 1.669-.072 2.516.21.518.173.994.681 1.2 1.273.184.532.16 1.162-.234 1.733.058.119.103.242.138.363.077.27.113.567.113.856 0 .289-.036.586-.113.856-.039.135-.09.273-.16.404.169.387.107.819-.003 1.148a3.163 3.163 0 0 1-.488.901c.054.152.076.312.076.465 0 .305-.089.625-.253.912C13.1 15.522 12.437 16 11.5 16H8c-.605 0-1.07-.081-1.466-.218a4.82 4.82 0 0 1-.97-.484l-.048-.03c-.504-.307-.999-.609-2.068-.722C2.682 14.464 2 13.846 2 13V9c0-.85.685-1.432 1.357-1.615.849-.232 1.574-.787 2.132-1.41.56-.627.914-1.28 1.039-1.639.199-.575.356-1.539.428-2.59z"/>
            </svg>`;
            element.setAttribute('onclick', 'unlike_post(this)');
        })
}

function unlike_post(element) {
    let id = element.dataset.post_id;
    fetch('/n/post/' + parseInt(id) + '/unlike', {
        method: 'PUT'
    })
        .then(() => {
            let count = element.querySelector('.likes_count');
            let value = count.innerHTML;
            value--;
            count.innerHTML = value;
            element.querySelector('.svg-span').innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-hand-thumbs-up" viewBox="0 0 16 16">
                                                            <path d="M8.864.046C7.908-.193 7.02.53 6.956 1.466c-.072 1.051-.23 2.016-.428 2.59-.125.36-.479 1.013-1.04 1.639-.557.623-1.282 1.178-2.131 1.41C2.685 7.288 2 7.87 2 8.72v4.001c0 .845.682 1.464 1.448 1.545 1.07.114 1.564.415 2.068.723l.048.03c.272.165.578.348.97.484.397.136.861.217 1.466.217h3.5c.937 0 1.599-.477 1.934-1.064a1.86 1.86 0 0 0 .254-.912c0-.152-.023-.312-.077-.464.201-.263.38-.578.488-.901.11-.33.172-.762.004-1.149.069-.13.12-.269.159-.403.077-.27.113-.568.113-.857 0-.288-.036-.585-.113-.856a2.144 2.144 0 0 0-.138-.362 1.9 1.9 0 0 0 .234-1.734c-.206-.592-.682-1.1-1.2-1.272-.847-.282-1.803-.276-2.516-.211a9.84 9.84 0 0 0-.443.05 9.365 9.365 0 0 0-.062-4.509A1.38 1.38 0 0 0 9.125.111L8.864.046zM11.5 14.721H8c-.51 0-.863-.069-1.14-.164-.281-.097-.506-.228-.776-.393l-.04-.024c-.555-.339-1.198-.731-2.49-.868-.333-.036-.554-.29-.554-.55V8.72c0-.254.226-.543.62-.65 1.095-.3 1.977-.996 2.614-1.708.635-.71 1.064-1.475 1.238-1.978.243-.7.407-1.768.482-2.85.025-.362.36-.594.667-.518l.262.066c.16.04.258.143.288.255a8.34 8.34 0 0 1-.145 4.725.5.5 0 0 0 .595.644l.003-.001.014-.003.058-.014a8.908 8.908 0 0 1 1.036-.157c.663-.06 1.457-.054 2.11.164.175.058.45.3.57.65.107.308.087.67-.266 1.022l-.353.353.353.354c.043.043.105.141.154.315.048.167.075.37.075.581 0 .212-.027.414-.075.582-.05.174-.111.272-.154.315l-.353.353.353.354c.047.047.109.177.005.488a2.224 2.224 0 0 1-.505.805l-.353.353.353.354c.006.005.041.05.041.17a.866.866 0 0 1-.121.416c-.165.288-.503.56-1.066.56z"/>
                                                          </svg>`;
            element.setAttribute('onclick', 'like_post(this)');
        })
}

function save_post(element) {
    if (document.querySelector('#user_is_authenticated').value === 'False') {
        login_popup('save');
        return false;
    }
    let id = element.dataset.post_id;
    fetch('/n/post/' + parseInt(id) + '/save', {
        method: 'PUT'
    })
        .then(() => {
            element.querySelector('.svg-span').innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pin-fill" viewBox="0 0 16 16">
                                                            <path d="M4.146.146A.5.5 0 0 1 4.5 0h7a.5.5 0 0 1 .5.5c0 .68-.342 1.174-.646 1.479-.126.125-.25.224-.354.298v4.431l.078.048c.203.127.476.314.751.555C12.36 7.775 13 8.527 13 9.5a.5.5 0 0 1-.5.5h-4v4.5c0 .276-.224 1.5-.5 1.5s-.5-1.224-.5-1.5V10h-4a.5.5 0 0 1-.5-.5c0-.973.64-1.725 1.17-2.189A5.921 5.921 0 0 1 5 6.708V2.277a2.77 2.77 0 0 1-.354-.298C4.342 1.674 4 1.179 4 .5a.5.5 0 0 1 .146-.354z"/>
                                                          </svg>`;
            element.setAttribute('onclick', 'unsave_post(this)');
        });
}

function unsave_post(element) {
    let id = element.dataset.post_id;
    fetch('/n/post/' + parseInt(id) + '/unsave', {
        method: 'PUT'
    })
        .then(() => {
            element.querySelector('.svg-span').innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pin" viewBox="0 0 16 16">
                                                            <path d="M4.146.146A.5.5 0 0 1 4.5 0h7a.5.5 0 0 1 .5.5c0 .68-.342 1.174-.646 1.479-.126.125-.25.224-.354.298v4.431l.078.048c.203.127.476.314.751.555C12.36 7.775 13 8.527 13 9.5a.5.5 0 0 1-.5.5h-4v4.5c0 .276-.224 1.5-.5 1.5s-.5-1.224-.5-1.5V10h-4a.5.5 0 0 1-.5-.5c0-.973.64-1.725 1.17-2.189A5.921 5.921 0 0 1 5 6.708V2.277a2.77 2.77 0 0 1-.354-.298C4.342 1.674 4 1.179 4 .5a.5.5 0 0 1 .146-.354zm1.58 1.408-.002-.001.002.001zm-.002-.001.002.001A.5.5 0 0 1 6 2v5a.5.5 0 0 1-.276.447h-.002l-.012.007-.054.03a4.922 4.922 0 0 0-.827.58c-.318.278-.585.596-.725.936h7.792c-.14-.34-.407-.658-.725-.936a4.915 4.915 0 0 0-.881-.61l-.012-.006h-.002A.5.5 0 0 1 10 7V2a.5.5 0 0 1 .295-.458 1.775 1.775 0 0 0 .351-.271c.08-.08.155-.17.214-.271H5.14c.06.1.133.191.214.271a1.78 1.78 0 0 0 .37.282z"/>
                                                          </svg>`;
            element.setAttribute('onclick', 'save_post(this)');
        });
}


function follow_user(element, username, origin) {
    if (document.querySelector('#user_is_authenticated').value === 'False') {
        login_popup('follow');
        return false;
    }
    fetch('/' + username + '/follow', {
        method: 'PUT'
    })
        .then(() => {
            if (origin === 'suggestion') {
                element.parentElement.innerHTML = `<button class="btn btn-success" type="button" onclick="unfollow_user(this,'${username}','suggestion')">Following</button>`;
            }
            else if (origin === 'edit_page') {
                element.parentElement.innerHTML = `<button class="btn btn-success float-right" onclick="unfollow_user(this,'${username}','edit_page')" id="following-btn">Following</button>`;
            }
            else if (origin === 'dropdown') {
                ////////////////////////////////////////////////////////////////////////////////////////////
            }

            if (document.querySelector('.body').dataset.page === 'profile') {
                if (document.querySelector('.profile-view').dataset.user === username) {
                    document.querySelector('#follower__count').innerHTML++;
                }
            }
            if (document.querySelector('.body').dataset.page === 'profile') {
                if (document.querySelector('.profile-view').dataset.user === document.querySelector('#user_is_authenticated').dataset.username) {
                    document.querySelector('#following__count').innerHTML++;
                }
            }
        });
}

function unfollow_user(element, username, origin) {
    if (document.querySelector('#user_is_authenticated').value === 'False') {
        login_popup('follow');
        return false;
    }
    fetch('/' + username + '/unfollow', {
        method: 'PUT'
    })
        .then(() => {
            if (origin === 'suggestion') {
                element.parentElement.innerHTML = `<button class="btn btn-outline-success" type="button" onclick="follow_user(this,'${username}','suggestion')">Follow</button>`;
            }
            else if (origin === 'edit_page') {
                element.parentElement.innerHTML = `<button class="btn btn-outline-success float-right" onclick="follow_user(this,'${username}','edit_page')" id="follow-btn">Follow</button>`;
            }
            else if (origin === 'dropdown') {
                ///////////////////////////////////////////////////////////////////////////////////////////
            }

            if (document.querySelector('.body').dataset.page === 'profile') {
                if (document.querySelector('.profile-view').dataset.user === username) {
                    document.querySelector('#follower__count').innerHTML--;
                }
            }
            if (document.querySelector('.body').dataset.page === 'profile') {
                if (document.querySelector('.profile-view').dataset.user === document.querySelector('#user_is_authenticated').dataset.username) {
                    document.querySelector('#following__count').innerHTML--;
                }
            }
        });
}


function show_comment(element) {
    if (document.querySelector('#user_is_authenticated').value === 'False') {
        login_popup('comment');
        return;
    }
    let post_div = element.parentElement.parentElement.parentElement.parentElement;
    let post_id = post_div.dataset.post_id;
    let comment_div = post_div.querySelector('.comment-div');
    let comment_div_data = comment_div.querySelector('.comment-div-data');
    let comment_comments = comment_div_data.querySelector('.comment-comments');
    if (comment_div.style.display === 'block') {
        comment_div.querySelector('input').focus()
        return;
    }
    comment_div.querySelector('#spinner').style.display = 'block';
    comment_div.style.display = 'block';
    fetch('/n/post/' + parseInt(post_id) + '/comments')
        .then(response => response.json())
        .then(comments => {
            comments.forEach(comment => {
                display_comment(comment, comment_comments);
            });
        })
        .then(() => {
            setTimeout(() => {
                comment_div.querySelector('.spinner-div').style.display = 'none';
                comment_div.querySelector('.comment-div-data').style.display = 'block';
                comment_div.style.overflow = 'auto';
            }, 500);
        });
}

function write_comment(element) {
    let post_id = element.parentElement.parentElement.parentElement.parentElement.parentElement.dataset.post_id;
    let comment_text = element.querySelector('.comment-input').value;
    let comment_comments = element.parentElement.parentElement.parentElement.parentElement.querySelector('.comment-comments');
    let comment_count = comment_comments.parentElement.parentElement.parentElement.querySelector('.cmt-count');
    if (comment_text.trim().length <= 0) {
        return false;
    }
    fetch('/n/post/' + parseInt(post_id) + '/write_comment', {
        method: 'POST',
        body: JSON.stringify({
            comment_text: comment_text
        })
    })
        .then(response => response.json())
        .then(comment => {
            console.log(comment);
            element.querySelector('input').value = '';
            comment_count.innerHTML++;
            display_comment(comment[0], comment_comments, true);
            return false;
        });
    return false;
}

function display_comment(comment, container, new_comment = false) {
    let writer = document.querySelector('#user_is_authenticated').dataset.username;
    let eachrow = document.createElement('div');
    eachrow.className = 'eachrow';
    eachrow.setAttribute('data-id', comment.id);
    eachrow.innerHTML = `
        <div>
            <a href='/${comment.commenter.username}'>
                <div class="small-profilepic" style="background-image: url(${comment.commenter.profile_pic})"></div>
            </a>
        </div>
        <div style="flex: 1;">
            <div class="comment-text-div">
                <div class="comment-user">
                    <a href="/${comment.commenter.username}">
                        ${comment.commenter.first_name} ${comment.commenter.last_name}
                    </a>
                </div>
                ${comment.body}
            </div>
        </div>`;
    if (new_comment) {
        eachrow.classList.add('godown');
        let comments = container.innerHTML;
        container.prepend(eachrow);
    }
    else {
        container.append(eachrow);
    }
}






function goto_register() {
    window.location.href = '/n/register';
}

function goto_login() {
    window.location.href = '/n/login';
}

function readmore() {
    let des_event = document.getElementById("description").innerHTML;
    let loca_event = document.getElementById("location").innerHTML;
    let name_event = document.getElementById("ename").innerHTML;
    document.getElementById("eventname").innerHTML = name_event + `<br>` + des_event + `<br>` + loca_event;
}

const dropdown = document.querySelector('.dropdown');
let delayTimer;

dropdown.addEventListener('mouseleave', () => {
    delayTimer = setTimeout(() => {
        document.querySelector('.dropdown-content').style.display = 'none';
    }, 100); // delay for 2 seconds before hiding
});

dropdown.addEventListener('mouseenter', () => {
    clearTimeout(delayTimer);
    document.querySelector('.dropdown-content').style.display = 'block';
});