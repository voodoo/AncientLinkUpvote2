document.addEventListener('DOMContentLoaded', function() {
    // Upvote functionality
    const upvoteButtons = document.querySelectorAll('.upvote-btn');
    upvoteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const linkId = this.dataset.linkId;
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            
            fetch(`/api/upvote/${linkId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
            })
            .then(response => {
                if (!response.ok) {
                    if (response.status === 401) {
                        throw new Error('You must be logged in to vote');
                    }
                    return response.json().then(err => { throw err; });
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
                    throw new Error(data.error || 'An error occurred while voting');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert(error.message || 'An error occurred while voting');
                if (error.message === 'You must be logged in to vote') {
                    window.location.href = '/login?next=' + encodeURIComponent(window.location.pathname);
                }
            });
        });
    });

    // Reply functionality (unchanged)
    const replyButtons = document.querySelectorAll('.reply-btn');
    replyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const commentId = this.dataset.commentId;
            const replyForm = document.querySelector(`.reply-form[data-comment-id="${commentId}"]`);
            replyForm.classList.toggle('hidden');
        });
    });
});

// Function to get CSRF token from meta tag (unused, keeping for reference)
function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}
