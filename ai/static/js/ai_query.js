// ai/static/ai/js/ai_query.js
document.addEventListener('DOMContentLoaded', () => {
    const aiForm = document.getElementById('ai-form');
    
    if (aiForm) {
        const questionTextarea = aiForm.querySelector('textarea[name="question"]');
        const attachFileBtn = document.getElementById('attach-file-btn');
        const aiFileInput = document.getElementById('ai-file-input');
        const fileDisplayContainer = document.getElementById('file-display-container');

        // Textarea Auto-Resize
        questionTextarea.addEventListener('input', () => {
            questionTextarea.style.height = 'auto';
            questionTextarea.style.height = `${questionTextarea.scrollHeight}px`;
        });

        // File Attachment Logic
        attachFileBtn.addEventListener('click', () => aiFileInput.click());

        aiFileInput.addEventListener('change', () => {
            fileDisplayContainer.innerHTML = aiFileInput.files.length > 0 ?
                `<div class="file-display-item"><span>${aiFileInput.files[0].name}</span><span class="clear-file-btn" title="Remove file">&times;</span></div>` : '';
        });

        // Clear Attached File Logic
        fileDisplayContainer.addEventListener('click', (e) => {
            if (e.target.classList.contains('clear-file-btn')) {
                aiFileInput.value = '';
                fileDisplayContainer.innerHTML = '';
            }
        });

        // Form Submission with Fetch API
        aiForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(aiForm);
            const submitBtn = aiForm.querySelector('button[type="submit"]');
            submitBtn.disabled = true;

            fetch(aiForm.action, {
                method: 'POST',
                body: formData,
                headers: { 'X-CSRFToken': formData.get('csrfmiddlewaretoken') },
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message); // Use a better notification in a real app
                if (data.status === 'success') {
                    aiForm.reset();
                    fileDisplayContainer.innerHTML = '';
                    questionTextarea.style.height = 'auto';
                }
            })
            .catch(error => {
                console.error('Submission error:', error);
                alert('An unexpected error occurred.');
            })
            .finally(() => {
                submitBtn.disabled = false;
            });
        });
    }
});