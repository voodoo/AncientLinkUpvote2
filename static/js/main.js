document.addEventListener('DOMContentLoaded', function() {
    // Upvote functionality
    const upvoteButtons = document.querySelectorAll('.upvote-btn');
    upvoteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const linkId = this.dataset.linkId;
            fetch(`/api/upvote/${linkId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const scoreElement = document.getElementById(`score-${linkId}`);
                    scoreElement.textContent = data.new_score;
                    this.disabled = true;
                    this.style.color = '#4a5568';
                } else {
                    alert('You have already voted for this link');
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
