document.addEventListener('DOMContentLoaded', function() {
    // Upvote functionality
    const upvoteButtons = document.querySelectorAll('.upvote-btn');
    upvoteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const linkId = this.dataset.linkId;
            fetch(`/api/upvote/${linkId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrf_token')
                },
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const scoreElement = document.getElementById(`score-${linkId}`);
                    scoreElement.textContent = data.new_score;
                    this.classList.add('text-blue-500');
                    this.disabled = true;
                } else {
                    alert(data.error || 'An error occurred while voting');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while voting');
            });
        });
    });

    // Reply functionality
    const replyButtons = document.querySelectorAll('.reply-btn');
    replyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.dataset.commentId;
            const replyForm = document.querySelector(`.reply-form[data-comment-id="${commentId}"]`);
            replyForm.classList.toggle('hidden');
        });
    });
});

// Function to get CSRF token from cookies
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
