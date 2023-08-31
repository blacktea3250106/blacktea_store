document.addEventListener('DOMContentLoaded', () => {
    const deleteButtons = document.querySelectorAll('.comment-delete-btn');

    deleteButtons.forEach(deleteButton => {
        deleteButton.addEventListener('click', event => {
            event.stopPropagation(); // 阻止事件冒泡
            const commentIdToDelete = deleteButton.getAttribute('data-comment-id');

            Swal.fire({
                title: '確定刪除這則留言嗎？',
                text: "刪除後將無法恢復！",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: '確定刪除',
                cancelButtonText: '取消',
                reverseButtons: true
            }).then((result) => {
                if (result.isConfirmed) {

                    const data = {
                        comment_id: commentIdToDelete,
                    };

                    fetch(`/delete_comment`, {
                            method: 'DELETE',
                            headers: {
                                'X-CSRFToken': getCookie('csrftoken'),
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(data)
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire(
                                    '刪除成功',
                                    '留言已被刪除',
                                    'success'
                                ).then(() => {
                                    location.reload();
                                });
                            } else {
                                Swal.fire(
                                    '刪除失敗',
                                    data.message,
                                    'error'
                                );
                            }
                        })
                        .catch(error => {
                            console.error('Error:', error);
                        });
                }
            });
        });
    });

    // 取得 CSRF Token 的函數
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});