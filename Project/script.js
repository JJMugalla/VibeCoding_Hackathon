document.addEventListener('DOMContentLoaded', function() {
    // Initialize Intrasend
    window.intrasend = new window.Intrasend('YOUR_INTRASEND_APP_ID');
    
    // DOM Elements
    const languageSelection = document.getElementById('language-selection');
    const practiceInterface = document.getElementById('practice-interface');
    const currentLanguageElement = document.getElementById('current-language');
    const questionInput = document.getElementById('question-input');
    const askButton = document.getElementById('ask-button');
    const answerText = document.getElementById('answer-text');
    const backToLanguagesButton = document.getElementById('back-to-languages');
    const premiumLink = document.getElementById('premium-link');
    const premiumSection = document.getElementById('premium-section');
    const subscribeButton = document.getElementById('subscribe-button');
    
    let currentLanguage = '';
    
    // Language selection
    document.querySelectorAll('.language-card').forEach(card => {
        card.addEventListener('click', function() {
            currentLanguage = this.getAttribute('data-lang');
            currentLanguageElement.textContent = `Practice: ${currentLanguage.charAt(0).toUpperCase() + currentLanguage.slice(1)}`;
            languageSelection.classList.add('d-none');
            practiceInterface.classList.remove('d-none');
        });
    });
    
    // Back to languages
    backToLanguagesButton.addEventListener('click', function() {
        practiceInterface.classList.add('d-none');
        languageSelection.classList.remove('d-none');
        questionInput.value = '';
        answerText.textContent = 'Your answer will appear here...';
    });
    
    // Ask question
    askButton.addEventListener('click', async function() {
        const question = questionInput.value.trim();
        if (!question) {
            alert('Please enter a question');
            return;
        }
        
        answerText.textContent = 'Thinking...';
        
        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    language: currentLanguage,
                    question: question
                })
            });
            
            const data = await response.json();
            
            if (data.error) {
                answerText.textContent = `Error: ${data.error}`;
            } else {
                answerText.textContent = data.answer;
            }
        } catch (error) {
            answerText.textContent = 'Sorry, there was an error processing your question.';
            console.error('Error:', error);
        }
    });
    
    // Premium section
    premiumLink.addEventListener('click', function(e) {
        e.preventDefault();
        premiumSection.classList.remove('d-none');
        window.scrollTo(0, document.body.scrollHeight);
    });
    
    // Subscribe button
    subscribeButton.addEventListener('click', function() {
        window.intrasend.openCheckout({
            planId: 'premium_monthly',
            onSuccess: function() {
                alert('Subscription successful! Premium features unlocked.');
                premiumSection.classList.add('d-none');
            },
            onClose: function() {
                console.log('Checkout closed');
            }
        });
    });
});