document.addEventListener('DOMContentLoaded', () => {
    const editButtons = document.querySelectorAll('.comment-edit-btn');
    const starBoxs = document.querySelectorAll('.star-box');
    const commentTexts = document.querySelectorAll('.comment-text');
    const editForms = document.querySelectorAll('.comment-edit-form');
    /*const saveButtons = document.querySelectorAll('.comment-save-btn');*/
    const cancelButtons = document.querySelectorAll('.comment-cancel-save-btn');

    function toggleCommentEdit(starbox, commentText, form) {
        if (commentText.style.display === 'none') {
            starbox.style.display = 'block';
            commentText.style.display = 'block';
            form.style.display = 'none';
        } else {
            starbox.style.display = 'none';
            commentText.style.display = 'none';
            form.style.display = 'block';
        }
    }

    editButtons.forEach((editButton, index) => {
        editButton.addEventListener('click', () => {
            const formId = editButton.getAttribute('data-form-id');
            const commentId = formId.split('-')[2];
            const form = document.querySelector(`#${formId}`);
            const commentText = document.querySelector(`#comment-text-${commentId}`);
            const starbox = document.querySelector(`#stars-${commentId}`);
            console.log('commentText:', commentText);
            console.log('starbox:', starbox);
            console.log('form:', form);
            toggleCommentEdit(starbox, commentText, form);


            /*插入這裡*/
            var divStars = document.getElementById(`edit-stars-${commentId}`);
            var star_num = -1;
            var starNumInput = document.getElementById(`id_star_num-${commentId}`);
            var starArray = Array.from(divStars.children);
            var starImagePath = "{% static 'store/images/star.png' %}";
            var graystarImagePath = "{% static 'store/images/star-gray.png' %}";


            divStars.onmouseover = function(e) {
                if (e.target.tagName === "IMG") { //事件源是圖片
                    //把滑鼠移動到的星星替換圖片
                    e.target.src = starImagePath;
                    //把滑鼠移動到的星星之前的星星替換圖片
                    var prev = e.target.previousElementSibling;
                    while (prev) {
                        prev.src = starImagePath;
                        prev = prev.previousElementSibling;
                    }
                    //把滑鼠移動到的星星之後的星星替換圖片
                    var next = e.target.nextElementSibling;
                    while (next) { //把滑鼠移動到的星星之後的星星替換圖片
                        next.src = graystarImagePath;
                        next = next.nextElementSibling;
                    }

                    var index = starArray.indexOf(e.target); //找到滑鼠移動到的星星的序號
                }
            }

            //滑鼠點擊
            divStars.onclick = function(e) {
                if (e.target.tagName === "IMG") {
                    //記錄當前點擊的星星序號
                    star_num = starArray.indexOf(e.target);
                    starNumInput.value = star_num;
                    console.log('starArray:', starArray.indexOf(e.target));
                    console.log('star_num:', star_num);
                    console.log('starNumInput:', starNumInput.value);
                }
            }


            divStars.onmouseout = function(e) {
                if (star_num !== -1) { //滑鼠點擊事件發生，將評分固定在點擊的星星上
                    for (var i = 0; i < divStars.children.length; i++) {
                        if (i <= star_num) {
                            divStars.children[i].src = starImagePath;

                        } else {
                            divStars.children[i].src = graystarImagePath;
                        }
                    }
                } else {
                    for (var i = 0; i < divStars.children.length; i++) {
                        divStars.children[i].src = graystarImagePath;
                    }
                }
            }


        });
    });

    cancelButtons.forEach((cancelButton, index) => {
        cancelButton.addEventListener('click', () => {
            const formId = cancelButton.getAttribute('data-form-id');
            const commentId = formId.split('-')[2];
            const form = document.querySelector(`#${formId}`);
            const commentText = document.querySelector(`#comment-text-${commentId}`);
            const starbox = document.querySelector(`#stars-${commentId}`);
            console.log('commentText:', commentText);
            console.log('starbox:', starbox);
            console.log('form:', form);
            toggleCommentEdit(starbox, commentText, form);

        });
    });
});

// 動態編輯星星