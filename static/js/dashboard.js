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
const userName = document.getElementById('userName');
const userEmail = document.getElementById('userEmail');
const logoutBtn = document.getElementById('logoutBtn');
const navItems = document.querySelectorAll('.nav-item');
const contentSections = document.querySelectorAll('.content-section');
const projectsGrid = document.getElementById('projectsGrid');
const newProjectBtn = document.getElementById('newProjectBtn');
const createBtn = document.getElementById('createBtn');
const createPrompt = document.getElementById('createPrompt');
const projectModal = document.getElementById('projectModal');
const modalTitle = document.getElementById('modalTitle');
const modalPreviewFrame = document.getElementById('modalPreviewFrame');
const downloadProjectBtn = document.getElementById('downloadProjectBtn');
const deleteProjectBtn = document.getElementById('deleteProjectBtn');

let currentUser = null;
let currentProject = null;

// Auth state observer
auth.onAuthStateChanged((user) => {
    if (user) {
        currentUser = user;
        updateUserInfo();
        loadProjects();
        console.log('👤 Dashboard user logged in:', user.email);
    } else {
        console.log('❌ No user found, redirecting to auth...');
        window.location.href = '/auth';
    }
});

function updateUserInfo() {
    if (currentUser) {
        userName.textContent = currentUser.displayName || 'User';
        userEmail.textContent = currentUser.email;
        
        // Update settings form if it exists
        const settingsEmail = document.getElementById('settingsEmail');
        const settingsName = document.getElementById('settingsName');
        if (settingsEmail) settingsEmail.value = currentUser.email;
        if (settingsName) settingsName.value = currentUser.displayName || '';
        
        console.log('✅ User info updated');
    }
}

// Navigation
navItems.forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        
        // Update active nav item
        navItems.forEach(nav => nav.classList.remove('active'));
        item.classList.add('active');
        
        // Show corresponding section
        const section = item.dataset.section;
        showSection(section);
        
        console.log('📱 Navigation changed to:', section);
    });
});

function showSection(sectionName) {
    contentSections.forEach(section => {
        section.style.display = 'none';
    });
    
    const targetSection = document.getElementById(`${sectionName}Section`);
    if (targetSection) {
        targetSection.style.display = 'block';
        console.log('📄 Section displayed:', sectionName);
    }
}

// Logout
logoutBtn.addEventListener('click', async () => {
    try {
        await auth.signOut();
        console.log('👋 User logged out');
        window.location.href = '/';
    } catch (error) {
        console.error('❌ Logout error:', error);
    }
});

// Load user projects
async function loadProjects() {
    try {
        console.log('📂 Loading projects for user:', currentUser.uid);
        
        const response = await fetch(`/api/get-projects/${currentUser.uid}`);
        const data = await response.json();
        
        if (data.success) {
            displayProjects(data.projects);
            console.log('✅ Projects loaded:', data.projects.length);
        } else {
            console.error('❌ Error loading projects:', data.error);
            projectsGrid.innerHTML = '<p>Error loading projects. Please refresh the page.</p>';
        }
    } catch (error) {
        console.error('❌ Error loading projects:', error);
        projectsGrid.innerHTML = '<p>Error loading projects. Please check your internet connection.</p>';
    }
}

function displayProjects(projects) {
    projectsGrid.innerHTML = '';
    
    if (projects.length === 0) {
        projectsGrid.innerHTML = `
            <div class="empty-state" style="grid-column: 1 / -1; text-align: center; padding: 60px 20px;">
                <i class="fas fa-folder-open" style="font-size: 48px; color: #d1d5db; margin-bottom: 16px;"></i>
                <h3 style="margin-bottom: 8px; color: #374151;">No projects yet</h3>
                <p style="color: #6b7280; margin-bottom: 20px;">Create your first AI-generated website!</p>
                <button class="btn btn-primary" onclick="showCreateSection()">
                    <i class="fas fa-plus"></i>
                    Create Project
                </button>
            </div>
        `;
        return;
    }
    
    projects.forEach(project => {
        const projectCard = document.createElement('div');
        projectCard.className = 'project-card';
        
        const createdDate = project.created_at ? 
            new Date(project.created_at * 1000).toLocaleDateString() : 
            'Unknown date';
            
        projectCard.innerHTML = `
            <h3>${project.title || 'Untitled Project'}</h3>
            <p>${(project.prompt || '').substring(0, 100)}${project.prompt && project.prompt.length > 100 ? '...' : ''}</p>
            <div class="project-meta">
                <span>Created: ${createdDate}</span>
                <i class="fas fa-external-link-alt"></i>
            </div>
        `;
        
        projectCard.addEventListener('click', () => {
            openProjectModal(project);
        });
        
        projectsGrid.appendChild(projectCard);
    });
    
    console.log('🎨 Projects displayed:', projects.length);
}

function showCreateSection() {
    showSection('create');
    // Update nav
    navItems.forEach(nav => nav.classList.remove('active'));
    const createNav = document.querySelector('[data-section="create"]');
    if (createNav) createNav.classList.add('active');
    
    console.log('➕ Create section shown');
}

// Create new project
if (newProjectBtn) {
    newProjectBtn.addEventListener('click', showCreateSection);
}

if (createBtn) {
    createBtn.addEventListener('click', async () => {
        const prompt = createPrompt.value.trim();
        
        if (!prompt) {
            alert('Please enter a description for your website.');
            return;
        }
        
        if (prompt.length < 10) {
            alert('Please provide a more detailed description (at least 10 characters).');
            return;
        }
        
        createBtn.disabled = true;
        createBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
        
        try {
            console.log('🚀 Creating new project:', prompt);
            
            const response = await fetch('/api/generate-website', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt: prompt,
                    user_id: currentUser.uid
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                createPrompt.value = '';
                loadProjects(); // Refresh projects list
                showSection('projects');
                // Update nav
                navItems.forEach(nav => nav.classList.remove('active'));
                const projectsNav = document.querySelector('[data-section="projects"]');
                if (projectsNav) projectsNav.classList.add('active');
                
                alert(`Website "${data.title}" generated successfully!`);
                console.log('✅ Project created successfully:', data.title);
            } else {
                alert('Error generating website: ' + data.error);
                console.error('❌ Project creation failed:', data.error);
            }
            
        } catch (error) {
            console.error('❌ Generation error:', error);
            alert('Error generating website. Please check your internet connection and try again.');
        } finally {
            createBtn.disabled = false;
            createBtn.innerHTML = '<i class="fas fa-magic"></i> Generate Website';
        }
    });
}

// Project modal
function openProjectModal(project) {
    currentProject = project;
    modalTitle.textContent = project.title || 'Untitled Project';
    
    // Create blob URL for preview
    const blob = new Blob([project.code || '<p>No code available</p>'], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    modalPreviewFrame.src = url;
    
    projectModal.style.display = 'block';
    
    console.log('🖼️ Project modal opened:', project.title);
}

// Modal close
const modalClose = document.querySelector('.modal-close');
if (modalClose) {
    modalClose.addEventListener('click', () => {
        projectModal.style.display = 'none';
        if (modalPreviewFrame.src.startsWith('blob:')) {
            URL.revokeObjectURL(modalPreviewFrame.src);
        }
        console.log('❌ Project modal closed');
    });
}

// Download project
if (downloadProjectBtn) {
    downloadProjectBtn.addEventListener('click', async () => {
        if (!currentProject) return;
        
        try {
            console.log('⬇️ Downloading project:', currentProject.id);
            
            const response = await fetch(`/api/download-project/${currentProject.id}`);
            
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
                
                console.log('✅ Project downloaded successfully');
            } else {
                alert('Error downloading project.');
                console.error('❌ Download failed:', response.status);
            }
        } catch (error) {
            console.error('❌ Download error:', error);
            alert('Error downloading project.');
        }
    });
}

// Delete project
if (deleteProjectBtn) {
    deleteProjectBtn.addEventListener('click', async () => {
        if (!currentProject) return;
        
        if (!confirm(`Are you sure you want to delete "${currentProject.title}"? This action cannot be undone.`)) {
            return;
        }
        
        try {
            console.log('🗑️ Deleting project:', currentProject.id);
            
            const response = await fetch(`/api/delete-project/${currentProject.id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                projectModal.style.display = 'none';
                loadProjects(); // Refresh projects list
                alert('Project deleted successfully.');
                console.log('✅ Project deleted successfully');
            } else {
                alert('Error deleting project.');
                console.error('❌ Delete failed:', response.status);
            }
        } catch (error) {
            console.error('❌ Delete error:', error);
            alert('Error deleting project.');
        }
    });
}

// Close modal when clicking outside
if (projectModal) {
    projectModal.addEventListener('click', (e) => {
        if (e.target === projectModal) {
            projectModal.style.display = 'none';
            if (modalPreviewFrame.src.startsWith('blob:')) {
                URL.revokeObjectURL(modalPreviewFrame.src);
            }
        }
    });
}

// Handle Enter key in create prompt
if (createPrompt) {
    createPrompt.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (createBtn) createBtn.click();
        }
    });
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Dashboard.js initialized');
    
    // Show projects section by default
    showSection('projects');
});
