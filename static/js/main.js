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
                    return response.json().then(err => { throw err; });
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const scoreElement = document.getElementById(`score-${linkId}`);
                    if (scoreElement) {
                        scoreElement.textContent = data.new_score;
                    } else {
                        console.error(`Score element not found for link ${linkId}`);
                    }
                    this.classList.remove('upvote-btn-inactive');
                    this.classList.add('upvote-btn-active');
                    this.disabled = true;
                } else {
                    throw new Error(data.error || 'An error occurred while voting');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (error.message === 'Unauthorized') {
                    const currentPath = encodeURIComponent(window.location.pathname);
                    window.location.href = `/login?next=${currentPath}`;
                } else if (error.message === 'You have already voted for this link') {
                    this.classList.remove('upvote-btn-inactive');
                    this.classList.add('upvote-btn-active');
                    this.disabled = true;
                    alert('You have already voted for this link');
                } else {
                    alert(error.message || 'An error occurred while voting');
                }
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

    // Dark mode functionality
    const darkModeToggle = document.getElementById('darkModeToggle');
    const htmlElement = document.documentElement;

    // Check for saved theme preference or use system preference
    const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const hasUserPreference = localStorage.getItem('darkMode');

    function setDarkMode(isDark) {
        if (isDark) {
            htmlElement.classList.add('dark');
        } else {
            htmlElement.classList.remove('dark');
        }
        localStorage.setItem('darkMode', isDark);
    }

    // Set initial dark mode
    if (hasUserPreference === 'true' || (!hasUserPreference && darkModeMediaQuery.matches)) {
        setDarkMode(true);
    }

    // Toggle dark mode
    darkModeToggle.addEventListener('click', () => {
        const isDark = htmlElement.classList.toggle('dark');
        setDarkMode(isDark);
    });

    // Listen for system preference changes
    darkModeMediaQuery.addListener((e) => {
        if (!localStorage.getItem('darkMode')) {
            setDarkMode(e.matches);
        }
    });
});
