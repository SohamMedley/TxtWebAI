// Firebase configuration for your project
const firebaseConfig = {
    apiKey: "AIzaSyARsUQe9N6CfOzXaa02HhkYBrhQ2ngWjRU",
    authDomain: "webbuilder-6f7f3.firebaseapp.com",
    projectId: "webbuilder-6f7f3",
    storageBucket: "webbuilder-6f7f3.firebasestorage.app",
    messagingSenderId: "980941820475",
    appId: "1:980941820475:web:787458a6acce3d3c94821e",
    measurementId: "G-VD9JF734GZ"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.firestore();

// DOM elements
const loginBtn = document.getElementById('loginBtn');
const signupBtn = document.getElementById('signupBtn');
const dashboardBtn = document.getElementById('dashboardBtn');
const logoutBtn = document.getElementById('logoutBtn');
const promptInput = document.getElementById('promptInput');
const generateBtn = document.getElementById('generateBtn');
const chatMessages = document.getElementById('chatMessages');
const previewSection = document.getElementById('previewSection');
const previewFrame = document.getElementById('previewFrame');
const downloadBtn = document.getElementById('downloadBtn');
const saveBtn = document.getElementById('saveBtn');
const loadingModal = document.getElementById('loadingModal');
const authNotice = document.getElementById('authNotice');

let currentUser = null;
let currentProject = null;
let loadingStepIndex = 0;

// Auth state observer
auth.onAuthStateChanged((user) => {
    currentUser = user;
    updateAuthUI();
    console.log('Auth state changed:', user ? 'Logged in' : 'Logged out');
});

function updateAuthUI() {
    if (currentUser) {
        loginBtn.style.display = 'none';
        signupBtn.style.display = 'none';
        dashboardBtn.style.display = 'inline-flex';
        logoutBtn.style.display = 'inline-flex';
        authNotice.style.display = 'none';
        console.log('UI updated for logged in user');
    } else {
        loginBtn.style.display = 'inline-flex';
        signupBtn.style.display = 'inline-flex';
        dashboardBtn.style.display = 'none';
        logoutBtn.style.display = 'none';
        // Don't show auth notice immediately, only when user tries to generate
        console.log('UI updated for logged out user');
    }
}

// Event listeners
loginBtn.addEventListener('click', () => {
    window.location.href = '/auth';
});

signupBtn.addEventListener('click', () => {
    window.location.href = '/auth';
});

dashboardBtn.addEventListener('click', () => {
    window.location.href = '/dashboard';
});

logoutBtn.addEventListener('click', async () => {
    try {
        await auth.signOut();
        window.location.reload();
    } catch (error) {
        console.error('Logout error:', error);
    }
});

generateBtn.addEventListener('click', generateWebsite);
downloadBtn.addEventListener('click', downloadProject);
saveBtn.addEventListener('click', saveProject);

// Handle Enter key in prompt input
promptInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        generateWebsite();
    }
});

// Auto-resize textarea
promptInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});

async function generateWebsite() {
    const prompt = promptInput.value.trim();
    
    if (!prompt) {
        alert('Please enter a description for your website.');
        return;
    }

    if (prompt.length < 10) {
        alert('Please provide a more detailed description (at least 10 characters).');
        return;
    }

    // Add user message to chat
    addMessage(prompt, 'user');
    
    // Clear input
    promptInput.value = '';
    promptInput.style.height = 'auto';
    
    // Show loading with steps
    showLoadingWithSteps();
    generateBtn.disabled = true;
    
    try {
        console.log('🚀 Starting website generation...');
        
        const response = await fetch('/api/generate-website', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                user_id: currentUser ? currentUser.uid : 'anonymous_user'
            })
        });
        
        const data = await response.json();
        console.log('📦 Generation response:', data);
        
        if (data.success) {
            currentProject = data;
            
            // Add bot response
            addMessage(`✨ I've generated your beautiful website "${data.title}"! The design includes modern styling, responsive layout, and interactive elements. You can preview it below and download the HTML file when you're ready.`, 'assistant');
            
            // Show preview
            showPreview(data.code);
            
            console.log('✅ Website generated successfully!');
            
        } else {
            if (data.requiresAuth) {
                showAuthNotice();
                addMessage('Please sign in to generate websites with AI. Your account helps us provide better service and save your projects.', 'assistant');
            } else {
                addMessage(`Sorry, there was an error generating your website: ${data.error}`, 'assistant');
            }
            console.error('❌ Generation failed:', data.error);
        }
        
    } catch (error) {
        console.error('❌ Generation error:', error);
        addMessage('Sorry, there was an error generating your website. Please check your internet connection and try again.', 'assistant');
    } finally {
        hideLoading();
        generateBtn.disabled = false;
    }
}

function showAuthNotice() {
    authNotice.style.display = 'block';
    authNotice.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function addMessage(content, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const messageAvatar = document.createElement('div');
    messageAvatar.className = 'message-avatar';
    
    const avatarIcon = document.createElement('div');
    avatarIcon.className = 'avatar-icon';
    
    if (type === 'assistant') {
        avatarIcon.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
            </svg>
        `;
    } else {
        avatarIcon.innerHTML = `<i class="fas fa-user"></i>`;
    }
    
    messageAvatar.appendChild(avatarIcon);
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.textContent = content;
    
    messageContent.appendChild(messageText);
    messageDiv.appendChild(messageAvatar);
    messageDiv.appendChild(messageContent);
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    console.log(`💬 Added ${type} message:`, content.substring(0, 50) + '...');
}

function showPreview(code) {
    console.log('🖼️ Showing preview...');
    previewSection.style.display = 'block';
    
    // Create blob URL for the HTML content
    const blob = new Blob([code], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    
    previewFrame.src = url;
    
    // Scroll to preview
    previewSection.scrollIntoView({ behavior: 'smooth' });
    
    console.log('✅ Preview displayed successfully');
}

function showLoadingWithSteps() {
    console.log('⏳ Showing loading modal...');
    loadingModal.style.display = 'block';
    loadingStepIndex = 0;
    
    const steps = document.querySelectorAll('.step');
    steps.forEach(step => step.classList.remove('active'));
    
    // Animate through steps
    const stepInterval = setInterval(() => {
        if (loadingStepIndex < steps.length) {
            steps[loadingStepIndex].classList.add('active');
            console.log(`📋 Step ${loadingStepIndex + 1} active`);
            loadingStepIndex++;
        } else {
            clearInterval(stepInterval);
        }
    }, 3000);
    
    // Store interval ID to clear it later
    loadingModal.stepInterval = stepInterval;
}

function hideLoading() {
    console.log('✅ Hiding loading modal...');
    loadingModal.style.display = 'none';
    if (loadingModal.stepInterval) {
        clearInterval(loadingModal.stepInterval);
    }
}

async function downloadProject() {
    if (!currentProject) {
        alert('No project to download.');
        return;
    }
    
    try {
        console.log('⬇️ Starting download...');
        
        const response = await fetch(`/api/download-project/${currentProject.project_id}`);
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${currentProject.title || 'website'}.html`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            // Show success message
            addMessage('🎉 Website downloaded successfully! You can now open the HTML file in any browser or upload it to your web hosting service.', 'assistant');
            
            console.log('✅ Download completed successfully');
        } else {
            alert('Error downloading project.');
            console.error('❌ Download failed:', response.status);
        }
    } catch (error) {
        console.error('❌ Download error:', error);
        alert('Error downloading project.');
    }
}

async function saveProject() {
    if (!currentUser) {
        alert('Please login to save projects.');
        return;
    }
    
    if (!currentProject) {
        alert('No project to save.');
        return;
    }
    
    // Project is already saved during generation
    addMessage('💾 Project saved successfully! You can view and manage all your projects in your dashboard.', 'assistant');
    console.log('💾 Project save confirmed');
}

// Preview device controls
document.addEventListener('DOMContentLoaded', function() {
    const previewControls = document.querySelectorAll('.preview-control[data-device]');
    const previewFrameContainer = document.querySelector('.preview-frame-container');
    
    if (previewControls.length > 0 && previewFrameContainer) {
        previewControls.forEach(control => {
            control.addEventListener('click', function() {
                const device = this.dataset.device;
                
                // Update active state
                previewControls.forEach(c => c.classList.remove('active'));
                this.classList.add('active');
                
                // Update frame size
                if (device === 'mobile') {
                    previewFrameContainer.style.maxWidth = '375px';
                    previewFrameContainer.style.margin = '0 auto';
                } else if (device === 'tablet') {
                    previewFrameContainer.style.maxWidth = '768px';
                    previewFrameContainer.style.margin = '0 auto';
                } else {
                    previewFrameContainer.style.maxWidth = '100%';
                    previewFrameContainer.style.margin = '0';
                }
                
                console.log(`📱 Preview device changed to: ${device}`);
            });
        });
    }
});

// Refresh preview function
function refreshPreview() {
    if (previewFrame.src && previewFrame.src !== 'about:blank') {
        previewFrame.src = previewFrame.src;
        console.log('🔄 Preview refreshed');
    }
}

// Example prompt function
function useExamplePrompt(prompt) {
    promptInput.value = prompt;
    promptInput.style.height = 'auto';
    promptInput.style.height = Math.min(promptInput.scrollHeight, 120) + 'px';
    promptInput.focus();
    
    // Scroll to input
    promptInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    console.log('📝 Example prompt used:', prompt);
}

// Close modal when clicking outside
loadingModal.addEventListener('click', (e) => {
    if (e.target === loadingModal) {
        hideLoading();
    }
});

// Header scroll effect
window.addEventListener('scroll', () => {
    const header = document.querySelector('.header');
    if (header) {
        if (window.scrollY > 50) {
            header.style.background = 'rgba(255, 255, 255, 0.95)';
            header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
        } else {
            header.style.background = 'rgba(255, 255, 255, 0.8)';
            header.style.boxShadow = 'none';
        }
    }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Main.js initialized');
    console.log('🔧 Firebase config loaded');
    
    // Check if user is already logged in
    auth.onAuthStateChanged((user) => {
        if (user) {
            console.log('👤 User already logged in:', user.email);
        } else {
            console.log('👤 No user logged in');
        }
    });
});
